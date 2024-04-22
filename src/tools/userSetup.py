# Copyright (C) 2023 Robert Wiese - All Rights Reserved.
"""Maya startup script.

This file executes on Maya's startup and helps with building
the Previs Menu in Maya.
"""
# pylint: disable=invalid-name
# This file needs to be stay as userSetup.py for Maya to recognize on launch
# to run this code.
import logging
import os

from Core.menu.PipeMenu.src import build_pipe_menu as pipe
from Core.ui.MayaCustomization.src import build_project_banner as bpb
from importlib import reload

reload(bpb)

# from core.shelves.DnegPrevisShelf.src import build_dneg_previs_shelf as bdn

from maya import mel
import maya.utils as mutil

# from tools.util.AfterEffectsUtils.src import copy_dneg_ae_tools as dae
# from tools.util.virusCleanup import virus_cleanup as vc

from src import setup_logging as sl

LOG = logging.getLogger("userSetup.py")


def launch_previs_menu():
    """Launch previs menu."""
    LOG.info("Building Pipe Menu...")
    pipe.BuildPipeMenu()


# def add_previs_shelf():
#     """Add Previs shelf."""
#     LOG.info("Building Previs Shelf...")
#     bdn.BuildDnegPrevisShelf()


def add_banner_button():
    """Add show button."""
    LOG.info("Adding show button to Maya UI...")
    bpb.create_project_banner()


# def virus_check():
#     """Call virus cleanup."""
#     LOG.info("Checking for scriptjob virus node...")
#     vc.virus_cleanup()


def prepare_env():
    """Prepare current Maya environment i.e. prod or dev"""
    current_env = mel.eval('getenv "CURRENT_ENV"')
    sl.setup_logging(current_env)


mutil.executeDeferred(prepare_env)

mutil.executeDeferred(launch_previs_menu)
# mutil.executeDeferred(add_previs_shelf)
mutil.executeDeferred(add_banner_button)
# mutil.executeDeferred(virus_check)
