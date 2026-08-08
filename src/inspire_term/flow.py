from dataclasses import replace
from datetime import date
from importlib.metadata import version
from random import choice

import typer

from inspire_term.cache import QuoteCache
from inspire_term.exceptions import QuoteFetchError, TranslationError
from inspire_term.models import QuoteCacheData
from inspire_term.quote import QuoteService
from inspire_term.translator import TranslatorService
from inspire_term.ui import ConsoleRenderer

APP_VERSION = version("inspiring-terminal")


def run(no_translate: bool = False) -> None:
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

    try:
        quote = choice(cache_data.quotes)
        selected_index = cache_data.quotes.index(quote)
    except IndexError:
        renderer.error(
            "Todas as frases do dia foram usadas. Aguardamos você no dia de amanhã!"
        )
        return

    if no_translate:
        translated = quote.text
    else:
        try:
            translated = translator.translate(quote.text)
            quote = replace(quote, translated=translated)
        except TranslationError:
            renderer.error("Tradução falhou! Exibindo frase em Inglês.")
            quote = replace(quote, translated=quote.text)

    renderer.show(quote.translated or quote.text, quote.author)

    cache_data.quotes.pop(selected_index)
    cache.save(cache_data)


def version_callback(value: bool) -> None:
    if value:
        typer.echo(f"inspiring-terminal {APP_VERSION}")
        raise typer.Exit()
