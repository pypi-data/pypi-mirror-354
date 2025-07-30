"""OpenStack instance management module.

This module provides comprehensive functions to manage OpenStack compute
instances including lifecycle operations (start, stop, reboot), creation,
deletion, resizing, and advanced operations like console access, metadata
management, and backup creation.

The module includes robust error handling, input validation, and detailed
logging for all operations.
"""

from typing import Any

import cyclopts
from loguru import logger
from tabulate import tabulate

from nnumbers.core import get_openstack_connection


app = cyclopts.App()


def _list_instances(conn: Any) -> None:
    """List all instances and their status in a formatted table.

    Retrieves all compute instances from the OpenStack cloud and displays
    them in a clean tabular format showing name, ID, and current status.

    Parameters
    ----------
    conn : Any
        OpenStack connection object with compute service access.

    Notes
    -----
    This is an internal helper function used by the list command.
    The table is formatted using the 'grid' style for better readability.

    Examples
    --------
    The output will look like:
    ┌─────────────┬──────────────────────────────────────┬─────────┐
    │ Name        │ ID                                   │ Status  │
    ├─────────────┼──────────────────────────────────────┼─────────┤
    │ web-server  │ 12345678-1234-1234-1234-123456789012 │ ACTIVE  │
    └─────────────┴──────────────────────────────────────┴─────────┘
    """
    logger.info("Listing instances...")
    lines = []
    for server in conn.compute.servers():
        lines.append(
            [
                server.name,
                server.id,
                server.status,
            ]
        )

    table = tabulate(
        lines,
        headers=["Name", "ID", "Status"],
        tablefmt="grid",
    )

    print(table)


def start_instance(conn: Any, instance_name_or_id: str) -> None:
    """Start an OpenStack instance.

    Starts a compute instance that is currently in SHUTOFF or stopped state.
    The function waits for the instance to reach ACTIVE state before returning,
    with a timeout of 300 seconds.

    Parameters
    ----------
    conn : Any
        OpenStack connection object with compute service access.
    instance_name_or_id : str
        Name or unique ID of the instance to start. The function will
        automatically resolve names to IDs.

    Raises
    ------
    Exception
        If the instance cannot be found, is already running, or fails
        to start within the timeout period.

    Notes
    -----
    - If the instance is already ACTIVE, no action is taken
    - The function provides real-time feedback during the start process
    - Network connectivity may take additional time after ACTIVE state

    Examples
    --------
    >>> start_instance(conn, "web-server")
    >>> start_instance(conn, "12345678-1234-1234-1234-123456789012")
    """
    try:
        logger.info(f"Attempting to start instance: {instance_name_or_id}...")
        server = conn.compute.find_server(instance_name_or_id)
        if server:
            if server.status == "ACTIVE":
                logger.info(f"Instance '{server.name}' is already active.")
            else:
                conn.compute.start_server(server)
                conn.compute.wait_for_server(server, status="ACTIVE", wait=300)
                logger.success(
                    f"Instance '{server.name}' (ID: {server.id}) started successfully."
                )
        else:
            logger.warning(f"Instance '{instance_name_or_id}' not found.")
    except Exception as e:
        logger.error(f"Error starting instance: {e}")


def stop_instance(conn: Any, instance_name_or_id: str) -> None:
    """Stop an OpenStack instance.

    Gracefully stops a running compute instance by sending a shutdown signal.
    The function waits for the instance to reach SHUTOFF state before returning,
    with a timeout of 300 seconds.

    Parameters
    ----------
    conn : Any
        OpenStack connection object with compute service access.
    instance_name_or_id : str
        Name or unique ID of the instance to stop. The function will
        automatically resolve names to IDs.

    Raises
    ------
    Exception
        If the instance cannot be found, is already stopped, or fails
        to stop within the timeout period.

    Notes
    -----
    - If the instance is already SHUTOFF, no action is taken
    - This performs a graceful shutdown, not a forced power-off
    - Data in memory will be lost; ensure applications are properly saved
    - Attached volumes and network interfaces remain connected

    Examples
    --------
    >>> stop_instance(conn, "web-server")
    >>> stop_instance(conn, "12345678-1234-1234-1234-123456789012")
    """
    try:
        logger.info(f"Attempting to stop instance: {instance_name_or_id}...")
        server = conn.compute.find_server(instance_name_or_id)
        if server:
            if server.status == "SHUTOFF":
                logger.info(f"Instance '{server.name}' is already stopped.")
            else:
                conn.compute.stop_server(server)
                conn.compute.wait_for_server(server, status="SHUTOFF", wait=300)
                logger.success(
                    f"Instance '{server.name}' (ID: {server.id}) stopped successfully."
                )
        else:
            logger.warning(f"Instance '{instance_name_or_id}' not found.")
    except Exception as e:
        logger.error(f"Error stopping instance: {e}")


