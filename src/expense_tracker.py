"""Expense Tracker Object."""

from pathlib import Path

import pandas as pd

from utils.file_helper import load_yaml
from utils.validation import validate_excel

PARENT_DIR = Path(__file__).resolve().parent.parent


class ExpenseTracker:
    """
    Expense Tracker Object.

    Parameters
    ----------
    excel_path : str
        Path to the expense tracker excel file.
    expense_sheet : str
        Name of the sheet containing the expense log.
    budget_sheet : str
        Name of the sheet containing the budgeted amounts per category.

    """

    def __init__(
        self,
        excel_path: str,
        expense_sheet: str,
        budget_sheet: str,
    ) -> None:
        """
        Initialize the ExpenseTracker object.

        Parameters
        ----------
        excel_path : str
            Path to the expense tracker excel file.
        expense_sheet : str
            Name of the sheet containing the expense log.
        budget_sheet : str
            Name of the sheet containing the budgeted amounts per category.

        """
        self.excel_path = excel_path
        self.expense_sheet = expense_sheet
        self.budget_sheet = budget_sheet
        config_path = f"{PARENT_DIR}/configs/data_schema.yaml"
        self.dtypes_dict = load_yaml(config_path)
        self.expense_log_dtypes = self.dtypes_dict["EXPENSE_LOG"]
        self.budget_dtypes = self.dtypes_dict["BUDGET"]

        self.expense_log = validate_excel(
            pd.read_excel(self.excel_path, sheet_name=self.expense_sheet),
            self.expense_log_dtypes,
        )
        self.budget = validate_excel(
            pd.read_excel(self.excel_path, sheet_name=self.budget_sheet),
            self.budget_dtypes,
        )

    def get_expense_log(self) -> pd.DataFrame:
        """
        Return the expense log.

        Returns
        -------
        pd.DataFrame
            Expense log.

        """
        return self.expense_log

    def get_budget(self) -> pd.DataFrame:
        """
        Return the budget.

        Returns
        -------
        pd.DataFrame
            Budget.

        """
        return self.budget

    def create_grouped_report(self) -> pd.DataFrame:
        """
        Return an expense report grouped by category and subcategory.

        Returns
        -------
        pd.DataFrame
            Expense report.

        """
        self.expense_log["month"] = self.expense_log[
            "date"
        ].dt.month_name()

        # Calculate total amount spent per category and subcategory
        self.expense_log["total_amount_spent"] = self.expense_log.groupby([
            "month",
            "category",
            "subcategory",
        ])["amount"].transform("sum")

        # Create expense_report
        self.grouped_report = (
            self.expense_log.merge(
                self.budget,
                on=["category", "subcategory"],
                how="left",
            )
            # Drop transaction details
            .drop(columns=["date", "amount", "payment_type", "note"])
            # Sort by category and subcategory
            .sort_values(
                by=["month", "category", "subcategory"],
            )
        ).drop_duplicates()

        # Calculate difference between budgeted and spent
        self.grouped_report["difference"] = (
            self.grouped_report["amount_budgeted"]
            - self.grouped_report["total_amount_spent"]
        )

        # Reorder columns
        column_order = [
            "month",
            "category",
            "subcategory",
            "amount_budgeted",
            "total_amount_spent",
            "difference",
        ]

        return self.grouped_report[column_order]

    def create_split_report(self) -> tuple[pd.DataFrame, ...]:
        """
        Return a tuple of DataFrames, one for each month.

        Returns
        -------
        tuple[pd.DataFrame, ...]
            Tuple of DataFrames, one per month.

        """
        if not hasattr(self, "grouped_report"):
            self.create_grouped_report()
        return tuple(
            self.grouped_report[self.grouped_report["month"] == month]
            for month in self.grouped_report["month"].unique()
        )
