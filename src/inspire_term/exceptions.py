class InspiringTerminalError(Exception):
    """Base exception for the application."""


class QuoteFetchError(InspiringTerminalError):
    """Raised when the quote cannot be fetched."""


class TranslationError(InspiringTerminalError):
    """Raised when translation fails."""
