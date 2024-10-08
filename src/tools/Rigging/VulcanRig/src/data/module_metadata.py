# Copyright (C) 2024 Robert Wiese - All Rights Reserved.
"""Vulcan Metadata controller class."""

# from __future__ import annotations
from dataclasses import dataclass, field, fields
from enum import Enum
import logging
import os
from typing import Any, List

from maya import cmds

from Core import core_paths as cpath

from .module_types import ModuleType

from importlib import reload


# Current Module root path
MODULE_PATH = f"{cpath.get_parent_directory(__file__, 2)}"

LOG = logging.getLogger(os.path.basename(__file__))


class MetadataAttributes(Enum):
    """Any metadata attribute names commonly used by the tool."""

    MODULE_META_ATTRIBUTE = "vulcan_metadata"  # Core module metadata attribute name


class RootOrganizeNodes(Enum):
    """Root Organization Maya node names."""

    DEFAULT_TOP_NODE = "Asset"
    JOINTS_GRP = "JOINTS_GRP"
    CONTROLS_GRP = "CONTROLS_GRP"
    GUTS_GRP = "GUTS_GRP"
    MODULES_GRP = "MODULES_GRP"


@dataclass
class ModuleConfig:
    metanode: str = ""
    parent_metanode: str = ""
    child_metanodes: List[str] = field(default_factory=list)
    module_type: str = ""


@dataclass
class RootConfig(ModuleConfig):
    asset_name: str = ""
    root_joints_group: str = RootOrganizeNodes.JOINTS_GRP.value
    root_controls_group: str = RootOrganizeNodes.CONTROLS_GRP.value
    root_guts_group: str = RootOrganizeNodes.GUTS_GRP.value
    root_modules_group: str = RootOrganizeNodes.MODULES_GRP.value


@dataclass
class BipedSpineConfig(ModuleConfig):
    module_name: str = ""


def convert_dict_to_dataclass(
    metadata: dict, subclass_type: ModuleConfig
) -> ModuleConfig:
    """Try to convert dictionary data to specific Vulcan dataclass type.

    Args:
        metadata (dict): Metadata structure to check.
        subclass_type (ModuleConfig): Which dataclass to equate to.

    Returns:
        ModuleConfig: Returns instantiated data class object if
            successful. Otherwise, returns None.
    """
    new_dataclass: ModuleConfig
    try:
        new_dataclass = subclass_type(**metadata)
    except TypeError:
        LOG.debug("Module's metadata isn't of type %s.", type(subclass_type))
        return None

    return new_dataclass
