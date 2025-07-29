import typer

from t3py.commands.auth_check import auth_check

app = typer.Typer(
    help="[bold magenta]T3 CLI utilities[/] for working with Metrc and Track & Trace.",
    rich_markup_mode="rich",
)

app.command(name="auth_check")(auth_check)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()
