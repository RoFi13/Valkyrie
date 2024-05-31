# Copyright (C) 2024 Robert Wiese - All Rights Reserved.
"""Helper build option data classes and Enums."""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import logging
import os

from PySide6.QtWidgets import QTreeWidgetItem

from Core import core_paths as cpath

from .module_types import ModuleType
from . import module_metadata

from importlib import reload

reload(module_metadata)


# Current Module root path
MODULE_PATH = f"{cpath.get_parent_directory(__file__, 2)}"

LOG = logging.getLogger(os.path.basename(__file__))


class MetadataAttributes(Enum):
    """Any metadata attribute names commonly used by the tool."""

    MODULE_META_ATTRIBUTE = "vulcan_metadata"  # Core module metadata attribute name


class ModuleBuildMethod(Enum):
    """Module building options."""

    BUILD_PROXY = 0
    BUILD_MAYA = 1
    BUILD_INTERNAL = 2


@dataclass
class ModuleBuildOptions:
    build_method: ModuleBuildMethod = ModuleBuildMethod.BUILD_PROXY
    module_stack_item: QTreeWidgetItem = None
    parent_stack_item: QTreeWidgetItem = None
    module_type: ModuleType = None
    existing_metadata: module_metadata.ModuleConfig = None