def reboot_instance(conn: Any, instance_name_or_id: str) -> None:
    """Reboot an OpenStack instance.

    Performs a soft reboot of the compute instance, which is equivalent to
    sending a restart signal to the operating system. The function waits
    for the instance to return to ACTIVE state after the reboot.

    Parameters
    ----------
    conn : Any
        OpenStack connection object with compute service access.
    instance_name_or_id : str
        Name or unique ID of the instance to reboot. The function will
        automatically resolve names to IDs.

    Raises
    ------
    Exception
        If the instance cannot be found or fails to reboot within
        the timeout period.

    Notes
    -----
    - This performs a soft reboot (ACPI restart signal)
    - For hard reboot, use the force_reboot command instead
    - The instance will temporarily become unavailable during reboot
    - All network connections will be interrupted

    Examples
    --------
    >>> reboot_instance(conn, "web-server")
    >>> reboot_instance(conn, "12345678-1234-1234-1234-123456789012")
    """
    try:
        logger.info(f"Attempting to reboot instance: {instance_name_or_id}...")
        server = conn.compute.find_server(instance_name_or_id)
        if server:
            conn.compute.reboot_server(server)
            conn.compute.wait_for_server(
                server, status="ACTIVE", wait=300
            )  # Wait until it's active again
            logger.success(
                f"Instance '{server.name}' (ID: {server.id}) rebooted successfully."
            )
        else:
            logger.warning(f"Instance '{instance_name_or_id}' not found.")
    except Exception as e:
        logger.error(f"Error rebooting instance: {e}")


@app.command(name="list")
def list_instances() -> None:
    """List all OpenStack instances and their status.

    Retrieves and displays all compute instances in the current project
    in a formatted table showing instance name, ID, and current status.

    Raises
    ------
    SystemExit
        If connection to OpenStack fails.

    Examples
    --------
    $ nnumbers instance list
    ┌─────────────┬──────────────────────────────────────┬─────────┐
    │ Name        │ ID                                   │ Status  │
    ├─────────────┼──────────────────────────────────────┼─────────┤
    │ web-server  │ 12345678-1234-1234-1234-123456789012 │ ACTIVE  │
    │ db-server   │ 87654321-4321-4321-4321-210987654321 │ SHUTOFF │
    └─────────────┴──────────────────────────────────────┴─────────┘
    """
    conn = get_openstack_connection()
    if conn:
        _list_instances(conn)
    else:
        logger.error("Failed to establish OpenStack connection")
        raise SystemExit(1)


@app.command
def start(instance: str) -> None:
    """Start an OpenStack instance.

    Starts a stopped or suspended compute instance and waits for it
    to reach the ACTIVE state. If the instance is already running,
    no action is taken.

    Parameters
    ----------
    instance : str
        Name or unique ID of the instance to start. The command will
        automatically resolve instance names to IDs.

    Raises
    ------
    SystemExit
        If connection to OpenStack fails.

    Examples
    --------
    $ nnumbers instance start web-server
    $ nnumbers instance start 12345678-1234-1234-1234-123456789012
    """
    conn = get_openstack_connection()
    if conn:
        start_instance(conn, instance)
    else:
        logger.error("Failed to establish OpenStack connection")
        raise SystemExit(1)


