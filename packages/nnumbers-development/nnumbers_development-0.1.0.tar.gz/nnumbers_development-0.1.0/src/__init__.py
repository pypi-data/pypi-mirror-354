"""NNumbers CLI - OpenStack Cloud Management Tool.

A  command-line interface for managing OpenStack cloud resources
with modern Python features, comprehensive error handling, and excellent
developer experience.

This package provides:
- Instance lifecycle management
- Network and floating IP management
- SSH keypair management
- Resource quota and usage monitoring
- Volume management
- Comprehensive logging and error handling

Example usage:
    $ nnumbers instance list
    $ nnumbers instance create my-server m1.medium ubuntu-20.04
    $ nnumbers network list-floating-ips
    $ nnumbers core quota

For more information, see the README.md file or run:
    $ nnumbers --help
"""

__version__ = "0.1.0"
__author__ = "Eric Miguel"
__email__ = "eric.mrib@gmail.com"
__license__ = "MIT"

# Package metadata
__title__ = "nnumbers-cli"
__description__ = "A CLI tool for managing OpenStack cloud resources"
__url__ = "https://github.com/your-org/nnumbers-cli"

# Version info tuple for programmatic access
__version_info__ = tuple(int(x) for x in __version__.split("."))

# Export main components
from src.core import OpenStackConnectionError
from src.core import get_openstack_connection


__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "get_openstack_connection",
    "OpenStackConnectionError",
]
