"""Test configuration and fixtures for nnumbers-cli test suite."""

from unittest.mock import Mock

import pytest


@pytest.fixture
def mock_openstack_connection() -> Mock:
    """Provide a mock OpenStack connection for testing."""
    mock_conn = Mock()
    mock_conn.current_project_id = "test-project-123"

    # Mock compute service
    mock_conn.compute = Mock()
    mock_conn.compute.servers.return_value = []
    mock_conn.compute.flavors.return_value = []

    # Mock network service
    mock_conn.network = Mock()
    mock_conn.network.networks.return_value = []
    mock_conn.network.ips.return_value = []

    # Mock block storage service
    mock_conn.block_storage = Mock()
    mock_conn.block_storage.volumes.return_value = []

    return mock_conn


@pytest.fixture
def sample_instance() -> Mock:
    """Provide a sample instance object for testing."""
    instance = Mock()
    instance.id = "12345678-1234-1234-1234-123456789012"
    instance.name = "test-instance"
    instance.status = "ACTIVE"
    instance.flavor = Mock()
    instance.flavor.id = "m1.medium"
    instance.image = Mock()
    instance.image.name = "ubuntu-20.04"
    instance.addresses = {
        "public": [{"addr": "203.0.113.10"}],
        "private": [{"addr": "10.0.0.15"}],
    }
    return instance


@pytest.fixture
def sample_network() -> Mock:
    """Provide a sample network object for testing."""
    network = Mock()
    network.id = "net-12345678-1234-1234-1234-123456789012"
    network.name = "public"
    network.status = "ACTIVE"
    network.is_router_external = True
    return network


@pytest.fixture
def sample_floating_ip() -> Mock:
    """Provide a sample floating IP object for testing."""
    fip = Mock()
    fip.id = "fip-12345678-1234-1234-1234-123456789012"
    fip.floating_ip_address = "203.0.113.10"
    fip.status = "ACTIVE"
    fip.fixed_ip_address = "10.0.0.15"
    fip.port_id = "port-123"
    fip.description = "Test floating IP"
    return fip
