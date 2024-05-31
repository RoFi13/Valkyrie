# Copyright (C) 2023 Robert Wiese - All Rights Reserved.
"""Various Vulcan metadata utility functions."""

from __future__ import annotations
from dataclasses import dataclass, field
import logging
import os
from typing import TYPE_CHECKING

from PySide6.QtWidgets import QTreeWidgetItem

from maya import cmds

from Core import core_paths as cpath

from ..rig_modules.module_product_factories import ModuleProductFactory

# from . import gui_factories
# from ..rig_modules import module_factory
# from ..data.module_types import ModuleType

if TYPE_CHECKING:
    from ..vulcan_rig import VulcanRig

from importlib import reload

# Current Module root path
MODULE_PATH = f"{cpath.get_parent_directory(__file__, 2)}"

LOG = logging.getLogger(os.path.basename(__file__))
