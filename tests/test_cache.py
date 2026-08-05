import json
from datetime import date, timedelta

import pytest

from inspire_term.cache import QuoteCache
from inspire_term.models import Quote


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
    def quote_data(self, quote):
        return {
            "date": date.today().isoformat(),
            "text": quote.text,
            "translated": quote.translated,
            "author": quote.author,
        }

    def test_save_and_load_quote(self, cache, quote):
        cache.save(quote)
        assert cache.load() == quote

    def test_load_returns_none_when_cache_file_does_not_exist(self, cache):
        assert cache.load() is None

    def test_load_returns_none_when_cache_is_expired(self, cache, quote_data):
        quote_data["date"] = (date.today() - timedelta(days=1)).isoformat()

        cache.ensure_cache_dir()
        with cache.cache_file.open("w", encoding="utf-8") as file:
            json.dump(quote_data, file)

        assert cache.load() is None

    def test_load_returns_none_when_cache_file_is_corrupted(self, cache):
        cache.ensure_cache_dir()
        with cache.cache_file.open("w", encoding="utf-8") as file:
            file.write("{ isso não é um json")

        assert cache.load() is None
