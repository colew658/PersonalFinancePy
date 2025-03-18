"""Unit tests for file_helper.py."""

import sys
import tempfile
from pathlib import Path

import pandas as pd
import pytest
import yaml

from utils.file_helper import load_yaml, write_to_excel

sys.path.append(str(Path(__file__).resolve().parent.parent))


@pytest.mark.parametrize(
    ("yaml_content", "expected_output"),
    [
        ("key: value", {"key": "value"}),  # Simple key-value pair
        (
            "list:\n  - item1\n  - item2",
            {"list": ["item1", "item2"]},
        ),  # List
        (
            "nested:\n  key: value",
            {"nested": {"key": "value"}},
        ),  # Nested dictionary
        ("number: 42", {"number": 42}),  # Integer value
        ("boolean: true", {"boolean": True}),  # Boolean value
    ],
)
def test_load_yaml_valid(yaml_content: str, expected_output: dict) -> None:
    """
    Test loading valid YAML content.

    Parameters
    ----------
    yaml_content : str
        The YAML content to be tested.
    expected_output : dict
        The expected output after loading the YAML content.

    """
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".yaml",
    ) as temp_file:
        temp_file.write(yaml_content.encode("utf-8"))
        temp_file_path = temp_file.name

    try:
        result = load_yaml(temp_file_path)
        assert result == expected_output
    finally:
        Path.unlink(temp_file_path)  # Clean up


@pytest.mark.parametrize(
    ("invalid_yaml_content"),
    [
        "key: value: another_value",  # Invalid YAML syntax
        "- item1\n- item2\nitem3:",  # Malformed list
        "{unclosed: mapping",  # Unclosed dictionary
    ],
)
def test_load_yaml_invalid_yaml(invalid_yaml_content: str) -> None:
    """
    Test loading invalid YAML content.

    Parameters
    ----------
    invalid_yaml_content : str
        The invalid YAML content to be tested.

    """
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".yaml",
    ) as temp_file:
        temp_file.write(invalid_yaml_content.encode("utf-8"))
        temp_file_path = temp_file.name

    try:
        with pytest.raises(yaml.YAMLError):
            load_yaml(temp_file_path)
    finally:
        Path.unlink(temp_file_path)


def test_load_yaml_file_not_found() -> None:
    """Test loading a non-existent YAML file."""
    with pytest.raises(FileNotFoundError):
        load_yaml("non_existent_file.yaml")


# TODO: Write this test in a way that doesn't require writing to a file.
# Currently, this test writes to a file and then reads from it.
# This prevents the pytest pre-commit hook from passing.
@pytest.mark.skip(
    reason="This test writes a file, causing pre-commit to fail."
)
def test_write_to_excel() -> None:
    """
    Test writing multiple DataFrames to an Excel file using the
    write_to_excel function.
    """
    # Define input
    df1 = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    df2 = pd.DataFrame({"X": ["a", "b", "c"], "Y": ["d", "e", "f"]})
    df_tuple = (df1, df2)
    sheet_names = ["Sheet1", "Sheet2"]
    test_file_path = "tests/fixtures/test_write_to_excel.xlsx"

    # Call the function
    write_to_excel(
        df_tuple=df_tuple,
        file_path=test_file_path,
        sheet_names=sheet_names,
    )

    actual_sheet1 = pd.read_excel(
        test_file_path, sheet_name=sheet_names[0]
    )
    actual_sheet2 = pd.read_excel(
        test_file_path, sheet_name=sheet_names[1]
    )

    assert (
        pd.testing.assert_frame_equal(
            actual_sheet1,
            df1,
        )
        is None
    )
    assert (
        pd.testing.assert_frame_equal(
            actual_sheet2,
            df2,
        )
        is None
    )
