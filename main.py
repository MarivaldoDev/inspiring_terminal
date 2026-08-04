import asyncio

from rich.console import Console

from src.config.config import Config
from src.config.tradutor import translate_text

config = Config()
console = Console()


sentence, author = config.sentence_day()
result = asyncio.run(translate_text(sentence))


console.print(f"{result}\n- {author}", style="bold green")
