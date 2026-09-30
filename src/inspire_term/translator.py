import asyncio

from deep_translator import GoogleTranslator
from deep_translator.exceptions import (
    RequestError,
    TooManyRequests,
    TranslationNotFound,
)
from googletrans import Translator

from inspire_term.exceptions import TranslationError


class TranslatorService:
    '''Service to handle translation of text using external translators.
    Args:
        language (str): The target language for translation.
    '''
    def __init__(self, language: str) -> None:
        self.language = language
        self.translator_deep = GoogleTranslator(source="auto", target=self.language)
        self.translator = Translator()

    def translate_deep(self, text: str) -> str:
        '''Translate text using the deep_translator library.
        Args:
            text (str): The text to be translated.
        Returns:
            str: The translated text.
        Raises:
            TranslationError: If the translation fails due to an error.
        '''
        try:
            return self.translator_deep.translate(text)
        except (RequestError, TooManyRequests, TranslationNotFound) as exc:
            raise TranslationError("Não foi possível traduzir a citação.") from exc

    async def _translate_text(self, text: str) -> str:
        '''Asynchronously translate text using the googletrans library.
        Args:
            text (str): The text to be translated.
        Returns:
            str: The translated text.
        Raises:
            TranslationError: If the translation fails due to an error.
        '''
        try:
            async with self.translator as translator:
                result = await translator.translate(text, dest=self.language)

                return result.text
        except Exception as exc:
            raise TranslationError("Não foi possível traduzir a citação.") from exc

    def translate_google(self, text: str) -> str:
        '''Translate text using the googletrans library.
        Args:
            text (str): The text to be translated.
        Returns:
            str: The translated text.
        Raises:
            TranslationError: If the translation fails due to an error.
        '''
        try:
            return asyncio.run(self._translate_text(text))
        except Exception as exc:
            raise TranslationError("Não foi possível traduzir a citação.") from exc
