import requests

from inspire_term.exceptions import QuoteFetchError
from inspire_term.models import Quote


class QuoteService:
    url = "https://zenquotes.io/api/quotes/"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    def get_quotes(self) -> list[Quote]:
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()

            data = response.json()

            return [Quote(text=item["q"], author=item["a"]) for item in data]
        except requests.RequestException as exc:
            raise QuoteFetchError(
                "Não foi possível obter as citações. Verifique sua conexão."
            ) from exc
