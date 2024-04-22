# Copyright (C) 2023 Robert Wiese - All Rights Reserved.
"""Various string utility functions."""
# Can't find PySide2 modules pylint: disable=I1101

import logging
import os
import re

LOG = logging.getLogger(os.path.basename(__file__))


def cleanup_path_slashes(file_path: str):
    """Remove extra maya slashes from filepath.

    Maya sometimes returns a weird number of forward slashes sometimes. This function
    will attempt to cleanthem up.

    Args:
        file_path (str): File path string to clean up.

    Returns:
        str: Cleaned up file path string.
    """
    if "\\\\" in file_path:
        LOG.info("Replacing \\\\ with /")
        file_path = file_path.replace("\\\\", "/")
    elif "\\" in file_path:
        LOG.info("Replacing \\ with /")
        file_path = file_path.replace("\\", "/")

    LOG.info("Sanitized file path: %s", file_path)

    return file_path


def find_version_string(source_string: str, padding_amount: int = 3):
    version_regex = f"v[0-9]{{{padding_amount},{padding_amount}}}"
    return re.search(version_regex, source_string)


def replace_version_string(
    source_string: str, new_version: int, padding_amount: int = 3
):
    new_version_string = f"v{str(new_version).rjust(padding_amount, '0')}"

    string_version_search = find_version_string(source_string)

    updated_string = source_string.replace(
        source_string[string_version_search.start() : string_version_search.end()],
        new_version_string,
    )

    return updated_string