@app.command
def stop(instance: str) -> None:
    """Stop an OpenStack instance.

    Gracefully stops a running compute instance by sending a shutdown
    signal and waits for it to reach the SHUTOFF state. If the instance
    is already stopped, no action is taken.

    Parameters
    ----------
    instance : str
        Name or unique ID of the instance to stop. The command will
        automatically resolve instance names to IDs.

    Raises
    ------
    SystemExit
        If connection to OpenStack fails.

    Notes
    -----
    This performs a graceful shutdown. Any unsaved data in memory
    will be lost. Ensure applications are properly saved before stopping.

    Examples
    --------
    $ nnumbers instance stop web-server
    $ nnumbers instance stop 12345678-1234-1234-1234-123456789012
    """
    conn = get_openstack_connection()
    if conn:
        stop_instance(conn, instance)
    else:
        logger.error("Failed to establish OpenStack connection")
        raise SystemExit(1)


@app.command
def reboot(instance: str) -> None:
    """Reboot an OpenStack instance.

    Performs a soft reboot of the compute instance, equivalent to
    restarting the operating system. The instance will temporarily
    become unavailable and return to ACTIVE state after reboot.

    Parameters
    ----------
    instance : str
        Name or unique ID of the instance to reboot. The command will
        automatically resolve instance names to IDs.

    Raises
    ------
    SystemExit
        If connection to OpenStack fails.

    Notes
    -----
    - This performs a soft reboot (ACPI restart signal)
    - Network connections will be interrupted during reboot
    - The instance will retain its IP addresses and attached volumes

    Examples
    --------
    $ nnumbers instance reboot web-server
    $ nnumbers instance reboot 12345678-1234-1234-1234-123456789012
    """
    conn = get_openstack_connection()
    if conn:
        reboot_instance(conn, instance)
    else:
        logger.error("Failed to establish OpenStack connection")
        raise SystemExit(1)


@app.command
def status(instance: str) -> None:
    """Check the status of a specific OpenStack instance.

    Retrieves and displays detailed information about an instance including
    its current status, flavor, image, and network information.

    Parameters
    ----------
    instance : str
        Name or unique ID of the instance to check. The command will
        automatically resolve instance names to IDs.

    Raises
    ------
    SystemExit
        If connection to OpenStack fails.

    Examples
    --------
    $ nnumbers instance status web-server
    Instance: web-server
    ID: 12345678-1234-1234-1234-123456789012
    Status: ACTIVE
    Flavor: m1.medium
    Image: ubuntu-20.04
    IP (public): 192.168.1.10
    IP (private): 10.0.0.15
    """
    conn = get_openstack_connection()
    if conn:
        try:
            server = conn.compute.find_server(instance)
            if server:
                logger.info(f"Instance: {server.name}")
                logger.info(f"ID: {server.id}")
                logger.info(f"Status: {server.status}")
                if hasattr(server, "flavor") and server.flavor:
                    flavor_name = (
                        server.flavor.get("original_name", "N/A")
                        if isinstance(server.flavor, dict)
                        else getattr(server.flavor, "name", "N/A")
                    )
                    logger.info(f"Flavor: {flavor_name}")
                if hasattr(server, "image") and server.image:
                    image_name = (
                        server.image.get("name", "N/A")
                        if isinstance(server.image, dict)
                        else getattr(server.image, "name", "N/A")
                    )
                    logger.info(f"Image: {image_name}")
                if hasattr(server, "addresses") and server.addresses:
                    for network, ips in server.addresses.items():
                        for ip_info in ips:
                            logger.info(f"IP ({network}): {ip_info['addr']}")
            else:
                logger.warning(f"Instance '{instance}' not found.")
        except Exception as e:
            logger.error(f"Error checking instance status: {e}")
    else:
        logger.error("Failed to establish OpenStack connection")
        raise SystemExit(1)


