import maya.cmds as cmds

'''
black 1
blue 6
pink? 9
Red 13 
key green 14
white 16
yellow 17
brown 24
dark turqoise 23
aqua marine blue 28
purple 30
pinkish red 31
12 buttons
'''
def drawOverride():
	drawWin = "drawWin"
	if cmds.window(drawWin, exists=True):
		cmds.deleteUI(drawWin)
	if cmds.windowPref(drawWin, exists=True):
		cmds.windowPref(drawWin, remove=True)

	# Opens UI to change
	# Background color is just for the buttons. Determine color using RGB values in the attr editor
	# Pass the integer number for the color variable into the next function
	# Then have the next function use that integer for the overrideColor index designation
	cmds.window("drawWin", title="Drawing Overrides", width=300)
	cmds.gridLayout(numberOfRows=2, numberOfColumns=6, cellWidthHeight=(50, 50))

	# Blue
	cmds.button(" ", backgroundColor=(0,0,1), 
		command="from robwTools.vulcanRig import drawOverride as draw; draw.changeColor(" + str(6) + ")")
	# Red
	cmds.button("  ", backgroundColor=(1,0,0), 
		command="from robwTools.vulcanRig import drawOverride as draw; draw.changeColor(" + str(13) + ")")
	# Yellow
	cmds.button("   ", backgroundColor=(1,1,0), 
		command="from robwTools.vulcanRig import drawOverride as draw; draw.changeColor(" + str(17) + ")")
	# Purple
	cmds.button("    ", backgroundColor=(.784,0,.784), 
		command="from robwTools.vulcanRig import drawOverride as draw; draw.changeColor(" + str(9) + ")")
	# Green
	cmds.button("     ", backgroundColor=(0,1,0), 
		command="from robwTools.vulcanRig import drawOverride as draw; draw.changeColor(" + str(14) + ")")
	# White
	cmds.button("      ", backgroundColor=(1,1,1), 
		command="from robwTools.vulcanRig import drawOverride as draw; draw.changeColor(" + str(16) + ")", )
	# Brown
	cmds.button("       ", backgroundColor=(.631,.412,.188), 
		command="from robwTools.vulcanRig import drawOverride as draw; draw.changeColor(" + str(24) + ")")
	# Dark Turquoise
	cmds.button("        ", backgroundColor=(0,.6,.329), 
		command="from robwTools.vulcanRig import drawOverride as draw; draw.changeColor(" + str(23) + ")")
	# Aqua Blue
	cmds.button("         ", backgroundColor=(.188,.631,.631), 
		command="from robwTools.vulcanRig import drawOverride as draw; draw.changeColor(" + str(28) + ")")
	# Deep Purple
	cmds.button("          ", backgroundColor=(.435,.188,.631), 
		command="from robwTools.vulcanRig import drawOverride as draw; draw.changeColor(" + str(30) + ")")
	# Maroon
	cmds.button("           ", backgroundColor=(.631,.188,.412), 
		command="from robwTools.vulcanRig import drawOverride as draw; draw.changeColor(" + str(31) + ")")
	# Black
	cmds.button("            ", backgroundColor=(0,0,0), 
		command="from robwTools.vulcanRig import drawOverride as draw; draw.changeColor(" + str(1) + ")")

	cmds.showWindow("drawWin")
	
def changeColor(col):
	# Get selection, for each selected object, get shape node, turn on drawOverride and change color
	sel = cmds.ls(selection=True)

	if len(sel) == 1:
		shape = cmds.listRelatives(sel, shapes=True, fullPath=True)[0]
		cmds.setAttr(shape + ".overrideEnabled", True)
		cmds.setAttr(shape + ".overrideRGBColors", False)
		cmds.setAttr(shape + ".overrideColor", int(col))
	else:
		for item in sel:
			allShapes = cmds.listRelatives(item, shapes=True, fullPath=True)
			for shape in allShapes:
				cmds.setAttr(shape + ".overrideRGBColors", False)
				cmds.setAttr(shape + ".overrideEnabled", True)
				cmds.setAttr(shape + ".overrideColor", int(col))