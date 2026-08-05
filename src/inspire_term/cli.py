from inspire_term.exceptions import QuoteFetchError, TranslationError
from inspire_term.quote import QuoteService
from inspire_term.translator import TranslatorService
from inspire_term.ui import ConsoleRenderer


def main() -> None:
    renderer = ConsoleRenderer()
    quote_service = QuoteService()
    translator = TranslatorService()

    try:
        quote = quote_service.get_quote()
    except QuoteFetchError as e:
        renderer.error(str(e))
        return

    try:
        translated_quote = translator.translate(quote.text)
    except TranslationError as e:
        translated_quote = quote.text

    renderer.show(translated_quote, quote.author)


if __name__ == "__main__":
    main()