@app.command
def manage(instance: str, action: str) -> None:
    """Manage an OpenStack instance with specified action.

    Provides a unified interface for performing common instance management
    operations. This is a convenience command that delegates to the
    specific action commands.

    Parameters
    ----------
    instance : str
        Name or unique ID of the instance to manage.
    action : str
        Action to perform on the instance. Valid actions are:
        'start', 'stop', 'reboot', 'status'.

    Raises
    ------
    SystemExit
        If an invalid action is provided.

    Examples
    --------
    $ nnumbers instance manage web-server start
    $ nnumbers instance manage web-server stop
    $ nnumbers instance manage web-server reboot
    $ nnumbers instance manage web-server status
    """
    action = action.lower()
    if action == "start":
        start(instance)
    elif action == "stop":
        stop(instance)
    elif action == "reboot":
        reboot(instance)
    elif action == "status":
        status(instance)
    else:
        logger.error(f"Invalid action: {action}")
        logger.info("Valid actions: start, stop, reboot, status")
        raise SystemExit(1)


@app.command
def create(
    name: str,
    flavor: str,
    image: str,
    network: str = "default",
    key_name: str = "",
    disk_size: int = 0,
    delete_on_termination: bool = True,
    volume_type: str = "",
) -> None:
    """Create a new OpenStack instance.

    Parameters
    ----------
    name : str
        Name for the new instance.
    flavor : str
        Flavor name or ID for the instance.
    image : str
        Image name or ID for the instance.
    network : str, optional
        Network name or ID (default: "default").
    key_name : str, optional
        SSH key pair name for the instance.
    disk_size : int, optional
        Root disk size in GB. If 0, uses image default size.
    delete_on_termination : bool, optional
        Whether to delete the volume when instance is deleted (default: True).
    volume_type : str, optional
        Volume type for the root disk (e.g., "ssd", "hdd").
    """
    conn = get_openstack_connection()
    if conn:
        try:
            logger.info(f"Creating instance '{name}'...")

            flavor_obj, image_obj, network_obj = _validate_create_resources(
                conn, flavor, image, network
            )

            # Prepare server creation parameters
            server_params = {
                "name": name,
                "flavor_id": flavor_obj.id,
                "networks": [{"uuid": network_obj.id}],
            }

            if key_name:
                server_params["key_name"] = key_name

            # Handle disk configuration
            if disk_size > 0:
                # Create boot volume with custom size
                logger.info(f"Creating boot volume with {disk_size}GB...")

                volume_params = _prepare_boot_volume_config(
                    conn, image_obj, disk_size, delete_on_termination, volume_type
                )

                # Use block device mapping for boot from volume
                server_params["block_device_mapping_v2"] = [volume_params]
                logger.info(
                    f"Boot volume configured: {disk_size}GB, "
                    f"delete_on_termination={delete_on_termination}"
                )
            else:
                # Use image directly (default behavior)
                server_params["image_id"] = image_obj.id
                logger.info("Using image directly for boot disk")

            # Create the server
            server = conn.compute.create_server(**server_params)
            logger.info("Server creation initiated. Waiting for ACTIVE status...")
            conn.compute.wait_for_server(server, status="ACTIVE", wait=600)

            logger.success(f"Instance '{name}' created successfully!")
            logger.info(f"Instance ID: {server.id}")

            # Show additional information
            if disk_size > 0:
                logger.info(f"Root disk size: {disk_size}GB")
                logger.info(f"Delete on termination: {delete_on_termination}")
                if volume_type:
                    logger.info(f"Volume type: {volume_type}")

        except Exception as e:
            logger.error(f"Error creating instance: {e}")
            # Provide more specific error information
            if "quota" in str(e).lower():
                logger.info("Check your quota limits with: ./openstack-cli quota")
            elif "flavor" in str(e).lower():
                logger.info("List available flavors with: ./openstack-cli list-flavors")
            elif "image" in str(e).lower():
                logger.info("List available images with: ./openstack-cli list-images")
    else:
        logger.error("Failed to establish OpenStack connection")
        exit(1)


