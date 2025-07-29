from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from t3py.__main__ import app

runner = CliRunner()

@patch("t3py.commands.auth_check.get_authenticated_client_or_error")
@patch("t3py.commands.auth_check.AuthenticationApi")
def test_auth_check_success(mock_auth_api_cls, mock_get_client):
    # Mock API client
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client

    # Mock identity response
    mock_identity = MagicMock()
    mock_identity.has_t3plus = True
    mock_identity.t3plus_subscription_tier = "Pro"
    mock_identity.to_json.return_value = {
        "hasT3plus": True,
        "t3plus_subscription_tier": "Pro",
    }

    # Return the mock identity from API
    mock_auth_api_instance = MagicMock()
    mock_auth_api_instance.v2_auth_whoami_get.return_value = mock_identity
    mock_auth_api_cls.return_value = mock_auth_api_instance

    result = runner.invoke(app, ["auth_check"])

    print(result.output)  # helpful for debugging test output
    assert result.exit_code == 0
    assert "T3+ Auth Check" in result.output
    assert "Registered" in result.output
