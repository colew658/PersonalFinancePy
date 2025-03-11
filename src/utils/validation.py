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