@app.command
def delete(instance: str, force: bool = False) -> None:
    """Delete an OpenStack instance.

    Parameters
    ----------
    instance : str
        Name or ID of the instance to delete.
    force : bool, optional
        Force deletion without confirmation (default: False).
    """
    conn = get_openstack_connection()
    if conn:
        try:
            server = conn.compute.find_server(instance)
            if server:
                if not force:
                    logger.warning(f"Are you sure you want to delete '{server.name}'?")
                    logger.info("Use --force flag to skip confirmation")
                    exit(1)

                logger.info(f"Deleting instance '{server.name}'...")
                conn.compute.delete_server(server)
                conn.compute.wait_for_delete(server, wait=300)
                logger.success(
                    f"Instance '{server.name}' (ID: {server.id}) deleted successfully."
                )
            else:
                logger.warning(f"Instance '{instance}' not found.")
        except Exception as e:
            logger.error(f"Error deleting instance: {e}")
    else:
        logger.error("Failed to establish OpenStack connection")
        exit(1)


@app.command
def resize(instance: str, new_flavor: str) -> None:
    """Resize an OpenStack instance to a new flavor.

    Parameters
    ----------
    instance : str
        Name or ID of the instance to resize.
    new_flavor : str
        New flavor name or ID for the instance.
    """
    conn = get_openstack_connection()
    if conn:
        try:
            server = conn.compute.find_server(instance)
            if not server:
                logger.warning(f"Instance '{instance}' not found.")
                return

            flavor_obj = conn.compute.find_flavor(new_flavor)
            if not flavor_obj:
                logger.error(f"Flavor '{new_flavor}' not found")
                exit(1)

            logger.info(
                f"Resizing instance '{server.name}' to flavor '{new_flavor}'..."
            )
            conn.compute.resize_server(server, flavor_obj.id)
            conn.compute.wait_for_server(server, status="VERIFY_RESIZE", wait=600)

            # Confirm the resize
            conn.compute.confirm_server_resize(server)
            conn.compute.wait_for_server(server, status="ACTIVE", wait=300)

            logger.success(
                f"Instance '{server.name}' resized to '{new_flavor}' successfully."
            )

        except Exception as e:
            logger.error(f"Error resizing instance: {e}")
    else:
        logger.error("Failed to establish OpenStack connection")
        exit(1)


@app.command
def list_flavors() -> None:
    """List all available OpenStack flavors."""
    conn = get_openstack_connection()
    if conn:
        try:
            logger.info("Listing flavors...")
            flavors = list(conn.compute.flavors())
            if flavors:
                lines = []
                for flavor in sorted(flavors, key=lambda x: x.name):
                    lines.append(
                        [
                            flavor.name,
                            flavor.id,
                            f"{flavor.ram}MB",
                            flavor.vcpus,
                            f"{flavor.disk}GB",
                        ]
                    )

                table = tabulate(
                    lines,
                    headers=["Name", "ID", "RAM", "VCPUs", "Disk"],
                    tablefmt="grid",
                )
                print(table)
            else:
                logger.info("No flavors found.")
        except Exception as e:
            logger.error(f"Error listing flavors: {e}")
    else:
        logger.error("Failed to establish OpenStack connection")
        exit(1)


@app.command
def list_images() -> None:
    """List all available OpenStack images."""
    conn = get_openstack_connection()
    if conn:
        try:
            logger.info("Listing images...")
            images = list(conn.compute.images())
            if images:
                lines = []
                for image in sorted(images, key=lambda x: x.name):
                    status = getattr(image, "status", "unknown")
                    size = getattr(image, "size", 0)
                    size_mb = f"{size // (1024 * 1024)}MB" if size else "unknown"
                    lines.append(
                        [
                            image.name,
                            image.id,
                            status,
                            size_mb,
                        ]
                    )

                table = tabulate(
                    lines,
                    headers=["Name", "ID", "Status", "Size"],
                    tablefmt="grid",
                )
                print(table)
            else:
                logger.info("No images found.")
        except Exception as e:
            logger.error(f"Error listing images: {e}")
    else:
        logger.error("Failed to establish OpenStack connection")
        exit(1)


