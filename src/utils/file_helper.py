"""Utils functions to help with file operations."""

from pathlib import Path

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
