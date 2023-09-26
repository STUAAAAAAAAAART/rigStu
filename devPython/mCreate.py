from typing import List, NoReturn

import maya.cmds as mc
import maya.api.OpenMaya as om2

#beginCode

def mCreate(node, name=None) -> om2.MSelectionList:
	"""
	mCreate
	utility function for maya

	series of function calls: creates and returns DG node
	"""