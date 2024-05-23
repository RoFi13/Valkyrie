try:
	reload  # Python 2.7
except NameError:
	try:
		from importlib import reload  # Python 3.4+
	except ImportError:
		from imp import reload  # Python 3.0 - 3.3

from functools import wraps
import maya.cmds as cmds
import maya.mel as mel

def viewportOff( func ):
	"""
	Decorator - turn off Maya display while func is running.
	if func will fail, the error will be raised after.
	"""
	@wraps(func)
	def wrap( *args, **kwargs ):

		# Turn $gMainPane Off:
		mel.eval("paneLayout -e -manage false $gMainPane")

		# Decorator will try/except running the function. 
		# But it will always turn on the viewport at the end.
		# In case the function failed, it will prevent leaving maya viewport off.
		try:
			return func( *args, **kwargs )
		except Exception:
			raise # will raise original error
		finally:
			mel.eval("paneLayout -e -manage true $gMainPane")

	return wrap

# Turns viewport off from refreshing to not slow down the bake process
@viewportOff

def bakeMocapToVulcanRig():
	cmds.undoInfo(chunkName="bakeMocap_chunk", openChunk=True)

	sel = cmds.ls(selection=True)[0]
	ns = sel.split(":")[0]

	animJnts = allJnts(ns)

	# Make sure that rig is in FK mode
	cmds.setAttr("%s:L_armSwitch_CTL.IKFK" % ns, 10)
	cmds.setAttr("%s:R_armSwitch_CTL.IKFK" % ns, 10)
	cmds.setAttr("%s:L_legSwitch_CTL.IKFK" % ns, 10)
	cmds.setAttr("%s:R_legSwitch_CTL.IKFK" % ns, 10)

	allTempNodes = cmds.group(name="temp_constraints_DNT", empty=True)
	for jnt in animJnts:
		# For root
		if jnt == "%s:C_root_CTL" % ns:
			cmds.orientConstraint(animJnts[jnt], jnt, maintainOffset=False)
			cmds.pointConstraint(animJnts[jnt], jnt, maintainOffset=True)

		# For legs
		elif "R_legFK" in jnt or "R_kneeFK" in jnt or "R_footFK" in jnt or "R_toeFK" in jnt:
			parGrp = cmds.group(name="parGrp_" + jnt, empty=True)
			cmds.select(clear=True)
			childGrp = cmds.group(name="childGrp_" + jnt, empty=True)
			# For some reason one child group node contains a "|" in the name so I have filter that out
			if "|" in childGrp:
				childGrp = childGrp[1:]
			cmds.parent(childGrp, parGrp)
			cmds.parentConstraint(animJnts[jnt], parGrp, maintainOffset=False)
			# DISCLAIMER!!!
			# These values below were determined by Lt. Belica Rig from Paragon and are not indicative of
			# a rig and model built from scratch like I would build with legs straight down, toes pointing forward, etc.
			if "R_legFK" in jnt:
				cmds.setAttr(childGrp + ".rx", -90)
				cmds.setAttr(childGrp + ".rz", 85)
			elif "R_kneeFK" in jnt:
				cmds.setAttr(childGrp + ".rx", -90)
				cmds.setAttr(childGrp + ".rz", 90)
			elif "R_footFK" in jnt:
				cmds.setAttr(childGrp + ".rx", -109)
				cmds.setAttr(childGrp + ".ry", 46)
				cmds.setAttr(childGrp + ".rz", 71)
			# If jnt is toe:
			else:
				cmds.setAttr(childGrp + ".rx", -112)
				cmds.setAttr(childGrp + ".ry", 73)
				cmds.setAttr(childGrp + ".rz", 57)

			if "R_kneeFK" in jnt:
				cmds.orientConstraint(childGrp, jnt, skip=("x", "y"), maintainOffset=False)

			cmds.orientConstraint(childGrp, jnt, maintainOffset=False)
			cmds.parent(parGrp, allTempNodes)
		

		# For legs
		elif "L_legFK" in jnt or "L_kneeFK" in jnt or "L_footFK" in jnt or "L_toeFK" in jnt:
			parGrp = cmds.group(name="parGrp_" + jnt, empty=True)
			cmds.select(clear=True)
			childGrp = cmds.group(name="childGrp_" + jnt, empty=True)
			# For some reason one child group node contains a "|" in the name so I have filter that out
			if "|" in childGrp:
				childGrp = childGrp[1:]
			cmds.parent(childGrp, parGrp)
			cmds.parentConstraint(animJnts[jnt], parGrp, maintainOffset=False)
			# DISCLAIMER!!!
			# These values below were determined by Lt. Belica Rig from Paragon and are not indicative of
			# a rig and model built from scratch like I would build with legs straight down, toes pointing forward, etc.
			if "L_legFK" in jnt:
				cmds.setAttr(childGrp + ".rx", 90)
				cmds.setAttr(childGrp + ".rz", -85)
			elif "L_kneeFK" in jnt:
				cmds.setAttr(childGrp + ".rx", 90)
				cmds.setAttr(childGrp + ".rz", -90)
			elif "L_footFK" in jnt:
				cmds.setAttr(childGrp + ".rx", 134)
				cmds.setAttr(childGrp + ".ry", -44)
				cmds.setAttr(childGrp + ".rz", -122)
			# If jnt is toe:
			else:
				cmds.setAttr(childGrp + ".rx", 165)
				cmds.setAttr(childGrp + ".ry", -53)
				cmds.setAttr(childGrp + ".rz", -158)

			if "L_kneeFK" in jnt:
				cmds.orientConstraint(childGrp, jnt, skip=("x", "y"), maintainOffset=False)

			cmds.orientConstraint(childGrp, jnt, maintainOffset=False)
			cmds.parent(parGrp, allTempNodes)
		
		# For spine
		elif "spine" in jnt or "chest" in jnt or "neck" in jnt or "head" in jnt:
			parGrp = cmds.group(name="parGrp_" + jnt, empty=True)
			cmds.select(clear=True)
			childGrp = cmds.group(name="childGrp_" + jnt, empty=True)
			# For some reason one child group node contains a "|" in the name so I have filter that out
			if "|" in childGrp:
				childGrp = childGrp[1:]

			cmds.parent(childGrp, parGrp)
			cmds.parentConstraint(animJnts[jnt], parGrp, maintainOffset=False)
			if "head" in jnt:
				cmds.setAttr(childGrp + ".rx", 90)
				cmds.setAttr(childGrp + ".ry", 30)
				cmds.setAttr(childGrp + ".rz", 90)
			else:
				cmds.setAttr(childGrp + ".rx", 90)
				cmds.setAttr(childGrp + ".rz", 90)

			cmds.orientConstraint(childGrp, jnt, maintainOffset=False)
			cmds.parent(parGrp, allTempNodes)

		# For Arms
		elif "R_clavicle" in jnt or "R_arm" in jnt or "R_elbow" in jnt or "R_wrist" in jnt:
			parGrp = cmds.group(name="parGrp_" + jnt, empty=True)
			cmds.select(clear=True)
			childGrp = cmds.group(name="childGrp_" + jnt, empty=True)
			# For some reason one child group node contains a "|" in the name so I have filter that out
			if "|" in childGrp:
				childGrp = childGrp[1:]
			cmds.parent(childGrp, parGrp)
			cmds.parentConstraint(animJnts[jnt], parGrp, maintainOffset=False)
			cmds.setAttr(childGrp + ".rx", -90)
			# AGAIN!! For Belica Rig for value below!!!
			if "R_wrist" in jnt:
				cmds.setAttr(childGrp + ".rz", -12)

			if "R_elbow" in jnt:
				cmds.orientConstraint(childGrp, jnt, skip=("x", "y"), maintainOffset=False)

			cmds.orientConstraint(childGrp, jnt, maintainOffset=False)
			cmds.parent(parGrp, allTempNodes)

		# For Arms
		elif "L_clavicle" in jnt or "L_arm" in jnt or "L_elbow" in jnt or "L_wrist" in jnt:
			parGrp = cmds.group(name="parGrp_" + jnt, empty=True)
			cmds.select(clear=True)
			childGrp = cmds.group(name="childGrp_" + jnt, empty=True)
			# For some reason one child group node contains a "|" in the name so I have filter that out
			if "|" in childGrp:
				childGrp = childGrp[1:]
			cmds.parent(childGrp, parGrp)
			cmds.parentConstraint(animJnts[jnt], parGrp, maintainOffset=False)
			cmds.setAttr(childGrp + ".rx", 90)
			# AGAIN!! For Belica Rig for value below!!!
			if "L_wrist" in jnt:
				cmds.setAttr(childGrp + ".rz", 12)

			if "L_elbow" in jnt:
				cmds.orientConstraint(childGrp, jnt, skip=("x", "y"), maintainOffset=False)

			cmds.orientConstraint(childGrp, jnt, maintainOffset=False)
			cmds.parent(parGrp, allTempNodes)

		
		# For all Fingers
		else:
			parGrp = cmds.group(name="parGrp_" + jnt, empty=True)
			cmds.select(clear=True)
			childGrp = cmds.group(name="childGrp_" + jnt, empty=True)
			# For some reason one child group node contains a "|" in the name so I have filter that out
			if "|" in childGrp:
				childGrp = childGrp[1:]
			cmds.parent(childGrp, parGrp)
			cmds.parentConstraint(animJnts[jnt], parGrp, maintainOffset=False)
			if "R_" in jnt:
				cmds.setAttr(childGrp + ".rx", -90)
			elif "L_" in jnt:
				cmds.setAttr(childGrp + ".rx", 90)
			# cmds.setAttr(childGrp + ".rz", -180)
			cmds.orientConstraint(childGrp, jnt, maintainOffset=False)
			cmds.parent(parGrp, allTempNodes)			

	# Bake down to FK controls
	animCtrls = [key for key in animJnts]
	endFrame = bakeToFk(animCtrls)

	# Cleanup
	cmds.delete(allTempNodes, "NoitomRobot:Reference")
	print("All Done!")
	cmds.undoInfo(chunkName="bakeMocap_chunk", closeChunk=True)
	

