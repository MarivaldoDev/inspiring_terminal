import json
from dataclasses import asdict
from datetime import date
from pathlib import Path

from inspire_term.models import Quote


class QuoteCache:
    def __init__(self) -> None:
        self.cache_dir = Path.home() / ".cache" / "inspiring-terminal"
        self.cache_file = self.cache_dir / "quote.json"

    def ensure_cache_dir(self) -> None:
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def save(self, quote: Quote) -> None:
        self.ensure_cache_dir()

        data = asdict(quote)
        data["date"] = date.today().isoformat()

        with self.cache_file.open("w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4,
            )

    def load(self) -> Quote | None:
        if not self.cache_file.exists():
            return None

        with self.cache_file.open("r", encoding="utf-8") as file:
            data = json.load(file)

        data.pop("date")

        return Quote(**data)
