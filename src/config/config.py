from random import choice, randint

import requests


class Config:
    keywords = ["inspiration", "success", "dreams"]

    def sentence_day(self) -> tuple[str, str]:
        keyword = choice(self.keywords)
        URL_BASE = f"https://zenquotes.io/api/quotes/&keyword={choice(keyword)}"

        response = requests.get(URL_BASE)
        data = response.json()
        idx = randint(0, len(data) - 1)

        return data[idx]["q"], data[idx]["a"]
