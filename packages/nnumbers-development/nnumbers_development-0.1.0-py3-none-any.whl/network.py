"""OpenStack network management module.

This module provides comprehensive functions to manage OpenStack networking
resources including networks, subnets, floating IPs, and security groups.
It offers both listing capabilities and creation/management operations
with robust error handling and validation.
"""

from typing import Any

import cyclopts
from loguru import logger
from tabulate import tabulate

from core import get_openstack_connection


app = cyclopts.App()


@app.command
def list_networks() -> None:
    """List all available OpenStack networks.

    Retrieves and displays all networks accessible to the current project,
    showing network name, ID, status, and whether it's an external network.
    Results are sorted alphabetically by network name for easier browsing.

    Raises
    ------
    SystemExit
        If connection to OpenStack fails.

    Examples
    --------
    $ nnumbers network list-networks
    ┌─────────────┬──────────────────────────────────────┬─────────┬──────────┐
    │ Name        │ ID                                   │ Status  │ External │
    ├─────────────┼──────────────────────────────────────┼─────────┼──────────┤
    │ public      │ 12345678-1234-1234-1234-123456789012 │ ACTIVE  │ Yes      │
    │ private     │ 87654321-4321-4321-4321-210987654321 │ ACTIVE  │ No       │
    └─────────────┴──────────────────────────────────────┴─────────┴──────────┘
    """
    conn = get_openstack_connection()
    if conn:
        try:
            logger.info("Listing networks...")
            networks = list(conn.network.networks())
            if networks:
                lines = []
                for network in sorted(networks, key=lambda x: x.name):
                    status = getattr(network, "status", "unknown")
                    is_external = getattr(network, "is_router_external", False)
                    external_str = "Yes" if is_external else "No"
                    lines.append(
                        [
                            network.name,
                            network.id,
                            status,
                            external_str,
                        ]
                    )

                table = tabulate(
                    lines,
                    headers=["Name", "ID", "Status", "External"],
                    tablefmt="grid",
                )
                print(table)
            else:
                logger.info("No networks found.")
        except Exception as e:
            logger.error(f"Error listing networks: {e}")
    else:
        logger.error("Failed to establish OpenStack connection")
        raise SystemExit(1)


@app.command
def create_floating_ip(network: str = "", description: str = "") -> None:
    """Create a new floating IP from an external network.

    Allocates a new floating IP address from the specified external network
    pool. If no network is specified, the system will automatically select
    the first available external network.

    Parameters
    ----------
    network : str, optional
        External network name or ID to allocate the floating IP from.
        If not provided, the first available external network will be used.
    description : str, optional
        Optional description for the floating IP to help identify its purpose.

    Raises
    ------
    SystemExit
        If connection to OpenStack fails or no external networks are available.

    Examples
    --------
    $ nnumbers network create-floating-ip
    $ nnumbers network create-floating-ip --network public
    $ nnumbers network create-floating-ip --description "Web server IP"
    """
    conn = get_openstack_connection()
    if conn:
        try:
            external_network = _get_external_network(conn, network)
            if not external_network:
                raise SystemExit(1)

            logger.info("Creating floating IP...")
            floating_ip_params = {"floating_network_id": external_network.id}

            if description:
                floating_ip_params["description"] = description

            floating_ip = conn.network.create_ip(**floating_ip_params)

            logger.success("Floating IP created successfully!")
            logger.info(f"IP Address: {floating_ip.floating_ip_address}")
            logger.info(f"ID: {floating_ip.id}")
            logger.info(f"Status: {floating_ip.status}")
            if description:
                logger.info(f"Description: {description}")

        except Exception as e:
            logger.error(f"Error creating floating IP: {e}")
    else:
        logger.error("Failed to establish OpenStack connection")
        raise SystemExit(1)


@app.command
def list_floating_ips() -> None:
    """List all floating IPs in the current project.

    Retrieves and displays all floating IP addresses allocated to the
    current project, showing their status, assignment details, and
    associated instances or ports.

    Raises
    ------
    SystemExit
        If connection to OpenStack fails.

    Examples
    --------
    $ nnumbers network list-floating-ips
    ┌───────────────┬─────────┬──────────────┬─────────────────────┐
    │ IP Address    │ Status  │ Fixed IP     │ Description         │
    ├───────────────┼─────────┼──────────────┼─────────────────────┤
    │ 203.0.113.10  │ ACTIVE  │ 10.0.0.15    │ Web server          │
    │ 203.0.113.11  │ DOWN    │ None         │ Available           │
    └───────────────┴─────────┴──────────────┴─────────────────────┘
    """
    conn = get_openstack_connection()
    if conn:
        try:
            logger.info("Listing floating IPs...")
            floating_ips = list(conn.network.ips())
            if floating_ips:
                lines = []
                for fip in sorted(floating_ips, key=lambda x: x.floating_ip_address):
                    status = getattr(fip, "status", "unknown")
                    fixed_ip = getattr(fip, "fixed_ip_address", None)
                    port_id = getattr(fip, "port_id", None)
                    description = getattr(fip, "description", "")
                    # Determine association status
                    if fixed_ip and port_id:
                        associated_with = f"{fixed_ip}"
                        # Try to get instance name
                        try:
                            port = conn.network.get_port(port_id)
                            device_id = getattr(port, "device_id", None)
                            if device_id:
                                server = conn.compute.get_server(device_id)
                                associated_with = f"{server.name} ({fixed_ip})"
                        except Exception:
                            pass
                    else:
                        associated_with = "Available"

                    lines.append(
                        [
                            fip.floating_ip_address,
                            fip.id,
                            status,
                            associated_with,
                            description or "-",
                        ]
                    )

                table = tabulate(
                    lines,
                    headers=["IP Address", "ID", "Status", "Associated", "Description"],
                    tablefmt="grid",
                )
                print(table)
            else:
                logger.info("No floating IPs found.")
        except Exception as e:
            logger.error(f"Error listing floating IPs: {e}")
    else:
        logger.error("Failed to establish OpenStack connection")
        exit(1)


