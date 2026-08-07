import json
from datetime import date, timedelta

import pytest

from inspire_term.cache import QuoteCache
from inspire_term.models import Quote, QuoteCacheData


class TestQuoteCache:
    @pytest.fixture
    def cache(self, tmp_path):
        return QuoteCache(cache_dir=tmp_path)

    @pytest.fixture
    def quote(self) -> Quote:
        return Quote(
            text="Success is not final.",
            translated="O sucesso não é definitivo.",
            author="Winston Churchill",
        )

    @pytest.fixture
    def quote_cache_data(self, quote):
        return QuoteCacheData(date=date.today(), quotes=[quote])

    def test_save_and_load_quotes(self, cache, quote_cache_data):
        cache.save(quote_cache_data)

        assert cache.load() == quote_cache_data

    def test_load_returns_none_when_cache_file_does_not_exists(self, cache):
        assert cache.load() is None

    def test_load_returns_none_when_cache_is_expired(self, cache, quote):
        expired_data = {
            "date": (date.today() - timedelta(days=1)).isoformat(),
            "quotes": [
                {
                    "text": quote.text,
                    "translated": quote.translated,
                    "author": quote.author,
                }
            ],
        }

        cache.ensure_cache_dir()

        with cache.cache_file.open("w", encoding="utf-8") as file:
            json.dump(expired_data, file)

        assert cache.load() is None

    def test_load_returns_none_when_cache_file_is_corrupted(self, cache):
        cache.ensure_cache_dir()

        with cache.cache_file.open("w", encoding="utf-8") as file:
            file.write("{ isso não é um json")

        assert cache.load() is None

    def test_save_and_load_multiple_quotes(self, cache):
        quotes = [
            Quote(
                text="Success is not final.",
                translated="O sucesso não é definitivo.",
                author="Winston Churchill",
            ),
            Quote(
                text="The future depends on what you do today.",
                translated="O futuro depende do que você faz hoje.",
                author="Mahatma Gandhi",
            ),
        ]

        cache_data = QuoteCacheData(
            date=date.today(),
            quotes=quotes,
        )

        cache.save(cache_data)

        assert cache.load() == cache_data
