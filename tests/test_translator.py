import pytest
from deep_translator.exceptions import RequestError

from inspire_term.exceptions import TranslationError
from inspire_term.translator import TranslatorService


class _FakeAsyncTranslatorContext:
    def __init__(self, text: str | None = None, exc: Exception | None = None):
        self._text = text
        self._exc = exc

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def translate(self, text: str, dest: str):
        if self._exc is not None:
            raise self._exc

        class _Result:
            def __init__(self, translated_text: str):
                self.text = translated_text

        return _Result(self._text or "")


def test_translate_returns_translated_text(mocker):
    fake_translator = mocker.Mock()
    fake_translator.translate.return_value = "O sucesso não é definitivo."

    mocker.patch(
        "inspire_term.translator.GoogleTranslator",
        return_value=fake_translator,
    )

    service = TranslatorService(language="en")

    translated = service.translate_deep("Success is not final.")

    assert translated == "O sucesso não é definitivo."


def test_translate_raises_translation_error(mocker):
    fake_translator = mocker.Mock()
    fake_translator.translate.side_effect = RequestError()

    mocker.patch(
        "inspire_term.translator.GoogleTranslator",
        return_value=fake_translator,
    )

    service = TranslatorService(language="pt")

    with pytest.raises(
        TranslationError,
        match="Não foi possível traduzir a citação.",
    ):
        service.translate_deep("Success is not final.")


def test_translate_google_returns_translated_text(mocker):
    fake_deep = mocker.Mock()
    fake_google = _FakeAsyncTranslatorContext(text="O sucesso não é definitivo.")

    mocker.patch("inspire_term.translator.GoogleTranslator", return_value=fake_deep)
    mocker.patch("inspire_term.translator.Translator", return_value=fake_google)

    service = TranslatorService(language="pt")

    translated = service.translate_google("Success is not final.")

    assert translated == "O sucesso não é definitivo."


def test_translate_google_raises_translation_error(mocker):
    fake_deep = mocker.Mock()
    fake_google = _FakeAsyncTranslatorContext(exc=RuntimeError("googletrans down"))

    mocker.patch("inspire_term.translator.GoogleTranslator", return_value=fake_deep)
    mocker.patch("inspire_term.translator.Translator", return_value=fake_google)

    service = TranslatorService(language="en")

    with pytest.raises(
        TranslationError,
        match="Não foi possível traduzir a citação.",
    ):
        service.translate_google("Success is not final.")
