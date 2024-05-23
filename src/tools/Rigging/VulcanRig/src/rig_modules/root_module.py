# Copyright (C) 2024 Robert Wiese - All Rights Reserved.
"""Root Rig Module."""

import ast
import logging
import os

# Import PySide modules
from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QSizePolicy,
    QSpacerItem,
    QTreeWidget,
    QVBoxLayout,
)

from maya import cmds

from Core import core_paths as cpath
from Core.ui.UIUtilTools.src import pyside_util_tools as put
from Core.util import maya_colors

from . import module_product_factories
from ..data import module_metadata
from ..data.module_types import ModuleType
from ..data.ue_skeleton_names import EpicBasicSkeleton
from ..controls.control_factory import ControlFactory
from ..util import vulcan_validations

from importlib import reload

reload(module_product_factories)
reload(maya_colors)
reload(vulcan_validations)
reload(module_metadata)
reload(put)

# Current Module root path
MODULE_PATH = f"{cpath.get_parent_directory(__file__, 2)}"

LOG = logging.getLogger(os.path.basename(__file__))


class RootModule(module_product_factories.ModuleProductFactory):
    def __init__(self, vulcan_window: QMainWindow):
        super().__init__(vulcan_window)

        self._current_metadata = module_metadata.RootConfig()
        self.hbox_asset_name: QHBoxLayout
        self.lbl_asset_name: QLabel
        self.txt_asset_name: QLineEdit

    def get_metanode_metadata(self):
        """Get the metanode's metadata.

        Returns:
            ModuleConfig: Dataclass module's metadata.
        """
        metadata_dict = ast.literal_eval(
            cmds.getAttr(
                f"{self._current_metadata.metanode}."
                f"{module_metadata.MetadataAttributes.MODULE_META_ATTRIBUTE.value}"
            )
        )
        return module_metadata.RootConfig(**metadata_dict)

    def build_proxy(self):
        # Skipping proxy for Root as all other modules should be built under this.
        return

    def build_module(self):
        """Create Root nodes and starting proxy joint hierarchy."""
        LOG.info("Building Root module...")
        cmds.undoInfo(chunkName="BuildRootModule_chunk", openChunk=True)

        top_group = cmds.group(empty=True, name="Asset")

        joints_group = cmds.group(empty=True, name="JOINTS_GRP", parent=top_group)
        controls_group = cmds.group(empty=True, name="CONTROLS_GRP", parent=top_group)
        guts_group = cmds.group(empty=True, name="GUTS_GRP", parent=top_group)
        modules_group = cmds.group(empty=True, name="MODULES_GRP", parent=top_group)

        # Create controllers
        # Create orient controller
        control_factory = ControlFactory()
        orient_ctl = control_factory.create_controller(
            "orient", "Orient", parent=controls_group
        )
        # World offset
        offset_ctl = control_factory.create_controller(
            "circle", "WorldOffset", parent=orient_ctl
        )
        cmds.setAttr(f"{offset_ctl}.sx", 5)
        cmds.setAttr(f"{offset_ctl}.sy", 5)
        cmds.setAttr(f"{offset_ctl}.sz", 5)
        cmds.select(offset_ctl, replace=True)
        cmds.makeIdentity(
            apply=True, translate=True, rotate=True, scale=True, normal=False
        )
        # Path Follow offset
        path_follow_ctl = control_factory.create_controller(
            "chevron", "PathFollow", parent=offset_ctl
        )

        # Change color controller
        maya_colors.set_draw_override_color(orient_ctl, "yellow")
        maya_colors.set_draw_override_color(offset_ctl, "yellow")
        maya_colors.set_draw_override_color(path_follow_ctl, "purple")

        # Setup root proxy joints
        cmds.select(clear=True)
        root_joint = cmds.joint(name="root", position=[0, 0, 0])
        cmds.joint(name="interaction", position=[0, 0, 0])
        cmds.select(root_joint, replace=True)
        cmds.joint(name="center_of_mass", position=[0, 0, 0])
        cmds.parent(root_joint, joints_group)

        # Parent existing bind skeleton pelvis to root
        cmds.parent(EpicBasicSkeleton.PELVIS.value, root_joint)

        # Update metadata config
        self.set_module_metadata(module_metadata.RootConfig(metanode="Asset"))

        # Lock all group nodes to prevent renaming or reparenting
        cmds.lockNode(
            [top_group, joints_group, controls_group, guts_group, modules_group]
        )

        cmds.undoInfo(chunkName="BuildRootModule_chunk", closeChunk=True)

        return True

        # TODO: Below contains some final scale and parent constraints to add
        # to all the module groups with the orient control. Probably should do that
        # to the path follow instead.

        # # Parent and scale constrain all module subGroups to orient control and parent modules to rig modules group
        # for mod in allModules:
        #     modGrps = cmds.listRelatives(mod, children=True)
        #     for child in modGrps:
        #         if not "GUTS" in child:
        #             cmds.parentConstraint(orientCtrl, child, maintainOffset=True)
        #             cmds.scaleConstraint(orientCtrl, child, maintainOffset=True)
        #     cmds.parent(mod, rigModulesGrp)

    def build_details_panel(self):
        put.clear_box_layout(self._vulcan_window.root.vb_details)

        metadata = self.get_module_metadata()

        # Build GUI elements for root module
        self.hbox_asset_name = QHBoxLayout()
        self.lbl_asset_name = QLabel("Asset Name:", self._vulcan_window)
        self.txt_asset_name = QLineEdit(self._vulcan_window)
        bottom_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.hbox_asset_name.addWidget(self.lbl_asset_name)
        self.hbox_asset_name.addWidget(self.txt_asset_name)

        self._vulcan_window.root.vb_details.addLayout(self.hbox_asset_name)
        self._vulcan_window.root.vb_details.addItem(bottom_spacer)

        self.txt_asset_name.setText(metadata.asset_name)

        # Setup signals
        self.txt_asset_name.textChanged.connect(self.update_asset_name)

    def update_asset_name(self, new_name: str):
        current_metadata = self.get_metanode_metadata()
        current_metadata.asset_name = new_name
        self.set_module_metadata(current_metadata)
