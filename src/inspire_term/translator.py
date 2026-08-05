import asyncio

from googletrans import Translator

from inspire_term.exceptions import TranslationError


class TranslatorService:
    def __init__(self) -> None:
        self.translator = Translator()

    async def _translate_text(self, text: str) -> str:
        try:
            async with self.translator as translator:
                result = await translator.translate(text, dest="pt")

                return result.text
        except Exception as exc:
            raise TranslationError("Unable to translate quote.") from exc

    def translate(self, text: str):
        return asyncio.run(self._translate_text(text))
