"""Various Shot Builder Gui Utility functions."""

# Can't find PySide6 modules pylint: disable=I1101

import logging
import os
import shutil

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QMainWindow

from Core.util import project_util_tools as prj
from Core.ui.UIUtilTools.src import maya_ui_util_tools as mui


LOG = logging.getLogger(os.path.basename(__file__))


def set_asset_naming_validators_example(root_object: QtWidgets.QWidget):
    """Set the asset name and variation line edit object's text validators.

    Args:
        root_object (QtWidgets.QWidget): Main tool window object.
    """
    # asset_name_regex = QtCore.QRegExp(prj.get_project_config_item("asset_name_regex"))
    asset_name_regex = QtCore.QRegularExpression(
        prj.get_project_config_item("asset_name_regex")
    )
    asset_name_text_validator = QtGui.QRegularExpressionValidator(asset_name_regex)

    asset_variant_regex = QtCore.QRegularExpression(
        prj.get_project_config_item("asset_variant_regex")
    )
    asset_variant_text_validator = QtGui.QRegularExpressionValidator(
        asset_variant_regex
    )

    # Assign text validators
    # APB Section
    root_object.line_apb_asset_name.setValidator(asset_name_text_validator)
    root_object.line_apb_variation.setValidator(asset_variant_text_validator)
    # Publish Section
    root_object.line_publish_asset_name.setValidator(asset_name_text_validator)
    root_object.line_publish_variation.setValidator(asset_variant_text_validator)
