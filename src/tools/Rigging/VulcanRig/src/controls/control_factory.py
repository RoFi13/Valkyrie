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

from ..data.node_affix_types import RigSideTypes

from importlib import reload

LOG = logging.getLogger(os.path.basename(__file__))


# Abstract Factory
class ControllerFactory(ABC):
    """Main Controller factory."""

    @abstractmethod
    def create_controller(
        self,
        desired_type: str,
        control_name: str = "",
        desired_side: str = "center",
        parent: str = None,
    ):
        """Create a new Rig controller curve."""
        raise NotImplementedError("You should implement this method")

    def _get_side_enum(self, desired_side: str = "center"):
        found_key: RigSideTypes
        match desired_side.lower():
            case "center":
                found_key = RigSideTypes.CENTER
            case "left":
                found_key = RigSideTypes.LEFT
            case "right":
                found_key = RigSideTypes.RIGHT
        return found_key

    def _parent_controller(self, new_control: str, parent: str):
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

    def create_controller(
        self,
        desired_type: str,
        control_name: str = None,
        desired_side: str = "center",
        parent: str = None,
    ):
        desired_side = self._get_side_enum(desired_side)

        new_control: str = None
        # Basic Controls here
        for key in BasicControllerTypes:
            if key.name.lower() == desired_type.lower():
                new_control = control_products.BasicControl().create(
                    key, control_name=control_name, side=desired_side
                )
                self._parent_controller(new_control, parent)
                return new_control

        # Complex Controls here.
        match desired_type.lower():
            case "circle":
                new_control = control_products.CircleControl().create(
                    control_name, side=desired_side
                )
            case "sphere":
                new_control = control_products.SphereControl().create(
                    control_name, side=desired_side
                )
            case "info":
                new_control = control_products.InfoControl().create(
                    control_name, side=desired_side
                )
            case "eyes":
                new_control = control_products.EyesControl().create(
                    control_name, side=desired_side
                )
            case "arrow_swap":
                new_control = control_products.ArrowSwapControl().create(
                    control_name, side=desired_side
                )
            case "pelvis":
                new_control = control_products.PelvisControl().create(
                    control_name, side=desired_side
                )
            case _:
                error_msg = (
                    f"Invalid control name entered: {desired_type}. Please "
                    "use one of the following valid names:\n"
                    "------------------------------------------------\n"
                )
                for basic_control in BasicControllerTypes:
                    error_msg += f"{basic_control.name.lower()}\n"

                for complex_control in ComplexControllerTypes:
                    error_msg += f"{complex_control.name.lower()}\n"

                LOG.error(error_msg)
                return None

        self._parent_controller(new_control, parent)

        return new_control
