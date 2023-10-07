from typing import List, NoReturn

import maya.cmds as mc
import maya.api.OpenMaya as om2

"""
note fallback behaviour of cmds.rename()
https://help.autodesk.com/cloudhelp/2022/ENU/Maya-Tech-Docs/CommandsPython/rename.html
"""

#beginCode

def mRename(inNode:om2.MSelectionList, name:str) -> NoReturn:
	"""
	mRename
	lazy utility for maya

	quickly renames DG/DAG node without retyping MSL lines
	
	:param inNode:	expects om2.MSelectionList - singular node to be renamed
	:param name:	expects string - new name
	"""
	
	nodeName = inNode.getSelectionStrings()[0]
	mc.rename(nodeName,name)