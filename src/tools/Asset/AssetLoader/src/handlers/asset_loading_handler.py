"""Asset loading handler functions."""

# Can't find PySide6 modules pylint: disable=I1101

from __future__ import annotations
import logging
import os

from maya import cmds

from Core import core_paths as cpath

from Util.UtilTools.src import outliner_utils


# Main paths
MAIN_PATHS = cpath.core_paths()

# Current Module root path
MODULE_PATH = f"{cpath.get_parent_directory(__file__, 2)}"

# Full path to where resource files are stored
RSRC_PATH = f"{MODULE_PATH}/resources"
NO_PREVIEW_IMAGE_PATH = f"{RSRC_PATH}/images/No_preview.png"
ASSET_WIDGET_UI_PATH = f"{RSRC_PATH}/ui/asset_widget.ui"

LOG = logging.getLogger(os.path.basename(__file__))


def reference_asset(
    asset_category: str,
    asset_file_path: str,
    load_namespace: str,
    load_count: int,
    organize: bool = False,
) -> bool:
    if not os.path.exists(asset_file_path):
        LOG.error("Asset file path invalid at: %s", asset_file_path)
        return False

    for _ in range(load_count):
        new_nodes = cmds.file(
            asset_file_path,
            ignoreVersion=True,
            mergeNamespacesOnClash=False,
            groupLocator=True,
            namespace=load_namespace,
            options="v=0",
            preserveReferences=True,
            returnNewNodes=True,
            r=True,
        )
        if organize:
            organize_loaded_asset(asset_category, new_nodes)

    return True


def import_asset(
    asset_category: str,
    asset_file_path: str,
    load_namespace: str,
    load_count: int,
    organize: bool = False,
) -> bool:
    if not os.path.exists(asset_file_path):
        LOG.error("Asset file path invalid at: %s", asset_file_path)
        return False

    for _ in range(load_count):
        new_nodes = cmds.file(
            asset_file_path,
            ignoreVersion=True,
            mergeNamespacesOnClash=False,
            groupLocator=True,
            namespace=load_namespace,
            options="v=0",
            preserveReferences=True,
            returnNewNodes=True,
            i=True,
        )
        if organize:
            organize_loaded_asset(asset_category, new_nodes)

    return True


def organize_loaded_asset(imported_asset_category: str, imported_nodes: list) -> None:
    """Parent top node of imported Asset into Asset Category group node.

    Important: For this function to work, the imported/referenced Asset must be a
    published asset from the Asset Manager tool. It is expecting that there is a single
    top node for all nodes within the imported file that is either named "asset" or
    "rig".
    """
    # Get namespace that maya assigned to new asset
    assigned_namespace = imported_nodes[0].split(":")[0].upper()
    top_node = f"{assigned_namespace}:rig"
    asset_node = f"{assigned_namespace}:asset"
    if cmds.objExists(asset_node):
        if cmds.listRelatives(asset_node, parent=True) is None:
            top_node = asset_node

    # Make sure outliner has top organizational group nodes
    outliner_utils.create_shot_tree()

    match imported_asset_category:
        case "characters":
            cmds.parent(top_node, "CHAR")
        case "creatures":
            cmds.parent(top_node, "CRE")
        case "environments":
            cmds.parent(top_node, "ENV")
        case "fx":
            cmds.parent(top_node, "FX")
        case "gami":
            cmds.parent(top_node, "GAMI")
        case "props":
            cmds.parent(top_node, "PROP")
        case "vehicles":
            cmds.parent(top_node, "VEH")
