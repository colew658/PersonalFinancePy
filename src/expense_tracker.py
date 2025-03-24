"""Expense Tracker Object."""

import copy
from pathlib import Path

import pandas as pd

from utils.data_helper import (
    append_category_totals,
    append_totals_row,
    convert_datetime_to_str,
    fill_missing_expenses,
    place_totals_rows,
)
from utils.file_helper import load_yaml, write_to_excel
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

    def create_split_report(self) -> list[pd.DataFrame, ...]:
        """
        Return a list of DataFrames, one for each month.

        Returns
        -------
        list[pd.DataFrame, ...]
            List of DataFrames, one per month.

        """
        if not hasattr(self, "grouped_report"):
            self.create_grouped_report()
        self.split_report = [
            self.grouped_report[self.grouped_report["month"] == month]
            for month in self.grouped_report["month"].unique()
        ]
        # Fill missing expenses with no transactions attached to them
        for i in range(len(self.split_report)):
            # Get the month name from the DataFrame
            month = self.split_report[i]["month"].unique()[0]
            # Fill missing expenses for the month
            self.split_report[i] = fill_missing_expenses(
                self.split_report[i],
                self.budget,
                month,
            ).sort_values(
                by=["category", "subcategory"],
            )
        return self.split_report

    def append_totals_rows(self) -> list[pd.DataFrame, ...]:
        """
        Append overall and category-wise totals to the report.

        Returns
        -------
        list[pd.DataFrame, ...]
            List of DataFrames, one per month, with totals rows appended.

        """
        if not hasattr(self, "split_report"):
            self.create_split_report()
            # Store original unmodified split report
            self.original_split_report = copy.deepcopy(self.split_report)

        # Reset `split_report` to its original state before modification
        self.split_report = copy.deepcopy(self.original_split_report)

        for i in range(len(self.split_report)):
            # Append overall totals row
            self.split_report[i] = append_totals_row(self.split_report[i])

            # Append category-wise totals row
            self.split_report[i] = append_category_totals(
                self.split_report[i]
            )

            # Place totals rows in correct order
            self.split_report[i] = place_totals_rows(self.split_report[i])

        return self.split_report

    def write_report_to_excel(
        self,
        file_path: str,
    ) -> None:
        """
        Write the expense report to an Excel file.

        Parameters
        ----------
        file_path : str
            Path to the output Excel file.

        """
        if not hasattr(self, "split_report"):
            self.append_totals_rows()

        # Append the expense log and budget to the report
        self.full_report = (
            self.expense_log,
            self.budget,
            *self.split_report,
        )

        # Convert datetime columns to string columns
        self.full_report = tuple(
            convert_datetime_to_str(df) for df in self.full_report
        )

        sheet_names = [
            "Expense Log",
            "Budget",
            *list(self.grouped_report["month"].unique()),
        ]

        write_to_excel(
            df_tuple=self.full_report,
            file_path=file_path,
            sheet_names=sheet_names,
        )
