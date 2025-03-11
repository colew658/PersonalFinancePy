"""Unit tests for file_helper.py."""

import tempfile
from pathlib import Path

import pytest
import yaml

from utils.file_helper import load_yaml


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
