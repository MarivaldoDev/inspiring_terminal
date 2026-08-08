from datetime import date

import pytest

from inspire_term.cli import main
from inspire_term.exceptions import QuoteFetchError, TranslationError
from inspire_term.flow import run
from inspire_term.models import Quote, QuoteCacheData


@pytest.fixture
def sample_quotes():
    return [
        Quote(text="Success is not final.", author="Winston Churchill"),
        Quote(text="Stay hungry, stay foolish.", author="Steve Jobs"),
    ]


@pytest.fixture
def patched_services(mocker, sample_quotes):
    cache = mocker.Mock()
    quote_service = mocker.Mock()
    translator = mocker.Mock()
    renderer = mocker.Mock()

    mocker.patch("inspire_term.cli.QuoteCache", return_value=cache)
    mocker.patch("inspire_term.cli.QuoteService", return_value=quote_service)
    mocker.patch("inspire_term.cli.TranslatorService", return_value=translator)
    mocker.patch("inspire_term.cli.ConsoleRenderer", return_value=renderer)

    return cache, quote_service, translator, renderer


def test_shows_translated_cached_quote(mocker, patched_services, sample_quotes):
    cache, quote_service, translator, renderer = patched_services
    cache_data = QuoteCacheData(date=date.today(), quotes=sample_quotes.copy())
    cache.load.return_value = cache_data

    mocker.patch("inspire_term.cli.choice", return_value=cache_data.quotes[0])
    translator.translate.return_value = "O sucesso não é definitivo."

    main()

    assert cache_data.quotes == [sample_quotes[1]]
    cache.save.assert_called_once_with(cache_data)
    quote_service.get_quotes.assert_not_called()
    translator.translate.assert_called_once_with("Success is not final.")
    renderer.show.assert_called_once_with(
        "O sucesso não é definitivo.", "Winston Churchill"
    )


def test_fetches_and_saves_when_cache_missing(mocker, patched_services, sample_quotes):
    cache, quote_service, translator, renderer = patched_services
    cache.load.return_value = None
    quote_service.get_quotes.return_value = sample_quotes.copy()

    mocker.patch(
        "inspire_term.cli.choice", return_value=quote_service.get_quotes.return_value[0]
    )
    translator.translate.return_value = "O sucesso não é definitivo."

    main()

    cache.save.assert_called_once()
    saved = cache.save.call_args[0][0]
    assert saved.date == date.today()
    assert (
        saved.quotes == sample_quotes.copy()[1:]
    )  # espera que a citação escolhida tenha sido removida
    renderer.show.assert_called_once_with(
        "O sucesso não é definitivo.", "Winston Churchill"
    )


def test_handles_quote_fetch_error(mocker, patched_services):
    cache, quote_service, translator, renderer = patched_services
    cache.load.return_value = None
    quote_service.get_quotes.side_effect = QuoteFetchError(
        "Unable to fetch today's quote."
    )

    main()

    quote_service.get_quotes.assert_called_once_with()
    renderer.error.assert_called_once_with("Unable to fetch today's quote.")
    cache.save.assert_not_called()
    renderer.show.assert_not_called()


def test_handles_index_error(mocker, patched_services):
    cache, quote_service, translator, renderer = patched_services
    cache.load.return_value = QuoteCacheData(date=date.today(), quotes=[])

    main()

    renderer.error.assert_called_once_with(
        "Todas as frases do dia foram usadas. Aguardamos você no dia de amanhã!"
    )
    renderer.show.assert_not_called()
    cache.save.assert_not_called()
    quote_service.get_quotes.assert_not_called()


def test_handles_translation_error(mocker, patched_services, sample_quotes):
    cache, quote_service, translator, renderer = patched_services
    cache_data = QuoteCacheData(date=date.today(), quotes=sample_quotes.copy())
    cache.load.return_value = cache_data

    mocker.patch("inspire_term.cli.choice", return_value=cache_data.quotes[0])
    translator.translate.side_effect = TranslationError("boom")

    main()

    renderer.error.assert_called_once_with("Tradução falhou! Exibindo frase em Inglês.")
    renderer.show.assert_called_once_with("Success is not final.", "Winston Churchill")

    cache.save.assert_called_once()
    saved = cache.save.call_args[0][0]
    assert saved.quotes == [sample_quotes[1]]


def test_run_without_translation(
    mocker,
    patched_services,
    sample_quotes,
):
    cache, quote_service, translator, renderer = patched_services

    cache_data = QuoteCacheData(
        date=date.today(),
        quotes=sample_quotes.copy(),
    )
    cache.load.return_value = cache_data

    mocker.patch(
        "inspire_term.cli.choice",
        return_value=cache_data.quotes[0],
    )

    run(no_translate=True)

    translator.translate.assert_not_called()

    renderer.show.assert_called_once_with(
        "Success is not final.",
        "Winston Churchill",
    )

    cache.save.assert_called_once_with(cache_data)
