"""Tests for formatting utilities."""

from datetime import datetime

from lightwave.core.utils.formatting import format_currency, format_date


class TestFormatDate:
    def test_format_date_with_datetime(self):
        """Test formatting a datetime object."""
        date = datetime(2023, 1, 15, 12, 30, 45)
        assert format_date(date) == "2023-01-15"
        assert format_date(date, "%m/%d/%Y") == "01/15/2023"

    def test_format_date_with_string(self):
        """Test formatting an ISO date string."""
        assert format_date("2023-01-15T12:30:45Z") == "2023-01-15"
        assert format_date("2023-01-15T12:30:45+00:00", "%m/%d/%Y") == "01/15/2023"

    def test_format_date_with_none(self):
        """Test formatting None returns None."""
        assert format_date(None) is None

    def test_format_date_with_invalid_string(self):
        """Test formatting an invalid date string returns None."""
        assert format_date("not-a-date") is None


class TestFormatCurrency:
    def test_format_currency_usd(self):
        """Test formatting a USD currency amount."""
        assert format_currency(1234.56) == "$1,234.56"

    def test_format_currency_non_usd(self):
        """Test formatting a non-USD currency amount."""
        assert format_currency(1234.56, "EUR") == "$1,234.56 EUR"

    def test_format_currency_with_none(self):
        """Test formatting None returns None."""
        assert format_currency(None) is None
