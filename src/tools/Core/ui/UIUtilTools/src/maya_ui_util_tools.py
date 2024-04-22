# Copyright (C) 2023 Robert Wiese - All Rights Reserved.
"""Various Maya UI utility functions"""

# Can't find PySide2 modules pylint: disable=I1101

import logging
import os

from maya import cmds

LOG = logging.getLogger(os.path.basename(__file__))


def browse_dialog_maya_files(start_dir: str, line_widget=None):
    """Open Maya file dialog and display only Maya file types.

    Args:
        start_dir (str): Path of the start directory.
        line_widget (obj): Line widget to set the path of file.

    Returns:
        str: The file at the given path. If start_dir path doesn't exist,
            returns empty string.
    """

    if not os.path.exists(start_dir):
        LOG.warning("Starting directory doesn't exist here: %s", start_dir)
        return ""

    if line_widget is None:
        file_filter = "Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb)"
        return cmds.fileDialog2(
            fileFilter=file_filter,
            dialogStyle=2,
            fileMode=1,
            startingDirectory=start_dir,
        )[0]

    file_filter = "Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb)"
    file_path = cmds.fileDialog2(
        fileFilter=file_filter, dialogStyle=2, fileMode=1, startingDirectory=start_dir
    )[0]
    line_widget.setText(file_path)

    return file_path


def display_confirm_dialog(
    title: str, message: str, buttons: list = None, default_button: str = "Ok"
):
    """Display confirmation success message.

    Args:
        title (str): Title of confirm dialog window.
        message (str): Message of confirm dialog window.
        buttons (list): List of button names user can press. Defaults to ['Ok'].
        default_button (str): Default string button for default, cancel, and
            dismiss. Defaults to 'Ok'.
    """

    if buttons is None:
        buttons = ["Ok"]

    return cmds.confirmDialog(
        title=title,
        message=message,
        button=buttons,
        defaultButton=default_button,
        cancelButton=default_button,
        dismissString=default_button,
    )
