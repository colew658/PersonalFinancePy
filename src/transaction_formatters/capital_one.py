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
            # Schema does not include date columns
            schema={
                "Card No.": "Int64",
                "Description": "str",
                "Category": "str",
                "Debit": "float64",
                "Credit": "float64",
            },
            date_cols=["Transaction Date", "Posted Date"],
        )

        if self.cap_one_df is None:
            self.logger.error(
                "Failed to read Capital One transaction logs."
            )
            return

    def format_cap_one_logs(self) -> pd.DataFrame:
        """
        Format the transaction logs for Capital One.

        Returns
        -------
        pd.DataFrame
            The formatted DataFrame containing the transaction logs.

        """
        # Remove credit transactions
        self.cap_one_df = self.cap_one_df[
            (self.cap_one_df["Credit"] == 0)
            | (self.cap_one_df["Credit"].isna())
        ]

        # Insert blank columns for category and subcategory
        self.cap_one_df["category"] = ""
        self.cap_one_df["subcategory"] = ""

        # Insert payment_type
        self.cap_one_df["payment_type"] = "Venture"

        # Drop unneeded columns
        self.cap_one_df = self.cap_one_df[
            [
                "Posted Date",
                "category",
                "subcategory",
                "Debit",
                "payment_type",
                "Description",
            ]
        ]

        # Rename columns to match expected output
        self.cap_one_df = self.cap_one_df.rename(
            columns={
                "Posted Date": "date",
                "Debit": "amount",
                "Description": "note",
            }
        )

        return self.cap_one_df
