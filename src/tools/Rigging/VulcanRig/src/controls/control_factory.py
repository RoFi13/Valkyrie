# Copyright (C) 2024 Robert Wiese - All Rights Reserved.
"""Controller Factory classes to help in creating rig controllers.

When adding new controls, you must do a couple small things. But first let's define
the difference between a Basic Control and a Complex Control.

Basic Controls are any controller that can be created with a single nurbs curve that
doesn't require the start and end points to be connected. They can visually connect,
but they must be able to be built with the curve command by passing in the CV points.

Complex Controls are any controller that could involve multiple curve shape nodes
into one control or in taking a Basic Control and modifying it with extra steps.

After you've determined what kind of control you'd like to add to the factory, you must
do a couple things depending on the control.

Basic Controls:
1. Add the CV points into the BasicControllerTypes Enum.

Complex Controls:
1.  Add a new match case inside the create_controller() method of the ControlFactory.
2.  Then implement the concrete Complex Control product class in the control_products.py
    file and adjust the create() method to achieve the control's desired composition.

Still looking for a way to simplify the complex controls implementation, but right now
it is pretty good and simple when trying to add a more complex controller.
"""

from abc import ABC, abstractmethod
import logging
import os

from maya import cmds

from . import control_products
from .control_vault import BasicControllerTypes, ComplexControllerTypes

from ..data.node_affix_types import MayaSuffixTypes, RigSideTypes
from ..data.build_options import ControllerBuildOptions
from Util.UtilTools.src import snapping_utils

from importlib import reload

reload(snapping_utils)

LOG = logging.getLogger(os.path.basename(__file__))


# Abstract Factory
class ControllerFactory(ABC):
    """Main Controller factory."""

    @abstractmethod
    def create_controller(self, build_instructions: ControllerBuildOptions):
        """Create a new Rig controller curve."""
        raise NotImplementedError("You should implement this method")

    def create_offset_group(
        self,
        name: str,
        match_node: str = None,
        match_position: bool = True,
        match_rotation: bool = True,
    ) -> str:
        """Create an empty group at the match controller's location if desired.

        The function does no name changes to the name parameter. If there are any
        string changes you wish to make, do them before executing this function.

        The match_node parameter is the name of the node in Maya that you wish
        to potentially match the position and/or rotation to.
        """
        new_group = cmds.group(
            empty=True, name=f"{name}_{MayaSuffixTypes.OFFSET_GROUP.value}"
        )
        if len(match_node) is not None:
            snapping_utils.snap_object(
                match_node, new_group, match_position, match_rotation
            )

        return new_group

    def add_offset_group(self, child_control: str) -> str:
        """Attachs a group offset node above the child controller.

        This moves the child_control object underneath a group offset node.
        """
        offset_name = f"{child_control}_{MayaSuffixTypes.OFFSET_GROUP.value}"
        if "_CTL" in offset_name:
            offset_name = (
                f"{offset_name.split('_CTL')[0]}_{MayaSuffixTypes.OFFSET_GROUP.value}"
            )
        # offset_group = cmds.group(empty=True, name=offset_name)
        offset_group = self.create_offset_group(offset_name, child_control)
        # Get child_control's current parent
        current_parent = cmds.listRelatives(child_control, parent=True)
        # Parent child_control to offset group
        cmds.parent(child_control, offset_group)
        # Parent offset group to old child_control parent
        if current_parent is not None:
            cmds.parent(offset_group, current_parent)

        return offset_group

    def _parent_node(self, new_control: str, parent: str):
        # Parent new controller if desired
        if parent is not None:
            if cmds.objExists(parent):
                cmds.parent(new_control, parent)
            else:
                LOG.warning(
                    "Parent object named '%s' doesn't exist. Skipping parenting...",
                    parent,
                )


# Concrete Factory
class ControlFactory(ControllerFactory):
    """Factory for building new Rig Controller curves."""

    def create_controller(self, build_instructions: ControllerBuildOptions):
        # desired_side = self._get_side_enum(build_instructions.desired_side.value)

        new_control: str = None
        # Basic Controls here
        for key in BasicControllerTypes:
            if key.name.lower() == build_instructions.controller_type.lower():
                new_control = control_products.BasicControl().create(
                    key,
                    control_name=build_instructions.control_name,
                    side=build_instructions.desired_side,
                )
                self._parent_node(new_control, build_instructions.parent_node)
                return new_control

        # Complex Controls here.
        match build_instructions.controller_type.lower():
            case "circle":
                new_control = control_products.CircleControl().create(
                    build_instructions.control_name,
                    side=build_instructions.desired_side,
                )
            case "sphere":
                new_control = control_products.SphereControl().create(
                    build_instructions.control_name,
                    side=build_instructions.desired_side,
                )
            case "info":
                new_control = control_products.InfoControl().create(
                    build_instructions.control_name,
                    side=build_instructions.desired_side,
                )
            case "eyes":
                new_control = control_products.EyesControl().create(
                    build_instructions.control_name,
                    side=build_instructions.desired_side,
                )
            case "arrow_swap":
                new_control = control_products.ArrowSwapControl().create(
                    build_instructions.control_name,
                    side=build_instructions.desired_side,
                )
            case "pelvis":
                new_control = control_products.PelvisControl().create(
                    build_instructions.control_name,
                    side=build_instructions.desired_side,
                )
            case _:
                error_msg = (
                    f"Invalid control name entered: "
                    f"{build_instructions.controller_type}. Please use one of the "
                    "following valid names:\n"
                    "------------------------------------------------\n"
                )
                for basic_control in BasicControllerTypes:
                    error_msg += f"{basic_control.name.lower()}\n"

                for complex_control in ComplexControllerTypes:
                    error_msg += f"{complex_control.name.lower()}\n"

                LOG.error(error_msg)
                return None

        self._parent_node(new_control, build_instructions.parent_node)

        return new_control
