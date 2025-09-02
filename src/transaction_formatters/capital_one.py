"""Transaction log formatter for Capital One data."""

import logging

import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CapitalOneFormatter:
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
        self.file_path = file_path
        self.logger = logger

    def _read_cap_one_csv(self) -> pd.DataFrame:
        """
        Read the Capital One CSV file and return a DataFrame.

        Returns
        -------
        pd.DataFrame
            The DataFrame containing the transaction logs.

        """
        schema = {
            "Transaction Date": "datetime64[ns]",
            "Posted Date": "datetime64[ns]",
            "Card No.": "Int64",
            "Description": "str",
            "Category": "str",
            "Debit": "float64",
            "Credit": "float64",
        }
        try:
            return pd.read_csv(self.file_path, dtype=schema)
        except Exception:
            self.logger.exception("Error reading Capital One CSV")
            return pd.DataFrame(columns=schema.keys())
