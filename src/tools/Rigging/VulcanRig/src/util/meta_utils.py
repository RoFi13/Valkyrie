# Copyright (C) 2023 Robert Wiese - All Rights Reserved.
"""Various Vulcan metadata utility functions."""

from dataclasses import dataclass, field
import logging
import os

from maya import cmds

from Core import core_paths as cpath

# from . import gui_factories
# from ..rig_modules import module_factory
# from ..data.module_types import ModuleType

from importlib import reload

# Current Module root path
MODULE_PATH = f"{cpath.get_parent_directory(__file__, 2)}"

LOG = logging.getLogger(os.path.basename(__file__))


def initialize_metanode():
    metanode = "VulcanMeta"
    if not cmds.objExists(metanode):
        cmds.group(empty=True, name=metanode)

    # metadata_struct = {
    #     "name": "rigData",
    #     "fields": [
    #         {"name": "type", "type": "string"},
    #         {"name": "complexity", "type": "int"},
    #     ],
    # }
    # LOG.info("data structures: %s", cmds.dataStructure(query=True, format=True))
    # # cmds.dataStructure(format="json", asString=str(metadata_struct))
    # cmds.dataStructure(
    #     format="raw",
    #     asString="name=VulcanInfo:string=rigType:int=complexity:string=notes",
    # )
    # # new_meta = {"rigType": "biped", "complexity": 3, "notes": "this is a note!"}
    # cmds.select(metanode, replace=True)
    # # cmds.addMetadata(data=str(new_meta), structure="VulcanStream")
    # cmds.addMetadata(
    #     streamName="VulcanStream", channelName="nodeState", structure="VulcanInfo"
    # )
    # cmds.select(metanode, replace=True)

    # LOG.info("%s", cmds.getMetadata(streamName="VulcanStream", memberName="rigType"))

    return metanode


@dataclass
class RootConfig:
    child_node: str
