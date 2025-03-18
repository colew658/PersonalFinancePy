"""Unit tests for data_helper.py."""

import pandas as pd

from utils.data_helper import append_totals_row, convert_datetime_to_str


def test_convert_datetime_to_str() -> None:
    """
    Test the convert_datetime_to_str function, ensuring it correctly
    converts datetime columns to string format and leaves other columns
    unchanged.
    """
    # Create a sample DataFrame with datetime columns
    test_df = pd.DataFrame({
        "date_col": pd.to_datetime([
            "2024-03-17",
            "2025-06-21",
            "2023-01-01",
        ]),
        "num_col": [1, 2, 3],
        "str_col": ["a", "b", "c"],
    })

    # Apply the function
    df_converted = convert_datetime_to_str(test_df)

    # Check that the datetime column is now of type string
    assert (
        df_converted["date_col"].dtype == object
    )  # Strings are stored as objects in pandas

    # Check that the values are correctly formatted as strings
    expected_dates = ["2024-03-17", "2025-06-21", "2023-01-01"]
    assert df_converted["date_col"].tolist() == expected_dates

    # Check that non-datetime columns remain unchanged
    assert df_converted["num_col"].tolist() == [1, 2, 3]
    assert df_converted["str_col"].tolist() == ["a", "b", "c"]
    assert df_converted["num_col"].dtype == test_df["num_col"].dtype
    assert df_converted["str_col"].dtype == test_df["str_col"].dtype


def test_append_totals_row() -> None:
    """
    Test the append_totals_row function to ensure it correctly appends
    a totals row to the DataFrame.
    The totals row should contain the sum of each numeric column
    and appropriate labels for the other columns.
    """
    # Create a sample DataFrame
    data = pd.DataFrame({
        "category": ["Food", "Transport"],
        "subcategory": ["Groceries", "Bus"],
        "month": ["January", "January"],
        "total_amount_spent": [100, 50],
        "amount_budgeted": [120, 60],
        "difference": [-20, -10],
    })

    # Expected totals row
    expected_totals = {
        "category": "Total",
        "subcategory": None,
        "month": None,
        "total_amount_spent": sum(data["total_amount_spent"]),
        "amount_budgeted": sum(data["amount_budgeted"]),
        "difference": sum(data["difference"]),
    }

    # Call the function
    result_df = append_totals_row(data)

    # Check if the last row is the totals row
    totals_row = result_df.iloc[-1]
    assert totals_row["category"] == expected_totals["category"]
    assert (
        totals_row["subcategory"] is expected_totals["subcategory"]
    )  # Ensure None comparison
    assert (
        totals_row["month"] is expected_totals["month"]
    )  # Ensure None comparison
    assert (
        totals_row["total_amount_spent"]
        == expected_totals["total_amount_spent"]
    )
    assert (
        totals_row["amount_budgeted"] == expected_totals["amount_budgeted"]
    )
    assert totals_row["difference"] == expected_totals["difference"]

    # Ensure the row count increased by 1
    assert len(result_df) == len(data) + 1
