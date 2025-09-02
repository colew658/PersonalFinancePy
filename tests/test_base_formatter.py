"""Unit tests for base_formatter.py."""

import pandas as pd

from transaction_formatters.base_formatter import BaseFormatter


def test_read_transaction_logs_valid() -> None:
    """
    Test the _read_transaction_logs method of BaseFormatter with a valid
    CSV file.
    """
    bf = BaseFormatter("tests/fixtures/example_cap_one.csv")
    schema = {
        "Card No.": "Int64",
        "Description": "str",
        "Category": "str",
        "Debit": "float64",
        "Credit": "float64",
    }
    date_cols = ["Transaction Date", "Posted Date"]
    test_df = bf._read_transaction_logs(schema, date_cols)
    assert isinstance(test_df, pd.DataFrame)
    assert list(test_df.columns) == [
        "Transaction Date",
        "Posted Date",
        "Card No.",
        "Description",
        "Category",
        "Debit",
        "Credit",
    ]
    assert pd.api.types.is_datetime64_any_dtype(
        test_df["Transaction Date"]
    )
    assert pd.api.types.is_datetime64_any_dtype(test_df["Posted Date"])


def test_read_transaction_logs_invalid_file() -> None:
    """
    Test the _read_transaction_logs method of BaseFormatter with an invalid
    CSV file.
    """
    bf = BaseFormatter("tests/fixtures/invalid_file.csv")
    schema = {
        "Card No.": "Int64",
        "Description": "str",
        "Category": "str",
        "Debit": "float64",
        "Credit": "float64",
    }
    date_cols = ["Transaction Date", "Posted Date"]
    test_df = bf._read_transaction_logs(schema, date_cols)
    assert test_df is None


def test_read_transaction_logs_invalid_dtype() -> None:
    """
    Test the _read_transaction_logs method of BaseFormatter with an invalid
    data type in the schema.
    """
    bf = BaseFormatter("tests/fixtures/example_cap_one.csv")
    schema = {
        "Card No.": "Int64",
        "Description": "str",
        "Category": "str",
        "Debit": "invalid_dtype",
        "Credit": "float64",
    }
    date_cols = ["Transaction Date", "Posted Date"]
    test_df = bf._read_transaction_logs(schema, date_cols)
    assert test_df is None