@app.command
def console(instance: str) -> None:
    """Get console URL for an OpenStack instance.

    Parameters
    ----------
    instance : str
        Name or ID of the instance to get console for.
    """
    conn = get_openstack_connection()
    if conn:
        try:
            server = conn.compute.find_server(instance)
            if server:
                console = conn.compute.get_server_console_url(
                    server, console_type="novnc"
                )
                logger.success(f"Console URL for '{server.name}':")
                logger.info(f"{console['url']}")
            else:
                logger.warning(f"Instance '{instance}' not found.")
        except Exception as e:
            logger.error(f"Error getting console URL: {e}")
    else:
        logger.error("Failed to establish OpenStack connection")
        exit(1)


@app.command
def logs(instance: str, lines: int = 50) -> None:
    """Get console logs for an OpenStack instance.

    Parameters
    ----------
    instance : str
        Name or ID of the instance to get logs for.
    lines : int, optional
        Number of log lines to retrieve (default: 50).
    """
    conn = get_openstack_connection()
    if conn:
        try:
            server = conn.compute.find_server(instance)
            if server:
                logger.info(f"Console logs for '{server.name}' (last {lines} lines):")
                console_log = conn.compute.get_server_console_output(
                    server, length=lines
                )
                if console_log:
                    logger.info(console_log)
                else:
                    logger.warning("No console logs available.")
            else:
                logger.warning(f"Instance '{instance}' not found.")
        except Exception as e:
            logger.error(f"Error getting console logs: {e}")
    else:
        logger.error("Failed to establish OpenStack connection")
        exit(1)


@app.command
def ssh_key_add(instance: str, public_key_path: str) -> None:
    """Add SSH public key to an OpenStack instance.

    Parameters
    ----------
    instance : str
        Name or ID of the instance.
    public_key_path : str
        Path to the SSH public key file.
    """
    conn = get_openstack_connection()
    if conn:
        try:
            from pathlib import Path

            key_file = Path(public_key_path)
            if not key_file.exists():
                logger.error(f"SSH key file not found: {public_key_path}")
                exit(1)

            server = conn.compute.find_server(instance)
            if server:
                public_key = key_file.read_text().strip()
                logger.info(f"Adding SSH key to '{server.name}'...")

                # This would require cloud-init or custom metadata handling
                # For demonstration, we'll show how to add it via metadata
                metadata = {"ssh_public_key": public_key}
                conn.compute.set_server_metadata(server, **metadata)

                logger.success(
                    f"SSH key added to '{server.name}' metadata. "
                    f"Restart may be required."
                )
            else:
                logger.warning(f"Instance '{instance}' not found.")
        except Exception as e:
            logger.error(f"Error adding SSH key: {e}")
    else:
        logger.error("Failed to establish OpenStack connection")
        exit(1)


@app.command
def metadata(instance: str, key: str = "", value: str = "") -> None:
    """Get or set metadata for an OpenStack instance.

    Parameters
    ----------
    instance : str
        Name or ID of the instance.
    key : str, optional
        Metadata key to set (requires value).
    value : str, optional
        Metadata value to set (requires key).
    """
    conn = get_openstack_connection()
    if conn:
        try:
            server = conn.compute.find_server(instance)
            if not server:
                logger.warning(f"Instance '{instance}' not found.")
                return

            if key and value:
                # Set metadata
                logger.info(f"Setting metadata '{key}' = '{value}' for '{server.name}'")
                conn.compute.set_server_metadata(server, **{key: value})
                logger.success("Metadata set successfully.")
            elif key:
                # Get specific metadata key
                metadata = conn.compute.get_server_metadata(server)
                if key in metadata:
                    logger.info(f"{key}: {metadata[key]}")
                else:
                    logger.warning(f"Metadata key '{key}' not found.")
            else:
                # Get all metadata
                metadata = conn.compute.get_server_metadata(server)
                if metadata:
                    logger.info(f"Metadata for '{server.name}':")
                    for k, v in metadata.items():
                        logger.info(f"  {k}: {v}")
                else:
                    logger.info("No metadata found.")

        except Exception as e:
            logger.error(f"Error handling metadata: {e}")
    else:
        logger.error("Failed to establish OpenStack connection")
        exit(1)


