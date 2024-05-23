# Copyright (C) 2023 Robert Wiese - All Rights Reserved.
"""Maya Rig Module Factories."""
# Can't find PySide2 modules pylint: disable=I1101

from abc import ABC, abstractmethod
import logging
import os

from maya import cmds

# # Import PySide modules
# from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QMainWindow

from Core import core_paths as cpath

from .module_product_factories import ModuleProductFactory
from . import root_module
from .biped_modules import biped_spine_module
from ..data.module_metadata import ModuleConfig
from ..data.module_types import ModuleType

from importlib import reload

reload(root_module)
reload(biped_spine_module)

# Current Module root path
MODULE_PATH = f"{cpath.get_parent_directory(__file__, 2)}"

LOG = logging.getLogger(os.path.basename(__file__))


# Abstract factory
class AbstractModuleFactory(ABC):
    def __init__(self, vulcan_window: QMainWindow):
        self._vulcan_window = vulcan_window

    @abstractmethod
    def create_module(self, module_type: ModuleType):
        """Build the proxy module.

        Args:
            module_type (ModuleType): Module type to create.

        Raises:
            NotImplementedError: Raised if abstract method isn't created.
        """
        raise NotImplementedError("You should implement this method")


# Concrete Factory
class ModuleFactory(AbstractModuleFactory):
    def create_module(
        self,
        module_type: ModuleType,
        module_name: str = "",
        build_maya_module: bool = False,
    ) -> ModuleProductFactory:
        LOG.warning("Creating module for type: '%s'.", module_type)

        new_module: ModuleProductFactory
        match module_type:
            case ModuleType.ROOT:
                new_module = root_module.RootModule(self._vulcan_window)

            case ModuleType.BIPED_SPINE:
                new_module = biped_spine_module.BipedSpineModule(
                    self._vulcan_window, module_name
                )

        if build_maya_module:
            new_module.build_module()

        return new_module
