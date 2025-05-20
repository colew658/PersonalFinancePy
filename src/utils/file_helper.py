"""Utils functions to help with file operations."""

from calendar import month_name
from pathlib import Path

import pandas as pd
import xlsxwriter
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


def convert_dfs_to_workbook(
    df_list: list[pd.DataFrame, ...],
    file_path: str,
    sheet_names: list[str],
) -> xlsxwriter.Workbook:
    """
    Convert a list of DataFrames to an xlsxwriter Workbook.

    Parameters
    ----------
    df_list : list[pd.DataFrame, ...]
        A list of DataFrames to be written to the Excel file.
    file_path : str
        The path for the Excel file to be created.
    sheet_names : list[str]
        A list of sheet names corresponding to each DataFrame in the tuple.

    Returns
    -------
    xlsx.Workbook
        A Workbook object containing the DataFrames as sheets.

    """
    writer = pd.ExcelWriter(file_path, engine="xlsxwriter")

    for df, sheet_name in zip(df_list, sheet_names):
        df.to_excel(writer, sheet_name=sheet_name, index=False)

    return writer.book


def bold_totals(report_wb: xlsxwriter.Workbook) -> xlsxwriter.Workbook:
    """
    Bold the total rows in the report Workbook.

    Parameters
    ----------
    report_wb : xlsxwriter.Workbook
        The report Workbook containing the total rows.

    Returns
    -------
    report_wb : xlsxwriter.Workbook
        The report Workbook with bolded total rows.

    """
    # Define a format for bold text
    bold_format = report_wb.add_format({"bold": True})

    # Iterate through all the sheets in the workbook
    for sheet_name in report_wb.sheetnames:
        worksheet = report_wb.get_worksheet_by_name(sheet_name)
        # Apply bold format to monthly reports
        if sheet_name in month_name:
            # Get the number of rows in the worksheet
            num_rows = worksheet.dim_rowmax
            # Apply bold format to the last row (total row)
            worksheet.set_row(num_rows, None, bold_format)

    return report_wb
