# Copyright (C) 2024 Robert Wiese - All Rights Reserved.
"""Rig Suffix types."""

from enum import Enum
import logging
import os

LOG = logging.getLogger(os.path.basename(__file__))


class MayaSuffixTypes(Enum):
    """Common Node Suffix types."""

    CONTROL = "CTL"
    BIND_JOINT = "BindJnt"
    JOINT = "Jnt"
    GEOMETRY = "geo"
    GROUP = "GRP"
    OFFSET_GROUP = "Offset_GRP"


class RigSideTypes(Enum):
    LEFT = "L"
    RIGHT = "R"
    CENTER = "C"
