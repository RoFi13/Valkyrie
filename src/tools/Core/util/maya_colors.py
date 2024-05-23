# Copyright (C) 2024 Robert Wiese - All Rights Reserved.
"""Maya Color RGB values."""

from enum import Enum
import logging
import os

from maya import cmds

from Core import core_paths as cpath

# Main paths
MAIN_PATHS = cpath.core_paths()

LOG = logging.getLogger(os.path.basename(__file__))


class RGBColorOverride(Enum):
    """RGB Colors to apply to different color controllers."""

    RED = [1, 0, 0]
    BLUE = [0, 0, 1]
    YELLOW = [1, 1, 0]
    PURPLE = [1, 0, 1]
    ORANGE = [1, 0.247, 0]
    DARK_GREEN = [0.073, 0.156, 0]


def get_draw_override_color(color_choice: str):
    """Get Draw Override enum color values.

    Args:
        color_choice (str): Name of color to get values for.

    Returns:
        list[float]: Returns a list of float values for RGB.
    """
    color_value = None
    match color_choice.lower():
        case "red":
            color_value = RGBColorOverride.RED.value
        case "blue":
            color_value = RGBColorOverride.BLUE.value
        case "yellow":
            color_value = RGBColorOverride.YELLOW.value
        case "purple":
            color_value = RGBColorOverride.PURPLE.value
        case "orange":
            color_value = RGBColorOverride.ORANGE.value
        case "dark_green":
            color_value = RGBColorOverride.DARK_GREEN.value
        case _:
            error_msg = (
                f"Color entered '{color_choice}' isn't valid. Please see below for valid "
                "color choices:\n------------------------------------\n"
            )
            for key in RGBColorOverride:
                error_msg += f"{key}\n"

            LOG.error(error_msg)
            return None

    return color_value


def set_draw_override_color(node: str, color_choice: str):
    """Set the Draw Override Color for the object's shape nodes.

    Args:
        node (str): Object name. Can be either a Transform node or a Shape node.
        color_choice (str): Choice of color.
    """

    object_shape_nodes: list
    if cmds.objectType(node, isType="transform"):
        object_shape_nodes = cmds.listRelatives(node, shapes=True)
    else:
        object_shape_nodes = [node]

    color_value = get_draw_override_color(color_choice)

    for curve_shape in object_shape_nodes:
        cmds.setAttr(f"{curve_shape}.overrideEnabled", True)
        cmds.setAttr(f"{curve_shape}.overrideRGBColors", True)

        i = 0
        for channel in ["R", "G", "B"]:
            cmds.setAttr(f"{curve_shape}.overrideColor{channel}", color_value[i])
            i += 1
