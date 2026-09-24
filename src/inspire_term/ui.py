from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table


class ConsoleRenderer:
    def __init__(self, style: str = "default"):
        self.console = Console()
        self.style = style

    def welcome(self) -> None:
        self.console.print(
            Panel(
                "[bold cyan]Welcome to Inspiring Terminal![/]\n\n"
                "The initial setup will be completed now.\n"
                "After that, all that remains is execution [bold]inspire[/] "
                "to receive a new inspiring quote.",
                title="Inspiring Terminal",
                border_style="cyan",
                box=box.ROUNDED,
                padding=(1, 2),
            ),
            justify="center",
        )

    def show(self, text: str, author: str) -> None:
        if self.style == "simple":
            self.console.print(f"[bold bright_yellow]{text}[/]")
            self.console.print(f"[italic cyan]— {author}[/]")
            return
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

    def show_config(self) -> str:
        languages = {
            "en": "English",
            "pt": "Portuguese (Brazil)",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
        }

        language_table = Table(
            box=box.SIMPLE,
            show_header=True,
            padding=(0, 2),
        )
        language_table.add_column("Code", style="bold cyan")
        language_table.add_column("Language", style="white")

        for code, language in languages.items():
            language_table.add_row(code, language)

        self.console.print(
            Panel(
                language_table,
                title="Translation language",
                subtitle="Choose one of the available options.",
                border_style="yellow",
                box=box.ROUNDED,
                padding=(1, 2),
            ),
            justify="center",
        )

        selected_language = Prompt.ask(
            "Enter the language code",
            choices=list(languages),
            default="en",
        )

        return selected_language

    def screen_reset(self) -> bool:
        self.console.print(
            Panel(
                "Your current configuration will be removed.\n"
                "You will be asked to configure it again\n"
                "the next time you run [bold cyan]inspire[/].",
                title="Inspiring Terminal",
                border_style="yellow",
                box=box.ROUNDED,
                padding=(1, 2),
            ),
            justify="center",
        )

        selected_reset = Prompt.ask(
            "Reset configuration?",
            choices=["y", "n"],
            default="n",
        )

        if selected_reset == "y":
            return True
        else:
            return False

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
