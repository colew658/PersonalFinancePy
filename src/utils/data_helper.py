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
