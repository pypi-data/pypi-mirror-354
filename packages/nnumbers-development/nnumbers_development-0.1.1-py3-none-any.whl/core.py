"""Core OpenStack connection and resource management functionality.

This module provides the fundamental OpenStack connection handling and
core resource management commands including quota and usage monitoring.
"""

from __future__ import annotations

from typing import Any

import cyclopts
from loguru import logger
import openstack
from tabulate import tabulate


app = cyclopts.App()


class OpenStackConnectionError(Exception):
    """Custom exception for OpenStack connection errors.

    This exception is raised when the CLI fails to establish a connection
    to the OpenStack cloud, typically due to missing or invalid credentials.

    Attributes
    ----------
    message : str
        Human-readable error message describing the connection failure.
    original_exception : Exception, optional
        The original exception that caused the connection failure.
    """

    def __init__(
        self, message: str, original_exception: Exception | None = None
    ) -> None:
        """Initialize the OpenStackConnectionError.

        Parameters
        ----------
        message : str
            Human-readable error message.
        original_exception : Exception, optional
            The original exception that caused this error.
        """
        super().__init__(message)
        self.message = message
        self.original_exception = original_exception


def get_openstack_connection() -> Any:
    """Establish a connection with OpenStack.

    Attempts to create an OpenStack connection using credentials from
    environment variables or a clouds.yaml file. The connection is
    automatically configured based on the OpenStack SDK's standard
    credential discovery mechanism.

    Returns
    -------
    Any
        OpenStack connection object if successful.

    Raises
    ------
    OpenStackConnectionError
        If connection to OpenStack fails due to missing or invalid
        credentials, network issues, or service unavailability.

    Notes
    -----
    The function expects OpenStack credentials to be available through:
    - Environment variables (OS_USERNAME, OS_PASSWORD, OS_AUTH_URL, etc.)
    - A clouds.yaml file in standard locations (~/.config/openstack/, etc.)

    Examples
    --------
    >>> conn = get_openstack_connection()
    >>> servers = list(conn.compute.servers())
    """
    try:
        conn = openstack.connect()
        # Test the connection by attempting a simple operation
        _ = conn.current_project_id
        return conn
    except Exception as e:
        logger.error(f"Error connecting to OpenStack: {e}")
        logger.info(
            "Make sure your OpenStack environment variables are configured "
            "(e.g., source openrc) or that the clouds.yaml file is present."
        )
        raise OpenStackConnectionError(
            "Failed to connect to OpenStack", original_exception=e
        ) from e


@app.command
def quota() -> None:
    """Show OpenStack quota information for the current project.

    Displays detailed quota information including:
    - Compute quotas (instances, VCPUs, RAM)
    - Volume quotas (volumes, snapshots, storage)
    - Network quotas (networks, subnets, ports, routers, floating IPs)

    The command automatically retrieves quotas for the currently
    authenticated project and displays them in a human-readable format.

    Raises
    ------
    OpenStackConnectionError
        If connection to OpenStack fails.
    SystemExit
        If quota information cannot be retrieved.

    Examples
    --------
    $ nnumbers core quota
    Compute Quotas:
      Instances: 10
      VCPUs: 20
      RAM (MB): 51200
    ...
    """
    conn = get_openstack_connection()
    if conn:
        try:
            # Get compute quotas
            cq = conn.compute.get_quota_set(conn.current_project_id)

            logger.info("Compute Quotas:")
            logger.info(f"  Instances: {cq.instances}")
            logger.info(f"  VCPUs: {cq.cores}")
            logger.info(f"  RAM (MB): {cq.ram}")

            # Get volume quotas from block storage service
            try:
                volume_quotas = conn.block_storage.get_quota_set(
                    conn.current_project_id
                )
                logger.info("\nVolume Quotas:")
                logger.info(f"  Volumes: {volume_quotas.volumes}")
                logger.info(f"  Snapshots: {volume_quotas.snapshots}")
                logger.info(f"  Volume Storage (GB): {volume_quotas.gigabytes}")
                if hasattr(volume_quotas, "backups"):
                    logger.info(f"  Backups: {volume_quotas.backups}")
            except Exception as e:
                logger.warning(f"Volume quota information not available: {e}")
            try:
                network_quotas = conn.network.get_quota(conn.current_project_id)
                logger.info("\nNetwork Quotas:")
                logger.info(f"  Networks: {network_quotas.networks}")
                logger.info(f"  Subnets: {network_quotas.subnets}")
                logger.info(f"  Ports: {network_quotas.ports}")
                logger.info(f"  Routers: {network_quotas.routers}")
                logger.info(f"  Floating IPs: {network_quotas.floating_ips}")
                if hasattr(network_quotas, "security_groups"):
                    logger.info(f"  Security Groups: {network_quotas.security_groups}")
                if hasattr(network_quotas, "security_group_rules"):
                    logger.info(
                        f"  Security Group Rules: {network_quotas.security_group_rules}"
                    )
            except Exception as e:
                logger.warning(f"Network quota information not available: {e}")

        except Exception as e:
            logger.error(f"Error getting quota information: {e}")
    else:
        logger.error("Failed to establish OpenStack connection")
        raise SystemExit(1)


