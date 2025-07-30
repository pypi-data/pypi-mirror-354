"""Tests for instance management functionality."""

from unittest.mock import Mock
from unittest.mock import patch

from instance import reboot_instance
from instance import start_instance
from instance import stop_instance
import pytest


class TestInstanceOperations:
    """Test instance lifecycle operations."""

    def test_start_instance_success(
        self, mock_openstack_connection, sample_instance
    ) -> None:
        """Test successful instance start."""
        sample_instance.status = "SHUTOFF"
        mock_openstack_connection.compute.find_server.return_value = sample_instance

        # Should not raise any exceptions
        start_instance(mock_openstack_connection, "test-instance")

        # Verify the correct methods were called
        mock_openstack_connection.compute.find_server.assert_called_once_with(
            "test-instance"
        )
        mock_openstack_connection.compute.start_server.assert_called_once_with(
            sample_instance
        )
        mock_openstack_connection.compute.wait_for_server.assert_called_once()

    def test_start_instance_already_active(
        self, mock_openstack_connection, sample_instance: Mock
    ):
        """Test starting an already active instance."""
        sample_instance.status = "ACTIVE"
        mock_openstack_connection.compute.find_server.return_value = sample_instance

        start_instance(mock_openstack_connection, "test-instance")

        # Should not call start_server for already active instance
        mock_openstack_connection.compute.start_server.assert_not_called()

    def test_start_instance_not_found(self, mock_openstack_connection) -> None:
        """Test starting a non-existent instance."""
        mock_openstack_connection.compute.find_server.return_value = None

        # Should not raise exception, just log warning
        start_instance(mock_openstack_connection, "non-existent")

        mock_openstack_connection.compute.start_server.assert_not_called()

    def test_stop_instance_success(
        self, mock_openstack_connection, sample_instance
    ) -> None:
        """Test successful instance stop."""
        sample_instance.status = "ACTIVE"
        mock_openstack_connection.compute.find_server.return_value = sample_instance

        stop_instance(mock_openstack_connection, "test-instance")

        mock_openstack_connection.compute.find_server.assert_called_once_with(
            "test-instance"
        )
        mock_openstack_connection.compute.stop_server.assert_called_once_with(
            sample_instance
        )

    def test_stop_instance_already_stopped(
        self, mock_openstack_connection, sample_instance: Mock
    ) -> None:
        """Test stopping an already stopped instance."""
        sample_instance.status = "SHUTOFF"
        mock_openstack_connection.compute.find_server.return_value = sample_instance

        stop_instance(mock_openstack_connection, "test-instance")

        # Should not call stop_server for already stopped instance
        mock_openstack_connection.compute.stop_server.assert_not_called()

    def test_reboot_instance_success(
        self, mock_openstack_connection, sample_instance
    ) -> None:
        """Test successful instance reboot."""
        mock_openstack_connection.compute.find_server.return_value = sample_instance

        reboot_instance(mock_openstack_connection, "test-instance")

        mock_openstack_connection.compute.find_server.assert_called_once_with(
            "test-instance"
        )
        mock_openstack_connection.compute.reboot_server.assert_called_once_with(
            sample_instance
        )
        mock_openstack_connection.compute.wait_for_server.assert_called_once()


class TestInstanceCLI:
    """Test instance CLI commands."""

    @patch("instance.get_openstack_connection")
    def test_list_command_success(
        self, mock_get_conn, mock_openstack_connection
    ) -> None:
        """Test instance list command."""
        from instance import list_instances

        mock_get_conn.return_value = mock_openstack_connection
        mock_openstack_connection.compute.servers.return_value = []

        # Should not raise any exceptions
        list_instances()

        mock_get_conn.assert_called_once()

    @patch("instance.get_openstack_connection")
    def test_start_command_connection_failure(self, mock_get_conn):
        """Test start command with connection failure."""
        from instance import start

        mock_get_conn.side_effect = Exception("Connection failed")

        with pytest.raises(SystemExit):
            start("test-instance")

    @patch("instance.get_openstack_connection")
    def test_manage_command_valid_actions(
        self, mock_get_conn, mock_openstack_connection: Mock
    ) -> None:
        """Test manage command with valid actions."""
        from instance import manage

        mock_get_conn.return_value = mock_openstack_connection
        sample_instance = Mock()
        sample_instance.status = "ACTIVE"
        sample_instance.name = "test"
        sample_instance.id = "123"
        mock_openstack_connection.compute.find_server.return_value = sample_instance

        # Test each valid action
        valid_actions = ["start", "stop", "reboot", "status"]
        for action in valid_actions:
            # Should not raise exceptions for valid actions
            manage("test-instance", action)

    def test_manage_command_invalid_action(self) -> None:
        """Test manage command with invalid action."""
        from instance import manage

        with pytest.raises(SystemExit):
            manage("test-instance", "invalid-action")
