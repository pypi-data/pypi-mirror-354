"""Tests for network management functionality."""

from unittest.mock import Mock
from unittest.mock import patch

import pytest

from src.network import _get_external_network


class TestNetworkOperations:
    """Test network management operations."""

    def test_get_external_network_by_name(
        self, mock_openstack_connection, sample_network: Mock
    ) -> None:
        """Test getting external network by name."""
        mock_openstack_connection.network.find_network.return_value = sample_network

        result = _get_external_network(mock_openstack_connection, "public")

        assert result == sample_network
        mock_openstack_connection.network.find_network.assert_called_once_with("public")

    def test_get_external_network_auto_select(
        self, mock_openstack_connection: Mock, sample_network: Mock
    ) -> None:
        """Test auto-selecting first external network."""
        sample_network.is_router_external = True
        mock_openstack_connection.network.networks.return_value = [sample_network]

        result = _get_external_network(mock_openstack_connection, "")

        assert result == sample_network

    def test_get_external_network_none_available(
        self, mock_openstack_connection: Mock
    ) -> None:
        """Test when no external networks are available."""
        mock_openstack_connection.network.networks.return_value = []

        result = _get_external_network(mock_openstack_connection, "")

        assert result is None


class TestNetworkCLI:
    """Test network CLI commands."""

    @patch("src.network.get_openstack_connection")
    def test_list_networks_success(
        self, mock_get_conn, mock_openstack_connection, sample_network: Mock
    ) -> None:
        """Test network list command."""
        from src.network import list_networks

        mock_get_conn.return_value = mock_openstack_connection
        mock_openstack_connection.network.networks.return_value = [sample_network]

        # Should not raise any exceptions
        list_networks()

        mock_get_conn.assert_called_once()

    @patch("src.network.get_openstack_connection")
    def test_list_networks_connection_failure(self, mock_get_conn) -> None:
        """Test list networks with connection failure."""
        from src.network import list_networks

        mock_get_conn.side_effect = Exception("Connection failed")

        with pytest.raises(SystemExit):
            list_networks()

    @patch("src.network.get_openstack_connection")
    @patch("src.network._get_external_network")
    def test_create_floating_ip_success(
        self,
        mock_get_external,
        mock_get_conn,
        mock_openstack_connection,
        sample_network,
        sample_floating_ip,
    ):
        """Test creating floating IP successfully."""
        from src.network import create_floating_ip

        mock_get_conn.return_value = mock_openstack_connection
        mock_get_external.return_value = sample_network
        mock_openstack_connection.network.create_ip.return_value = sample_floating_ip

        # Should not raise any exceptions
        create_floating_ip("public", "Test description")

        mock_openstack_connection.network.create_ip.assert_called_once()

    @patch("src.network.get_openstack_connection")
    def test_list_floating_ips_success(
        self, mock_get_conn, mock_openstack_connection: Mock, sample_floating_ip: Mock
    ) -> None:
        """Test listing floating IPs."""
        from src.network import list_floating_ips

        mock_get_conn.return_value = mock_openstack_connection
        mock_openstack_connection.network.ips.return_value = [sample_floating_ip]

        # Should not raise any exceptions
        list_floating_ips()

        mock_get_conn.assert_called_once()
