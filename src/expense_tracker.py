"""Expense Tracker Object."""

import pandas as pd


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

        self.expense_log = pd.read_excel(
            self.excel_path,
            sheet_name=self.expense_sheet,
        )
        self.budget = pd.read_excel(
            self.excel_path,
            sheet_name=self.budget_sheet,
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
