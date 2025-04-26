"""Unit tests for validation.py."""

import pandas as pd
import pytest

from utils.validation import validate_excel, validate_expenses


@pytest.mark.parametrize(
    ("sheet_df", "sheet_schema", "expected_exception", "expected_message"),
    [
        (
            pd.DataFrame(),
            {"column1": "int"},
            ValueError,
            "Sheet is empty.",
        ),
        (
            pd.DataFrame({"column1": [1, 2, 3]}),
            {"column1": "int", "column2": "float"},
            ValueError,
            r"Missing columns in sheet. Expected:",
        ),
        (
            pd.DataFrame({"column1": [1, 2, "three"]}),
            {"column1": "int"},
            ValueError,
            r"Column 'column1' cannot be converted to int:",
        ),
    ],
)
def test_validate_excel_exceptions(
    sheet_df: pd.DataFrame,
    sheet_schema: dict,
    expected_exception: ValueError,
    expected_message: str,
) -> None:
    """
    Test possible error-causing edge cases for validate_excel() to ensure
    proper errors are raised.
    Cases:
    - Empty sheet
    - Missing columns
    - Column with data that cannot be cast to expected type.
    """
    with pytest.raises(expected_exception, match=expected_message):
        validate_excel(sheet_df, sheet_schema)


def test_validate_excel_success() -> None:
    """Test valid case for validate_excel() to ensure proper output."""
    test_df = pd.DataFrame({
        "column1": [1, 2, 3],
        "column2": [1.1, 2.2, 3.3],
    })
    sheet_schema = {"column1": "int", "column2": "float"}
    expected_dtypes = {"column1": "int", "column2": "float"}
    validated_df = validate_excel(test_df, sheet_schema)
    for col, dtype in expected_dtypes.items():
        assert validated_df[col].dtype == dtype


def test_validate_expenses_valid() -> None:
    """Test valid case for validate_expenses() to ensure no output."""
    expense_df = pd.DataFrame({
        "category": ["Food", "Transport"],
        "subcategory": ["Groceries", "Bus"],
    })

    budget_df = pd.DataFrame({
        "category": ["Food", "Transport"],
        "subcategory": ["Groceries", "Bus"],
    })

    # Should not raise any error
    validate_expenses(expense_df, budget_df)


def test_validate_expenses_invalid() -> None:
    """Test invalid case for validate_expenses() to ensure proper error."""
    expense_df = pd.DataFrame({
        "category": ["Food", "Transport", "Entertainment"],
        "subcategory": ["Groceries", "Bus", "Movies"],
    })

    budget_df = pd.DataFrame({
        "category": ["Food", "Transport"],
        "subcategory": ["Groceries", "Bus"],
    })

    with pytest.raises(
        ValueError, match="Categories or subcategories"
    ) as exc_info:
        validate_expenses(expense_df, budget_df)

    assert "Entertainment_Movies" in str(exc_info.value)
