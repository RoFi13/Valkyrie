# Copyright (C) 2023 Robert Wiese - All Rights Reserved.
"""Stack Handler for handling command requests."""
# Can't find PySide2 modules pylint: disable=I1101

import logging
import os

# Import PySide modules
from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QMainWindow, QTreeWidget

from Core import core_paths as cpath
from Core.ui.UIUtilTools.src import pyside_util_tools as put

from . import gui_factories
from . import module_stack_util as msu
from ..data.module_types import ModuleType
from ..rig_modules import module_factory, module_product_factories
from ..util import vulcan_validations

from importlib import reload

reload(gui_factories)
reload(put)
reload(msu)
reload(module_factory)
reload(module_product_factories)
reload(vulcan_validations)

# Current Module root path
MODULE_PATH = f"{cpath.get_parent_directory(__file__, 2)}"

LOG = logging.getLogger(os.path.basename(__file__))


def handle_module_click(
    stack_widget: QTreeWidget, module_type: ModuleType, vulcan_window: QMainWindow
) -> None:
    """Handle Module button click.

    Should initiate the creation of GUI elements specific to the clicked module.

    Args:
        stack_widget (QTreeWidget): Parent Stack Tree Widget to add GUI elements to.
        module_type (ModuleType): Type of Module to create.
        details_panel (QVBoxLayout): Where to generate detail UI elements about the
            newly created module.
    """
    if not vulcan_validations.validate_bind_skeleton():
        return False

    # Get Parent module in order to add the newly created module as a child
    # TODO: need to rethink how to set/get parent and child modules in metadata
    parent_module: module_product_factories.ModuleProductFactory
    if vulcan_window.root.tree_module_stack.currentItem() is None:
        parent_module = msu.find_all_modules_of_type(
            stack_widget, ModuleType.ROOT, True
        )[0]
    else:
        parent_module = vulcan_window.current_modules[
            vulcan_window.root.tree_module_stack.currentItem()
        ]

    # Create new GUI item in tree
    new_module_item = vulcan_window.gui_stack_factory.create_stack_module(module_type)

    if new_module_item is None:
        LOG.error("New Module failed to be created...")
        return False

    # Add new module GUI item and its associated new product module object
    vulcan_window.current_modules[new_module_item] = (
        vulcan_window.module_factory.create_module(module_type, new_module_item.text(0))
    )

    # Select the new item
    vulcan_window.root.tree_module_stack.setCurrentItem(new_module_item)
    vulcan_window.current_modules[new_module_item].build_details_panel()

    LOG.warning("All current modules: %s", vulcan_window.current_modules)

    # Add interface? when clicking item to populate details panel of current nodes

    # biped_factory.create_biped_stack_module(module_type)

    # TODO: Add Quadruped factory creation here...
