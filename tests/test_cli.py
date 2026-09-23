from datetime import date

import pytest
import typer

from inspire_term.cli import main
from inspire_term.exceptions import QuoteFetchError, TranslationError
from inspire_term.flow import APP_VERSION, run, version_callback
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

    mocker.patch(
        "inspire_term.flow.load_config",
        return_value={"language": "en"},
    )

    mocker.patch("inspire_term.flow.QuoteCache", return_value=cache)
    mocker.patch("inspire_term.flow.QuoteService", return_value=quote_service)
    mocker.patch("inspire_term.flow.TranslatorService", return_value=translator)
    renderer_class = mocker.patch(
        "inspire_term.flow.ConsoleRenderer", return_value=renderer
    )

    return cache, quote_service, translator, renderer, renderer_class


def test_shows_translated_cached_quote(mocker, patched_services, sample_quotes):
    cache, quote_service, translator, renderer, renderer_class = patched_services

    cache_data = QuoteCacheData(
        date=date.today(),
        quotes=sample_quotes.copy(),
    )
    cache.load.return_value = cache_data

    mocker.patch(
        "inspire_term.flow.choice",
        return_value=cache_data.quotes[0],
    )
    translator.translate_deep.return_value = "O sucesso não é definitivo."

    run(style="simple")

    renderer_class.assert_called_once_with(style="simple")

    assert cache_data.quotes == [sample_quotes[1]]
    cache.save.assert_called_once_with(cache_data)
    quote_service.get_quotes.assert_not_called()
    translator.translate_deep.assert_called_once_with("Success is not final.")
    renderer.show.assert_called_once_with(
        "O sucesso não é definitivo.",
        "Winston Churchill",
    )


def test_fetches_and_saves_when_cache_missing(mocker, patched_services, sample_quotes):
    cache, quote_service, translator, renderer, _ = patched_services
    cache.load.return_value = None
    quote_service.get_quotes.return_value = sample_quotes.copy()

    mocker.patch(
        "inspire_term.flow.choice",
        return_value=quote_service.get_quotes.return_value[0],
    )
    translator.translate_deep.return_value = "O sucesso não é definitivo."

    run()

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
    cache, quote_service, translator, renderer, _ = patched_services
    cache.load.return_value = None
    quote_service.get_quotes.side_effect = QuoteFetchError(
        "Unable to fetch today's quote."
    )

    run()

    quote_service.get_quotes.assert_called_once_with()
    renderer.error.assert_called_once_with("Unable to fetch today's quote.")
    cache.save.assert_not_called()
    renderer.show.assert_not_called()


def test_handles_index_error(mocker, patched_services):
    cache, quote_service, translator, renderer, _ = patched_services
    cache.load.return_value = QuoteCacheData(date=date.today(), quotes=[])

    run()

    renderer.error.assert_called_once_with(
        "Todas as frases do dia foram usadas. Aguardamos você no dia de amanhã!"
    )
    renderer.show.assert_not_called()
    cache.save.assert_not_called()
    quote_service.get_quotes.assert_not_called()


def test_handles_translation_error(mocker, patched_services, sample_quotes):
    cache, quote_service, translator, renderer, _ = patched_services
    cache_data = QuoteCacheData(date=date.today(), quotes=sample_quotes.copy())
    cache.load.return_value = cache_data

    mocker.patch("inspire_term.flow.choice", return_value=cache_data.quotes[0])
    translator.translate_deep.side_effect = TranslationError("boom")
    translator.translate_google.side_effect = TranslationError("boom")

    run()

    renderer.error.assert_called_once_with("Tradução falhou! Exibindo frase em Inglês.")
    renderer.show.assert_called_once_with("Success is not final.", "Winston Churchill")
    translator.translate_google.assert_called_once_with("Success is not final.")

    cache.save.assert_called_once()
    saved = cache.save.call_args[0][0]
    assert saved.quotes == [sample_quotes[1]]


def test_falls_back_to_google_when_deep_returns_server_error(
    mocker,
    patched_services,
    sample_quotes,
):
    cache, quote_service, translator, renderer, _ = patched_services
    cache_data = QuoteCacheData(date=date.today(), quotes=sample_quotes.copy())
    cache.load.return_value = cache_data

    mocker.patch("inspire_term.flow.choice", return_value=cache_data.quotes[0])
    translator.translate_deep.return_value = (
        "Error 500 (Server Error)!!1500.That's an error."
    )
    translator.translate_google.return_value = "O sucesso não é definitivo."

    run()

    translator.translate_deep.assert_called_once_with("Success is not final.")
    translator.translate_google.assert_called_once_with("Success is not final.")
    renderer.error.assert_not_called()
    renderer.show.assert_called_once_with(
        "O sucesso não é definitivo.",
        "Winston Churchill",
    )


def test_run_without_translation(
    mocker,
    patched_services,
    sample_quotes,
):
    cache, quote_service, translator, renderer, _ = patched_services

    cache_data = QuoteCacheData(
        date=date.today(),
        quotes=sample_quotes.copy(),
    )
    cache.load.return_value = cache_data

    mocker.patch(
        "inspire_term.flow.choice",
        return_value=cache_data.quotes[0],
    )

    run(no_translate=True)

    translator.translate.assert_not_called()

    renderer.show.assert_called_once_with(
        "Success is not final.",
        "Winston Churchill",
    )

    cache.save.assert_called_once_with(cache_data)


def test_main_accepts_simple_style(mocker):
    run = mocker.patch("inspire_term.cli.run")

    main(no_translate=False, style="simple")

    run.assert_called_once_with(
        no_translate=False,
        style="simple",
    )


def test_version_callback_exits_and_prints_version(mocker):
    echo = mocker.patch("typer.echo")

    with pytest.raises(typer.Exit):
        version_callback(True)

    echo.assert_called_once_with(f"inspiring-terminal {APP_VERSION}")


def test_version_callback_does_nothing_when_false(mocker):
    echo = mocker.patch("typer.echo")

    version_callback(False)

    echo.assert_not_called()
