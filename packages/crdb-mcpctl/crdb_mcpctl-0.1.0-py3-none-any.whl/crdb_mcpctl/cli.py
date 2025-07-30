import typer
from crdb_mcpctl.commands import create, get, list_, delete
from crdb_mcpctl.commands import export
from crdb_mcpctl.commands import run
from crdb_mcpctl.commands import simulate
from rich.console import Console
from rich.align import Align
from rich.panel import Panel
from crdb_mcpctl.logging_config import setup_logging
from crdb_mcpctl import __version__

app = typer.Typer(name="crdb-mcpctl", help="Model Context Protocol CLI for CockroachDB")


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        False, "--version", "-v", help="Show version and exit"
    ),
    log_level: str = typer.Option("INFO", "--log-level", help="Set logging level"),
):
    setup_logging(log_level)
    show_banner()

    if version:
        typer.echo(f"crdb-mcpctl version {__version__}")
        raise typer.Exit()
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()


app.add_typer(create.app, name="create", help="Create a new context")
app.add_typer(get.app, name="get", help="Get a context by ID")
app.add_typer(list_.app, name="list", help="List all contexts")
app.add_typer(delete.app, name="delete", help="Delete a context by ID")
app.add_typer(export.app, name="export", help="Export a context to a file")
app.add_typer(
    run.app, name="run", help="Simulate or invoke a model context with an LLM"
)
app.add_typer(
    simulate.app, name="simulate", help="Run a batch of inputs against a model context"
)


def show_banner():
    console = Console()
    title = "[bold cyan]crdb-mcpctl[/bold cyan]"
    subtitle = "[white]Model Context Protocol CLI for CockroachDB[/white]"
    version = f"[dim]v{__version__}[/dim]"

    banner = f"{title}\n{subtitle}\n{version}"
    panel = Panel(Align.center(banner), border_style="cyan", padding=(1, 4))
    console.print(panel)


if __name__ == "__main__":
    app()
