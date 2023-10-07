from typing import List, NoReturn

import maya.cmds as mc
import maya.api.OpenMaya as om2

"""
based on maya's rotateHelper plugin
a legacy node, not well defined due to orentation language of maya
(Z is forward? X is side?)

with regards to cross products of vectors A and B (AxB) and result C:
A = forward vector	= node.up
B = plane vector	= node.forward
C = result vector	= node.rotate

result vector is perpendicular to both A and B
"""

#beginCode

def nAutoRotateHelper(	inList:om2.MSelectionList,
						result:om2.MSelectionList
						) -> om2.MSelectionList:
	"""
	nAutoRotateHelper
	
	:param inList:	expects om2.MSelectionList:
	 	[forwardVector Attribute MObject, upVector Attribute MObject]
	:param result:	expects om2.MSelectionList - result rotation attribute MObject

	:return:	om2.MSelectionList - rotateHelper DG node
	"""