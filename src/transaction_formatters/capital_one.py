"""Transaction log formatter for Capital One data."""

import logging

import pandas as pd

from transaction_formatters.base_formatter import BaseFormatter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CapitalOneFormatter(BaseFormatter):
    """
    Formats transaction logs for Capital One data.

    Parameters
    ----------
    file_path : str
        The path to the CSV file containing the transaction logs.

    """

    def __init__(self, file_path: str) -> None:
        """
        Initialize the CapitalOneFormatter object.

        Parameters
        ----------
        file_path : str
            The path to the CSV file containing the transaction logs.

        """
        super().__init__(file_path)
        self.logger = logger
        self.cap_one_df = self._read_transaction_logs(
            schema={
                "Card No.": "Int64",
                "Description": "str",
                "Category": "str",
                "Debit": "float64",
                "Credit": "float64",
            },
            date_cols=["Transaction Date", "Posted Date"],
        )

    def format_cap_one_logs(self, keep_credits: str) -> pd.DataFrame:
        """
        Format the transaction logs for Capital One.

        Parameters
        ----------
        keep_credits : str
            Whether to keep credit transactions in the DataFrame (y/n).

        Returns
        -------
        pd.DataFrame
            The formatted DataFrame containing the transaction logs.

        """
        if keep_credits == "n":
            # Remove credit transactions
            self.cap_one_df = self.cap_one_df[
                (self.cap_one_df["Credit"] == 0)
                | (self.cap_one_df["Credit"].isna())
            ]

        return self.cap_one_df
