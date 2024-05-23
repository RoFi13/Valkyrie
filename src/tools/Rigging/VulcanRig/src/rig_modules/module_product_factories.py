# Copyright (C) 2024 Robert Wiese - All Rights Reserved.
"""Abstract Product Factory classes to help in creating rig controllers."""

from abc import ABC, abstractmethod
import ast
from dataclasses import asdict
import logging
import os

from PySide6.QtWidgets import QMainWindow

from maya import cmds

from ..data.module_metadata import MetadataAttributes, ModuleConfig

# from . import controls_util
# from .control_vault import BasicControllerTypes

# from ..data.node_affix_types import RigSideTypes

from importlib import reload

LOG = logging.getLogger(os.path.basename(__file__))


# Abstract Factory
class ModuleProductFactory(ABC):
    def __init__(self, vulcan_window: QMainWindow):
        self._vulcan_window = vulcan_window
        self._current_metadata: ModuleConfig

    @abstractmethod
    def build_proxy(self):
        """Build the module's Maya proxy nodes."""
        raise NotImplementedError("You should implement this method")

    @abstractmethod
    def build_module(self):
        """Build the module's Maya rig nodes."""
        raise NotImplementedError("You should implement this method")

    @abstractmethod
    def build_details_panel(self):
        """Replace and build the Details Panel area to this specific Module's needs."""
        raise NotImplementedError("You should implement this method")

    @abstractmethod
    def get_metanode_metadata(self):
        """Get the metanode's metadata."""
        raise NotImplementedError("You should implement this method")

    def set_module_metadata(self, new_metadata: ModuleConfig):
        """Set the module's metadata.

        Set both the Tool's GUI module dataclass information and the string version
        on the Module's metanode attribute.

        Args:
            new_metadata (ModuleConfig): New metadata to update to.
        """
        self._current_metadata = new_metadata
        self._update_metanode_metadata(new_metadata)

    def get_module_metadata(self):
        """Get the current module's metadata data class object.

        Returns:
            ModuleConfig: Data class for module metadata.
        """
        return self._current_metadata

    def _update_metanode_metadata(self, new_metadata: ModuleConfig):
        """Set the Module's metadata on module's designated node.

        Args:
            new_metadata (dict): New metadata to apply to node's attribute.

        Raises:
            NotImplementedError: Raised if abstract method isn't created.
        """
        metanode_object = self._current_metadata.metanode
        if not cmds.objExists(metanode_object):
            LOG.error("Module's metadata node could not be found!")
            return False

        if not cmds.attributeQuery(
            MetadataAttributes.MODULE_META_ATTRIBUTE.value,
            node=self._current_metadata.metanode,
            exists=True,
        ):
            cmds.addAttr(
                metanode_object,
                longName=MetadataAttributes.MODULE_META_ATTRIBUTE.value,
                dataType="string",
            )

        # Set the new metadata
        cmds.setAttr(
            f"{metanode_object}.{MetadataAttributes.MODULE_META_ATTRIBUTE.value}",
            str(asdict(new_metadata)),
            type="string",
        )

        return True
