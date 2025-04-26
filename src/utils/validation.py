"""Utils functions for validation."""

import pandas as pd


def validate_excel(
    sheet_df: pd.DataFrame,
    sheet_schema: dict,
) -> pd.DataFrame:
    """
    Validate an excel file to ensure sheets, columns, and data types are
    as expected.

    Parameters
    ----------
    sheet_df : pd.DataFrame
        The DataFrame pulled from an Excel sheet.
    sheet_schema : dict
        The expected schema for the given sheet.

    Returns
    -------
    pd.DataFrame
        The validated DataFrame with specified data types, if possible.

    Raises
    ------
    ValueError
        If the sheet is empty, missing columns, or has columns that cannot
        be cast to their expected data types.

    """
    # Validate sheet name
    if sheet_df.empty:
        msg = "Sheet is empty."
        raise ValueError(msg)

    # Validate columns
    expected_columns = sheet_schema.keys()
    if not all(col in sheet_df.columns for col in expected_columns):
        msg = f"Missing columns in sheet. Expected: {expected_columns}"
        raise ValueError(msg)

    # Validate data types
    try:
        for col, dtype in sheet_schema.items():
            sheet_df[col] = sheet_df[col].astype(dtype)
    except ValueError as e:
        msg = f"Column '{col}' cannot be converted to {dtype}: {e}"
        raise ValueError(msg) from e

    return sheet_df


def validate_expenses(
    expense_df: pd.DataFrame,
    budget_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Validate expenses to ensure all expense categories and subcategories
    have corresponding budgeted amounts.

    Parameters
    ----------
    expense_df : pd.DataFrame
        The DataFrame containing expenses.
    budget_df : pd.DataFrame
        The DataFrame containing budgeted amounts.

    Raises
    ------
    ValueError
        If there are categories or subcategories in the expense report
        that are not present in the budget.

    """
    tmp_expense_df = expense_df.copy()
    tmp_budget_df = budget_df.copy()
    tmp_expense_df["category_subcategory"] = (
        tmp_expense_df["category"] + "_" + tmp_expense_df["subcategory"]
    )
    tmp_budget_df["category_subcategory"] = (
        tmp_budget_df["category"] + "_" + tmp_budget_df["subcategory"]
    )
    missing_categories = tmp_expense_df[
        ~tmp_expense_df["category_subcategory"].isin(
            tmp_budget_df["category_subcategory"]
        )
    ]["category_subcategory"].unique()
    if len(missing_categories) > 0:
        msg = (
            f"Categories or subcategories in the expense report are not "
            f"present in the budget: {missing_categories}"
        )
        raise ValueError(msg)
