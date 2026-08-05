import pytest
import requests

from inspire_term.exceptions import QuoteFetchError
from inspire_term.models import Quote
from inspire_term.quote import QuoteService


def test_get_quote_returns_quote(mocker):
    fake_response = mocker.Mock()

    fake_response.json.return_value = [
        {
            "q": "Success is not final.",
            "a": "Winston Churchill",
        }
    ]

    fake_response.raise_for_status.return_value = None

    mocker.patch(
        "inspire_term.quote.requests.get",
        return_value=fake_response,
    )

    service = QuoteService()

    quote = service.get_quote()

    assert quote == Quote(
        text="Success is not final.",
        author="Winston Churchill",
    )


def test_get_quote_raises_quote_fetch_error_when_request_fails(mocker):
    mocker.patch(
        "inspire_term.quote.requests.get",
        side_effect=requests.RequestException,
    )

    service = QuoteService()

    with pytest.raises(QuoteFetchError, match="Unable to fetch today's quote."):
        service.get_quote()
