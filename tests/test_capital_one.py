"""Unit tests for capital_one.py."""

import pandas as pd

from transaction_formatters.capital_one import CapitalOneFormatter


def test_format_cap_one_logs_valid() -> None:
    """Test case for formatting Capital One logs with valid data."""
    formatter = CapitalOneFormatter("tests/fixtures/example_cap_one.csv")

    # Case 1: Removes credit transactions, only debit remain
    result = formatter.format_cap_one_logs()
    assert all(result["amount"] > 0)
    assert all(result["payment_type"] == "Venture")
    assert list(result.columns) == [
        "date",
        "category",
        "subcategory",
        "amount",
        "payment_type",
        "note",
    ]
    assert not any(result["note"].str.contains("CAPITAL ONE MOBILE PYMT"))

    # Case 2: Column values
    assert result.iloc[0]["note"] == "STARBUCKS"
    assert pd.to_datetime(result.iloc[0]["date"]) == pd.to_datetime(
        "2024-01-02"
    )


def test_format_cap_one_logs_empty_df() -> None:
    """
    Test case for formatting Capital One logs with an empty
    DataFrame.
    """
    formatter = CapitalOneFormatter("tests/fixtures/empty_cap_one.csv")
    empty_result = formatter.format_cap_one_logs()
    assert empty_result.empty
    assert list(empty_result.columns) == [
        "date",
        "category",
        "subcategory",
        "amount",
        "payment_type",
        "note",
    ]


def test_format_cap_one_logs_all_credit_rows() -> None:
    """Test case for formatting Capital One logs with all credit rows."""
    formatter = CapitalOneFormatter(
        "tests/fixtures/cap_one_all_credit.csv"
    )
    credit_result = formatter.format_cap_one_logs()
    assert credit_result.empty
    assert list(credit_result.columns) == [
        "date",
        "category",
        "subcategory",
        "amount",
        "payment_type",
        "note",
    ]
