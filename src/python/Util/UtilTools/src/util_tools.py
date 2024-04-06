# Copyright (C) 2023 Robert Wiese - All Rights Reserved.
"""Various maya utility functions."""
# Can't find PySide2 modules pylint: disable=I1101

import logging
import os
import re

from maya import cmds

LOG = logging.getLogger(os.path.basename(__file__))


def version_up_file():
    """Versions up the current open file if version string exists.

    File name must have "v###" in its name. The number of version padding
    doesn't matter.
    """
    version_regex = re.compile("v[0-9]{1,10}")

    current_file_path = str(cmds.file(query=True, sceneName=True))
    split_file_path = current_file_path.split("/")
    parent_directory_path = "/".join(split_file_path[:-1])
    current_file_name = split_file_path[-1]

    regex_search_object = re.search(version_regex, current_file_name)
    # If no version string can be found in file name, skip
    if regex_search_object is None:
        cmds.confirmDialog(
            title="No Version in Filename",
            message='No "_v####" found in filename.',
            button=["Ok"],
            defaultButton="Ok",
            cancelButton="Ok",
            dismissString="Ok",
        )
        return

    current_version = int(
        current_file_name[regex_search_object.start() + 1 : regex_search_object.end()]
    )
    new_version = current_version + 1

    version_padding_length = len(
        current_file_name[regex_search_object.start() + 1 : regex_search_object.end()]
    )
    padded_number = str(new_version).rjust(version_padding_length, "0")

    string_before_version = current_file_name[: regex_search_object.start()]
    string_after_version = current_file_name[regex_search_object.end() :]

    new_file_name = f"{string_before_version}v{padded_number}{string_after_version}"

    file_details = {
        "parent_directory_path": parent_directory_path,
        "string_before_version": string_before_version,
        "string_after_version": string_after_version,
    }

    new_file_path = create_latest_version(
        file_details,
        f"{parent_directory_path}/{new_file_name}",
        new_version,
        version_padding_length,
    )
    logging.info("New filename being saved as: %s", new_file_path)

    cmds.file(rename=new_file_path)
    cmds.file(force=True, save=True, options="v=0;")


def create_latest_version(
    file_details, current_file_path, new_version_number, version_padding
):
    """Create latest version of file.

    Loop until version of file doesn't exist.

    Args:
        file_details (dict):            File details.
                                        {
                                            "parent_directory_path": (str),
                                            "string_before_version": (str),
                                            "string_after_version": (str)
                                        }
        current_file_path (str):        Current file path to start checking.
        new_version_number (int):       Version to check for.
        version_padding (int):   How much padding for version number.

    Return:
        Return string of latest version file path.
    """
    new_file_path = current_file_path
    parent_directory_path = file_details["parent_directory_path"]
    string_before_version = file_details["string_before_version"]
    string_after_version = file_details["string_after_version"]

    if not os.path.exists(new_file_path):
        return new_file_path

    while os.path.exists(new_file_path):
        new_version_number += 1
        padded_number = str(new_version_number).rjust(version_padding, "0")
        new_file_name = f"{string_before_version}v{padded_number}{string_after_version}"
        new_file_path = f"{parent_directory_path}/{new_file_name}"

    return new_file_path


def check_scene_for_joints():
    all_joints = cmds.ls(type="joint")

    if len(all_joints) == 0:
        return False

    return True
