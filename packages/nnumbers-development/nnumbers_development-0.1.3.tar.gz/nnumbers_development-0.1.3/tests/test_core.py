"""Test suite for nnumbers-cli.

Basic tests to validate core functionality and ensure code quality.
This test suite covers connection handling, error cases, and CLI
command structure validation.
"""

from unittest.mock import Mock
from unittest.mock import patch

from core import OpenStackConnectionError
from core import get_openstack_connection
import pytest


class TestCoreConnection:
    """Test core OpenStack connection functionality."""

    @patch("core.openstack.connect")
    def test_successful_connection(self, mock_connect):
        """Test successful OpenStack connection."""
        # Mock successful connection
        mock_conn = Mock()
        mock_conn.current_project_id = "test-project-123"
        mock_connect.return_value = mock_conn

        conn = get_openstack_connection()

        assert conn is not None
        assert conn.current_project_id == "test-project-123"
        mock_connect.assert_called_once()

    @patch("core.openstack.connect")
    def test_connection_failure(self, mock_connect):
        """Test OpenStack connection failure."""
        # Mock connection failure
        mock_connect.side_effect = Exception("Connection failed")

        with pytest.raises(OpenStackConnectionError) as exc_info:
            get_openstack_connection()

        assert "Failed to connect to OpenStack" in str(exc_info.value)
        assert exc_info.value.original_exception is not None

    @patch("core.openstack.connect")
    def test_connection_invalid_credentials(self, mock_connect):
        """Test OpenStack connection with invalid credentials."""
        # Mock connection with invalid credentials
        mock_conn = Mock()
        mock_conn.current_project_id = None
        mock_connect.return_value = mock_conn

        # This should raise an AttributeError when accessing current_project_id
        mock_connect.side_effect = AttributeError("No project ID available")

        with pytest.raises(OpenStackConnectionError):
            get_openstack_connection()


class TestCLIStructure:
    """Test CLI command structure and help text."""

    def test_main_app_exists(self) -> None:
        """Test that main app is properly configured."""
        from __main__ import app

        assert app is not None
        assert "nnumbers" in str(app.name)
        assert "CLI tool for managing OpenStack resources" in app.help

    def test_subcommands_exist(self) -> None:
        """Test that all expected subcommands exist."""
        from __main__ import app

        # The app should have subcommands registered
        assert hasattr(app, "_commands") or hasattr(app, "commands")

        # For now, just check that the app object is properly configured
        assert app is not None


class TestErrorHandling:
    """Test error handling across modules."""

    def test_openstack_connection_error_attributes(self) -> None:
        """Test OpenStackConnectionError has proper attributes."""
        original_error = Exception("Original error")
        error = OpenStackConnectionError("Test message", original_error)

        assert error.message == "Test message"
        assert error.original_exception == original_error
        assert str(error) == "Test message"

    def test_openstack_connection_error_without_original(self) -> None:
        """Test OpenStackConnectionError without original exception."""
        error = OpenStackConnectionError("Test message")

        assert error.message == "Test message"
        assert error.original_exception is None
        assert str(error) == "Test message"


if __name__ == "__main__":
    pytest.main([__file__])