@app.command
def associate_floating_ip(floating_ip: str, instance: str, fixed_ip: str = "") -> None:
    """Associate a floating IP with an instance.

    Parameters
    ----------
    floating_ip : str
        Floating IP address or ID to associate.
    instance : str
        Name or ID of the instance to associate with.
    fixed_ip : str, optional
        Specific fixed IP address (if instance has multiple IPs).
    """
    conn = get_openstack_connection()
    if conn:
        try:
            fip_obj = _find_floating_ip(conn, floating_ip)
            if not fip_obj:
                logger.error(f"Floating IP '{floating_ip}' not found")
                exit(1)

            if getattr(fip_obj, "port_id", None):
                logger.error(
                    f"Floating IP {fip_obj.floating_ip_address} is already associated"
                )
                exit(1)

            server = conn.compute.find_server(instance)
            if not server:
                logger.error(f"Instance '{instance}' not found")
                exit(1)

            target_ip, target_port = _get_instance_port_info(conn, server, fixed_ip)
            if not target_port:
                exit(1)

            logger.info(
                f"Associating floating IP {fip_obj.floating_ip_address} "
                f"with instance '{server.name}' ({target_ip})..."
            )

            conn.network.update_ip(
                fip_obj, port_id=target_port.id, fixed_ip_address=target_ip
            )

            logger.success(
                f"Floating IP {fip_obj.floating_ip_address} "
                f"successfully associated with '{server.name}'"
            )
            logger.info(f"Instance IP: {target_ip}")

        except Exception as e:
            logger.error(f"Error associating floating IP: {e}")
    else:
        logger.error("Failed to establish OpenStack connection")
        exit(1)


@app.command
def disassociate_floating_ip(floating_ip: str) -> None:
    """Disassociate a floating IP from its current instance.

    Parameters
    ----------
    floating_ip : str
        Floating IP address or ID to disassociate.
    """
    conn = get_openstack_connection()
    if conn:
        try:
            fip_obj = _find_floating_ip(conn, floating_ip)
            if not fip_obj:
                logger.error(f"Floating IP '{floating_ip}' not found")
                exit(1)

            if not getattr(fip_obj, "port_id", None):
                logger.warning(
                    f"Floating IP {fip_obj.floating_ip_address} "
                    "is not currently associated"
                )
                return

            logger.info(f"Disassociating floating IP {fip_obj.floating_ip_address}...")

            conn.network.update_ip(fip_obj, port_id=None, fixed_ip_address=None)

            logger.success(
                f"Floating IP {fip_obj.floating_ip_address} successfully disassociated"
            )

        except Exception as e:
            logger.error(f"Error disassociating floating IP: {e}")
    else:
        logger.error("Failed to establish OpenStack connection")
        exit(1)


@app.command
def delete_floating_ip(floating_ip: str, force: bool = False) -> None:
    """Delete a floating IP.

    Parameters
    ----------
    floating_ip : str
        Floating IP address or ID to delete.
    force : bool, optional
        Force deletion without confirmation (default: False).
    """
    conn = get_openstack_connection()
    if conn:
        try:
            fip_obj = _find_floating_ip(conn, floating_ip)
            if not fip_obj:
                logger.error(f"Floating IP '{floating_ip}' not found")
                exit(1)

            if getattr(fip_obj, "port_id", None) and not force:
                logger.error(
                    f"Floating IP {fip_obj.floating_ip_address} "
                    "is currently associated with an instance"
                )
                logger.info("Disassociate it first or use --force flag")
                exit(1)

            if not force:
                logger.warning(
                    f"Are you sure you want to delete floating IP "
                    f"{fip_obj.floating_ip_address}?"
                )
                logger.info("Use --force flag to skip confirmation")
                exit(1)

            logger.info(f"Deleting floating IP {fip_obj.floating_ip_address}...")
            conn.network.delete_ip(fip_obj)
            logger.success(
                f"Floating IP {fip_obj.floating_ip_address} deleted successfully"
            )

        except Exception as e:
            logger.error(f"Error deleting floating IP: {e}")
    else:
        logger.error("Failed to establish OpenStack connection")
        exit(1)


