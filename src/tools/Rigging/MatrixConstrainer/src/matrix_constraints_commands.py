# Copyright (C) 2024 Robert Wiese - All Rights Reserved.
"""Matrix Constraints commands and functionality."""

from __future__ import annotations
from enum import Enum
import logging
import os
from typing import TYPE_CHECKING

from maya import cmds

import maya.api.OpenMaya as om

from Core import core_paths as cpath

from Util.UtilTools.src import animation_utils

if TYPE_CHECKING:
    from ..vulcan_rig import VulcanRig

from importlib import reload

# Current Module root path
MODULE_PATH = f"{cpath.get_parent_directory(__file__, 2)}"

LOG = logging.getLogger(os.path.basename(__file__))


class ConstraintMethod(Enum):
    PARENT_NO_OFFSET = 0
    PARENT_OFFSET = 1
    POINT_NO_OFFSET = 2
    POINT_OFFSET = 3
    ORIENT_NO_OFFSET = 4
    ORIENT_OFFSET = 5
    SCALE_NO_OFFSET = 6
    SCALE_OFFSET = 7
    REMOVE_CONSTRAINT = 8


class MatrixConstraintCommand:
    """Matrix Constraint command."""

    def __init__(self, constraint_method: ConstraintMethod, vulcan_window: VulcanRig):
        self._constraint_method = constraint_method
        self._vulcan_window = vulcan_window

    def create_constraint(self) -> None:
        """Create new matrix constraint."""
        LOG.info("Creating constraint of type: %s", self._constraint_method)
        selection = cmds.ls(selection=True)
        if not len(selection) == 2:
            LOG.error("Please select two objects!")
            return

        self.create_matrix_constraint(
            selection[0], selection[1], self._constraint_method
        )

    def remove_constraint(self):
        """Remove Matrix Constraint."""
        LOG.info("Removing constraint...")
        selection = cmds.ls(selection=True)
        if not len(selection) == 1:
            LOG.error("Please select an object!")
            return

        selected_node = selection[0]

        if not cmds.attributeQuery(
            "MatrixConstrainer", exists=True, node=selected_node
        ):
            LOG.info(
                "No attribute named 'MatrixConstrainer' found on node: %s",
                selected_node,
            )
            return

        constraint_nodes = cmds.getAttr(f"{selected_node}.MatrixNodes")
        for node in constraint_nodes:
            try:
                cmds.delete(node)
            except ValueError:
                continue

        # Reset original relative transforms and offset parent matrix
        cmds.setAttr(
            f"{selected_node}.offsetParentMatrix",
            type="matrix",
            *cmds.getAttr(f"{selected_node}.PreMatrixOffsetParent"),
        )
        # Restore Translation
        cmds.setAttr(
            f"{selected_node}.translateX",
            cmds.getAttr(f"{selected_node}.pre_matrix_translation_x"),
        )
        cmds.setAttr(
            f"{selected_node}.translateY",
            cmds.getAttr(f"{selected_node}.pre_matrix_translation_y"),
        )
        cmds.setAttr(
            f"{selected_node}.translateZ",
            cmds.getAttr(f"{selected_node}.pre_matrix_translation_z"),
        )
        # Restore Rotation
        cmds.setAttr(
            f"{selected_node}.rotateX",
            cmds.getAttr(f"{selected_node}.pre_matrix_rotation_x"),
        )
        cmds.setAttr(
            f"{selected_node}.rotateY",
            cmds.getAttr(f"{selected_node}.pre_matrix_rotation_y"),
        )
        cmds.setAttr(
            f"{selected_node}.rotateZ",
            cmds.getAttr(f"{selected_node}.pre_matrix_rotation_z"),
        )
        # Restore Scale
        cmds.setAttr(
            f"{selected_node}.scaleX",
            cmds.getAttr(f"{selected_node}.pre_matrix_scale_x"),
        )
        cmds.setAttr(
            f"{selected_node}.scaleY",
            cmds.getAttr(f"{selected_node}.pre_matrix_scale_y"),
        )
        cmds.setAttr(
            f"{selected_node}.scaleZ",
            cmds.getAttr(f"{selected_node}.pre_matrix_scale_z"),
        )
        self.remove_constraint_attributes(selected_node)

    def remove_constraint_attributes(self, node_name: str):
        """Cleanup constraint attributes."""
        if not cmds.attributeQuery("MatrixConstrainer", exists=True, node=node_name):
            LOG.info(
                "No attribute named 'MatrixConstrainer' found on node: %s", node_name
            )
            return

        cmds.deleteAttr(f"{node_name}.MatrixConstrainer")

    def create_matrix_constraint(
        self, driver: str, driven: str, constraint_method: ConstraintMethod
    ) -> None:
        """Create a Parent Constraint style matrix constraint."""
        # Grab pre-constraint relative transforms of driven object
        self.create_storage_attributes(driven)
        self.store_pre_constraint_transforms(driven)

        # Calculate and set up offset matrix connections and reset transforms after
        offset_matrix_position = self.calculate_offset_matrix(driver, driven)

        new_nodes = []
        multiply_node = cmds.shadingNode("multMatrix", asUtility=True)
        new_nodes.append(multiply_node)
        try:
            driven_parent_obj = cmds.listRelatives(driven, parent=True)[0]
        except TypeError:
            driven_parent_obj = None

        # Make connections to multiply matrix node
        cmds.connectAttr(
            f"{driver}.worldMatrix[0]", f"{multiply_node}.matrixIn[0]", force=True
        )
        if driven_parent_obj is not None:
            cmds.connectAttr(
                f"{driven_parent_obj}.worldInverseMatrix[0]",
                f"{multiply_node}.matrixIn[1]",
                force=True,
            )
        # Create pick matrix
        pick_matrix = self.create_pick_matrix(constraint_method)
        new_nodes.append(pick_matrix)

        # Connect multiply matrix node to driven object
        cmds.connectAttr(
            f"{multiply_node}.matrixSum", f"{pick_matrix}.inputMatrix", force=True
        )
        cmds.connectAttr(
            f"{pick_matrix}.outputMatrix", f"{driven}.offsetParentMatrix", force=True
        )
        # If no offset is needed...
        if constraint_method == ConstraintMethod.PARENT_NO_OFFSET:
            # Store all new nodes associated with the new constraint
            cmds.setAttr(
                f"{driven}.MatrixNodes", len(new_nodes), *new_nodes, type="stringArray"
            )
            # Reset driven object transforms to match driver's position
            animation_utils.reset_transforms(driven, scale=False)
            return

        # Set the offset matrix values
        if driven_parent_obj is not None:
            cmds.disconnectAttr(
                f"{driven_parent_obj}.worldInverseMatrix[0]",
                f"{multiply_node}.matrixIn[1]",
            )
        cmds.disconnectAttr(f"{driver}.worldMatrix[0]", f"{multiply_node}.matrixIn[0]")

        # The * unpacks the matrix data
        cmds.setAttr(
            f"{multiply_node}.matrixIn[0]", *offset_matrix_position, type="matrix"
        )
        # Reconnect the driver and driven parent's matrices
        cmds.connectAttr(
            f"{driver}.worldMatrix[0]", f"{multiply_node}.matrixIn[1]", force=True
        )
        if driven_parent_obj is not None:
            cmds.connectAttr(
                f"{driven_parent_obj}.worldInverseMatrix[0]",
                f"{multiply_node}.matrixIn[2]",
                force=True,
            )

        # Reset driven object transforms to match driver's position
        animation_utils.reset_transforms(driven, scale=False)
        # Store all new nodes associated with the new constraint
        cmds.setAttr(
            f"{driven}.MatrixNodes", len(new_nodes), *new_nodes, type="stringArray"
        )

    def store_pre_constraint_transforms(self, node: str):
        """Store all Pre-constraint transforms and offset parent matrix values."""
        if not cmds.attributeQuery("MatrixConstrainer", exists=True, node=node):
            LOG.error("Object '%s' has no MatrixConstrainer attribute!", node)
            return

        current_offset_parent_matrix = cmds.getAttr(f"{node}.offsetParentMatrix")
        current_translation = cmds.xform(
            node, query=True, relative=True, translation=True
        )
        current_rotation = cmds.xform(node, query=True, relative=True, rotation=True)
        current_scale = cmds.xform(node, query=True, relative=True, scale=True)

        # Store Offset Parent Matrix
        cmds.setAttr(
            f"{node}.PreMatrixOffsetParent",
            type="matrix",
            *current_offset_parent_matrix,
        )
        # Store Translation
        cmds.setAttr(f"{node}.pre_matrix_translation_x", current_translation[0])
        cmds.setAttr(f"{node}.pre_matrix_translation_y", current_translation[1])
        cmds.setAttr(f"{node}.pre_matrix_translation_z", current_translation[2])
        # Store Rotation
        cmds.setAttr(f"{node}.pre_matrix_rotation_x", current_rotation[0])
        cmds.setAttr(f"{node}.pre_matrix_rotation_y", current_rotation[1])
        cmds.setAttr(f"{node}.pre_matrix_rotation_z", current_rotation[2])
        # Store Scale
        cmds.setAttr(f"{node}.pre_matrix_scale_x", current_scale[0])
        cmds.setAttr(f"{node}.pre_matrix_scale_y", current_scale[1])
        cmds.setAttr(f"{node}.pre_matrix_scale_z", current_scale[2])

    def create_storage_attributes(self, node_name: str) -> None:
        """Create pre-constraint transform attributes on object."""
        if not cmds.attributeQuery("MatrixConstrainer", exists=True, node=node_name):
            LOG.info("MatrixConstrainer attribute doesn't exist. Creating...")
            cmds.addAttr(
                node_name,
                longName="MatrixConstrainer",
                numberOfChildren=5,
                attributeType="compound",
            )
            # Current offset parent matrix
            cmds.addAttr(
                node_name,
                longName="PreMatrixOffsetParent",
                attributeType="matrix",
                parent="MatrixConstrainer",
            )
            # Associated constraint node names
            cmds.addAttr(
                node_name,
                longName="MatrixNodes",
                dataType="stringArray",
                parent="MatrixConstrainer",
            )
            # Translation
            cmds.addAttr(
                node_name,
                attributeType="double3",
                longName="PreMatrixTranslation",
                parent="MatrixConstrainer",
            )
            cmds.addAttr(
                node_name,
                attributeType="double",
                parent="PreMatrixTranslation",
                longName="pre_matrix_translation_x",
            )
            cmds.addAttr(
                node_name,
                attributeType="double",
                parent="PreMatrixTranslation",
                longName="pre_matrix_translation_y",
            )
            cmds.addAttr(
                node_name,
                attributeType="double",
                parent="PreMatrixTranslation",
                longName="pre_matrix_translation_z",
            )
            # Rotation
            cmds.addAttr(
                node_name,
                attributeType="double3",
                longName="PreMatrixRotation",
                parent="MatrixConstrainer",
            )
            cmds.addAttr(
                node_name,
                attributeType="double",
                parent="PreMatrixRotation",
                longName="pre_matrix_rotation_x",
            )
            cmds.addAttr(
                node_name,
                attributeType="double",
                parent="PreMatrixRotation",
                longName="pre_matrix_rotation_y",
            )
            cmds.addAttr(
                node_name,
                attributeType="double",
                parent="PreMatrixRotation",
                longName="pre_matrix_rotation_z",
            )
            # Scale
            cmds.addAttr(
                node_name,
                attributeType="double3",
                longName="PreMatrixScale",
                parent="MatrixConstrainer",
            )
            cmds.addAttr(
                node_name,
                attributeType="double",
                parent="PreMatrixScale",
                longName="pre_matrix_scale_x",
            )
            cmds.addAttr(
                node_name,
                attributeType="double",
                parent="PreMatrixScale",
                longName="pre_matrix_scale_y",
            )
            cmds.addAttr(
                node_name,
                attributeType="double",
                parent="PreMatrixScale",
                longName="pre_matrix_scale_z",
            )

    def create_pick_matrix(self, constraint_method: ConstraintMethod):
        """Create pick matrix type node based on constraint method."""
        pick_node = cmds.createNode("pickMatrix")
        match constraint_method:
            case ConstraintMethod.PARENT_NO_OFFSET | ConstraintMethod.PARENT_OFFSET:
                cmds.setAttr(f"{pick_node}.useScale", 0)
                cmds.setAttr(f"{pick_node}.useShear", 0)
            case ConstraintMethod.POINT_NO_OFFSET | ConstraintMethod.POINT_OFFSET:
                cmds.setAttr(f"{pick_node}.useRotate", 0)
                cmds.setAttr(f"{pick_node}.useScale", 0)
                cmds.setAttr(f"{pick_node}.useShear", 0)
            case ConstraintMethod.ORIENT_NO_OFFSET | ConstraintMethod.ORIENT_OFFSET:
                cmds.setAttr(f"{pick_node}.useTranslation", 0)
                cmds.setAttr(f"{pick_node}.useScale", 0)
                cmds.setAttr(f"{pick_node}.useShear", 0)
            case ConstraintMethod.SCALE_NO_OFFSET | ConstraintMethod.SCALE_OFFSET:
                cmds.setAttr(f"{pick_node}.useTranslation", 0)
                cmds.setAttr(f"{pick_node}.useRotate", 0)

        return pick_node

    def calculate_offset_matrix(self, driver: str, driven: str):
        """Calculate the current offset matrix between the driver and driven objects."""
        # Driven object's world matrix and driven's parent world
        driven_world_matrix = self.get_dag_path(driven).inclusiveMatrix()
        # Driver object's Parent Inverse Matrix
        driver_world_matrix = self.get_dag_path(driver).inclusiveMatrix()
        # Put driven's matrix inside the driver's matrix to get offset value
        offset_matrix = driven_world_matrix * driver_world_matrix.inverse()

        return offset_matrix

    def get_dag_path(self, node: str = None):
        """Get the node's dag path object."""
        selection_list = om.MSelectionList()
        selection_list.add(node)
        return selection_list.getDagPath(0)
