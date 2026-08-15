from deep_translator import GoogleTranslator
from deep_translator.exceptions import (
    RequestError,
    TooManyRequests,
    TranslationNotFound,
)

from inspire_term.exceptions import TranslationError


class TranslatorService:
    def __init__(self) -> None:
        self.translator = GoogleTranslator(source="auto", target="pt")

    def translate(self, text: str) -> str:
        try:
            return self.translator.translate(text)
        except (RequestError, TooManyRequests, TranslationNotFound) as exc:
            raise TranslationError("Não foi possível traduzir a citação.") from exc
