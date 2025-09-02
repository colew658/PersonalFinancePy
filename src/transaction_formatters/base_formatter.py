"""Base transaction log formatter object."""

import pandas as pd

from src.utils.file_handler import setup_logging

log = setup_logging()


class BaseFormatter:
    """
    Base class for transaction log formatters.

    Parameters
    ----------
    file_path : str
        The path to the file containing the transaction logs.

    """

    def __init__(self, file_path: str) -> None:
        """
        Initialize the BaseFormatter object.

        Parameters
        ----------
        file_path : str
            The path to the file containing the transaction logs.

        """
        self.file_path = file_path
        self.log = log

    def _read_transaction_logs(
        self, schema: dict[str, str]
    ) -> pd.DataFrame:
        """
        Read the transaction logs from the file and return a DataFrame.

        Returns
        -------
        pd.DataFrame
            The DataFrame containing the transaction logs.

        """
        try:
            return pd.read_csv(self.file_path, dtype=schema)
        except Exception:
            self.log.exception("Error reading transaction logs")
