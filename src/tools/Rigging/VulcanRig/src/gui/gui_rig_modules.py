# Copyright (C) 2024 Robert Wiese - All Rights Reserved.
"""GUI Rig Module classes."""
# Can't find PySide2 modules pylint: disable=I1101

from abc import ABC, abstractmethod
import logging
import os

# Import PySide modules
from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QSpacerItem,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from Core import core_paths as cpath
from Core.ui.UIUtilTools.src import pyside_util_tools as put
from Core.ui.UIUtilTools.src import pyside_styling_util as pstyle

from ..data.module_types import ModuleType, ModuleSide

from maya import cmds

from importlib import reload

reload(put)
reload(pstyle)

# Current Module root path
MODULE_PATH = f"{cpath.get_parent_directory(__file__, 2)}"

# Full path to where .ui files are stored
RSRC_PATH = f"{MODULE_PATH}/resources"

LOG = logging.getLogger(os.path.basename(__file__))


# Base Module class
class ModuleProduct(ABC):
    """Base Module Product for individual Rig objects.

    Args:
        ABC (ABC): Abstractor helper class.
    """

    def __init__(
        self,
        details_box: QVBoxLayout,
        module_details: dict,
        stack_item_widget: QTreeWidgetItem,
    ):
        self._details_box = details_box
        self._label = module_details["label"]
        self._module_type = module_details["module_type"]
        self._side = module_details["side"]
        self._stack_item_widget = stack_item_widget

    @abstractmethod
    def update_details_panel(self):
        """Update details panel of Vulcan tool."""

    @abstractmethod
    def _build_proxy(self):
        """Build/Rebuild Proxy."""

    @abstractmethod
    def _build_rig_module(self):
        """Build Maya Rig module objects."""

    @abstractmethod
    def _toggle_proxy_visibility(self, new_state: bool):
        """Toggle proxy objects visibility."""

    def get_module_type(self):  # No public setting of module type
        """Get this Product's Module type.

        Returns:
            ModuleType: The Module type.
        """
        return self._module_type

    def get_module_label(self):
        """Get this Product's Module label/name.

        Returns:
            str: Current label/name of this module.
        """
        return self._label

    def set_module_label(self, new_name: str):
        """Set this Product's Module label/name.

        Args:
            new_name (str): New name for Module.
        """
        self._label = new_name

    def get_module_side(self):
        """Get this Product's Module side e.g. Center, Left, Right.

        Returns:
            ModuleSide: Module's assigned side.
        """
        return self._side

    def set_module_side(self, new_side: ModuleSide):
        """Set this Product's Module side e.g. Center, Left, Right.

        Args:
            new_side (ModuleSide): Which side to set this Module to.
        """
        self._side = new_side


class RootProduct(ModuleProduct):
    """Product for Root Rig Controls.

    Args:
        ModuleProduct (ModuleProduct): Parent factory class.
    """

    def update_details_panel(self):
        LOG.debug("Updating module details panel...")
        LOG.debug("Details Box: %s", self._details_box)
        LOG.debug("Label: %s", self._label)
        LOG.debug("Module Type: %s", self._module_type)
        LOG.debug("Side: %s", self._side)
        LOG.debug("Stack Item Widget: %s", self._stack_item_widget)

    def _build_proxy(self):
        """Build/Rebuild Proxy."""
        LOG.debug("Building proxy %s proxy module...", self._module_type)

    def _build_rig_module(self):
        """Build Maya Rig module objects."""
        LOG.debug("Building Maya rig objects for %s...", self._label)

    def _toggle_proxy_visibility(self, new_state: bool):
        """Toggle proxy objects visibility."""
        LOG.debug("Toggle module visibility...")


class BipedSpineProduct(ModuleProduct):
    """Product for Spine Rig Controls.

    Args:
        ModuleProduct (ModuleProduct): Parent factory class.
    """

    def update_details_panel(self):
        LOG.debug("Updating module details panel...")
        LOG.debug("Details Box: %s", self._details_box)
        LOG.debug("Label: %s", self._label)
        LOG.debug("Module Type: %s", self._module_type)
        LOG.debug("Side: %s", self._side)
        LOG.debug("Stack Item Widget: %s", self._stack_item_widget)

    def _build_proxy(self):
        """Build/Rebuild Proxy."""
        LOG.debug("Building proxy %s proxy module...", self._module_type)

    def _build_rig_module(self):
        """Build Maya Rig module objects."""
        LOG.debug("Building Maya rig objects for %s...", self._label)

    def _toggle_proxy_visibility(self, new_state: bool):
        """Toggle proxy objects visibility."""
        LOG.debug("Toggle module visibility...")

        # rigName = lineRigName.text()

        # rigJoints = cmds.ls(selection=True)[0]
        # allModules = cmds.ls(selection=True)[1:]
        # if not cmds.objectType(rigJoints, isType="joint"):
        #     cmds.error(
        #         "Please select your rig hierarchy first then all other rig modules."
        #     )
        # # Create orient controller
        # orientCtrl = rc.createCircleCtrl("orient_CTL")

        # # Create final rig organization nodes
        # rigGrp = cmds.group(empty=True, name="%s_RIG" % rigName)
        # rigJointsGrp = cmds.group(empty=True, name="JOINTS_GRP", parent=rigGrp)
        # rigControlsGrp = cmds.group(empty=True, name="CONTROLS_GRP", parent=rigGrp)
        # rigGutsGrp = cmds.group(empty=True, name="GUTS_GRP", parent=rigGrp)
        # rigModulesGrp = cmds.group(empty=True, name="MODULES_GRP", parent=rigGrp)
        # # Parent orient to rig controls group; parent rig joint hierarchy to rig joint group
        # cmds.parent(orientCtrl, rigControlsGrp)
        # cmds.parent(rigJoints, rigJointsGrp)
        # # Parent and scale constrain all module subGroups to orient control and parent modules to rig modules group
        # for mod in allModules:
        #     modGrps = cmds.listRelatives(mod, children=True)
        #     for child in modGrps:
        #         if not "GUTS" in child:
        #             cmds.parentConstraint(orientCtrl, child, maintainOffset=True)
        #             cmds.scaleConstraint(orientCtrl, child, maintainOffset=True)
        #     cmds.parent(mod, rigModulesGrp)
