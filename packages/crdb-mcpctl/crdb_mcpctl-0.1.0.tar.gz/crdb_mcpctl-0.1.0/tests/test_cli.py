from typer.testing import CliRunner
from crdb_mcpctl.cli import app

runner = CliRunner()

def test_cli_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "crdb-mcpctl version" in result.output

def test_cli_help():
    result = runner.invoke(app, [])
    assert result.exit_code == 0
    assert "Usage:" in result.output
