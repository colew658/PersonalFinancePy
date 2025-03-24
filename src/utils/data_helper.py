"""Utils functions to help with data operations."""

from calendar import month_name

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
    Append an overall totals row to a DataFrame.

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


def append_category_totals(expense_report: pd.DataFrame) -> pd.DataFrame:
    """
    Append category totals to a DataFrame.

    Parameters
    ----------
    expense_report : pd.DataFrame
        The DataFrame to which the category totals will be appended.

    Returns
    -------
    pd.DataFrame
        The DataFrame with the category totals appended.

    """
    # Calculate category totals
    category_totals = (
        expense_report.groupby(["category"]).sum().reset_index()
    )
    # Drop overall total
    category_totals = category_totals[
        category_totals["category"] != "Total"
    ]
    category_totals["subcategory"] = "Total"
    category_totals["month"] = None
    category_totals["difference"] = (
        category_totals["amount_budgeted"]
        - category_totals["total_amount_spent"]
    )
    # Append category totals to the expense report
    return pd.concat([expense_report, category_totals], ignore_index=True)


def place_totals_rows(expense_report: pd.DataFrame) -> pd.DataFrame:
    """
    Place totals rows in the expense report in their correct locations.
    Category totals are placed below their respective categories,
    and an overall total is placed at the end.

    Parameters
    ----------
    expense_report : pd.DataFrame
        The expense report with totals rows unordered.

    Returns
    -------
    pd.DataFrame
        The DataFrame with the totals rows in their correct locations.

    """
    # Identify category total rows
    category_totals = expense_report[
        expense_report["subcategory"] == "Total"
    ]

    # Identify overall total row
    overall_total = expense_report[expense_report["category"] == "Total"]

    # Identify non-total rows
    non_totals = expense_report[
        ~(
            (expense_report["subcategory"] == "Total")
            | (expense_report["category"] == "Total")
        )
    ]

    # Create separate DataFrames for each category
    category_dfs = []
    category_list = category_totals["category"].unique()

    for cat in category_list:
        # Filter rows for the current category
        cat_df = non_totals[(non_totals["category"] == cat)]
        cat_total = category_totals[category_totals["category"] == cat]

        # Append the category total row to the DataFrame
        cat_df = pd.concat([cat_df, cat_total], ignore_index=True)
        category_dfs.append(cat_df)

    # Concatenate all category DataFrames
    sorted_report = pd.concat(category_dfs, ignore_index=True)

    # Append overall total at the end
    sorted_report = pd.concat([sorted_report, overall_total])

    return sorted_report.reset_index(drop=True)


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


def sort_month_order(
    df_list: list[pd.DataFrame, ...],
) -> list[pd.DataFrame, ...]:
    """
    Sort a list of DataFrames by the month column.

    Parameters
    ----------
    df_list : list[pd.DataFrame, ...]
        The list of DataFrames to be sorted. Each DataFrame must contain
        a "month" column. The month column should contain the full month
        name, and all month values should be the same.

    Returns
    -------
    list[pd.DataFrame, ...]
        The sorted list of DataFrames.

    """
    month_order = {month: i for i, month in enumerate(month_name) if month}
    return sorted(df_list, key=lambda df: month_order[df["month"].iloc[0]])
