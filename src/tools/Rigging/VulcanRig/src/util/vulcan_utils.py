# Copyright (C) 2024 Robert Wiese - All Rights Reserved.
"""Various Vulcan rigging utility functions."""

import logging
import os

from maya import cmds

from Core import core_paths as cpath


# from .. import module_product_factories


# reload(module_metadata)

# Current Module root path
MODULE_PATH = f"{cpath.get_parent_directory(__file__, 2)}"

LOG = logging.getLogger(os.path.basename(__file__))


def duplicate_joint_chain(start_joint: str, end_joint: str, suffix: str = "dup"):
    """Duplicates joint hierarchy given the start and end joints in chain."""
    # Check to delete twist joints if desired
    # if not include_twist_joints:
    #     joint_children = cmds.listRelatives(start_joint, allDescendents=True)
    #     for child in joint_children:
    #         if "twist" in child or "Twist" in child:
    #             cmds.delete(child)

    # # Pickwalk down starting from the start_joint until it reaches the end joint,
    # # storing each joint in a list on the way
    # i = 0
    # newJnts = [start_joint]
    # cmds.select(start_joint, replace=True)
    # while i < 99:
    #     # Pick walk and store each new joint down hierarchy
    #     curJnt = cmds.pickWalk(direction="down")[0]
    #     if end_joint in curJnt:
    #         # If the end_joint is equal to the current joint during pick walking, append to list and break loop
    #         newJnts.append(curJnt)
    #         break
    #     else:
    #         newJnts.append(curJnt)
    #     i += 1

    # Duplicate new joint list hierarchy
    joint_hierarchy = get_nodes_to_child(start_joint, end_joint)
    duplicate_joints = cmds.duplicate(
        joint_hierarchy, parentOnly=True, renameChildren=True
    )
    # Parent to world space
    cmds.parent(duplicate_joints[0], world=True)

    i = 0
    new_joints = []
    for chain_joint in duplicate_joints:
        new_joints.append(cmds.rename(chain_joint, f"{joint_hierarchy[i]}_{suffix}"))
        i += 1

    return new_joints


def get_nodes_to_child(start_node: str, end_node: str, reverse: bool = False):
    """Get all nodes in between (inclusive) the start and end nodes in a hierarchy.

    Note that the descending parameter inverts how this function operates. By default,
    it is expecting to
    """
    start_node_dag_path = cmds.ls(start_node, long=True)[0].split("|")
    end_node_dag_path = cmds.ls(end_node, long=True)[0].split("|")

    higher_node_index = start_node_dag_path.index(start_node)
    lower_node_dag_path = end_node_dag_path
    if len(end_node_dag_path) < len(start_node_dag_path):
        higher_node_index = end_node_dag_path.index(end_node)
        lower_node_dag_path = start_node_dag_path

    all_nodes = list(lower_node_dag_path[higher_node_index:])
    if reverse:
        all_nodes.sort(reverse=True)

    return all_nodes
