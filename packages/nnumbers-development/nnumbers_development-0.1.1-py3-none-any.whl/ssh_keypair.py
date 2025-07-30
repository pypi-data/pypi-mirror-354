"""OpenStack SSH keypair management module.

This module provides comprehensive functions to manage OpenStack SSH keypairs
including creation (both import and generation), listing, deletion, and
detailed information retrieval. Supports all standard SSH key types and
includes proper file handling with secure permissions.
"""

import cyclopts
from loguru import logger
from tabulate import tabulate

from core import get_openstack_connection


app = cyclopts.App()


@app.command
def ssh_keypair_create(
    name: str,
    public_key_file: str = "",
    key_type: str = "ssh-rsa",
) -> None:
    """Create an SSH keypair in OpenStack.

    Creates a new SSH keypair in OpenStack either by importing an existing
    public key file or by generating a new keypair. When generating a new
    keypair, the private key is automatically saved to ~/.ssh/ with proper
    file permissions (600).

    Parameters
    ----------
    name : str
        Name for the SSH keypair in OpenStack. Must be unique within
        the project.
    public_key_file : str, optional
        Path to existing public key file to import. If not provided,
        OpenStack will generate a new keypair.
    key_type : str, optional
        Type of key when generating new keypair. Supported types:
        ssh-rsa, ssh-dss, ssh-ecdsa, ecdsa-sha2-nistp256,
        ecdsa-sha2-nistp384, ecdsa-sha2-nistp521, ssh-ed25519.
        Default is ssh-rsa.

    Raises
    ------
    SystemExit
        If connection to OpenStack fails, keypair already exists,
        or file operations fail.

    Examples
    --------
    $ nnumbers ssh-keypair ssh-keypair-create my-key
    $ nnumbers ssh-keypair ssh-keypair-create my-key --public-key-file ~/.ssh/id_rsa.pub
    $ nnumbers ssh-keypair ssh-keypair-create my-key --key-type ssh-ed25519
    """
    conn = get_openstack_connection()
    if conn:
        try:
            # Check if keypair already exists
            existing_keypair = conn.compute.find_keypair(name)
            if existing_keypair:
                logger.warning(f"Keypair '{name}' already exists in OpenStack")
                return

            if public_key_file:
                # Import existing public key
                from pathlib import Path

                key_file = Path(public_key_file)
                if not key_file.exists():
                    logger.error(f"Public key file not found: {public_key_file}")
                    raise SystemExit(1)

                public_key = key_file.read_text().strip()
                logger.info(f"Importing public key from '{public_key_file}'...")

                keypair = conn.compute.create_keypair(name=name, public_key=public_key)

                logger.success(f"Keypair '{name}' imported successfully!")
                logger.info(f"Fingerprint: {keypair.fingerprint}")

            else:
                # Generate new keypair
                logger.info(f"Generating new {key_type} keypair '{name}'...")

                keypair = conn.compute.create_keypair(name=name, key_type=key_type)

                logger.success(f"Keypair '{name}' created successfully!")
                logger.info(f"Fingerprint: {keypair.fingerprint}")
                logger.info(f"Key type: {keypair.type}")

                # Save private key to file
                if hasattr(keypair, "private_key") and keypair.private_key:
                    from pathlib import Path

                    private_key_path = Path.home() / ".ssh" / f"{name}.pem"
                    private_key_path.parent.mkdir(exist_ok=True)

                    with open(private_key_path, "w") as f:
                        f.write(keypair.private_key)

                    # Set proper permissions
                    import os

                    os.chmod(private_key_path, 0o600)

                    logger.info(f"Private key saved to: {private_key_path}")
                    logger.info("Usage instructions:")
                    logger.info(f"  ssh -i {private_key_path} user@instance_ip")

        except Exception as e:
            logger.error(f"Error creating keypair: {e}")
            raise SystemExit(1) from e
    else:
        logger.error("Failed to establish OpenStack connection")
        raise SystemExit(1)


