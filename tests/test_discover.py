"""Unit tests for the DiscoverFormatter class."""

import pandas as pd

from transaction_formatters.discover import DiscoverFormatter


def test_format_discover_logs_valid() -> None:
    """Test case for formatting Discover logs with valid data."""
    formatter = DiscoverFormatter("tests/fixtures/example_discover.csv")

    # Case 1: Removes credit transactions, only debit remain
    result = formatter.format_discover_logs()
    assert all(result["amount"] > 0)
    assert all(result["payment_type"] == "Discover")
    assert list(result.columns) == [
        "date",
        "category",
        "subcategory",
        "amount",
        "payment_type",
        "note",
    ]

    # Case 2: Column values
    assert pd.to_datetime(result.iloc[0]["date"]) == pd.to_datetime(
        "2025-01-01"
    )
    assert result.iloc[0]["note"] == "Example Store 1"


def test_format_discover_logs_empty_df() -> None:
    """
    Test case for formatting Discover logs with an empty
    DataFrame.
    """
    formatter = DiscoverFormatter("tests/fixtures/empty_discover.csv")
    empty_result = formatter.format_discover_logs()
    assert empty_result.empty
    assert list(empty_result.columns) == [
        "date",
        "category",
        "subcategory",
        "amount",
        "payment_type",
        "note",
    ]


def test_format_discover_logs_all_credit_rows() -> None:
    """Test case for formatting Discover logs with all credit rows."""
    formatter = DiscoverFormatter("tests/fixtures/discover_all_credit.csv")
    credit_result = formatter.format_discover_logs()
    assert credit_result.empty
    assert list(credit_result.columns) == [
        "date",
        "category",
        "subcategory",
        "amount",
        "payment_type",
        "note",
    ]
