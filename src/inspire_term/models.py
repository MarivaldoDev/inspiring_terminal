from dataclasses import dataclass
from datetime import date


@dataclass(slots=True, frozen=True)
class Quote:
    '''Represents a quote with text, author, and translation information.'''
    text: str
    author: str
    translated: str | None = None


@dataclass
class QuoteCacheData:
    '''Represents cached quote data with a date and a list of quotes.'''
    date: date
    quotes: list[Quote]
