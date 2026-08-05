import asyncio

from inspire_term.quote import QuoteService
from inspire_term.translator import translate_text
from inspire_term.ui import ConsoleRenderer


def main() -> None:
    quote_service = QuoteService()
    renderer = ConsoleRenderer()

    quote = quote_service.get_quote()

    translated_quote = asyncio.run(translate_text(quote.text))

    renderer.show(translated_quote, quote.author)


if __name__ == "__main__":
    main()
