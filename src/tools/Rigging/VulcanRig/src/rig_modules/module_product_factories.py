# Copyright (C) 2024 Robert Wiese - All Rights Reserved.
"""Abstract Product Factory classes to help in creating rig controllers."""

from __future__ import annotations
from abc import ABC, abstractmethod
import ast
from dataclasses import asdict
import logging
import os
from typing import List, Type, TYPE_CHECKING

from PySide6.QtWidgets import QMainWindow, QTreeWidgetItem

from maya import cmds

from ..data.module_metadata import MetadataAttributes, ModuleConfig
from ..data.module_types import ModuleType

from Core.ui.UIUtilTools.src import pyside_util_tools as put

if TYPE_CHECKING:
    from Rigging.VulcanRig.src.vulcan_rig import VulcanRig

# from . import controls_util
# from .control_vault import BasicControllerTypes

# from ..data.node_affix_types import RigSideTypes

from importlib import reload

reload(put)

LOG = logging.getLogger(os.path.basename(__file__))


# Abstract Factory
class ModuleProductFactory(ABC):
    def __init__(self, vulcan_window: VulcanRig):
        self._vulcan_window = vulcan_window
        self._metadata: ModuleConfig
        self._module_config_type: ModuleConfig
        self._module_type: ModuleType

        self._stack_item: QTreeWidgetItem
        self._parent_item: QTreeWidgetItem
        self._parent_module: ModuleProductFactory
        self._child_items: List[QTreeWidgetItem] = []
        self._child_modules: List[ModuleProductFactory] = []

        self._module_config_type: ModuleConfig
        self._is_root_module: bool = False

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

    def get_children_names(self) -> List[str]:
        """Get Module's child metanode names."""
        return self.get_metadata().child_metanodes

    def get_children_items(self) -> List[QTreeWidgetItem]:
        """Get Module's child Tree items."""
        return put.get_tree_item_children(self._stack_item)

    def get_children_modules(self) -> List[ModuleProductFactory]:
        """Get Module's child module objects."""
        return self._child_modules

    def add_child(self, child_module: ModuleProductFactory) -> None:
        """Add Child metanode name to Parent's metadata children."""
        # metadata = self.get_metadata()
        if not child_module.get_metadata().metanode in self._metadata.child_metanodes:
            self._metadata.child_metanodes.append(child_module.get_metadata().metanode)
            self.set_metadata(self._metadata)

        # Add Module to this module's child modules
        if not child_module in self._child_modules:
            self._child_modules.append(child_module)

        # Add Module stack item to this module's child items
        if not child_module.get_stack_item() in self._child_items:
            self._child_items.append(child_module.get_stack_item())

    # def remove_child(self, child_name: str) -> bool:
    def remove_child(self, child_module: ModuleProductFactory) -> bool:
        """Remove the child name from the metadata's list of children metanodes."""
        # metadata = self.get_metadata()
        child_name = child_module.get_metadata().metanode
        if child_name not in self._metadata.child_metanodes:
            LOG.debug("Child '%s' doesn't exist in metadata.", child_name)
            return False

        self._metadata.child_metanodes.remove(child_module.get_metadata().metanode)
        self.set_metadata(self._metadata)

        # Remove child item and module objects
        self._child_items.remove(child_module.get_stack_item())
        self._child_modules.remove(child_module)

        return True

    def set_parent_metanode(self, new_parent: ModuleProductFactory) -> None:
        """Set the Module's parent metanode name in metadata."""
        modified_metadata = self.get_metadata()
        modified_metadata.parent_metanode = new_parent.get_metadata().metanode
        self.set_metadata(modified_metadata)
        # Set the new parent module object
        self.set_parent_module(new_parent)

    def get_metanode_metadata(self) -> ModuleConfig:
        """Get the metanode's metadata."""
        metadata_dict = ast.literal_eval(
            cmds.getAttr(
                f"{self._metadata.metanode}."
                f"{MetadataAttributes.MODULE_META_ATTRIBUTE.value}"
            )
        )
        return self._module_config_type(**metadata_dict)

    def set_metadata(self, new_metadata: ModuleConfig) -> None:
        """Set the module's metadata.

        Set both the Tool's GUI module dataclass information and the string version
        on the Module's metanode attribute.

        Args:
            new_metadata (ModuleConfig): New metadata to update to.
        """
        self._metadata = new_metadata
        self._update_metanode_metadata(new_metadata)

    def get_metadata(self) -> ModuleConfig:
        """Get the current module's metadata data class object."""
        return self._metadata

    def rename_module(self) -> bool:
        """Rename the rig module."""
        result = cmds.promptDialog(
            title="Rename Module",
            message="Enter New Name:",
            button=["OK", "Cancel"],
            defaultButton="OK",
            cancelButton="Cancel",
            dismissString="Cancel",
        )
        if result == "Cancel":
            return False

        new_name = cmds.promptDialog(query=True, text=True)

        if cmds.objExists(new_name):
            cmds.error(f"Object with name '{new_name}' already exists.")
            return False

        # Rename Module GUI element
        self._stack_item.setText(0, new_name)

        modified_metadata = self.get_metadata()
        old_name = modified_metadata.metanode

        # Unloack and Rename Maya node
        cmds.lockNode(modified_metadata.metanode, lock=False)
        cmds.rename(modified_metadata.metanode, new_name)
        # Update module's metadata
        modified_metadata.module_name = new_name
        modified_metadata.metanode = new_name
        self.set_metadata(modified_metadata)

        # Update Parent's child name
        self.get_parent_module().update_child_name(new_name, old_name)
        # Update Children's parent name
        self.update_children_parent(new_name)

        # Lock nodes
        cmds.lockNode(new_name)

        return True

    def delete_module(self) -> None:
        """Delete this module and all associated Maya nodes."""
        cmds.lockNode(self._metadata.metanode, lock=False)
        # Remove child name from Parent's children list
        # self._parent_module.remove_child(self._metadata.metanode)
        self._parent_module.remove_child(self)
        # Set the children's parent name in metadata
        for child_module in self._child_modules:
            child_module.set_parent_metanode(self._parent_module)
            self._parent_module.add_child(child_module)

        # Move all children items to the removed item's parent first
        put.move_children_to_parent(self._parent_item, self._stack_item)
        # Delete Maya Node
        cmds.delete(self._metadata.metanode)
        # Remove module item and module object
        put.remove_tree_item(self._stack_item.treeWidget(), self._stack_item)
        del self

    def get_stack_item(self) -> QTreeWidgetItem:
        """Get this module's QTreeWidgetItem from the Tree stack."""
        return self._stack_item

    def set_stack_item(self, new_item: QTreeWidgetItem) -> None:
        """Set the Tree widget stack item associated with this module."""
        self._stack_item = new_item

    def get_parent_item(self) -> QTreeWidgetItem:
        """Get parent item."""
        return self._parent_item

    def set_parent_item(self, new_parent_item: QTreeWidgetItem) -> None:
        """Set the parent item."""
        self._parent_item = new_parent_item

    def get_parent_module(self) -> ModuleProductFactory:
        """Get parent module class object."""
        return self._parent_module

    def set_parent_module(self, new_parent_module: ModuleProductFactory) -> None:
        """Set the parent module class object."""
        self._parent_module = new_parent_module

    def update_child_name(self, new_name: str, old_name: str) -> None:
        """Update child name in metadata only."""
        modified_metadata = self.get_metadata()
        modified_metadata.child_metanodes = [
            new_name if item == old_name else item
            for item in modified_metadata.child_metanodes
        ]

        self.set_metadata(modified_metadata)

    def update_children_parent(self, new_parent: str) -> None:
        """Update all Chilren module's metadata Parent Metanode name."""
        if len(put.get_tree_item_children(self._stack_item)) == 0:
            LOG.debug("No Child items found.")
            return

        for child_item in put.get_tree_item_children(self._stack_item):
            child_module = self._vulcan_window.current_modules[child_item]
            child_module_metadata = child_module.get_metadata()
            child_module_metadata.parent_metanode = new_parent
            child_module.set_metadata(child_module_metadata)

    def _update_metanode_metadata(self, new_metadata: ModuleConfig) -> bool:
        """Set the Module's metadata on module's designated node."""
        metanode_object = self._metadata.metanode
        if not cmds.objExists(metanode_object):
            LOG.error("Module's metadata node could not be found!")
            return False

        if not cmds.attributeQuery(
            MetadataAttributes.MODULE_META_ATTRIBUTE.value,
            node=self._metadata.metanode,
            exists=True,
        ):
            cmds.addAttr(
                metanode_object,
                longName=MetadataAttributes.MODULE_META_ATTRIBUTE.value,
                dataType="string",
            )

        # Unlock and Set the new metadata and relock
        cmds.lockNode(metanode_object, lock=False)
        cmds.setAttr(
            f"{metanode_object}.{MetadataAttributes.MODULE_META_ATTRIBUTE.value}",
            lock=False,
        )
        cmds.setAttr(
            f"{metanode_object}.{MetadataAttributes.MODULE_META_ATTRIBUTE.value}",
            str(asdict(new_metadata)),
            type="string",
            lock=True,
        )
        cmds.lockNode(metanode_object)

        return True
