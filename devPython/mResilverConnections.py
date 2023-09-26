from typing import List, NoReturn

import maya.cmds as mc
import maya.api.OpenMaya as om2

#beginCode

def mResilverConnections(inPlug):
	"""
	mResilverConnections
	utility function for maya

	gets attribute that has multiple inputs and re-connects all the plugs
	to remove gaps in connections

	maya currently does not correct or cleanup plug removals in attributes
	containing multiple inputs, 
	"""