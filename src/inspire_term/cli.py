import asyncio

from rich.console import Console
from rich.panel import Panel
from rich import box

from inspire_term.quote import QuoteService
from inspire_term.translator import translate_text


def main() -> None:
    quote = QuoteService()
    console = Console()

    sentence, author = quote.get_quote()
    result = asyncio.run(translate_text(sentence))

    console.print(
        Panel(
            f"[bold white]{result}[/]\n\n"
            f"[italic cyan]- {author}[/]",
            title="💡 Inspiring Terminal",
            border_style="green",
            box=box.ROUNDED,
            padding=(1, 2),
        ),
        justify="center",
    )


if __name__ == "__main__":
    main()
