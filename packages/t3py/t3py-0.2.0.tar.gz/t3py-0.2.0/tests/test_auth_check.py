from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from t3py.__main__ import app

runner = CliRunner()

@patch("t3py.commands.auth_check.get_authenticated_client")
@patch("t3py.commands.auth_check.AuthenticationApi")
def test_auth_check_success(mock_api_cls, mock_get_client):
    # Mock the authenticated client
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client

    # Mock the API
    mock_api_instance = MagicMock()
    mock_identity = MagicMock()
    mock_identity.has_t3plus = True
    mock_identity.to_json.return_value = {"username": "test_user", "hasT3plus": True}

    mock_api_instance.v2_auth_whoami_get.return_value = mock_identity
    mock_api_cls.return_value = mock_api_instance

    result = runner.invoke(app, ["auth_check"])

    assert result.exit_code == 0