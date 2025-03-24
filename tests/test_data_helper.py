"""Unit tests for data_helper.py."""

import pandas as pd

from utils.data_helper import (
    append_category_totals,
    append_totals_row,
    convert_datetime_to_str,
    fill_missing_expenses,
    place_totals_rows,
)


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


def test_fill_missing_expenses() -> None:
    """
    Test the fill_missing_expenses function to ensure it correctly fills
    missing expenses with budgeted amounts and calculates the difference.
    """
    # Sample expense report
    expense_report = pd.DataFrame({
        "category": ["Food", "Transport"],
        "subcategory": ["Groceries", "Bus"],
        "month": ["March", "March"],
        "total_amount_spent": [150, 50],
        "amount_budgeted": [200, 60],
        "difference": [50, 10],
    })

    # Sample budget including an additional category
    budget = pd.DataFrame({
        "category": ["Food", "Transport", "Entertainment"],
        "subcategory": ["Groceries", "Bus", "Movies"],
        "amount_budgeted": [200, 60, 100],
    })

    month = "March"

    # Call the function
    result = fill_missing_expenses(expense_report, budget, month)

    # Expected DataFrame after filling missing expenses
    expected = pd.DataFrame({
        "category": ["Food", "Transport", "Entertainment"],
        "subcategory": ["Groceries", "Bus", "Movies"],
        "month": ["March", "March", "March"],
        "total_amount_spent": [150, 50, 0],
        "amount_budgeted": [200, 60, 100],
        "difference": [50, 10, 100],
    })

    # Reset index for comparison
    result = result.sort_values(
        by=["category", "subcategory"]
    ).reset_index(drop=True)
    expected = expected.sort_values(
        by=["category", "subcategory"]
    ).reset_index(drop=True)

    # Assert that result matches expected
    pd.testing.assert_frame_equal(result, expected)


def test_append_category_totals() -> None:
    """
    Test the append_category_totals function to ensure it correctly
    appends category totals to the DataFrame.
    """
    # Create a sample expense report DataFrame
    data = {
        "category": ["Food", "Food", "Transport", "Transport"],
        "subcategory": ["Groceries", "Dining", "Bus", "Train"],
        "month": ["Jan", "Jan", "Jan", "Jan"],
        "amount_budgeted": [200, 150, 50, 100],
        "total_amount_spent": [180, 140, 60, 90],
    }
    expense_report = pd.DataFrame(data)

    # Expected category totals
    expected_totals = {
        "category": ["Food", "Transport"],
        "subcategory": ["Total", "Total"],
        "month": [None, None],
        "amount_budgeted": [350, 150],
        "total_amount_spent": [320, 150],
        "difference": [30, 0],
    }
    expected_totals_df = pd.DataFrame(expected_totals)

    # Run function
    result = append_category_totals(expense_report)

    # Extract category totals from result
    result_totals = result[result["subcategory"] == "Total"].reset_index(
        drop=True
    )

    # Compare expected and actual results
    pd.testing.assert_frame_equal(
        result_totals, expected_totals_df, check_dtype=False
    )


def test_place_totals_rows() -> None:
    """
    Test the place_totals_rows function to ensure it correctly
    places the totals rows at the end of each category and the overall
    total at the end of the DataFrame.
    """
    # Create a sample unordered expense report DataFrame
    data = {
        "category": [
            "Food",
            "Food",
            "Food",
            "Transport",
            "Food",
            "Transport",
            "Total",
        ],
        "subcategory": [
            "Groceries",
            "Dining",
            "Total",
            "Bus",
            "Snacks",
            "Total",
            None,
        ],
        "month": ["Jan", "Jan", None, "Jan", "Jan", None, None],
        "amount": [100, 50, 150, 30, 20, 30, 180],
    }
    unordered_df = pd.DataFrame(data)

    # Expected ordered DataFrame
    expected_data = {
        "category": [
            "Food",
            "Food",
            "Food",
            "Food",
            "Transport",
            "Transport",
            "Total",
        ],
        "subcategory": [
            "Groceries",
            "Dining",
            "Snacks",
            "Total",
            "Bus",
            "Total",
            None,
        ],
        "month": ["Jan", "Jan", "Jan", None, "Jan", None, None],
        "amount": [100, 50, 20, 150, 30, 30, 180],
    }
    expected_df = pd.DataFrame(expected_data)

    # Apply the function
    sorted_df = place_totals_rows(unordered_df)

    # Check if the output DataFrame matches the expected DataFrame
    pd.testing.assert_frame_equal(
        sorted_df, expected_df, check_dtype=False
    )