@app.command
def ssh_keypair_list() -> None:
    """List all SSH keypairs in OpenStack.

    Displays all SSH keypairs associated with the current project
    in a formatted table showing name, fingerprint, and key type.

    Raises
    ------
    SystemExit
        If connection to OpenStack fails.

    Examples
    --------
    $ nnumbers ssh-keypair ssh-keypair-list
    ┌────────────┬─────────────────────────────────────────────┬──────────┐
    │ Name       │ Fingerprint                                 │ Type     │
    ├────────────┼─────────────────────────────────────────────┼──────────┤
    │ my-key     │ SHA256:abc123...                            │ ssh-rsa  │
    └────────────┴─────────────────────────────────────────────┴──────────┘
    """
    conn = get_openstack_connection()
    if conn:
        try:
            logger.info("Listing SSH keypairs...")
            keypairs = list(conn.compute.keypairs())
            if keypairs:
                lines = []
                for keypair in sorted(keypairs, key=lambda x: x.name):
                    key_type = getattr(keypair, "type", "unknown")
                    lines.append(
                        [
                            keypair.name,
                            keypair.fingerprint,
                            key_type,
                        ]
                    )

                table = tabulate(
                    lines,
                    headers=["Name", "Fingerprint", "Type"],
                    tablefmt="grid",
                )
                print(table)
            else:
                logger.info("No SSH keypairs found.")
        except Exception as e:
            logger.error(f"Error listing keypairs: {e}")
    else:
        logger.error("Failed to establish OpenStack connection")
        raise SystemExit(1)


@app.command
def ssh_keypair_delete(name: str, force: bool = False) -> None:
    """Delete an SSH keypair from OpenStack.

    Removes the specified SSH keypair from OpenStack. This operation
    cannot be undone. The local private key files are not affected.

    Parameters
    ----------
    name : str
        Name of the SSH keypair to delete.
    force : bool, optional
        Skip confirmation prompt (default: False).

    Raises
    ------
    SystemExit
        If connection to OpenStack fails or keypair not found.

    Examples
    --------
    $ nnumbers ssh-keypair ssh-keypair-delete my-key
    $ nnumbers ssh-keypair ssh-keypair-delete my-key --force
    """
    conn = get_openstack_connection()
    if conn:
        try:
            keypair = conn.compute.find_keypair(name)
            if not keypair:
                logger.warning(f"Keypair '{name}' not found.")
                return

            if not force:
                response = input(f"Delete keypair '{name}'? (y/N): ")
                if response.lower() not in ["y", "yes"]:
                    logger.info("Deletion cancelled.")
                    return

            conn.compute.delete_keypair(keypair)
            logger.success(f"Keypair '{name}' deleted successfully!")

        except Exception as e:
            logger.error(f"Error deleting keypair: {e}")
    else:
        logger.error("Failed to establish OpenStack connection")
        raise SystemExit(1)


@app.command
def ssh_keypair_show(name: str) -> None:
    """Show detailed information about an SSH keypair.

    Displays comprehensive information about the specified SSH keypair
    including fingerprint, key type, and public key content.

    Parameters
    ----------
    name : str
        Name of the SSH keypair to show.

    Raises
    ------
    SystemExit
        If connection to OpenStack fails or keypair not found.

    Examples
    --------
    $ nnumbers ssh-keypair ssh-keypair-show my-key
    """
    conn = get_openstack_connection()
    if conn:
        try:
            keypair = conn.compute.find_keypair(name)
            if keypair:
                logger.info(f"Keypair: {keypair.name}")
                logger.info(f"Fingerprint: {keypair.fingerprint}")
                if hasattr(keypair, "type"):
                    logger.info(f"Type: {keypair.type}")
                if hasattr(keypair, "public_key"):
                    logger.info(f"Public Key: {keypair.public_key}")
            else:
                logger.warning(f"Keypair '{name}' not found.")
        except Exception as e:
            logger.error(f"Error showing keypair: {e}")
    else:
        logger.error("Failed to establish OpenStack connection")
        raise SystemExit(1)
