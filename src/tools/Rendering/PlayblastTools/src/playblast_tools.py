# Copyright (C) 2024 Robert Wiese - All Rights Reserved.
"""Various functions Playblasts in Maya."""

import logging
import os

from maya import cmds

LOG = logging.getLogger(os.path.basename(__file__))


def play_blast_quick():
    """Assign to marking menu for fast playblasting."""
    result = cmds.promptDialog(
        title="Playblast Prefix",
        message="Enter Prefix:",
        button=["OK", "Cancel"],
        defaultButton="OK",
        cancelButton="Cancel",
        dismissString="Cancel",
    )

    if result != "OK" and result != "Cancel":
        raise ValueError("Invalid selection: must choose 'OK' or 'Cancel'")
    if result == "Cancel":
        LOG.info("User selects Cancel button.")
        return
    if result == "OK":
        prefix_text = cmds.promptDialog(query=True, text=True)

    LOG.info("Master File: %s", cmds.file(query=True, sceneName=True))
    # Capture shot/file name
    master_file = str(cmds.file(query=True, sceneName=True))
    shot_name = master_file.split("/", maxsplit=-1)[-1].split(".")[0]
    play_blast_shot_folder = f"{'/'.join(master_file.split('/')[:-1])}/playblasts"
    LOG.info("Playblast folder: %s", play_blast_shot_folder)

    if not os.path.exists(play_blast_shot_folder):
        os.mkdir(play_blast_shot_folder)

    final_file_path = f"{play_blast_shot_folder}/{prefix_text}{shot_name}_pb.mov"
    LOG.info("Save path: %s", final_file_path)
    # Playblast rendercam view under "movies" directory as .mov with shot/file name
    cmds.playblast(
        format="image",
        filename=final_file_path,
        forceOverwrite=True,
        sequenceTime=False,
        clearCache=True,
        viewer=True,
        showOrnaments=False,
        framePadding=4,
        percent=50,
        compression="jpg",
        quality=100,
        widthHeight=(1920, 1080),
    )
