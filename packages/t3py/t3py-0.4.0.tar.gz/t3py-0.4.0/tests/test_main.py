from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from t3py.__main__ import app

runner = CliRunner()


def test_main_help_output():
    """Test that running 't3py' with no args shows the help screen."""
    result = runner.invoke(app, [])
    assert result.exit_code == 0
    assert "T3 CLI utilities for working with Metrc and Track & Trace." in result.output
    assert "auth_check" in result.output