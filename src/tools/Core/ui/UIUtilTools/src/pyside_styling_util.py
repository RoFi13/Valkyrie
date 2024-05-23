# Copyright (C) 2024 Robert Wiese - All Rights Reserved.
"""Various Pyside Styling utility functions."""

from enum import Enum
import logging
import os

from Core import core_paths as cpath
from Core.util import maya_colors

from PySide6 import QtCore, QtGui
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QComboBox, QMainWindow, QProgressDialog, QWidget

from importlib import reload

reload(maya_colors)

# Main paths
MAIN_PATHS = cpath.core_paths()

LOG = logging.getLogger(os.path.basename(__file__))


# class RGBColorOverride(Enum):
#     """RGB Colors to apply to different color controllers."""

#     RED = [1, 0, 0]
#     BLUE = [0, 0, 1]
#     YELLOW = [1, 1, 0]
#     PURPLE = [1, 0, 1]
#     ORANGE = [1, 0.247, 0]
#     DARK_GREEN = [0.073, 0.156, 0]


def set_right_border_color(
    widget: QWidget, width: float, color: maya_colors.RGBColorOverride
):
    """Set the Right side border to a new color.

    Args:
        widget (QWidget): Widget to add border to.
        width (float): Pixel width of border.
        color (maya_colors.RGBColorOverride): Color of border.
    """
    new_stylesheet: str
    match color:
        case maya_colors.RGBColorOverride.RED:
            new_stylesheet = f"QWidget {{border-right: {width}px solid red;}}"
        case maya_colors.RGBColorOverride.BLUE:
            new_stylesheet = f"QWidget {{border-right: {width}px solid blue;}}"
        case maya_colors.RGBColorOverride.YELLOW:
            new_stylesheet = f"QWidget {{border-right: {width}px solid yellow;}}"
        case maya_colors.RGBColorOverride.PURPLE:
            new_stylesheet = f"QWidget {{border-right: {width}px solid purple;}}"
        case maya_colors.RGBColorOverride.ORANGE:
            new_stylesheet = f"QWidget {{border-right: {width}px solid orange;}}"
        case maya_colors.RGBColorOverride.DARK_GREEN:
            new_stylesheet = f"QWidget {{border-right: {width}px solid #132800;}}"

    widget.setStyleSheet(new_stylesheet)
