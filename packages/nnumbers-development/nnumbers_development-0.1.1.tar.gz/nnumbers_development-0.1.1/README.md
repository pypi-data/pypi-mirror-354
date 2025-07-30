# NNumbers CLI - OpenStack Cloud Management Tool

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](http://mypy-lang.org/)

A command-line interface for managing OpenStack cloud resources built with modern Python features. This tool provides comprehensive instance lifecycle management, network operations, SSH keypair management, and resource monitoring with excellent developer experience and robust error handling.

## ✨ Features

- **🚀 Instance Management**: Complete lifecycle management of OpenStack compute instances
- **🌐 Network Operations**: Manage networks, subnets, and floating IP addresses  
- **🔑 SSH Keypair Management**: Create, import, and manage SSH keypairs
- **📊 Resource Monitoring**: View quotas, usage statistics, and resource information
- **🛡️ Robust Error Handling**: Comprehensive error handling with informative messages
- **📝 Comprehensive Logging**: Structured logging with different verbosity levels
- **🔧 Modern CLI**: Built with cyclopts for excellent user experience and help documentation
- **🧪 Well Tested**: Comprehensive test suite with high code coverage
- **📚 Type Safe**: Full type annotations using modern Python 3.11+ features

## 🔧 Prerequisites

- **Python 3.11+** (recommended: Python 3.12)
- **OpenStack credentials** configured via environment variables or clouds.yaml
- **Network access** to your OpenStack cloud environment

## 📦 Installation

### Using PDM (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-org/nnumbers-cli.git
cd nnumbers-cli

# Install with PDM
pdm install

# Activate the virtual environment  
eval $(pdm venv activate)
```

### Using pip

```bash
# Clone and install
git clone https://github.com/your-org/nnumbers-cli.git
cd nnumbers-cli
pip install -e .

# Or install from PyPI (when published)
pip install nnumbers-cli
```

### Development Installation

```bash
# Install with development dependencies
pdm install -G dev

# Install pre-commit hooks
pdm run pre-commit-install

# Run tests to verify installation
pdm run test
```

## ⚙️ Configuration

### Environment Variables

The most common way to configure OpenStack credentials:

```bash
# Source your OpenStack credentials file
source atlas-openrc.sh

# Or set environment variables manually
export OS_AUTH_URL=https://your-openstack.com:5000/v3
export OS_PROJECT_ID=your-project-id
export OS_PROJECT_NAME=your-project-name
export OS_USERNAME=your-username
export OS_PASSWORD=your-password
export OS_REGION_NAME=your-region
export OS_INTERFACE=public
export OS_IDENTITY_API_VERSION=3
```

### clouds.yaml Configuration

Alternative configuration using clouds.yaml file:

```yaml
# ~/.config/openstack/clouds.yaml
clouds:
  mycloud:
    auth:
      auth_url: https://your-openstack.com:5000/v3
      username: your-username
      password: your-password
      project_id: your-project-id
      project_name: your-project-name
      user_domain_name: Default
    region_name: your-region
    interface: public
```

Then use: `export OS_CLOUD=mycloud`

## 🚀 Usage

### Basic Commands

```bash
# Get help for any command
nnumbers --help
nnumbers instance --help
nnumbers network --help

# Check version
nnumbers --version
```

### Instance Management

```bash
# List all instances
nnumbers instance list

# Start an instance
nnumbers instance start web-server

# Stop an instance  
nnumbers instance stop web-server

# Reboot an instance
nnumbers instance reboot web-server

# Check instance status
nnumbers instance status web-server

# Manage instance with single command
nnumbers instance manage web-server start
```

### Network Operations

```bash
# List all networks
nnumbers network list-networks

# List floating IPs
nnumbers network list-floating-ips

# Create a floating IP
nnumbers network create-floating-ip --network public --description "Web server IP"
```

### SSH Keypair Management

```bash
# List SSH keypairs
nnumbers ssh-keypair ssh-keypair-list

# Create new keypair (generates new key)
nnumbers ssh-keypair ssh-keypair-create my-key

# Import existing public key
nnumbers ssh-keypair ssh-keypair-create my-key --public-key-file ~/.ssh/id_rsa.pub

# Delete keypair
nnumbers ssh-keypair ssh-keypair-delete my-key
```

### Resource Monitoring

```bash
# View quota information
nnumbers core quota

# View detailed usage statistics  
nnumbers core usage
```

## 📋 Examples

### Instance Lifecycle

```bash
# List all instances with status
nnumbers instance list

# Start a stopped instance
nnumbers instance start web-server-01

# Check detailed instance information
nnumbers instance status web-server-01

# Gracefully stop an instance
nnumbers instance stop web-server-01

# Reboot an instance
nnumbers instance reboot web-server-01
```

### Network Management

```bash
# View available networks
nnumbers network list-networks

# Check current floating IP allocation
nnumbers network list-floating-ips

# Allocate a new floating IP
nnumbers network create-floating-ip --description "Load balancer IP"
```

### Monitoring and Quotas

```bash
# Check project quotas
nnumbers core quota

# View current resource usage vs quotas
nnumbers core usage
```

## 🛠️ Development

### Code Quality

This project maintains high code quality standards:

```bash
# Format code
pdm run format

# Lint code
pdm run check

# Type checking
pdm run check-typing

# Find unused code
pdm run check-vulture

# Run tests with coverage
pdm run test

# Run full quality check
pdm run full
```

### Project Structure

```
src/
├── __init__.py          # Package metadata and exports
├── __main__.py          # CLI application entry point
├── core.py              # Core OpenStack connection and utilities
├── instance.py          # Instance management commands
├── network.py           # Network management commands
└── ssh_keypair.py       # SSH keypair management commands

tests/
├── conftest.py          # Test configuration and fixtures
├── test_core.py         # Core functionality tests
├── test_instance.py     # Instance management tests
└── test_network.py      # Network management tests
```

### Adding New Commands

To add new commands, follow these patterns:

```python
@app.command
def new_command(param: str) -> None:
    """Description of the new command.
    
    Detailed explanation of what the command does, its use cases,
    and any important behavior or limitations.
    
    Parameters
    ----------
    param : str
        Description of the parameter, including valid values
        and any constraints.
        
    Raises
    ------
    SystemExit
        If the operation fails or connection cannot be established.
        
    Examples
    --------
    $ nnumbers module new-command example-value
    """
    conn = get_openstack_connection()
    try:
        # Implementation here
        logger.success("Operation completed successfully")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise SystemExit(1) from e
```

### Contributing

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Install** development dependencies: `pdm install -G dev`
4. **Install** pre-commit hooks: `pdm run pre-commit-install`
5. **Make** your changes with proper tests and documentation
6. **Run** the full test suite: `pdm run full`
7. **Commit** your changes: `git commit -m 'Add amazing feature'`
8. **Push** to the branch: `git push origin feature/amazing-feature`
9. **Open** a Pull Request

## 🛡️ Error Handling

The CLI provides comprehensive error handling:

- **Connection Validation**: Automatic validation of OpenStack credentials
- **Resource Validation**: Checks for resource existence before operations
- **Informative Messages**: Clear error messages with suggested solutions
- **Graceful Degradation**: Continues operation when possible, fails fast when necessary
- **Structured Logging**: Consistent logging format with appropriate log levels

## 📝 Logging

The CLI uses structured logging with loguru:

- **`INFO`**: General information and operation progress
- **`SUCCESS`**: Successful completion of operations  
- **`WARNING`**: Non-critical issues that don't prevent operation
- **`ERROR`**: Critical errors that prevent operation completion

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

- **Documentation**: See this README and inline help (`nnumbers --help`)
- **Issues**: Report bugs and request features via GitHub Issues
- **Contributing**: See the Contributing section above

## 🏷️ Version

Current version: **0.1.0**

Check your installed version:
```bash
nnumbers --version
```
