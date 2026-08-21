import pytest
import requests

from inspire_term.exceptions import QuoteFetchError
from inspire_term.models import Quote
from inspire_term.quote import QuoteService


def test_get_quote_returns_quote(mocker):
    fake_response = mocker.Mock()
    fake_response.json.return_value = [
        {"q": "Success is not final.", "a": "Winston Churchill"}
    ]
    fake_response.raise_for_status.return_value = None

    fake_get = mocker.patch(
        "inspire_term.quote.Session.get",
        return_value=fake_response,
    )

    service = QuoteService()
    quote = service.get_quotes()

    assert quote == [Quote(text="Success is not final.", author="Winston Churchill")]
    fake_get.assert_called_once_with(service.url, timeout=(3.05, 10))


def test_get_quote_sends_browser_user_agent(mocker):
    fake_response = mocker.Mock()
    fake_response.json.return_value = []
    fake_response.raise_for_status.return_value = None

    mocker.patch(
        "inspire_term.quote.Session.get",
        return_value=fake_response,
    )

    service = QuoteService()
    service.get_quotes()

    user_agent = service.session.headers["User-Agent"]
    assert "python-requests" not in user_agent
    assert "Mozilla/5.0" in user_agent


def test_get_quote_raises_quote_fetch_error_when_request_fails(mocker):
    mocker.patch(
        "inspire_term.quote.Session.get",
        side_effect=requests.RequestException,
    )

    service = QuoteService()

    with pytest.raises(
        QuoteFetchError,
        match="Não foi possível obter as citações. Verifique sua conexão.",
    ):
        service.get_quotes()
