import requests

from inspire_term.exceptions import QuoteFetchError
from inspire_term.models import Quote


class QuoteService:
    url = "https://zenquotes.io/api/quotes/"

    def get_quotes(self) -> list[Quote]:
        try:
            response = requests.get(self.url)
            response.raise_for_status()

            data = response.json()

            return [Quote(text=item["q"], author=item["a"]) for item in data]
        except requests.RequestException as exc:
            raise QuoteFetchError("Unable to fetch quotes.") from exc
