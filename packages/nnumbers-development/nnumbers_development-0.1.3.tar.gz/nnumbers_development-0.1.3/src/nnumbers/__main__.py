"""NNumbers CLI - Main application entry point.

This module defines the main CLI application structure and command routing.
It combines all subcommands (core, instance, network, ssh-keypair) into
a unified command-line interface.
"""

import cyclopts

from nnumbers import core
from nnumbers import instance
from nnumbers import network
from nnumbers import ssh_keypair


app = cyclopts.App(
    name="nnumbers",
    help="A CLI tool for managing OpenStack resources",
    version="0.1.0",
)

app.command(
    core.app,
    name="core",
)

app.command(
    instance.app,
    name="instance",
)

app.command(
    network.app,
    name="network",
)

app.command(
    ssh_keypair.app,
    name="ssh-keypair",
)


def main() -> None:
    """Run the main CLI application.

    This function serves as the entry point for the nnumbers CLI.
    It processes command-line arguments and routes them to the
    appropriate subcommand handlers.
    """
    app()


if __name__ == "__main__":
    main()