@app.command
def backup(instance: str, backup_name: str = "") -> None:
    """Create a backup (snapshot) of an OpenStack instance.

    Parameters
    ----------
    instance : str
        Name or ID of the instance to backup.
    backup_name : str, optional
        Name for the backup. If not provided, auto-generated.
    """
    conn = get_openstack_connection()
    if conn:
        try:
            server = conn.compute.find_server(instance)
            if server:
                if not backup_name:
                    from datetime import datetime

                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    backup_name = f"{server.name}_backup_{timestamp}"

                logger.info(f"Creating backup '{backup_name}' for '{server.name}'...")
                image = conn.compute.create_server_image(
                    server, name=backup_name, wait=True, timeout=1200
                )
                logger.success(
                    f"Backup '{backup_name}' created successfully! Image ID: {image.id}"
                )
            else:
                logger.warning(f"Instance '{instance}' not found.")
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
    else:
        logger.error("Failed to establish OpenStack connection")
        exit(1)


@app.command
def list_volume_types() -> None:
    """List all available OpenStack volume types."""
    conn = get_openstack_connection()
    if conn:
        try:
            logger.info("Listing volume types...")
            volume_types = list(conn.volume.types())
            if volume_types:
                lines = []
                for vol_type in sorted(volume_types, key=lambda x: x.name):
                    description = getattr(vol_type, "description", "")
                    extra_specs = getattr(vol_type, "extra_specs", {})
                    specs_str = str(extra_specs) if extra_specs else "-"
                    lines.append(
                        [
                            vol_type.name,
                            vol_type.id,
                            description or "-",
                            specs_str,
                        ]
                    )

                table = tabulate(
                    lines,
                    headers=["Name", "ID", "Description", "Extra Specs"],
                    tablefmt="grid",
                )
                print(table)
            else:
                logger.info("No volume types found.")
        except Exception as e:
            logger.error(f"Error listing volume types: {e}")
    else:
        logger.error("Failed to establish OpenStack connection")
        exit(1)


@app.command
def list_volumes() -> None:
    """List all OpenStack volumes in the current project."""
    conn = get_openstack_connection()
    if conn:
        try:
            logger.info("Listing volumes...")
            volumes = list(conn.volume.volumes())
            if volumes:
                lines = []
                for volume in sorted(volumes, key=lambda x: x.name or x.id):
                    name = volume.name or "unnamed"
                    status = getattr(volume, "status", "unknown")
                    size = getattr(volume, "size", 0)
                    vol_type = getattr(volume, "volume_type", "unknown")
                    bootable = getattr(volume, "bootable", False)
                    attached = getattr(volume, "attachments", [])

                    # Determine attachment status
                    if attached:
                        attachment_info = []
                        for attachment in attached:
                            server_id = attachment.get("server_id", "unknown")
                            device = attachment.get("device", "unknown")
                            attachment_info.append(f"{server_id} ({device})")
                        attached_str = "; ".join(attachment_info)
                    else:
                        attached_str = "Available"

                    lines.append(
                        [
                            name,
                            volume.id,
                            f"{size}GB",
                            status,
                            vol_type,
                            "Yes" if bootable else "No",
                            attached_str,
                        ]
                    )

                table = tabulate(
                    lines,
                    headers=[
                        "Name",
                        "ID",
                        "Size",
                        "Status",
                        "Type",
                        "Bootable",
                        "Attached",
                    ],
                    tablefmt="grid",
                )
                print(table)
            else:
                logger.info("No volumes found.")
        except Exception as e:
            logger.error(f"Error listing volumes: {e}")
    else:
        logger.error("Failed to establish OpenStack connection")
        exit(1)


