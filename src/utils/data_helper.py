"""Utils functions to help with data operations."""

import pandas as pd


def convert_datetime_to_str(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert all datetime columns to string columns in a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing the datetime columns.

    Returns
    -------
    pd.DataFrame
        The DataFrame with datetime columns converted to string columns.

    """
    for column in df.select_dtypes(include=["datetime64[ns]"]).columns:
        df[column] = df[column].dt.date.astype(str)
    return df


def append_totals_row(df: pd.DataFrame) -> pd.DataFrame:
    """
    Append a totals row to a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to which the totals row will be appended.

    Returns
    -------
    pd.DataFrame
        The DataFrame with the totals row appended.

    """
    totals = pd.DataFrame({
        "category": ["Total"],
        "subcategory": [None],
        "month": [None],
        "total_amount_spent": [df["total_amount_spent"].sum()],
        "amount_budgeted": [df["amount_budgeted"].sum()],
        "difference": [df["difference"].sum()],
    })
    return pd.concat([df, totals], ignore_index=True)
