# Copyright (C) 2023 Robert Wiese - All Rights Reserved.
"""Vulcan Metadata controller class."""

# from __future__ import annotations
from dataclasses import dataclass, field, fields
from enum import Enum
import logging
import os
from typing import Any, List

from maya import cmds

from Core import core_paths as cpath

# from . import gui_factories
# from ..rig_modules import module_factory
# from ..data.module_types import ModuleType

from importlib import reload


# Current Module root path
MODULE_PATH = f"{cpath.get_parent_directory(__file__, 2)}"

LOG = logging.getLogger(os.path.basename(__file__))


class MetadataAttributes(Enum):
    """Any metadata attribute names commonly used by the tool."""

    MODULE_META_ATTRIBUTE = "vulcan_metadata"  # Core module metadata attribute name


class RootOrganizeNodes(Enum):
    """Root Organization Maya node names."""

    JOINTS_GRP = "JOINTS_GRP"
    CONTROLS_GRP = "CONTROLS_GRP"
    GUTS_GRP = "GUTS_GRP"
    MODULES_GRP = "MODULES_GRP"


@dataclass
class ModuleConfig:
    metanode: str = ""
    parent_metanode: str = ""
    child_metanodes: List[str] = field(default_factory=list)


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


# TODO: Deprecated probably. Just update the attribute in the module itself.
def update_config_field(data_instance: ModuleConfig, field_name: str, new_value: Any):
    # Retrieve the field object from the dataclass
    field_info = {f.name: f for f in fields(data_instance)}
    if field_name not in field_info:
        raise ValueError(f"Field '{field_name}' does not exist in the dataclass.")

    # Get the expected type from the field's type annotation
    expected_type = field_info[field_name].type

    # Check if the new value is of the expected type
    if not isinstance(new_value, expected_type):
        raise TypeError(
            f"Type mismatch: '{field_name}' expects {expected_type}, but got "
            f"{type(new_value).__name__}"
        )
    setattr(data_instance, field_name, new_value)

    return data_instance


def convert_dict_to_dataclass(metadata: dict, subclass_type: ModuleConfig):
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
