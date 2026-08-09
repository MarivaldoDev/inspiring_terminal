import pytest

from inspire_term.exceptions import TranslationError
from inspire_term.translator import TranslatorService


def test_translate_returns_translated_text(mocker):
    fake_result = mocker.Mock()
    fake_result.text = "O sucesso não é definitivo."

    fake_translator = mocker.AsyncMock()
    fake_translator.translate.return_value = fake_result

    fake_translator.__aenter__.return_value = fake_translator

    mocker.patch(
        "inspire_term.translator.Translator",
        return_value=fake_translator,
    )

    service = TranslatorService()

    translated = service.translate("Success is not final.")

    assert translated == "O sucesso não é definitivo."


def test_translate_raises_translation_error(mocker):
    fake_translator = mocker.AsyncMock()

    fake_translator.translate.side_effect = Exception("Google Translate error")
    fake_translator.__aenter__.return_value = fake_translator

    mocker.patch(
        "inspire_term.translator.Translator",
        return_value=fake_translator,
    )

    service = TranslatorService()

    with pytest.raises(
        TranslationError,
        match="Não foi possível traduzir a citação.",
    ):
        service.translate("Success is not final.")
