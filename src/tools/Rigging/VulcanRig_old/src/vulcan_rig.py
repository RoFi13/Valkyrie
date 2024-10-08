"""
For orient joints, use XYZ orientation settings. This is important for the foot rig with ball roll
and what not

"""
try:
    reload  # Python 2.7
except NameError:
    try:
        from importlib import reload  # Python 3.4+
    except ImportError:
        from imp import reload  # Python 3.0 - 3.3

import logging
import sys
import os
import platform
import json

# Imported modules should be put at the head of every tool
from maya import OpenMaya
from maya import OpenMayaMPx

# Imported Custom Modules
from Core import core_paths as cpath
from Core import maya_start as ms
from Core.ui.UIUtilTools.src import pyside_util_tools as put

# Import PySide2 modules
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtUiTools import QUiLoader

import maya.cmds as cmds

# Rigging Modules
from .arm_module import arm_module as amd

reload(amd)
from .spine_module import spine_module as smd

reload(smd)
from .biped_leg_module import biped_leg_module as blmd

reload(blmd)
from .neck_head_module import neck_head_module as hmd

reload(hmd)
from .hand_module import hand_module as hamd

reload(hamd)
from .util import attach_modules as att

reload(att)
from .util import create_space_switch as space

reload(space)
# Rigging Utilities
from .util import vulcan_utils as vutil

reload(vutil)

# Window title and object names
WINDOW_TITLE = "Vulcan Rig"
WINDOW_OBJECT = "vulcanRig"

LOADER = QUiLoader()

# Maya-specific
DOCK_WITH_MAYA_UI = False

# Main paths
MAIN_PATHS = cpath.core_paths()

# Current Module root path
MODULE_PATH = f"{cpath.get_parent_directory(__file__, 1)}"

# Full path to where .ui files are stored
RSRC_PATH = f"{MODULE_PATH}/resources"

# Full path to where custom controls are stored
CTLLIB = os.path.join(RSRC_PATH, "custom_controls")

LOG = logging.getLogger(os.path.basename(__file__))

"""
888     888 8888888       .d8888b.   .d88888b.  888b    888 8888888888 8888888 .d8888b.
888     888   888        d88P  Y88b d88P" "Y88b 8888b   888 888          888  d88P  Y88b
888     888   888        888    888 888     888 88888b  888 888          888  888    888
888     888   888        888        888     888 888Y88b 888 8888888      888  888
888     888   888        888        888     888 888 Y88b888 888          888  888  88888
888     888   888        888    888 888     888 888  Y88888 888          888  888    888
Y88b. .d88P   888        Y88b  d88P Y88b. .d88P 888   Y8888 888          888  Y88b  d88P
 "Y88888P"  8888888       "Y8888P"   "Y88888P"  888    Y888 888        8888888 "Y8888P88
"""