@app.command
def show_floating_ip(floating_ip: str) -> None:
    """Show detailed information about a floating IP.

    Parameters
    ----------
    floating_ip : str
        Floating IP address or ID to show details for.
    """
    conn = get_openstack_connection()
    if conn:
        try:
            fip_obj = _find_floating_ip(conn, floating_ip)
            if not fip_obj:
                logger.error(f"Floating IP '{floating_ip}' not found")
                exit(1)

            _display_floating_ip_details(conn, fip_obj)

        except Exception as e:
            logger.error(f"Error showing floating IP details: {e}")
    else:
        logger.error("Failed to establish OpenStack connection")
        exit(1)


def _get_external_network(conn: Any, network: str) -> Any:
    """Get external network for floating IP creation."""
    if network:
        external_network = conn.network.find_network(network)
        if not external_network:
            logger.error(f"Network '{network}' not found")
            return None
        if not getattr(external_network, "is_router_external", False):
            logger.error(f"Network '{network}' is not external")
            return None
    else:
        external_networks = [
            net
            for net in conn.network.networks()
            if getattr(net, "is_router_external", False)
        ]
        if not external_networks:
            logger.error("No external networks found")
            return None
        external_network = external_networks[0]
        logger.info(f"Using external network: {external_network.name}")

    return external_network


def _display_floating_ip_details(conn: Any, fip_obj: Any) -> None:
    """Display detailed information for a floating IP."""
    logger.info("Floating IP Details:")
    logger.info(f"  IP Address: {fip_obj.floating_ip_address}")
    logger.info(f"  ID: {fip_obj.id}")
    logger.info(f"  Status: {fip_obj.status}")

    # Network information
    floating_network_id = getattr(fip_obj, "floating_network_id", None)
    if floating_network_id:
        network = conn.network.get_network(floating_network_id)
        logger.info(f"  External Network: {network.name} ({floating_network_id})")

    # Association information
    port_id = getattr(fip_obj, "port_id", None)
    fixed_ip = getattr(fip_obj, "fixed_ip_address", None)

    if port_id and fixed_ip:
        logger.info("  Associated with:")
        logger.info(f"    Fixed IP: {fixed_ip}")
        logger.info(f"    Port ID: {port_id}")

        # Try to get instance information
        try:
            port = conn.network.get_port(port_id)
            device_id = getattr(port, "device_id", None)
            if device_id:
                server = conn.compute.get_server(device_id)
                logger.info(f"    Instance: {server.name} ({device_id})")
        except Exception:
            pass
    else:
        logger.info("  Status: Available (not associated)")

    # Additional attributes
    description = getattr(fip_obj, "description", "")
    if description:
        logger.info(f"  Description: {description}")

    created_at = getattr(fip_obj, "created_at", "")
    if created_at:
        logger.info(f"  Created: {created_at}")

    updated_at = getattr(fip_obj, "updated_at", "")
    if updated_at:
        logger.info(f"  Updated: {updated_at}")


def _get_instance_port_info(conn: Any, server: Any, fixed_ip: str) -> tuple[str, Any]:
    """Get port information for an instance."""
    # Get instance IPs
    instance_ips = []
    for _, ips in server.addresses.items():
        for ip_info in ips:
            if ip_info.get("OS-EXT-IPS:type") == "fixed":
                instance_ips.append(ip_info["addr"])

    if not instance_ips:
        logger.error(f"No fixed IPs found for instance '{server.name}'")
        return "", None

    # Select target IP
    target_ip = fixed_ip if fixed_ip else instance_ips[0]
    if target_ip not in instance_ips:
        logger.error(f"Fixed IP '{target_ip}' not found on instance '{server.name}'")
        logger.info(f"Available IPs: {', '.join(instance_ips)}")
        return "", None

    # Find the port for the target IP
    ports = list(conn.network.ports(device_id=server.id))
    for port in ports:
        for fixed_ip_info in port.fixed_ips:
            if fixed_ip_info["ip_address"] == target_ip:
                return target_ip, port

    logger.error(f"Could not find port for IP '{target_ip}'")
    return "", None


def _find_floating_ip(conn: Any, floating_ip_identifier: str) -> Any:
    """Find a floating IP by address or ID.

    Parameters
    ----------
    conn : Any
        OpenStack connection object.
    floating_ip_identifier : str
        Floating IP address or ID.

    Returns
    -------
    Any
        Floating IP object or None if not found.
    """
    try:
        # Try to find by ID first
        try:
            return conn.network.get_ip(floating_ip_identifier)
        except Exception:
            pass

        # Try to find by IP address
        floating_ips = list(conn.network.ips())
        for fip in floating_ips:
            if fip.floating_ip_address == floating_ip_identifier:
                return fip

        return None
    except Exception:
        return None
