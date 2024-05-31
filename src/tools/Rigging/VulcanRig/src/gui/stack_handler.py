# Copyright (C) 2023 Robert Wiese - All Rights Reserved.
"""Stack Handler for handling command requests."""
# Can't find PySide2 modules pylint: disable=I1101

from __future__ import annotations
import ast
import logging
import os
from typing import TYPE_CHECKING

from maya import cmds

# Import PySide modules
from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QMainWindow, QTreeWidget, QTreeWidgetItem

from Core import core_paths as cpath
from Core.ui.UIUtilTools.src import pyside_util_tools as put

from . import gui_factories
from . import module_stack_util as msu
from ..data import build_options, module_metadata
from ..data.module_types import ModuleType
from ..rig_modules import module_factory, module_product_factories
from ..util import vulcan_validations
from ..util import metadata_utils

if TYPE_CHECKING:
    from ..vulcan_rig import VulcanRig

from importlib import reload

reload(gui_factories)
reload(put)
reload(build_options)
reload(module_metadata)
reload(msu)
reload(module_factory)
reload(module_product_factories)
reload(vulcan_validations)

# Current Module root path
MODULE_PATH = f"{cpath.get_parent_directory(__file__, 2)}"

LOG = logging.getLogger(os.path.basename(__file__))


def initialize_scene(
    vulcan_window: VulcanRig, stack_factory: gui_factories.StackFactory
) -> None:

    # Find the root module first
    all_transforms = cmds.ls(type="transform")
    root_meta_attribute = module_metadata.MetadataAttributes.MODULE_META_ATTRIBUTE.value
    root_module_data: module_metadata.RootConfig = None
    for node in all_transforms:
        if cmds.attributeQuery(root_meta_attribute, node=node, exists=True):
            node_metadata = ast.literal_eval(
                cmds.getAttr(f"{node}.{root_meta_attribute}")
            )
            root_module_data = module_metadata.convert_dict_to_dataclass(
                node_metadata, module_metadata.RootConfig
            )
            break

    if root_module_data is None:
        LOG.info("No Root Module metadata found in scene.")
        return

    # Found the root module, recreating the GUI elements in the stack
    root_item = stack_factory.create_stack_module(ModuleType.ROOT)

    build_instructions = build_options.ModuleBuildOptions(
        build_method=build_options.ModuleBuildMethod.BUILD_PROXY,
        module_stack_item=root_item,
        module_type=ModuleType.ROOT,
        existing_metadata=root_module_data,
    )

    # Create module product class object without creating new Maya objects
    root_module = vulcan_window.module_factory.create_module(build_instructions)
    root_module.set_metadata(root_module_data)
    vulcan_window.current_modules[root_item] = root_module

    if len(root_module_data.child_metanodes) == 0:
        LOG.info("No children metanodes found!")
        return

    LOG.warning("root module metadata: %s", root_module_data)
    LOG.warning("root module metadata type: %s", type(root_module_data))

    generate_stack_children(vulcan_window, root_module)


def generate_stack_children(
    vulcan_window: VulcanRig,
    parent_module: module_product_factories.ModuleProductFactory,
) -> None:
    LOG.info("Building Stack modules...")
    meta_attribute = module_metadata.MetadataAttributes.MODULE_META_ATTRIBUTE.value
    parent_metadata = parent_module.get_metadata()
    for child_name in parent_metadata.child_metanodes:
        # Get Maya node metadata as dictionary
        node_metadata = ast.literal_eval(cmds.getAttr(f"{child_name}.{meta_attribute}"))
        # Match to the correct module type and generate module without building proxy
        # or Maya module. Just GUI and class objects.
        # TODO: Populate this match casing to include all other modules
        # TODO: Can this match case be pushed into a function that determines which
        # type of module type and config to use?
        match node_metadata["module_type"]:
            case ModuleType.BIPED_SPINE.name:
                module_config = module_metadata.convert_dict_to_dataclass(
                    node_metadata, module_metadata.BipedSpineConfig
                )
                # Metadata much match a known config data class
                if module_config is None:
                    continue
                # Generate new child top item
                new_module = generate_module(
                    ModuleType.BIPED_SPINE,
                    vulcan_window,
                    False,
                    parent_module.get_stack_item(),
                    module_config,
                )
                parent_module.add_child(new_module)
                # Generate top item's children recursively
                generate_stack_children(vulcan_window, new_module)


def generate_module(
    module_type: ModuleType,
    vulcan_window: VulcanRig,
    new_module: bool = True,
    existing_parent_item: QTreeWidgetItem = None,
    existing_metadata: module_metadata.ModuleConfig = None,
) -> module_product_factories.ModuleProductFactory:
    """Handle Module button click.

    Should initiate the creation of GUI elements specific to the clicked module.
    """
    if not vulcan_validations.validate_bind_skeleton():
        return None

    # Get Parent module in order to add the newly created module as a child
    parent_item: QTreeWidgetItem = None
    if (
        vulcan_window.tree_stack.currentItem() is None
        and not module_type == ModuleType.ROOT
    ):
        parent_item = msu.find_all_modules_of_type(
            vulcan_window.tree_stack, ModuleType.ROOT
        )[0]
    else:
        parent_item = vulcan_window.tree_stack.currentItem()

    if parent_item is None and not module_type == ModuleType.ROOT:
        LOG.error(
            "No Root Module or selected module found. Please create the Root module or "
            "select another module as a parent module."
        )
        return None

    if existing_parent_item is not None:
        parent_item = existing_parent_item

    # Create new GUI item in tree
    new_module_item = vulcan_window.gui_stack_factory.create_stack_module(
        module_type, parent_item, existing_metadata
    )

    if new_module_item is None:
        LOG.error("New Module failed to be created...")
        return None

    build_instructions = build_options.ModuleBuildOptions(
        build_method=build_options.ModuleBuildMethod.BUILD_PROXY,
        module_stack_item=new_module_item,
        parent_stack_item=parent_item,
        module_type=module_type,
        existing_metadata=existing_metadata,
    )
    if module_type == ModuleType.ROOT:
        build_instructions.build_method = build_options.ModuleBuildMethod.BUILD_MAYA

    if not new_module:
        build_instructions.build_method = build_options.ModuleBuildMethod.BUILD_INTERNAL

    # Add associated new product module object
    new_module_object = vulcan_window.module_factory.create_module(build_instructions)
    vulcan_window.current_modules[new_module_item] = new_module_object

    # Update metanode relationships with new module
    new_module_object.set_parent_metanode(vulcan_window.current_modules[parent_item])
    vulcan_window.current_modules[parent_item].add_child(new_module_object)

    # Select the new item
    vulcan_window.tree_stack.setCurrentItem(new_module_item)
    new_module_object.build_details_panel()

    LOG.debug("All current modules: %s", vulcan_window.current_modules)

    return new_module_object
