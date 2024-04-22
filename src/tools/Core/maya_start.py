# Copyright (C) 2023 DNEG - All Rights Reserved.
"""Run tool in Maya instance helper functions."""

import logging
import os
import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from maya import cmds


PY_VERSION = sys.version_info.major

sys.dont_write_bytecode = True  # Avoid writing .pyc files

LOG = logging.getLogger(os.path.basename(__file__))


def maya_delete_ui(window_object, window_title):
    """Delete existing UI in Maya.

    Args:
        window_object (str): Object name.
        window_title (str): Window title.
    """

    if cmds.window(window_object, query=True, exists=True):
        LOG.info("Found existing tool window for %s. Deleting UI...", window_object)
        cmds.deleteUI(window_object)  # Delete window

    LOG.info("Checking for docked tool window...")
    if cmds.dockControl("MayaWindow|" + window_title, query=True, exists=True):
        LOG.info("Found existing dock window for %s. Deleting UI...", window_title)
        cmds.deleteUI("MayaWindow|" + window_title)  # Delete docked window

    LOG.info("Existing tool window %s not found.", window_title)


def maya_main_window():
    """Return Maya's main window."""
    maya_window_object = None
    for obj in QApplication.topLevelWidgets():
        if obj.objectName() == "MayaWindow":
            LOG.info("Found MayaWindow instance.")
            maya_window_object = obj
            break

    return maya_window_object


def run_maya(
    tool_class: QMainWindow,
    window_object: str,
    window_title: str,
    dock_with_maya_ui: bool,
    **kwargs
):
    """Run the tool in Maya.

    Args:
        tool_class (obj): Tool class object to instantiate from
        window_object (str): object name.
        window_title (str): window title.
        dock_with_maya_ui (bool): Whether to launch tool as a dockable utility window.
        kwargs (dict): passing an arbitrary number of keyword arguments to the function.

    Raises:
        RuntimeError: Raised if no valid MayaWindow object is found.

    Returns:
        QMainWindow: Created Window object of tool being instantiated.
    """

    maya_window = maya_main_window()
    if maya_window is None:
        raise RuntimeError("No valid MayaWindow instance found.")

    # Delete any existing existing UI
    maya_delete_ui(window_object, window_title)
    if len(kwargs.items()) > 0:
        tool_object = tool_class(parent=maya_window, kwargs=kwargs)
    else:
        tool_object = tool_class(parent=maya_window)

    # Makes Maya perform magic which makes the window stay
    # on top in OS X and Linux. As an added bonus, it'll
    # make Maya remember the window position
    property_result = tool_object.setProperty("saveWindowPref", True)
    if property_result is not True:
        LOG.info("Maya saveWindowPref property not found or set.")

    if dock_with_maya_ui:
        allowed_areas = ["right", "left"]
        cmds.dockControl(
            window_title,
            label=window_title,
            area="left",
            content=window_object,
            allowedArea=allowed_areas,
        )
        return tool_object

    tool_object.show()  # Show the UI
    return tool_object
