"""Base transaction log formatter object."""

import pandas as pd

from src.utils.file_handler import setup_logging


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
        self.log = setup_logging()

    def _read_transaction_logs(
        self, schema: dict[str, str], date_format: str
    ) -> pd.DataFrame:
        """
        Read the transaction logs from the file and return a DataFrame.

        Parameters
        ----------
        schema : dict[str, str]
            The schema to use when reading the transaction logs.
        date_format : str
            The date format to use when parsing dates.

        Returns
        -------
        pd.DataFrame
            The DataFrame containing the transaction logs.

        """
        try:
            return pd.read_csv(
                self.file_path,
                dtype=schema,
                parse_dates=True,
                date_format=date_format,
            )
        except Exception:
            self.log.exception("Error reading transaction logs")
