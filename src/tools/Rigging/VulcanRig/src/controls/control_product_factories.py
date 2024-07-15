# Copyright (C) 2024 Robert Wiese - All Rights Reserved.
"""Product Abstract Factory classes to help in creating rig controllers."""

from abc import ABC, abstractmethod
import logging
import os

from maya import cmds

from . import control_util
from .control_vault import BasicControllerTypes

from ..data.node_affix_types import MayaSuffixTypes, RigSideTypes


from importlib import reload

# reload(BasicControllerTypes)
reload(control_util)

LOG = logging.getLogger(os.path.basename(__file__))


# Abstract Products
class SimpleControlProduct(ABC):
    """Simple Control Product factory."""

    @abstractmethod
    def create(
        self,
        control_type: BasicControllerTypes,
        control_name: str = None,
        side: RigSideTypes = RigSideTypes.CENTER,
    ):
        """Create the Rig Control curve."""
        raise NotImplementedError("You should implement this method")

    def _fix_control_name(self, side: RigSideTypes, control_name: str = None):
        """Fix control name to something unique."""
        if control_name is None:
            control_name = self.default_name

        if MayaSuffixTypes.CONTROL.value not in control_name:
            control_name = control_util.validate_name(
                f"{side.value}_{control_name}_{MayaSuffixTypes.CONTROL.value}"
            )
        else:
            control_name = control_util.validate_name(f"{side.value}_{control_name}")

        return control_name


class ComplexControlProduct(ABC):
    """Complex Control Product factory."""

    @abstractmethod
    def __init__(self):
        """Complex Control Product initialization."""
        raise NotImplementedError("You should implement this method")

    @abstractmethod
    def create(
        self, control_name: str = None, side: RigSideTypes = RigSideTypes.CENTER
    ):
        """Create the Rig Control curve."""
        raise NotImplementedError("You should implement this method")

    def _fix_control_name(self, side: RigSideTypes, control_name: str = None):
        """Fix control name to something unique."""
        if control_name is None:
            control_name = self.default_name

        if MayaSuffixTypes.CONTROL.value not in control_name:
            control_name = control_util.validate_name(
                f"{side.value}_{control_name}_{MayaSuffixTypes.CONTROL.value}"
            )
        else:
            control_name = control_util.validate_name(f"{side.value}_{control_name}")

        return control_name

    def combine_shape_nodes(self, selection: list):
        """Combine multiple shape nodes into one.

        Args:
            selection (list): List of Maya object names to query shape nodes from and
                combine.

        Returns:
            str: New Maya Object name.
        """
        new_control = cmds.group(empty=True)

        # Grab selection, freeze transforms, and delete history
        cmds.select(selection, replace=True)
        cmds.makeIdentity(
            apply=True, translate=True, rotate=True, scale=True, normal=False
        )
        cmds.delete(constructionHistory=True)

        for curve in selection:
            # Grab shape nodes of selection
            object_shape_nodes = cmds.listRelatives(curve, shapes=True)
            for shape_node in object_shape_nodes:
                cmds.parent(shape_node, new_control, add=True, shape=True)

        cmds.delete(selection)

        return new_control

    def fix_shape_node_names(self, new_control: str):
        """Fix the shape node names of the new control so they are unique.

        Names them after their parent transform node in the following format:

        <new_control_name>Shape#

        Args:
            new_control (str): New unique control name.
        """
        object_shape_nodes = cmds.listRelatives(new_control, shapes=True)
        for shape in object_shape_nodes:
            new_shape_name = f"{new_control}Shape"
            shape_num = 1
            while shape_num < 9999:
                if not cmds.objExists(new_shape_name):
                    break
                new_shape_name = f"{new_control}Shape{shape_num}"
                shape_num += 1

            cmds.rename(shape, new_shape_name)