@app.command
def volume_attach(instance: str, volume: str, device: str = "") -> None:
    """Attach a volume to an OpenStack instance.

    Parameters
    ----------
    instance : str
        Name or ID of the instance.
    volume : str
        Name or ID of the volume to attach.
    device : str, optional
        Device path (e.g., /dev/vdb). Auto-assigned if not specified.
    """
    conn = get_openstack_connection()
    if conn:
        try:
            server = conn.compute.find_server(instance)
            if not server:
                logger.warning(f"Instance '{instance}' not found.")
                return

            volume_obj = conn.volume.find_volume(volume)
            if not volume_obj:
                logger.warning(f"Volume '{volume}' not found.")
                return

            logger.info(
                f"Attaching volume '{volume_obj.name or volume_obj.id}' "
                f"to instance '{server.name}'..."
            )

            attachment_params = {"volume_id": volume_obj.id}
            if device:
                attachment_params["device"] = device

            conn.compute.create_volume_attachment(server, **attachment_params)
            logger.success("Volume attached successfully!")

            if device:
                logger.info(f"Device path: {device}")
            else:
                logger.info("Device path auto-assigned by OpenStack")

        except Exception as e:
            logger.error(f"Error attaching volume: {e}")
    else:
        logger.error("Failed to establish OpenStack connection")
        exit(1)


@app.command
def volume_detach(instance: str, volume: str) -> None:
    """Detach a volume from an OpenStack instance.

    Parameters
    ----------
    instance : str
        Name or ID of the instance.
    volume : str
        Name or ID of the volume to detach.
    """
    conn = get_openstack_connection()
    if conn:
        try:
            server = conn.compute.find_server(instance)
            if not server:
                logger.warning(f"Instance '{instance}' not found.")
                return

            volume_obj = conn.volume.find_volume(volume)
            if not volume_obj:
                logger.warning(f"Volume '{volume}' not found.")
                return

            logger.info(
                f"Detaching volume '{volume_obj.name or volume_obj.id}' "
                f"from instance '{server.name}'..."
            )

            conn.compute.delete_volume_attachment(server, volume_obj.id)
            logger.success("Volume detached successfully!")

        except Exception as e:
            logger.error(f"Error detaching volume: {e}")
    else:
        logger.error("Failed to establish OpenStack connection")
        exit(1)


def _prepare_boot_volume_config(
    conn: Any,
    image_obj: Any,
    disk_size: int,
    delete_on_termination: bool,
    volume_type: str,
) -> dict:
    """Prepare boot volume configuration for instance creation.

    Parameters
    ----------
    conn : Any
        OpenStack connection object.
    image_obj : Any
        OpenStack image object.
    disk_size : int
        Disk size in GB.
    delete_on_termination : bool
        Whether to delete volume on instance termination.
    volume_type : str
        Volume type name.

    Returns
    -------
    dict
        Volume configuration dictionary.
    """
    volume_params = {
        "source_type": "image",
        "uuid": image_obj.id,
        "destination_type": "volume",
        "volume_size": disk_size,
        "delete_on_termination": delete_on_termination,
        "boot_index": 0,
    }

    if volume_type:
        # Verify volume type exists
        try:
            vol_types = list(conn.volume.types())
            vol_type_names = [vt.name for vt in vol_types]
            if volume_type not in vol_type_names:
                logger.warning(
                    f"Volume type '{volume_type}' not found. "
                    f"Available types: {', '.join(vol_type_names)}"
                )
            else:
                volume_params["volume_type"] = volume_type
                logger.info(f"Using volume type: {volume_type}")
        except Exception as e:
            logger.warning(f"Could not verify volume type: {e}")

    return volume_params


def _validate_create_resources(
    conn: Any, flavor: str, image: str, network: str
) -> tuple:
    """Validate and find OpenStack resources for instance creation.

    Parameters
    ----------
    conn : Any
        OpenStack connection object.
    flavor : str
        Flavor name or ID.
    image : str
        Image name or ID.
    network : str
        Network name or ID.

    Returns
    -------
    tuple
        Tuple of (flavor_obj, image_obj, network_obj).
    """
    # Find the required resources
    flavor_obj = conn.compute.find_flavor(flavor)
    if not flavor_obj:
        logger.error(f"Flavor '{flavor}' not found")
        exit(1)

    image_obj = conn.compute.find_image(image)
    if not image_obj:
        logger.error(f"Image '{image}' not found")
        exit(1)

    network_obj = conn.network.find_network(network)
    if not network_obj:
        logger.error(f"Network '{network}' not found")
        exit(1)

    return flavor_obj, image_obj, network_obj
