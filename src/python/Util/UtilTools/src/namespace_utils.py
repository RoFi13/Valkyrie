# Copyright (C) 2024 Robert Wiese - All Rights Reserved.
"""Various functions for modifying namespaces in Maya."""

import logging
import os

from maya import cmds

LOG = logging.getLogger(os.path.basename(__file__))


def remove_first_namespace():
    """Remove the first namespace of the selected object."""
    selection = cmds.ls(selection=True)

    if len(selection) > 1:
        LOG.error("Please select only one object to remove namespace.")
        return

    first_namespace = selection[0].split(":")[0]
    cmds.namespace(removeNamespace=first_namespace, mergeNamespaceWithParent=True)