def bakeToFk(animCtrls):
	# Get the last keyframe of the mocap and set time range to accomodate all keyframes
	endFrame = int(cmds.findKeyframe("NoitomRobot:Hips.translateX", which="last") + 1)
	cmds.playbackOptions(animationEndTime=endFrame)

	cmds.bakeResults(animCtrls, simulation=True, time=(0,endFrame), sampleBy=2, oversamplingRate=2, disableImplicitControl=True, preserveOutsideKeys=True, 
		sparseAnimCurveBake=False, removeBakedAttributeFromLayer=False, removeBakedAnimFromLayer=False, bakeOnOverrideLayer=False, 
		minimizeRotation=True, controlPoints=False, shape=True)

	return endFrame

def allJnts(ns):
	# Vulcan controls as keys and mocap jnts as values
	matchJntDict = {
		"%s:C_root_CTL" % ns: "NoitomRobot:Hips",
		"%s:R_legFK_CTL" % ns: "NoitomRobot:RightUpLeg",
		"%s:R_kneeFK_CTL" % ns: "NoitomRobot:RightLeg",
		"%s:R_footFK_CTL" % ns: "NoitomRobot:RightFoot",
		"%s:R_toeFK_CTL" % ns: "NoitomRobot:RightFoot_End",
		
		"%s:L_legFK_CTL" % ns: "NoitomRobot:LeftUpLeg",
		"%s:L_kneeFK_CTL" % ns: "NoitomRobot:LeftLeg",
		"%s:L_footFK_CTL" % ns: "NoitomRobot:LeftFoot",
		"%s:L_toeFK_CTL" % ns: "NoitomRobot:LeftFoot_End",
		
		"%s:C_spine2FK_CTL" % ns: "NoitomRobot:Spine",
		"%s:C_spine3FK_CTL" % ns: "NoitomRobot:Spine2",
		"%s:C_chest_CTL" % ns: "NoitomRobot:Spine3",
		"%s:C_neck1FK_CTL" % ns: "NoitomRobot:Neck",
		"%s:C_headFK_CTL" % ns: "NoitomRobot:Head",
		
		"%s:R_clavicle_CTL" % ns: "NoitomRobot:RightShoulder",
		"%s:R_armFK_CTL" % ns: "NoitomRobot:RightArm",
		"%s:R_elbowFK_CTL" % ns: "NoitomRobot:RightForeArm",
		"%s:R_wristFK_CTL" % ns: "NoitomRobot:RightHand",
		"%s:R_thumb1Bind_CTL" % ns: "NoitomRobot:RightHandThumb1",
		"%s:R_thumb2Bind_CTL" % ns: "NoitomRobot:RightHandThumb2",
		"%s:R_thumb3Bind_CTL" % ns: "NoitomRobot:RightHandThumb3",
		"%s:R_index1Bind_CTL" % ns: "NoitomRobot:RightHandIndex1",
		"%s:R_index2Bind_CTL" % ns: "NoitomRobot:RightHandIndex2",
		"%s:R_index3Bind_CTL" % ns: "NoitomRobot:RightHandIndex3",
		"%s:R_middle1Bind_CTL" % ns: "NoitomRobot:RightHandMiddle1",
		"%s:R_middle2Bind_CTL" % ns: "NoitomRobot:RightHandMiddle2",
		"%s:R_middle3Bind_CTL" % ns: "NoitomRobot:RightHandMiddle3",
		"%s:R_ring1Bind_CTL" % ns: "NoitomRobot:RightHandRing1",
		"%s:R_ring2Bind_CTL" % ns: "NoitomRobot:RightHandRing2",
		"%s:R_ring3Bind_CTL" % ns: "NoitomRobot:RightHandRing3",
		"%s:R_pinky1Bind_CTL" % ns: "NoitomRobot:RightHandPinky1",
		"%s:R_pinky2Bind_CTL" % ns: "NoitomRobot:RightHandPinky2",
		"%s:R_pinky3Bind_CTL" % ns: "NoitomRobot:RightHandPinky3",

		"%s:L_clavicle_CTL" % ns: "NoitomRobot:LeftShoulder",
		"%s:L_armFK_CTL" % ns: "NoitomRobot:LeftArm",
		"%s:L_elbowFK_CTL" % ns: "NoitomRobot:LeftForeArm",
		"%s:L_wristFK_CTL" % ns: "NoitomRobot:LeftHand",
		"%s:L_thumb1Bind_CTL" % ns: "NoitomRobot:LeftHandThumb1",
		"%s:L_thumb2Bind_CTL" % ns: "NoitomRobot:LeftHandThumb2",
		"%s:L_thumb3Bind_CTL" % ns: "NoitomRobot:LeftHandThumb3",
		"%s:L_index1Bind_CTL" % ns: "NoitomRobot:LeftHandIndex1",
		"%s:L_index2Bind_CTL" % ns: "NoitomRobot:LeftHandIndex2",
		"%s:L_index3Bind_CTL" % ns: "NoitomRobot:LeftHandIndex3",
		"%s:L_middle1Bind_CTL" % ns: "NoitomRobot:LeftHandMiddle1",
		"%s:L_middle1Bind_CTL" % ns: "NoitomRobot:LeftHandMiddle2",
		"%s:L_middle1Bind_CTL" % ns: "NoitomRobot:LeftHandMiddle3",
		"%s:L_ring1Bind_CTL" % ns: "NoitomRobot:LeftHandRing1",
		"%s:L_ring1Bind_CTL" % ns: "NoitomRobot:LeftHandRing2",
		"%s:L_ring1Bind_CTL" % ns: "NoitomRobot:LeftHandRing3",
		"%s:L_pinky1Bind_CTL" % ns: "NoitomRobot:LeftHandPinky1",
		"%s:L_pinky1Bind_CTL" % ns: "NoitomRobot:LeftHandPinky2",
		"%s:L_pinky1Bind_CTL" % ns: "NoitomRobot:LeftHandPinky3",
		}

	return matchJntDict



