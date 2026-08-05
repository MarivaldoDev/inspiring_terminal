from rich import box
from rich.console import Console
from rich.panel import Panel


class ConsoleRenderer:
    def __init__(self):
        self.console = Console()

    def show(self, text: str, author: str) -> None:
        self.console.print(
            Panel(
                f"[bold white]{text}[/]\n\n" f"[italic cyan]— {author}[/]",
                title="💡 Inspiring Terminal",
                border_style="green",
                box=box.ROUNDED,
                padding=(1, 2),
            ),
            justify="center",
        )

    def error(self, text: str) -> None:
        self.console.print(
            Panel(
                f"[bold red]{text}[/]",
                title="❌ Inspiring Terminal",
                border_style="red",
                box=box.ROUNDED,
                padding=(1, 2),
            ),
            justify="center",
        )
