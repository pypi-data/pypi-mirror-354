import typer

from t3py.commands.auth_check import auth_check  # import the function, not a Typer app

app = typer.Typer(
    help="[bold magenta]T3 CLI utilities[/] for working with Metrc and Track & Trace. [bold magenta]T3 CLI utilities[/]",
    rich_markup_mode="rich",
)

app.command(name="auth_check")(auth_check)  # ✅ registers it as a top-level command


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()
