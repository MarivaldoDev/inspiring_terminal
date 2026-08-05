from googletrans import Translator


async def translate_text(text: str) -> str:
    async with Translator() as translator:
        result = await translator.translate(text, dest="pt")

        return result.text
