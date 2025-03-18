"""Utils functions to help with file operations."""

from pathlib import Path

import pandas as pd
import yaml


def load_yaml(yaml_path: str) -> dict:
    """
    Load a YAML file and return its contents as a dictionary.

    Parameters
    ----------
    yaml_path : str
        The path to the YAML file.

    Returns
    -------
    dict
        The contents of the YAML file as a dictionary.

    Raises
    ------
    FileNotFoundError
        If the specified YAML file does not exist.
    yaml.YAMLError
        If there is an error parsing the YAML file.

    """
    try:
        with Path.open(yaml_path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError as e:
        msg = f"File not found: {yaml_path}"
        raise FileNotFoundError(msg) from e
    except yaml.YAMLError as e:
        msg = f"Error parsing YAML file: {yaml_path}"
        raise yaml.YAMLError(msg) from e


def write_to_excel(
    df_tuple: tuple[pd.DataFrame, ...],
    file_path: str,
    sheet_names: list[str],
) -> None:
    """
    Write a tuple of DataFrames to an Excel file with given sheet names.

    Parameters
    ----------
    df_tuple : tuple[pd.DataFrame, ...]
        A tuple of DataFrames to be written to the Excel file.
    file_path : str
        The path for the Excel file to be created.
    sheet_names : list[str]
        A list of sheet names corresponding to each DataFrame in the tuple.

    """
    with pd.ExcelWriter(
        file_path,
        engine="openpyxl",
    ) as writer:
        for df, sheet_name in zip(df_tuple, sheet_names):
            df.to_excel(writer, sheet_name=sheet_name, index=False)
