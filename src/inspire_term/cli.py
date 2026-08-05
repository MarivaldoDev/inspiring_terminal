from inspire_term.exceptions import QuoteFetchError, TranslationError
from inspire_term.quote import QuoteService
from inspire_term.translator import TranslatorService
from inspire_term.ui import ConsoleRenderer


def main() -> None:
    renderer = ConsoleRenderer()

    try:
        quote_service = QuoteService()
    except QuoteFetchError as e:
        renderer.error(str(e))
        return

    try:
        translator = TranslatorService()
    except TranslationError as e:
        renderer.error(str(e))
        return

    quote = quote_service.get_quote()

    translated_quote = translator.translate(quote.text)

    renderer.show(translated_quote, quote.author)



if __name__ == "__main__":
    main()
