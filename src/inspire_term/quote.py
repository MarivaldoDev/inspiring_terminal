from random import choice, randint

import requests

from inspire_term.exceptions import QuoteFetchError
from inspire_term.models import Quote


class QuoteService:
    keywords = ["inspiration", "success", "dreams"]
    url_base = "https://zenquotes.io/api/quotes/"

    def get_quote(self) -> Quote:
        try:
            keyword = choice(self.keywords)

            response = requests.get(self.url_base + f"&keyword={choice(keyword)}")
            data = response.json()
            idx = randint(0, len(data) - 1)

            return Quote(text=data[idx]["q"], author=data[idx]["a"])
        except requests.RequestException as exc:
            raise QuoteFetchError("Unable to fetch today's quote.") from exc
