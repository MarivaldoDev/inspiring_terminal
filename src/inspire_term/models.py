from dataclasses import dataclass
from datetime import date


@dataclass(slots=True, frozen=True)
class Quote:
    text: str
    author: str
    translated: str | None = None


@dataclass
class QuoteCacheData:
    date: date
    quotes: list[Quote]
