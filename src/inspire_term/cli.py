from dataclasses import replace

from inspire_term.cache import QuoteCache
from inspire_term.exceptions import QuoteFetchError, TranslationError
from inspire_term.quote import QuoteService
from inspire_term.translator import TranslatorService
from inspire_term.ui import ConsoleRenderer


def main() -> None:
    renderer = ConsoleRenderer()
    quote_service = QuoteService()
    translator = TranslatorService()
    cache = QuoteCache()

    quote = cache.load()

    if quote is None:
        try:
            quote = quote_service.get_quote()
        except QuoteFetchError as e:
            renderer.error(str(e))
            return

        try:
            translated = translator.translate(quote.text)
            quote = replace(quote, translated=translated)
        except TranslationError:
            quote = replace(quote, translated=quote.text)

        cache.save(quote)

    renderer.show(quote.translated or quote.text, quote.author)


if __name__ == "__main__":
    main()
