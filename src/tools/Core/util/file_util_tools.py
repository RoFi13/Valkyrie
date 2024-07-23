# get_json_data
# get_list_of_maya_files

import json
import logging
import os
from pathlib import Path
import re

LOG = logging.getLogger(os.path.basename(__file__))


def get_files_or_folders(
    starting_directory: str,
    return_files: bool = False,
    full_path: bool = False,
    object_regex: str = None,
):
    """Get list of folders optionally with regex.

    Args:
        starting_directory (str): Name of the directory to get list of folders from.
        return_files (bool): Whether to return files only.
        full_path (bool, optional): Whether to return full folder path or not.
            Defaults to False.
        object_regex (str, optional): Regular expression of directory. Defaults to None.

    Returns:
        list: If more than 0 folders are found, return list of folders. Return full paths
            if requested. Otherwise, returns None.
    """
    if not os.path.exists(starting_directory):
        LOG.warning("Directory path doesn't exist at: %s", starting_directory)
        return []

    # Names in the given directory
    objects = os.listdir(starting_directory)
    found_paths = []
    object_names = []
    object_paths = []
    # Iterate over all the entries
    for item in objects:
        # Create full path
        full_directory_path = f"{starting_directory}/{item}"

        if return_files is True and os.path.isdir(full_directory_path) is True:
            continue

        if return_files is False and os.path.isdir(full_directory_path) is not True:
            continue

        # Not looking for pattern
        if object_regex is None:
            object_names.append(item)
            object_paths.append(full_directory_path)
            continue

        # File/Folder needs to match pattern
        if re.match(object_regex, item):
            object_names.append(item)
            object_paths.append(full_directory_path)

    if len(object_names) == 0:
        LOG.info("No files/folders found.")
        return []

    object_names.sort()
    object_paths.sort()

    found_paths = object_names
    if full_path is True:
        found_paths = object_paths

    return found_paths


def get_json_data(json_path: str):
    """Get json data.

    Args:
        json_path (str): Path of json file.

    Returns:
        Json data.
    """
    json_data = None
    with open(json_path, encoding="utf-8") as json_data:
        json_data = json.load(json_data)

    if isinstance(json_data, dict) is False:
        LOG.error("Failed to load JSON data. Check file at: %s", json_path)
        return None

    return json_data


def write_json_data(data: dict, json_path: str):
    """Write data to JSON file on disk.

    Args:
        data (dict): Data to be written.
        json_path (str): Path to JSON data to.
    """
    with open(json_path, "w", encoding="utf-8") as out_file:
        json.dump(data, out_file, indent=4)


def create_directory(directory_path: str):
    """Create directory if it doesn't exist.

    Args:
        directory_path (str): Path to directory.
    """
    Path(directory_path).mkdir(parents=True, exist_ok=True)
