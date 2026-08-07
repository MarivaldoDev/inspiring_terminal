import json
from dataclasses import asdict
from datetime import date
from pathlib import Path

from inspire_term.models import Quote, QuoteCacheData


class QuoteCache:
    def __init__(self, cache_dir: Path | None = None) -> None:
        self.cache_dir = cache_dir or Path.home() / ".cache" / "inspiring-terminal"
        self.cache_file = self.cache_dir / "quote.json"

    def ensure_cache_dir(self) -> None:
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def save(self, cache_data: QuoteCacheData) -> None:
        self.ensure_cache_dir()

        data = asdict(cache_data)
        data["date"] = cache_data.date.isoformat()

        with self.cache_file.open("w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4,
            )

    def load(self) -> QuoteCacheData | None:
        if not self.cache_file.exists():
            return None

        try:
            with self.cache_file.open("r", encoding="utf-8") as file:
                data = json.load(file)

            cached_date = date.fromisoformat(data["date"])

            if cached_date != date.today():
                return None

            quotes = [Quote(**quote) for quote in data["quotes"]]

            return QuoteCacheData(
                date=cached_date,
                quotes=quotes,
            )

        except (json.JSONDecodeError, KeyError, TypeError):
            return None
