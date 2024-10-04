"""Maya startup script.

This file executes on Maya's startup and helps with building
the Previs Menu in Maya.
"""

# userSetup file name for Maya pylint: disable=invalid-name
import logging

from maya import mel
import maya.utils as mutil

from val_maya_menu.menu import build_pipe_menu as pipe
from val_core.ui.banner import build_project_banner as bpb
from val_core.config import setup_logging as sl

from importlib import reload

reload(sl)

LOG = logging.getLogger("userSetup.py")


def launch_previs_menu():
    """Launch previs menu."""
    LOG.info("Building Pipe Menu...")
    pipe.BuildPipeMenu()

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
mutil.executeDeferred(add_banner_button)
# mutil.executeDeferred(virus_check)
