import typer
from t3api.api.authentication_api import AuthenticationApi
from t3api_utils.main.utils import get_authenticated_client

app = typer.Typer()

@app.command("auth_check")
def auth_check():
    """
    Verify that credentials are valid and identity can be retrieved from the T3 API.
    """
    api_client = get_authenticated_client()
    
    identity = AuthenticationApi(api_client=api_client).v2_auth_whoami_get()
    
    # user_data = identity.to_json()

    typer.secho("✅ Successfully authenticated with the T3 API", fg="green")
    typer.echo(
        "Status: T3+ access enabled"
        if identity.has_t3plus
        else "Status: Limited to free endpoints"
    )
    typer.echo("Docs: https://trackandtrace.tools/api")