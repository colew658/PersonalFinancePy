"""Transaction log formatter for Discover data."""

import logging

import pandas as pd

from transaction_formatters.base_formatter import BaseFormatter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DiscoverFormatter(BaseFormatter):
    """
    Formats transaction logs for Discover data.

    Parameters
    ----------
    file_path : str
        The path to the CSV file containing the transaction logs.

    """

    def __init__(self, file_path: str) -> None:
        """
        Initialize the DiscoverFormatter object.

        Parameters
        ----------
        file_path : str
            The path to the CSV file containing the transaction logs.

        """
        super().__init__(file_path)
        self.logger = logger
        self.discover_df = self._read_transaction_logs(
            # Schema does not include date columns
            schema={
                "Description": "str",
                "Amount": "float64",
                "Category": "str",
            },
            date_cols=["Trans. Date", "Post Date"],
        )

        if self.discover_df is None:
            self.logger.error("Failed to read Discover transaction logs.")
            return

    def format_discover_logs(self) -> pd.DataFrame:
        """
        Format the transaction logs for Discover.

        Returns
        -------
        pd.DataFrame
            The formatted DataFrame containing the transaction logs.

        """
        format_df = self.discover_df.copy()
        # Remove credit transactions (which are negative in Discover data)
        format_df = format_df[format_df["Amount"] > 0]

        # Insert blank columns for category and subcategory
        format_df["category"] = ""
        format_df["subcategory"] = ""

        # Insert payment_type
        format_df["payment_type"] = "Discover"

        # Keep only relevant columns and rename them
        format_df = format_df[
            [
                "Post Date",
                "category",
                "subcategory",
                "Amount",
                "payment_type",
                "Description",
            ]
        ]

        format_df = format_df.rename(
            columns={
                "Post Date": "date",
                "Amount": "amount",
                "Description": "note",
            },
        )

        self.discover_formatted_df = format_df
        return self.discover_formatted_df
