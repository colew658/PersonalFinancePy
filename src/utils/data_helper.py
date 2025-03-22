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


def fill_missing_expenses(
    expense_report: pd.DataFrame,
    budget: pd.DataFrame,
    month: str,
) -> pd.DataFrame:
    """
    Fill budgeted expenses with no transactions attached to them.

    Parameters
    ----------
    expense_report : pd.DataFrame
        The expense report for a given month.
    budget : pd.DataFrame
        The DataFrame containing the budget for a given month.
    month : str
        The month corresponding to the expense report and budget.

    Returns
    -------
    pd.DataFrame
        The DataFrame with missing expenses filled in.

    """
    # Find categories and subcategories that are in the budget
    # but not in the expense log
    missing_expenses = budget[
        ~budget.set_index(["category", "subcategory"]).index.isin(
            expense_report.set_index(["category", "subcategory"]).index
        )
    ]
    # Create a new DataFrame with the missing expenses
    missing_expenses = pd.DataFrame({
        "category": missing_expenses["category"],
        "subcategory": missing_expenses["subcategory"],
        "month": month,
        "total_amount_spent": [0] * len(missing_expenses),
        "amount_budgeted": missing_expenses["amount_budgeted"],
        "difference": missing_expenses["amount_budgeted"],
    })

    # Append the missing expenses to the expense report
    return pd.concat([expense_report, missing_expenses], ignore_index=True)
