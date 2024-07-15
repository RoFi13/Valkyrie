'''
Script for creating custom controllers
'''
import maya.cmds as cmds

def createSphereCtrl(ctrlName):
	crv = cmds.curve( degree = 1, name=ctrlName,
				knot = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
						21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38,
						39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52],
				point = [(0, 1, 0),
						 (0, 0.92388000000000003, 0.382683),
						 (0, 0.70710700000000004, 0.70710700000000004),
						 (0, 0.382683, 0.92388000000000003),
						 (0, 0, 1),
						 (0, -0.382683, 0.92388000000000003),
						 (0, -0.70710700000000004, 0.70710700000000004),
						 (0, -0.92388000000000003, 0.382683),
						 (0, -1, 0),
						 (0, -0.92388000000000003, -0.382683),
						 (0, -0.70710700000000004, -0.70710700000000004),
						 (0, -0.382683, -0.92388000000000003),
						 (0, 0, -1),
						 (0, 0.382683, -0.92388000000000003),
						 (0, 0.70710700000000004, -0.70710700000000004),
						 (0, 0.92388000000000003, -0.382683),
						 (0, 1, 0),
						 (0.382683, 0.92388000000000003, 0),
						 (0.70710700000000004, 0.70710700000000004, 0),
						 (0.92388000000000003, 0.382683, 0),
						 (1, 0, 0),
						 (0.92388000000000003, -0.382683, 0),
						 (0.70710700000000004, -0.70710700000000004, 0),
						 (0.382683, -0.92388000000000003, 0),
						 (0, -1, 0),
						 (-0.382683, -0.92388000000000003, 0),
						 (-0.70710700000000004, -0.70710700000000004, 0),
						 (-0.92388000000000003, -0.382683, 0),
						 (-1, 0, 0),
						 (-0.92388000000000003, 0.382683, 0),
						 (-0.70710700000000004, 0.70710700000000004, 0),
						 (-0.382683, 0.92388000000000003, 0),
						 (0, 1, 0),
						 (0, 0.92388000000000003, -0.382683),
						 (0, 0.70710700000000004, -0.70710700000000004),
						 (0, 0.382683, -0.92388000000000003),
						 (0, 0, -1),
						 (-0.382683, 0, -0.92388000000000003),
						 (-0.70710700000000004, 0, -0.70710700000000004),
						 (-0.92388000000000003, 0, -0.382683),
						 (-1, 0, 0),
						 (-0.92388000000000003, 0, 0.382683),
						 (-0.70710700000000004, 0, 0.70710700000000004),
						 (-0.382683, 0, 0.92388000000000003),
						 (0, 0, 1),
						 (0.382683, 0, 0.92388000000000003),
						 (0.70710700000000004, 0, 0.70710700000000004),
						 (0.92388000000000003, 0, 0.382683),
						 (1, 0, 0),
						 (0.92388000000000003, 0, -0.382683),
						 (0.70710700000000004, 0, -0.70710700000000004),
						 (0.382683, 0, -0.92388000000000003),
						 (0, 0, -1)]
			  )
	return crv

def createCircleCtrl(ctrlName):
	crv = cmds.curve( degree = 3, name=ctrlName,
                knot = [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                point = [(1.9590290622280626, 1.199559335247117e-016, -1.9590290622280595),
                         (-3.1607926519573314e-016, 1.6964330807777285e-016, -2.7704854688859699),
                         (-1.9590290622280606, 1.1995593352471178e-016, -1.9590290622280606),
                         (-2.7704854688859699, 4.9158386540469646e-032, -8.0281737680930749e-016),
                         (-1.9590290622280613, -1.1995593352471173e-016, 1.9590290622280602),
                         (-8.3480134089762987e-016, -1.6964330807777287e-016, 2.7704854688859704),
                         (1.9590290622280595, -1.199559335247118e-016, 1.9590290622280611),
                         (2.7704854688859699, -9.1115751697619806e-032, 1.4880331498201463e-015),
                         (1.9590290622280626, 1.199559335247117e-016, -1.9590290622280595),
                         (-3.1607926519573314e-016, 1.6964330807777285e-016, -2.7704854688859699),
                         (-1.9590290622280606, 1.1995593352471178e-016, -1.9590290622280606)] )
	return crv

def createSquareCtrl(ctrlName):
	square = cmds.curve(d= 1, name=ctrlName, knot = [0, 1, 2, 3, 4],
		p=[ (-12,0,-12),(12,0,-12),(12,0,12),(-12,0,12),(-12,0,-12)])
	return square

def createCubeCtrl(ctrlName):
	cube = cmds.curve(d= 1, name=ctrlName, p=[ (1,1,1),(-1,1,1),(-1,-1,1),(1,-1,1),(1,1,1),(1,1,-1),(1,-1,-1), (-1,-1,-1), (-1,1,-1), (1,1,-1), (-1,1,-1),(-1,1,1), (-1,-1,1),(-1,-1,-1), (1,-1,-1), (1,-1,1)])
	return cube
	
def createPelvisCtrl(ctrlName):
	pelvisCtrl = createCircleCtrl(ctrlName)
	cmds.select(pelvisCtrl + ".cv[1]", pelvisCtrl + ".cv[5]", pelvisCtrl + ".cv[9]", replace=True)
	cmds.move(0,-1.6,0, relative=True, objectSpace=True, worldSpaceDistance=True)
	cmds.select(pelvisCtrl + ".cv[2]", pelvisCtrl + ".cv[4]", pelvisCtrl + ".cv[10]", pelvisCtrl + ".cv[0]", pelvisCtrl + ".cv[6]", pelvisCtrl + ".cv[8]", replace=True)
	cmds.scale(0.65,1,1, relative=True, objectCenterPivot=True)
	return pelvisCtrl

def createIKFKBlendCtrl(side, jnt):
	crv = cmds.curve(degree=1, knot=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
		point=[(18.138634, 0, 17.078199),
		(18.138634, 0, -12.24095),
		(-0.331571, 0, -12.24095),
		(-0.331571, 0, -4.870378),
		(-14.939509, 0, -16.360743),
		(-0.331571, 0, -27.851234),
		(-0.331571, 0, -20.480663),
		(26.783316, 0, -20.480663),
		(26.783316, 0, 17.078199),
		(18.138634, 0, 17.078199) ] )
	# Duplicate curve and rotate 180 degrees
	dupCrv = cmds.duplicate(crv, renameChildren=True)[0]
	cmds.setAttr(dupCrv + ".ry", 180)
	# Combine Shape nodes, group under offset, and rename nodes
	cmds.select(crv, dupCrv, replace=True)
	newCrv = combineShapeNodes()
	newCrvName = cmds.rename(newCrv, "%s%sSwitch_CTL" % (side, jnt) )
	crvOffset = cmds.group(newCrvName, name="%s%sSwitchOffset_GRP" % (side, jnt) )

	return crvOffset

def combineShapeNodes():
	# Grab selection, freeze transforms, and delete history
	sel = cmds.ls(selection=True)
	cmds.makeIdentity(apply=True, translate=True, rotate=True, scale=True, normal=False)
	cmds.delete(constructionHistory=True)
	# Grab shape nodes of selection
	objShape = cmds.listRelatives(sel, shapes=True)
	# For each shape node, parent to single transform node
	# for i in xrange(len(objShape)-1):
	for i in range(len(objShape)-1):
		cmds.parent(objShape[i],sel[-1],add=True, shape=True)
		# Cleanup unused transform nodes
		cmds.delete(sel[i])
		cmds.select(sel[-1], replace=True)

	return sel[-1]