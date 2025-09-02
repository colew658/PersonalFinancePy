"""Base transaction log formatter object."""

import pandas as pd

from utils.file_helper import setup_logging


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
        self,
        schema: dict[str, str],
        date_cols: list[str],
    ) -> pd.DataFrame:
        """
        Read the transaction logs from the file and return a DataFrame.

        Parameters
        ----------
        schema : dict[str, str]
            The schema to use when reading the transaction logs. Should not
            include columns listed in date_cols.
        date_cols : list[str]
            The list of columns to convert to datetime.

        Returns
        -------
        pd.DataFrame
            The DataFrame containing the transaction logs.

        """
        try:
            trans_log = pd.read_csv(
                self.file_path,
                dtype=schema,
                parse_dates=date_cols,
            )
            trans_log[date_cols] = trans_log[date_cols].apply(
                pd.to_datetime
            )

        except Exception:
            self.log.exception("Error reading transaction logs:")

        else:
            self.log.info("Successfully read transaction log!")
            return trans_log
