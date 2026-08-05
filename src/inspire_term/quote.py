from random import choice, randint

import requests


class QuoteService:
    keywords = ["inspiration", "success", "dreams"]
    url_base = "https://zenquotes.io/api/quotes/"

    def get_quote(self) -> tuple[str, str]:
        keyword = choice(self.keywords)

        response = requests.get(self.url_base + f"&keyword={choice(keyword)}")
        data = response.json()
        idx = randint(0, len(data) - 1)

        return data[idx]["q"], data[idx]["a"]
