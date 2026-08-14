import pytest
from deep_translator.exceptions import RequestError

from inspire_term.exceptions import TranslationError
from inspire_term.translator import TranslatorService


def test_translate_returns_translated_text(mocker):
    fake_translator = mocker.Mock()
    fake_translator.translate.return_value = "O sucesso não é definitivo."

    mocker.patch(
        "inspire_term.translator.GoogleTranslator",
        return_value=fake_translator,
    )

    service = TranslatorService()

    translated = service.translate("Success is not final.")

    assert translated == "O sucesso não é definitivo."


def test_translate_raises_translation_error(mocker):
    fake_translator = mocker.Mock()
    fake_translator.translate.side_effect = RequestError()

    mocker.patch(
        "inspire_term.translator.GoogleTranslator",
        return_value=fake_translator,
    )

    service = TranslatorService()

    with pytest.raises(
        TranslationError,
        match="Não foi possível traduzir a citação.",
    ):
        service.translate("Success is not final.")
