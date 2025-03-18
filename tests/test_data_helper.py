"""Unit tests for data_helper.py."""

import pandas as pd

from utils.data_helper import convert_datetime_to_str


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
