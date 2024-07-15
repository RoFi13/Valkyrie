# Copyright (C) 2024 Robert Wiese - All Rights Reserved.
"""Concrete Controller Factory classes to help in creating rig controllers."""

import logging
import os
from uuid import uuid4

from maya import cmds

from .control_vault import BasicControllerTypes
from .control_product_factories import SimpleControlProduct, ComplexControlProduct

from ..data.node_affix_types import MayaSuffixTypes, RigSideTypes

# from importlib import reload

LOG = logging.getLogger(os.path.basename(__file__))


# Concrete Products
class BasicControl(SimpleControlProduct):
    """Basic Controller Implementation.

    Args:
        SimpleControlProduct (SimpleControlProduct): Parent abstract class.
    """

    def __init__(self):
        self.default_name = f"BasicControl_{MayaSuffixTypes.CONTROL.value}"

    def create(
        self,
        control_type: BasicControllerTypes,
        control_name: str = None,
        side: RigSideTypes = RigSideTypes.CENTER,
    ):
        control_name = self._fix_control_name(side, control_name)

        return cmds.curve(
            degree=control_type.value["degree"],
            name=control_name,
            point=control_type.value["points"],
        )


class CircleControl(ComplexControlProduct):
    """Circle Controller Implementation.

    Considered a complex control because of the nurbs curve connecting the start
    and end points in a loop.

    Args:
        ComplexControlProduct (ComplexControlProduct): Parent abstract class.
    """

    def __init__(self):
        self.default_name = f"Circle_{MayaSuffixTypes.CONTROL.value}"

    def create(
        self, control_name: str = None, side: RigSideTypes = RigSideTypes.CENTER
    ):
        control_name = self._fix_control_name(side, control_name)

        return cmds.circle(
            name=control_name,
            center=[0, 0, 0],
            normal=[0, 1, 0],
            sweep=360,
            radius=12,
            degree=3,
            useTolerance=False,
            tolerance=0.01,
            sections=8,
            constructionHistory=False,
        )[0]


class SphereControl(ComplexControlProduct):
    """Sphere Controller Implementation.

    Args:
        ComplexControlProduct (ComplexControlProduct): Parent abstract class.
    """

    def __init__(self):
        self.default_name = f"Sphere_{MayaSuffixTypes.CONTROL.value}"

    def create(
        self, control_name: str = None, side: RigSideTypes = RigSideTypes.CENTER
    ):
        control_name = self._fix_control_name(side, control_name)

        complex_control_product = CircleControl()
        circle_a = complex_control_product.create(f"circle_{uuid4()}")
        circle_b = complex_control_product.create(f"circle_{uuid4()}")
        circle_c = complex_control_product.create(f"circle_{uuid4()}")

        # Rotate curves
        cmds.setAttr(f"{circle_b}.rotateZ", 90)
        cmds.setAttr(f"{circle_c}.rotateX", 90)

        # Combine curves
        new_control = self.combine_shape_nodes([circle_a, circle_b, circle_c])

        new_control = cmds.rename(new_control, control_name)

        self.fix_shape_node_names(new_control)

        return new_control


class InfoControl(ComplexControlProduct):
    """Info Controller Implementation.

    Args:
        ComplexControlProduct (ComplexControlProduct): Parent abstract class.
    """

    def __init__(self):
        self.default_name = f"Info_{MayaSuffixTypes.CONTROL.value}"

    def create(
        self, control_name: str = None, side: RigSideTypes = RigSideTypes.CENTER
    ):
        control_name = self._fix_control_name(side, control_name)

        basic_control_product = BasicControl()
        circle_control_product = CircleControl()

        question_hook_control = basic_control_product.create(
            BasicControllerTypes.QUESTION_HOOK, f"hook_{uuid4()}"
        )

        question_dot_control = circle_control_product.create(f"circle_{uuid4()}")
        cmds.select(question_dot_control, replace=True)
        cmds.move(-0.402018, 0, 5.853324, rotatePivotRelative=True)
        cmds.scale(0.144, 0.144, 0.144, worldSpace=True, relative=True)

        container_circle_control = circle_control_product.create(f"circle_{uuid4()}")

        # Combine curves
        new_control = self.combine_shape_nodes(
            [question_hook_control, question_dot_control, container_circle_control]
        )

        new_control = cmds.rename(new_control, control_name)

        self.fix_shape_node_names(new_control)

        return new_control