class vulcanRig(QtWidgets.QMainWindow):
    """Example showing how UI files can be loaded using the same script
    when taking advantage of the Qt.py module and build-in methods
    from PySide/PySide2/PyQt4/PyQt5."""

    def __init__(self, parent=None):
        # super(vulcanRig, self).__init__(parent)
        super().__init__(parent)

        # Set up default UI settings
        self.ui_settings = {
            "main_ui_file": f"{RSRC_PATH}/ui/vulcan_rig.ui",
            "asset_widget": f"{RSRC_PATH}/ui/insert_joints.ui",
            "min_size": [],
            "max_size": [],
        }
        self.root = put.setup_class_ui(
            self, WINDOW_OBJECT, WINDOW_TITLE, self.ui_settings
        )

        """
		 .d8888b.  888      .d88888b. 88888888888 .d8888b.        .d8888b.            .d8888b. 8888888 .d8888b.  888b    888        d8888 888      .d8888b.
		d88P  Y88b 888     d88P" "Y88b    888    d88P  Y88b      d88P  "88b          d88P  Y88b  888  d88P  Y88b 8888b   888       d88888 888     d88P  Y88b
		Y88b.      888     888     888    888    Y88b.           Y88b. d88P          Y88b.       888  888    888 88888b  888      d88P888 888     Y88b.
		 "Y888b.   888     888     888    888     "Y888b.         "Y8888P"            "Y888b.    888  888        888Y88b 888     d88P 888 888      "Y888b.
			"Y88b. 888     888     888    888        "Y88b.      .d88P88K.d88P           "Y88b.  888  888  88888 888 Y88b888    d88P  888 888         "Y88b.
			  "888 888     888     888    888          "888      888"  Y888P"              "888  888  888    888 888  Y88888   d88P   888 888           "888
		Y88b  d88P 888     Y88b. .d88P    888    Y88b  d88P      Y88b .d8888b        Y88b  d88P  888  Y88b  d88P 888   Y8888  d8888888888 888     Y88b  d88P
		 "Y8888P"  88888888 "Y88888P"     888     "Y8888P"        "Y8888P" Y88b       "Y8888P" 8888888 "Y8888P88 888    Y888 d88P     888 88888888 "Y8888P"
		"""
        ########################################################################
        # SPINE UI Page
        # This is so I don't have to type out "self.root" before every signal line
        btn_grabSpineStartJoint = self.root.btn_grabSpineStartJoint
        line_spineStartJoint = self.root.line_spineStartJoint

        btn_grabSpineEndJoint = self.root.btn_grabSpineEndJoint
        line_spineEndJoint = self.root.line_spineEndJoint

        btn_createSpineModule = self.root.btn_createSpineModule

        btn_spineClearFields = self.root.btn_spineClearFields

        # Functions
        btn_grabSpineStartJoint.clicked.connect(
            lambda: self.grabSelection(line_spineStartJoint, None)
        )
        btn_grabSpineEndJoint.clicked.connect(
            lambda: self.grabSelection(line_spineEndJoint, None)
        )

        # Main
        btn_createSpineModule.clicked.connect(
            lambda: smd.createSpineMD(line_spineStartJoint, line_spineEndJoint)
        )

        btn_spineClearFields.clicked.connect(
            lambda: smd.clearLineFields([line_neckStartJoint, line_neckEndJoint])
        )

        ########################################################################
        # Neck/Head UI Page
        btn_grabNeckStartJoint = self.root.btn_grabNeckStartJoint
        line_neckStartJoint = self.root.line_neckStartJoint

        btn_grabNeckEndJoint = self.root.btn_grabNeckEndJoint
        line_neckEndJoint = self.root.line_neckEndJoint

        btn_createNeckHeadModule = self.root.btn_createNeckHeadModule

        btn_neckClearFields = self.root.btn_neckClearFields

        # Functions
        btn_grabNeckStartJoint.clicked.connect(
            lambda: self.grabSelection(line_neckStartJoint, None)
        )
        btn_grabNeckEndJoint.clicked.connect(
            lambda: self.grabSelection(line_neckEndJoint, None)
        )

        # Main
        btn_createNeckHeadModule.clicked.connect(
            lambda: hmd.createNeckHeadMD(line_neckStartJoint, line_neckEndJoint)
        )

        btn_neckClearFields.clicked.connect(
            lambda: self.clearLineFields([line_neckStartJoint, line_neckEndJoint])
        )

        ########################################################################
        # ARMS UI Page
        btn_clavicle = self.root.btn_grabClavicle
        line_clavicle = self.root.line_clavicle

        btn_shoulder = self.root.btn_grabShoulder
        line_shoulder = self.root.line_shoulder

        btn_wrist = self.root.btn_grabWrist
        line_wrist = self.root.line_wrist

        btn_createArmMD = self.root.btn_createArmMD

        btn_armClearFields = self.root.btn_armClearFields

        btn_createHandModule = self.root.btn_createHandModule

        # Functions
        btn_clavicle.clicked.connect(lambda: self.grabSelection(line_clavicle, None))
        btn_shoulder.clicked.connect(lambda: self.grabSelection(line_shoulder, None))
        btn_wrist.clicked.connect(lambda: self.grabSelection(line_wrist, None))

        # Main
        btn_createArmMD.clicked.connect(
            lambda: amd.createArmMD(line_clavicle, line_shoulder, line_wrist, CTLLIB)
        )

        btn_armClearFields.clicked.connect(
            lambda: self.clearLineFields([line_clavicle, line_shoulder, line_wrist])
        )

        btn_createHandModule.clicked.connect(hamd.createHandModule)

        ########################################################################
        # BIPED LEGS UI PAGE
        btn_placeFootPivots = self.root.btn_placeFootPivots

        btn_grabBipedLegStartJnt = self.root.btn_grabBipedLegStartJnt
        line_bipedLegStartJnt = self.root.line_bipedLegStartJnt

        btn_grabBipedLegEndJnt = self.root.btn_grabBipedLegEndJnt
        line_bipedLegEndJnt = self.root.line_bipedLegEndJnt

        btn_createBipedLegModule = self.root.btn_createBipedLegModule

        btn_bipedLegClearFields = self.root.btn_bipedLegClearFields

        # Functions
        btn_placeFootPivots.clicked.connect(blmd.placeFootPivots)

        btn_grabBipedLegStartJnt.clicked.connect(
            lambda: self.grabSelection(line_bipedLegStartJnt, None)
        )
        btn_grabBipedLegEndJnt.clicked.connect(
            lambda: self.grabSelection(line_bipedLegEndJnt, None)
        )

        btn_createBipedLegModule.clicked.connect(
            lambda: blmd.createBipedLeg(line_bipedLegStartJnt, line_bipedLegEndJnt)
        )

        btn_bipedLegClearFields.clicked.connect(
            lambda: self.clearLineFields([line_bipedLegStartJnt, line_bipedLegEndJnt])
        )

        ########################################################################
        # SPACE SWITCHES UI PAGE
        btn_grabLocalSpaceJnt = self.root.btn_grabLocalSpaceJnt
        line_localSpaceJnt = self.root.line_localSpaceJnt

        btn_grabSpaceSwitchCtrl = self.root.btn_grabSpaceSwitchCtrl
        line_spaceSwitchCtrl = self.root.line_spaceSwitchCtrl

        btn_grabSpaceSwitchModuleType = self.root.btn_grabSpaceSwitchModuleType
        line_spaceSwitchModuleType = self.root.line_spaceSwitchModuleType

        btn_grabSpaceSwitcherCtrl = self.root.btn_grabSpaceSwitcherCtrl
        line_spaceSwitcherCtrl = self.root.line_spaceSwitcherCtrl

        btn_createSpaceSwitch = self.root.btn_createSpaceSwitch
        btn_spaceSwitchClearFields = self.root.btn_spaceSwitchClearFields
        btn_attachSpaceSwitch = self.root.btn_attachSpaceSwitch

        # Functions
        btn_grabLocalSpaceJnt.clicked.connect(
            lambda: self.grabSelection(line_localSpaceJnt, None)
        )
        btn_grabSpaceSwitchCtrl.clicked.connect(
            lambda: self.grabSelection(line_spaceSwitchCtrl, None)
        )
        btn_grabSpaceSwitchModuleType.clicked.connect(
            lambda: self.grabSelection(line_spaceSwitchModuleType, None)
        )
        btn_grabSpaceSwitcherCtrl.clicked.connect(
            lambda: self.grabSelection(line_spaceSwitcherCtrl, None)
        )

        btn_createSpaceSwitch.clicked.connect(
            lambda: space.createSpaceSwitch(
                line_localSpaceJnt,
                line_spaceSwitchCtrl,
                line_spaceSwitcherCtrl,
                line_spaceSwitchModuleType,
            )
        )

        btn_spaceSwitchClearFields.clicked.connect(
            lambda: self.clearLineFields(
                [
                    line_localSpaceJnt,
                    line_spaceSwitchCtrl,
                    line_spaceSwitchModuleType,
                    line_spaceSwitcherCtrl,
                ]
            )
        )

        btn_attachSpaceSwitch.clicked.connect(space.attachToSpaceSwitch)

        ########################################################################
        # UTILITIES UI PAGE
        btn_mirrorCtrls = self.root.btn_mirrorCtrls

        btn_insertJoints = self.root.btn_insertJoints
        btn_insertTwistJoints = self.root.btn_insertTwistJoints
        spin_insertJoints = self.root.spin_insertJoints

        btn_selectNonEndJnts = self.root.btn_selectNonEndJnts

        btn_attachModules = self.root.btn_attachModules

        btn_finalizeRig = self.root.btn_finalizeRig
        line_rigName = self.root.line_rigName

        # Functions
        btn_selectNonEndJnts.clicked.connect(vutil.selectAllNonEndJoints)

        btn_mirrorCtrls.clicked.connect(vutil.mirrorCtrlShapes)

        btn_attachModules.clicked.connect(att.attachModules)

        btn_finalizeRig.clicked.connect(lambda: vutil.finalizeRig(line_rigName))

        ########################################################################
        # STABILIZER SETUP TAB
        btn_grabStabClavJoint = self.root.btn_grabStabClavJoint
        line_stabClavJoint = self.root.line_stabClavJoint

        btn_grabStabShoulderJoint = self.root.btn_grabStabShoulderJoint
        line_stabShoulderJoint = self.root.line_stabShoulderJoint

        btn_grabIkElbowJoint = self.root.btn_grabIkElbowJoint
        line_ikElbowJoint = self.root.line_ikElbowJoint

        btn_grabStabilizerCurve = self.root.btn_grabStabilizerCurve
        line_stabilizeCurve = self.root.line_stabilizeCurve

        btn_grabMultiTwistJoints = self.root.btn_grabMultiTwistJoints
        line_multiTwistJoints = self.root.line_multiTwistJoints

        btn_createStabilizeCurve = self.root.btn_createStabilizeCurve
        btn_stabilizeShoulder = self.root.btn_stabilizeShoulder

        # Functions
        btn_grabStabClavJoint.clicked.connect(
            lambda: self.grabSelection(line_stabClavJoint, None)
        )
        btn_grabStabShoulderJoint.clicked.connect(
            lambda: self.grabSelection(line_stabShoulderJoint, None)
        )
        btn_grabIkElbowJoint.clicked.connect(
            lambda: self.grabSelection(line_ikElbowJoint, None)
        )
        btn_grabStabilizerCurve.clicked.connect(
            lambda: self.grabSelection(line_stabilizeCurve, None)
        )
        btn_grabMultiTwistJoints.clicked.connect(
            lambda: self.grabMultiSelection(line_multiTwistJoints, None)
        )

        btn_createStabilizeCurve.clicked.connect(amd.createStabilizeCurve)
        btn_stabilizeShoulder.clicked.connect(
            lambda: amd.createShoulderStabilizer(
                line_stabClavJoint,
                line_stabShoulderJoint,
                line_ikElbowJoint,
                line_stabilizeCurve,
                line_multiTwistJoints,
            )
        )
        ########################################################################
        # TWIST SETUP TAB
        btn_grabTwistElbowJoint = self.root.btn_grabTwistElbowJoint
        line_twistElbowJoint = self.root.line_twistElbowJoint

        btn_grabTwistWristJoint = self.root.btn_grabTwistWristJoint
        line_twistWristJoint = self.root.line_twistWristJoint

        btn_grabTwistPointerJoint = self.root.btn_grabTwistPointerJoint
        line_twistPointerJoint = self.root.line_twistPointerJoint

        btn_grabTwistSetupJoints = self.root.btn_grabTwistSetupJoints
        line_twistSetupJoints = self.root.line_twistSetupJoints

        btn_createTwistSetup = self.root.btn_createTwistSetup

        btn_twistClearFields = self.root.btn_twistClearFields

        btn_grabTwistElbowJoint.clicked.connect(
            lambda: self.grabSelection(line_twistElbowJoint, None)
        )
        btn_grabTwistWristJoint.clicked.connect(
            lambda: self.grabSelection(line_twistWristJoint, None)
        )
        btn_grabTwistPointerJoint.clicked.connect(
            lambda: self.grabSelection(line_twistPointerJoint, None)
        )
        btn_grabTwistSetupJoints.clicked.connect(
            lambda: self.grabMultiSelection(line_twistSetupJoints, None)
        )

        # Functions
        btn_insertJoints.clicked.connect(
            lambda: vutil.insertJnts2(spin_insertJoints.value())
        )

        btn_insertTwistJoints.clicked.connect(
            lambda: vutil.insertTwistJoints(spin_insertJoints.value())
        )

        btn_createTwistSetup.clicked.connect(
            lambda: vutil.createTwistNetwork(
                line_twistElbowJoint,
                line_twistWristJoint,
                line_twistPointerJoint,
                line_twistSetupJoints,
            )
        )

        btn_twistClearFields.clicked.connect(
            lambda: self.clearLineFields(
                [line_twistElbowJoint, line_twistWristJoint, line_twistSetupJoints]
            )
        )

    """
	888b     d888        d8888 8888888 888b    888      8888888888 888     888 888b    888  .d8888b.   .d8888b.
	8888b   d8888       d88888   888   8888b   888      888        888     888 8888b   888 d88P  Y88b d88P  Y88b
	88888b.d88888      d88P888   888   88888b  888      888        888     888 88888b  888 888    888 Y88b.
	888Y88888P888     d88P 888   888   888Y88b 888      8888888    888     888 888Y88b 888 888         "Y888b.
	888 Y888P 888    d88P  888   888   888 Y88b888      888        888     888 888 Y88b888 888            "Y88b.
	888  Y8P  888   d88P   888   888   888  Y88888      888        888     888 888  Y88888 888    888       "888
	888   "   888  d8888888888   888   888   Y8888      888        Y88b. .d88P 888   Y8888 Y88b  d88P Y88b  d88P
	888       888 d88P     888 8888888 888    Y888      888         "Y88888P"  888    Y888  "Y8888P"   "Y8888P"
	"""

    """
	888     888 8888888      8888888888 888     888 888b    888  .d8888b. 88888888888 8888888 .d88888b.  888b    888  .d8888b.
	888     888   888        888        888     888 8888b   888 d88P  Y88b    888       888  d88P" "Y88b 8888b   888 d88P  Y88b
	888     888   888        888        888     888 88888b  888 888    888    888       888  888     888 88888b  888 Y88b.
	888     888   888        8888888    888     888 888Y88b 888 888           888       888  888     888 888Y88b 888  "Y888b.
	888     888   888        888        888     888 888 Y88b888 888           888       888  888     888 888 Y88b888     "Y88b.
	888     888   888        888        888     888 888  Y88888 888    888    888       888  888     888 888  Y88888       "888
	Y88b. .d88P   888        888        Y88b. .d88P 888   Y8888 Y88b  d88P    888       888  Y88b. .d88P 888   Y8888 Y88b  d88P
	 "Y88888P"  8888888      888         "Y88888P"  888    Y888  "Y8888P"     888     8888888 "Y88888P"  888    Y888  "Y8888P"
	"""

    def grabSelection(self, lineWidget, splitString):
        """
        Grabs selected joint objects and places their names in provided lineWidget in UI
        """
        # sel = cmds.ls(selection=True, type="joint", shortNames=True)
        sel = cmds.ls(selection=True, shortNames=True)

        if splitString == None:
            if not len(sel) > 1:
                lineWidget.setText(sel[0])
            else:
                cmds.error("Please select only one object.")

        # If the user wants to split the selected object's name, input as argument
        else:
            newSel = sel.split(splitString)[0]
            if not len(sel) > 1:
                lineWidget.setText(newSel)
            else:
                cmds.error("Please select only one object.")

    def grabMultiSelection(self, lineWidget, splitString):
        """
        Grabs selected joint objects and places their names in provided lineWidget in UI
        """
        # sel = cmds.ls(selection=True, type="joint", shortNames=True)
        sel = cmds.ls(selection=True, shortNames=True)

        lineText = ",".join(sel)
        lineWidget.setText(lineText)

    def clearLineFields(self, lineWidgets):
        """
        This function clears all text fields provided of any text.
        """
        for line in lineWidgets:
            line.setText("")

    """
	888     888 88888888888 8888888 888      8888888 88888888888 Y88b   d88P
	888     888     888       888   888        888       888      Y88b d88P
	888     888     888       888   888        888       888       Y88o88P
	888     888     888       888   888        888       888        Y888P
	888     888     888       888   888        888       888         888
	888     888     888       888   888        888       888         888
	Y88b. .d88P     888       888   888        888       888         888
	 "Y88888P"      888     8888888 88888888 8888888     888         888
	"""

    def reverseList(self, myList):
        """
        Reverses the order of a given list
        """
        myList.reverse()
        return myList


def run_maya():
    # Run tool in maya
    ms.run_maya(vulcanRig, WINDOW_OBJECT, WINDOW_TITLE, DOCK_WITH_MAYA_UI)
