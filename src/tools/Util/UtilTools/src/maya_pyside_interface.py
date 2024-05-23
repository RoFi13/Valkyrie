# Copyright Robert Wiese 2024 - All Rights Reserved.
"""Functions for various Maya and PySide interface operations."""

import logging
import os

from PySide6.QtWidgets import QLabel, QLineEdit


from maya import cmds

LOG = logging.getLogger(os.path.basename(__file__))


def add_selection_to_textfield(text_field: QLineEdit):
    text_field.setText(cmds.ls(selection=True)[0])