class EyesControl(ComplexControlProduct):
    """Eye Controller Implementation.

    One parent controller with two children controllers for each eye.

    Args:
        ComplexControlProduct (ComplexControlProduct): Parent abstract class.
    """

    def __init__(self):
        self.default_name = f"Eye_{MayaSuffixTypes.CONTROL.value}"

    def create(
        self, control_name: str = None, side: RigSideTypes = RigSideTypes.CENTER
    ):
        control_name = self._fix_control_name(side, control_name)

        basic_control_product = BasicControl()
        circle_control_product = CircleControl()

        # Create controllers
        container_circle = basic_control_product.create(
            BasicControllerTypes.SLIDER_CONTAINER,
            f"EyesLookAt_{MayaSuffixTypes.CONTROL.value}",
        )

        right_eye_control = circle_control_product.create(
            f"Eye_{MayaSuffixTypes.CONTROL.value}", RigSideTypes.RIGHT
        )
        left_eye_control = circle_control_product.create(
            f"Eye_{MayaSuffixTypes.CONTROL.value}", RigSideTypes.LEFT
        )

        # Resize individual eye controllers
        cmds.setAttr(f"{right_eye_control}.scaleX", 0.22)
        cmds.setAttr(f"{right_eye_control}.scaleY", 0.22)
        cmds.setAttr(f"{right_eye_control}.scaleZ", 0.22)
        cmds.setAttr(f"{left_eye_control}.scaleX", 0.22)
        cmds.setAttr(f"{left_eye_control}.scaleY", 0.22)
        cmds.setAttr(f"{left_eye_control}.scaleZ", 0.22)
        cmds.select([right_eye_control, left_eye_control], replace=True)
        cmds.makeIdentity(
            apply=True, translate=True, rotate=True, scale=True, normal=False
        )

        # Create offset groups
        container_offset = cmds.group(
            empty=True,
            name=container_circle.replace("CTL", MayaSuffixTypes.OFFSET_GROUP.value),
        )
        right_eye_offset = cmds.group(
            empty=True,
            name=right_eye_control.replace("CTL", MayaSuffixTypes.OFFSET_GROUP.value),
        )
        left_eye_offset = cmds.group(
            empty=True,
            name=left_eye_control.replace("CTL", MayaSuffixTypes.OFFSET_GROUP.value),
        )

        # Parent controllers to offset groups
        cmds.parent(container_circle, container_offset)
        cmds.parent(right_eye_control, right_eye_offset)
        cmds.parent(left_eye_control, left_eye_offset)

        # Move offset groups for individual eyes into place
        cmds.setAttr(f"{right_eye_offset}.tx", -4.7)
        cmds.setAttr(f"{left_eye_offset}.tx", 4.7)

        # Parent individual offsets to container offset
        cmds.parent(right_eye_offset, container_circle)
        cmds.parent(left_eye_offset, container_circle)

        cmds.select(container_circle, replace=True)

        return container_circle


class ArrowSwapControl(ComplexControlProduct):
    """Arrow Swap Controller Implementation.

    Args:
        ComplexControlProduct (ComplexControlProduct): Parent abstract class.
    """

    def __init__(self):
        self.default_name = f"ArrowSwap_{MayaSuffixTypes.CONTROL.value}"

    def create(
        self, control_name: str = None, side: RigSideTypes = RigSideTypes.CENTER
    ):
        control_name = self._fix_control_name(side, control_name)

        basic_control_product = BasicControl()

        left_turn_control = basic_control_product.create(
            BasicControllerTypes.LEFT_TURN_ARROW, f"left_turn_{uuid4()}"
        )
        right_turn_control = basic_control_product.create(
            BasicControllerTypes.RIGHT_TURN_ARROW, f"right_turn_{uuid4()}"
        )

        # Combine curves
        new_control = self.combine_shape_nodes([left_turn_control, right_turn_control])

        new_control = cmds.rename(new_control, control_name)

        self.fix_shape_node_names(new_control)

        return new_control


class PelvisControl(ComplexControlProduct):
    """Pelvis Controller Implementation.

    Args:
        ComplexControlProduct (ComplexControlProduct): Parent abstract class.
    """

    def __init__(self):
        self.default_name = f"Pelvis_{MayaSuffixTypes.CONTROL.value}"

    def create(
        self, control_name: str = None, side: RigSideTypes = RigSideTypes.CENTER
    ):
        control_name = self._fix_control_name(side, control_name)

        complex_control_product = CircleControl()
        pelvis_control = complex_control_product.create(control_name)

        # Move verteces
        cmds.setAttr(f"{pelvis_control}.scaleX", 1.6)
        cmds.setAttr(f"{pelvis_control}.scaleY", 1.6)
        cmds.setAttr(f"{pelvis_control}.scaleZ", 1.6)

        cmds.select(f"{pelvis_control}.cv[1]", f"{pelvis_control}.cv[5]", replace=True)
        cmds.move(0, -9.6, 0, relative=True, objectSpace=True, worldSpaceDistance=True)

        cmds.select(
            f"{pelvis_control}.cv[0]",
            f"{pelvis_control}.cv[2:4]",
            f"{pelvis_control}.cv[6:7]",
            replace=True,
        )
        cmds.move(0, 4.5, 0, relative=True, objectSpace=True, worldSpaceDistance=True)

        return pelvis_control
