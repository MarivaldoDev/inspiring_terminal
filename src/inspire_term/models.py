from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Quote:
    text: str
    author: str
    translated: str | None = None