@app.command
def usage() -> None:
    """Show detailed resource usage against quotas.

    Displays current resource consumption compared to quotas across:
    - Compute resources (instances, VCPUs, RAM usage vs limits)
    - Volume resources (volumes, snapshots, storage usage vs limits)
    - Network resources (networks, subnets, ports, routers vs limits)
    - Floating IP usage with allocation status breakdown

    The command calculates actual usage by examining existing resources
    and presents the data in tabular format for easy comparison against
    quota limits.

    Raises
    ------
    OpenStackConnectionError
        If connection to OpenStack fails.
    SystemExit
        If usage information cannot be retrieved.

    Examples
    --------
    $ nnumbers core usage
    Compute Usage
    ┌───────────┬────────┬───────────┐
    │ Instances │ VCPUs  │ RAM (MB)  │
    ├───────────┼────────┼───────────┤
    │ 5/10      │ 10/20  │ 8192/51200│
    └───────────┴────────┴───────────┘
    ...
    """
    conn = get_openstack_connection()
    if conn:
        try:
            # Compute usage
            instances = list(conn.compute.servers())
            total_vcpus = 0
            total_ram = 0

            flavors = list(conn.compute.flavors())
            if not flavors:
                raise ValueError("No flavors found in OpenStack")

            flavors_cache = {}
            for flavor in flavors:
                flavors_cache[flavor.name] = flavor.id

            for instance in instances:
                try:
                    flavor = conn.compute.get_flavor(flavors_cache[instance.flavor.id])
                    total_vcpus += flavor.vcpus
                    total_ram += flavor.ram
                except Exception as e:
                    logger.warning(
                        f"Could not get flavor {instance.flavor.id} "
                        f"for instance {instance.name}: {e}"
                    )
                    # Try to get flavor info from instance directly
                    # if available
                    if hasattr(instance, "flavor") and hasattr(
                        instance.flavor, "vcpus"
                    ):
                        total_vcpus += instance.flavor.vcpus
                        total_ram += instance.flavor.ram
                    else:
                        logger.warning(
                            f"Skipping resource count for instance {instance.name}"
                        )

            cq = conn.compute.get_quota_set(conn.current_project_id)

            print("Compute Usage")
            computation_table = tabulate(
                [
                    [
                        f"{len(instances)}/{cq.instances}",
                        f"{total_vcpus}/{cq.cores}",
                        f"{total_ram}/{cq.ram}",
                    ]
                ],
                headers=["Instances", "VCPUs", "RAM (MB)"],
                tablefmt="grid",
            )

            print(computation_table)

            # Volume usage
            volumes = list(conn.block_storage.volumes())
            snapshots = list(conn.block_storage.snapshots())
            total_storage = sum(v.size for v in volumes)

            vq = conn.block_storage.get_quota_set(conn.current_project_id)

            print("\nVolume Usage:")
            block_storage_table = tabulate(
                [
                    [
                        f"{len(volumes)}/{vq.volumes}",
                        f"{len(snapshots)}/{vq.snapshots}",
                        f"{total_storage}/{vq.gigabytes}",
                    ]
                ],
                headers=["Volumes", "Snapshots", "Storage (GB)"],
                tablefmt="grid",
            )

            print(block_storage_table)

            # Count actual network resources
            networks = list(conn.network.networks())
            subnets = list(conn.network.subnets())
            ports = list(conn.network.ports())
            routers = list(conn.network.routers())
            floating_ips = list(conn.network.ips())

            print("\nNetwork Usage:")
            nq = conn.network.get_quota(conn.current_project_id)
            network_table = tabulate(
                [
                    [
                        f"{len(networks)}/{nq.networks}",
                        f"{len(subnets)}/{nq.subnets}",
                        f"{len(ports)}/{nq.ports}",
                        f"{len(routers)}/{nq.routers}",
                    ]
                ],
                headers=["Networks", "Subnets", "Ports", "Routers"],
                tablefmt="grid",
            )
            print(network_table)

            # Floating IP usage with status breakdown
            floating_ips_allocated = len(
                [ip for ip in floating_ips if ip.status == "ACTIVE"]
            )
            floating_ips_available = len(
                [ip for ip in floating_ips if ip.status == "DOWN"]
            )

            print("\nFloating IP Usage:")
            floating_ip_table = tabulate(
                [
                    [
                        f"{len(floating_ips)}/{nq.floating_ips}",
                        f"{floating_ips_allocated}",
                        f"{floating_ips_available}",
                    ]
                ],
                headers=["Total FIPs", "Allocated", "Available"],
                tablefmt="grid",
            )
            print(floating_ip_table)

        except Exception as e:
            logger.error(f"Error getting usage information: {e}")
