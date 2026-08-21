import requests
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from inspire_term.exceptions import QuoteFetchError
from inspire_term.models import Quote


class QuoteService:
    url = "https://zenquotes.io/api/quotes/"

    def __init__(self) -> None:
        self.session = Session()

        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                "Accept": "application/json",
            }
        )

        retry = Retry(
            total=3,
            connect=3,
            read=3,
            backoff_factor=0.8,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
            raise_on_status=False,
        )

        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def get_quotes(self) -> list[Quote]:
        try:
            response = self.session.get(self.url, timeout=(3.05, 10))
            response.raise_for_status()
            data = response.json()
            return [Quote(text=item["q"], author=item["a"]) for item in data]
        except requests.RequestException as exc:
            raise QuoteFetchError(
                "Não foi possível obter as citações. Verifique sua conexão."
            ) from exc
        except (KeyError, TypeError, ValueError) as exc:
            raise QuoteFetchError("Resposta inválida do serviço de citações.") from exc
