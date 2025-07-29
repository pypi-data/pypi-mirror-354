from rich.console import Console, Group
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text
from t3api.api.authentication_api import AuthenticationApi
from t3api_utils.main.utils import get_authenticated_client_or_error

console = Console()


def auth_check() -> None:
    """
    Test if a username is registered to access T3+
    """
    api_client = get_authenticated_client_or_error()
    identity = AuthenticationApi(api_client=api_client).v2_auth_whoami_get()

    # Build the table
    table = Table(show_header=False, box=None, padding=(0, 1))

    if identity.has_t3plus:
        status = Text("Registered", style="bold green")
    else:
        status = Text("NOT registered", style="bold yellow")

    table.add_row("T3+ Status:", status)
    table.add_row("T3+ Subscription Tier:", Text(identity.t3plus_subscription_tier or "Free", style="bold magenta"))

    # Docs section with horizontal rule
    docs_section = Group(
        Rule(style="dim"),  # horizontal rule
        Text.from_markup(
            "[bold]Docs:[/] [underline blue]https://trackandtrace.tools/api[/]"
        ),
        Text.from_markup(
            "[bold]Wiki:[/] [underline blue]https://trackandtrace.tools/wiki[/]"
        ),
    )

    # Compose all content
    content = Group(table, Text(), docs_section)

    # Wrap in a panel
    console.print(
        Panel(
            content,
            title="T3+ Auth Check",
            title_align="left",
            border_style="purple",
            padding=(1, 1),
        )
    )
