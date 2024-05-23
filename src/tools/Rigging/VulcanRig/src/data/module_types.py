# Copyright (C) 2023 Robert Wiese - All Rights Reserved.
"""Module Data types."""
# Can't find PySide2 modules pylint: disable=I1101

from enum import Enum

from Core import core_paths as cpath

# Current Module root path
MODULE_PATH = f"{cpath.get_parent_directory(__file__, 2)}"

# Full path to where .ui files are stored
RSRC_PATH = f"{MODULE_PATH}/resources"


class ModuleType(Enum):
    """All Rigging Module Types"""

    ROOT = {"label": "Root", "icon": f"{RSRC_PATH}/icons/root_icons/root_icon.png"}
    BIPED_SPINE = {
        "label": "Biped Spine",
        "icon": f"{RSRC_PATH}/icons/biped_icons/spine_icon.png",
    }
    BIPED_HEAD = {
        "label": "Biped Head",
        "icon": f"{RSRC_PATH}/icons/biped_icons/head_icon.png",
    }
    BIPED_SHOULDER = {
        "label": "Biped Shoulder",
        "icon": f"{RSRC_PATH}/icons/biped_icons/shoulder_icon.png",
    }
    BIPED_ARM = {
        "label": "Biped Arm",
        "icon": f"{RSRC_PATH}/icons/biped_icons/arm_icon.png",
    }
    BIPED_HAND = {
        "label": "Biped Hand",
        "icon": f"{RSRC_PATH}/icons/biped_icons/hand_icon.png",
    }
    BIPED_LEG = {
        "label": "Biped Leg",
        "icon": f"{RSRC_PATH}/icons/biped_icons/leg_icon.png",
    }
    BIPED_FOOT = {
        "label": "Biped Foot",
        "icon": f"{RSRC_PATH}/icons/biped_icons/foot_icon.png",
    }
    QUAD_SPINE = {"label": "Quadruped Spine", "icon": None}
    QUAD_HEAD = {"label": "Quadruped Head", "icon": None}
    QUAD_ARM = {"label": "Quadruped Arm", "icon": None}
    QUAD_FOOT = {"label": "Quadruped Foot", "icon": None}
    REVERSE_LEG = {"label": "Reverse Leg", "icon": None}
    WING = {"label": "Wing", "icon": None}
    TAIL = {"label": "Tail", "icon": None}
    CHAIN = {"label": "Chain", "icon": None}


class ModuleSide(Enum):
    """Rig symmetry sides."""

    CENTER = "C"
    LEFT = "L"
    RIGHT = "R"
