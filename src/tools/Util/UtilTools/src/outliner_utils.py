"""Various functions for outliner utilities in Maya."""

import logging
import os

from maya import cmds

LOG = logging.getLogger(os.path.basename(__file__))


def create_shot_tree() -> None:
    """Create shot group nodes for organization."""
    group_names = [
        "ENV",
        "CHAR",
        "FX",
        "PROP",
        "DNT",
        "LIGHT",
        "CRE",
        "MISC",
        "TECH",
        "CAM",
        "VEH",
    ]
    all_attributes = [".tx", ".ty", ".tz", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz"]

    for group_node in group_names:
        if cmds.objExists(group_node):
            continue

        cmds.select(clear=True)
        cmds.group(name=group_node, empty=True)
        for attr in all_attributes:
            cmds.setAttr(
                f"{group_node}{attr}", keyable=False, lock=True, channelBox=False
            )
        # Change color of nodes in outliner
        cmds.setAttr(f"{group_node}.useOutlinerColor", 1)
        cmds.setAttr(f"{group_node}.outlinerColor", 0.876, 0.876, 0.179)
