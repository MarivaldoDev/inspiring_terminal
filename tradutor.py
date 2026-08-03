from googletrans import Translator


async def translate_text(text: str) -> None:
    async with Translator() as translator:
        result = await translator.translate(text, dest="pt")

        print(result)