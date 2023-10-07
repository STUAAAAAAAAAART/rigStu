from typing import List, NoReturn

import maya.cmds as mc
import maya.api.OpenMaya as om2

"""
the inputs of the multMatrix node in maya is arranged in evaluation order
e.g.
	for equation ABCDEFG = M
	multMatrix.matrixIn[] requires inputs to be:
		[G,F,E,D,C,B,A]
"""

#beginCode

def nAutoMultMatrix(inputList:om2.MSelectionList, 
					resultAttr:om2.MSelectionList,
					reverseEval=False) -> om2.MSelectionList:
	"""
	nAutoMultMatrix
	utility function for maya

	selection syntax: [A,B,C,D...]
		reverseEval False -> equation notation
			("ABCD = M")
		reverseEval True  -> evaluation direction
			(CD, then B, then A....)
			(Maya multMatrix default)
	
	:param inputList:	expects om2.MSelectionlist - MObjects of matrix attributes only
	:param resultAttr:	expects om2.MSelectionList - single MObject containing result node.attr to connect to
	:param reverseEval:	expects True/False - see syntax

	:return:	MSelectionList - with MObject containing singular multMatrix DG node
	"""