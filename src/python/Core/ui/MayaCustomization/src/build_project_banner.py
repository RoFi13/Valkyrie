# Copyright (C) 2023 Robert Wiese - All Rights Reserved.
"""This module is for showing maya show widget."""
# Can't find PySide2 modules pylint: disable=I1101

import json
import logging
import os

import pyperclip

from PySide6 import QtWidgets
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QPainter, QPaintEvent
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QPushButton, QWidget

from maya import OpenMayaUI, mel

import shiboken6

from Core import core_paths as cpath
from Core import maya_start as ms

MAIN_PATHS = cpath.core_paths()
LOG = logging.getLogger(os.path.basename(__file__))

# Module filepath
MODULE_PATH = os.sep.join(__file__.split(os.sep)[:-2])

# Resources filepath
RSRC_PATH = os.path.join(MODULE_PATH, "resources").replace("\\", "/")

LOADER = QUiLoader()


def create_project_banner():
    """Create the Project Banner button and embed it in Maya's status line widget.

    Returns:
        bool: Returns False if
    """
    if update_project_button() is True:
        LOG.info("Project button already exists. Updated existing button...")
        return False

    if build_banner_button() is None:
        return False

    return True


def build_banner_button():
    """Build a new banner button in Maya.

    Raises:
        RuntimeError: If no ProjectConfig.json file was found, raise error.

    Returns:
        QPushButton: Show button widget
    """
    LOG.info("Building banner button...")
    show_config_path = f"{MAIN_PATHS['dcc']}/ProjectConfig/ProjectConfig.json"
    LOG.info("Project config path: %s", show_config_path)
    if os.path.exists(show_config_path) is False:
        LOG.error(
            "Not a typical show or show has no ProjectConfig.json file. "
            "Please create it."
        )
        return False

    project_configs = None
    with open(show_config_path, encoding="utf-8") as metadata_file:
        project_configs = json.load(metadata_file)

    if isinstance(project_configs, dict) is False:
        LOG.error(
            "Failed to load ProjectConfig.json file data. Check file at: %s",
            show_config_path,
        )
        return False

    # Get status line python object
    status_line_name = mel.eval("$tmp=$gStatusLine")
    status_line_obj = convert_path_to_pyside_object(status_line_name)

    # Create button under status line parent object
    btn_project_banner = QPushButton(status_line_obj)
    btn_project_banner.setObjectName("project_button")

    # Customize button
    banner_image_path = MAIN_PATHS["project_maya_banner"]
    LOG.debug("Banner image path: %s", banner_image_path)

    # btn_project_banner.setStyleSheet(f"background-image: url({banner_image_path})")

    banner_icon = QIcon(banner_image_path)
    btn_project_banner.setIcon(banner_icon)
    btn_project_banner.setIconSize(
        QSize(btn_project_banner.width(), btn_project_banner.height())
    )

    btn_project_banner.setFixedSize(QSize(110, 35))

    # Connect function signal
    btn_project_banner.clicked.connect(show_project_details)

    # Add button to status line layout
    status_line_obj.layout().addWidget(btn_project_banner)

    return True


def update_project_button():
    """Update the text of the Project button.

    Returns:
        bool: True if change was successful. Otherwise, False.
    """
    # If Project button doesn't exist, create it
    project_button = find_project_button()
    if project_button is None:
        LOG.error("No Project button found in Maya UI.")
        return False

    project_configs_path = MAIN_PATHS["projectConfigs"]

    project_metadata = None
    if os.path.exists(project_configs_path):
        with open(project_configs_path, encoding="utf-8") as metadata_file:
            project_metadata = json.load(metadata_file)

    if isinstance(project_metadata, dict) is False:
        LOG.error(
            "Failed to load ProjectConfig.json file data. Check file at: %s",
            project_configs_path,
        )
        return False

    LOG.info("Deleting Existing Project Button...")
    project_button.deleteLater()
    LOG.info("Rebuilding Project Button...")
    build_banner_button()

    return True


def convert_path_to_pyside_object(name):
    """Convert a Maya UI element string into a PySide object.

    Using the Maya API, a match will be found if the string exists as a control,
    layout or menu item.

    Args:
        name (str): UI path of Maya UI element.

    Returns:
        PySide (QWidget) object of Maya UI element.
    """
    if not isinstance(name, str):
        raise ValueError("Parameter should be a string")

    ptr = OpenMayaUI.MQtUtil.findControl(name)
    if ptr is None:
        ptr = OpenMayaUI.MQtUtil.findLayout(name)
        result = None

    if ptr is None:
        ptr = OpenMayaUI.MQtUtil.findMenuItem(name)
        result = None

    if ptr is not None:
        result = shiboken6.wrapInstance(int(ptr), QWidget)

    return result


def show_project_details():
    """Show project details window."""
    ms.run_maya(ProjectDetailsWindow, "project_details", "Project Details", False)


def find_project_button():
    """Find the show button object in Maya's UI.

    Returns:
        QPushButton: Button object if found. Otherwise, None.
    """
    # Get status line python object
    status_line_name = mel.eval("$tmp=$gStatusLine")
    status_line_object = convert_path_to_pyside_object(status_line_name)
    # Get all button children of status line object
    status_children = status_line_object.findChildren(QPushButton)
    for child in status_children:
        # If button is the show button...
        if child.objectName() == "project_button":
            return child

    return None


def match_mel_variables(search_string=None):
    """Loop over all global MEL variables and if a search string is provided LOG.

    Info only the global MEL variables that match the search string.

    Args:
        search_string (str/None): String for searching.

    Example:
        for var in match_mel_variables("status"):
            LOG.info var
    """
    for var in sorted(mel.eval("env")):
        if not search_string or var.lower().count(search_string):
            yield var


class ProjectDetailsWindow(QtWidgets.QMainWindow):
    """Simple window showing crew and other project details.

    Args:
        Widget (QtWidgets.QMainWindow): Inheriting from QMainWindow
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        # Set up the window
        self.setWindowTitle("Project Details")
        self.setObjectName("project_details")

        # Load UIs
        LOG.info("ui file: %s", f"{RSRC_PATH}/ui/ProjectDetailsWindow.ui")

        self.main_tool_widget = LOADER.load(
            f"{RSRC_PATH}/ui/ProjectDetailsWindow.ui", self
        )

        self.setup_signals()

        # Window type
        self.setWindowFlags(Qt.Window)

        # Makes Maya perform magic which makes the window stay
        # on top in OS X and Linux. As an added bonus, it'll
        # make Maya remember the window position
        self.setProperty("saveWindowPref", True)

    def setup_signals(self):
        """Setup signals for window."""
        self.main_tool_widget.btn_close.clicked.connect(self.close)

        self.main_tool_widget.btn_mark_email.clicked.connect(
            lambda: pyperclip.copy("markconrad.animator@gmail.com")
        )
        self.main_tool_widget.btn_rob_email.clicked.connect(
            lambda: pyperclip.copy("rob@robwiese.com")
        )
        self.main_tool_widget.btn_gray_email.clicked.connect(
            lambda: pyperclip.copy("graysonducker@gmail.com")
        )

    def paintEvent(  # Override function pylint: disable=invalid-name
        self, event: QPaintEvent
    ):
        """Override the paintEvent to draw the background image

        Args:
            event (QPaintEvent): Paint event.
        """
        painter = QPainter(self)
        image_path = f"{RSRC_PATH}/ui/ProjectDetails_Background.png"
        painter.drawPixmap(0, 0, image_path)
        super().paintEvent(event)
