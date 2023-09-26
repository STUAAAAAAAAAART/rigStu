from typing import List, NoReturn

import maya.cmds as mc
import maya.api.OpenMaya as om2

#beginCode

def rControlCastShape(shapeList:om2.MSelectionList = -1):
	"""
	rControlCastShape
	lazy function for maya
	
	selection syntax: [Parent, Child, Child...]

	connects and disconnects the .create attribute of the target curve
	with a curveShape from a template/source curve node

	expects an MSelectionList of curveshapes;
	the first in the list will be used as the template
	and cast onto the other curveShapes

	:param shapeList:	expects MSelectionList - list of curveShapes
	"""