from dataclasses import replace
from datetime import date
from random import choice

from inspire_term.cache import QuoteCache
from inspire_term.exceptions import QuoteFetchError, TranslationError
from inspire_term.models import QuoteCacheData
from inspire_term.quote import QuoteService
from inspire_term.translator import TranslatorService
from inspire_term.ui import ConsoleRenderer


def main() -> None:
    renderer = ConsoleRenderer()
    quote_service = QuoteService()
    translator = TranslatorService()
    cache = QuoteCache()

    cache_data = cache.load()

    if cache_data is None:
        try:
            quotes = quote_service.get_quotes()
        except QuoteFetchError as e:
            renderer.error(str(e))
            return

        cache_data = QuoteCacheData(
            date=date.today(),
            quotes=quotes,
        )

        cache.save(cache_data)

    quote = choice(cache_data.quotes)

    try:
        translated = translator.translate(quote.text)
        quote = replace(quote, translated=translated)
    except TranslationError:
        quote = replace(quote, translated=quote.text)

    renderer.show(quote.translated or quote.text, quote.author)


if __name__ == "__main__":
    main()
