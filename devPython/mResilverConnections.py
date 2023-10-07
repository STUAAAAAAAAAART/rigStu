from typing import List, NoReturn

import maya.cmds as mc
import maya.api.OpenMaya as om2

"""
maya currently does not correct or cleanup
plug removals in attributes containing multiple inputs.

this function aims to automate this
"""

#beginCode

def mResilverConnections(inPlug) -> NoReturn:
	"""
	mResilverConnections
	utility function for maya

	gets attribute that has multiple inputs and re-connects all the plugs
	to remove gaps in connections

	:param inPlug:	expects MSelectionList of singular multi-attribute MObject
	"""
	
	