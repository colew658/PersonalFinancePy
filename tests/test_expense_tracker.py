"""Unit tests for expense_tracker.py."""

import pandas as pd

from expense_tracker import ExpenseTracker


def test_get_expense_report() -> None:
    """Test the get_expense_report method."""
    # Create an instance of the class

    test_tracker = ExpenseTracker(
        excel_path="tests/fixtures/example_excel_file.xlsx",
        budget_sheet="BUDGET",
        expense_sheet="EXPENSE_LOG",
    )
    # Run function
    report = test_tracker.create_grouped_report()

    # Expected data after processing
    expected_report = pd.DataFrame({
        "month": ["February", "January", "March"],
        "category": ["Housing", "Household", "Auto"],
        "subcategory": ["Rent", "Household Items", "Gas"],
        "amount_budgeted": [1000, 100, 100],
        "total_amount_spent": [1000, 10, 20],
        "difference": [0, 90, 80],
    })

    expected_dtypes = {
        "month": "object",
        "category": "object",
        "subcategory": "object",
        "amount_budgeted": "float64",
        "total_amount_spent": "float64",
        "difference": "float64",
    }

    expected_report = expected_report.astype(expected_dtypes)

    # Ensure expected report matches generated report
    pd.testing.assert_frame_equal(
        report.reset_index(drop=True), expected_report
    )


def test_create_split_report() -> None:
    """Test the create_split_report() function."""
    test_tracker = ExpenseTracker(
        excel_path="tests/fixtures/example_excel_file.xlsx",
        budget_sheet="BUDGET",
        expense_sheet="EXPENSE_LOG",
    )
    # Run function
    result = test_tracker.create_split_report()

    # Check that the function returns a list of DataFrames
    assert isinstance(result, list)
    assert all(isinstance(df, pd.DataFrame) for df in result)

    # Check that each DataFrame corresponds to a unique month
    expected_months = {"January", "February", "March"}
    result_months = {df["month"].iloc[0] for df in result if not df.empty}

    assert result_months == expected_months

    # Check that the number of rows in each DataFrame is correct
    for df in result:
        assert len(df) == len(test_tracker.budget["subcategory"].unique())
