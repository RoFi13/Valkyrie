# Copyright (C) 2024 Robert Wiese - All Rights Reserved.
"""Spine Rig Module."""

from __future__ import annotations
import ast
import logging
import os
from typing import TYPE_CHECKING

from maya import cmds

from Core import core_paths as cpath
from Core.ui.UIUtilTools.src import pyside_util_tools as put

from Util.UtilTools.src import maya_pyside_interface as mpi

from . import biped_spine_build

from .. import module_product_factories

from Rigging.VulcanRig.src.data.ue_skeleton_names import EpicBasicSkeleton
from Rigging.VulcanRig.src.data import module_metadata, build_options
from Rigging.VulcanRig.src.data.module_types import ModuleType
from Rigging.VulcanRig.src.util import vulcan_utils as vutil

from PySide6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
)

if TYPE_CHECKING:
    from Rigging.VulcanRig.src.vulcan_rig import VulcanRig

from importlib import reload

reload(module_product_factories)
reload(vutil)
reload(biped_spine_build)
reload(build_options)
reload(put)
reload(mpi)
reload(module_metadata)

# Current Module root path
MODULE_PATH = f"{cpath.get_parent_directory(__file__, 2)}"

LOG = logging.getLogger(os.path.basename(__file__))


class BipedSpineModule(module_product_factories.ModuleProductFactory):
    def __init__(
        self,
        vulcan_window: VulcanRig,
        build_instructions: build_options.ModuleBuildOptions,
    ):
        super().__init__(vulcan_window)
        self._vulcan_window = vulcan_window

        self._metadata = module_metadata.BipedSpineConfig(
            module_name=build_instructions.module_stack_item.text(0),
            metanode=build_instructions.module_stack_item.text(0),
            module_type=ModuleType.BIPED_SPINE.name,
        )
        if build_instructions.existing_metadata is not None:
            self._metadata = build_instructions.existing_metadata

        self._module_config_type = module_metadata.BipedSpineConfig
        self._stack_item = build_instructions.module_stack_item
        self._parent_item = build_instructions.parent_stack_item
        self._parent_module = self._vulcan_window.current_modules[self._parent_item]

        self.btn_rename_module: QPushButton
        self.hbox_start_joint: QHBoxLayout
        self.lbl_start_joint: QLabel
        self.txt_start_joint: QLineEdit
        self.btn_grab_start_joint: QPushButton
        self.hbox_end_joint: QHBoxLayout
        self.lbl_end_joint: QLabel
        self.txt_end_joint: QLineEdit
        self.btn_grab_end_joint: QPushButton
        self.btn_build_rig: QPushButton

    def build_proxy(self):
        cmds.undoInfo(chunkName="ProxyBipedSpineModule_chunk", openChunk=True)
        LOG.warning("BUILD SPINE PROXY!")
        # Create Maya top module node
        metadata = self.get_metadata()
        cmds.group(
            empty=True,
            name=metadata.module_name,
            parent=module_metadata.RootOrganizeNodes.MODULES_GRP.value,
        )

        parent_metadata = self._vulcan_window.current_modules[
            self._parent_item
        ].get_metadata()
        parent_metanode = parent_metadata.metanode
        # If parent module is Root Module, then set as no parent
        if hasattr(parent_metadata, "root_modules_group"):
            parent_metanode = ""

        self.set_metadata(
            module_metadata.BipedSpineConfig(
                module_name=metadata.module_name,
                metanode=metadata.module_name,
                parent_metanode=parent_metanode,
                module_type=ModuleType.BIPED_SPINE.name,
            )
        )

        cmds.undoInfo(chunkName="ProxyBipedSpineModule_chunk", closeChunk=True)

    def build_module(self):
        cmds.undoInfo(chunkName="BuildBipedSpineModule_chunk", openChunk=True)

        cmds.undoInfo(chunkName="BuildBipedSpineModule_chunk", closeChunk=True)

    def build_details_panel(self):
        put.clear_box_layout(self._vulcan_window.root.vb_details)

        # TODO: not sure I need this?
        metadata = self.get_metadata()

        # Build GUI elements for root module
        self.btn_rename_module = QPushButton("Rename Module")

        self.hbox_start_joint = QHBoxLayout()
        self.lbl_start_joint = QLabel("Start Joint:", self._vulcan_window)
        self.lbl_start_joint.setMinimumWidth(65)
        self.txt_start_joint = QLineEdit(self._vulcan_window)
        self.txt_start_joint.setEnabled(False)
        self.btn_grab_start_joint = QPushButton("Grab")

        self.hbox_start_joint.addWidget(self.lbl_start_joint)
        self.hbox_start_joint.addWidget(self.txt_start_joint)
        self.hbox_start_joint.addWidget(self.btn_grab_start_joint)

        self.hbox_end_joint = QHBoxLayout()
        self.lbl_end_joint = QLabel("End Joint:", self._vulcan_window)
        self.lbl_end_joint.setMinimumWidth(65)
        self.txt_end_joint = QLineEdit(self._vulcan_window)
        self.txt_end_joint.setEnabled(False)
        self.btn_grab_end_joint = QPushButton("Grab")

        self.hbox_end_joint.addWidget(self.lbl_end_joint)
        self.hbox_end_joint.addWidget(self.txt_end_joint)
        self.hbox_end_joint.addWidget(self.btn_grab_end_joint)

        bottom_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # Add objects to GUI
        self._vulcan_window.root.vb_details.addWidget(self.btn_rename_module)
        self._vulcan_window.root.vb_details.addLayout(self.hbox_start_joint)
        self._vulcan_window.root.vb_details.addLayout(self.hbox_end_joint)

        # Build Options
        lbl_build_options = QLabel("Build Options")
        hline_build_options = put.create_line()

        self.btn_build_rig = QPushButton("Build")

        self._vulcan_window.root.vb_details.addWidget(lbl_build_options)
        self._vulcan_window.root.vb_details.addWidget(hline_build_options)
        self._vulcan_window.root.vb_details.addWidget(self.btn_build_rig)

        self._vulcan_window.root.vb_details.addItem(bottom_spacer)

        self.set_details_panel_defaults()

        # Setup signals
        self.btn_grab_start_joint.clicked.connect(
            lambda: mpi.add_selection_to_textfield(self.txt_start_joint)
        )
        self.btn_grab_end_joint.clicked.connect(
            lambda: mpi.add_selection_to_textfield(self.txt_end_joint)
        )
        self.btn_rename_module.clicked.connect(self.rename_module)
        self.btn_build_rig.clicked.connect(self.generate_spine)

    def generate_spine(self):
        """Build the actual Maya rig system."""
        biped_spine_build.generate_spine_module(
            self.txt_start_joint.text(), self.txt_end_joint.text()
        )

    def set_details_panel_defaults(self):
        """Set Module's detail panel default values."""
        joints_placeholder_text = (
            "Click the Grab button to pick your selected Maya joint."
        )
        self.txt_start_joint.setPlaceholderText(joints_placeholder_text)
        self.txt_end_joint.setPlaceholderText(joints_placeholder_text)

        if cmds.objExists(EpicBasicSkeleton.SPINE_01.value):
            self.txt_start_joint.setText(EpicBasicSkeleton.SPINE_01.value)
        if cmds.objExists(EpicBasicSkeleton.SPINE_05.value):
            self.txt_end_joint.setText(EpicBasicSkeleton.SPINE_05.value)
