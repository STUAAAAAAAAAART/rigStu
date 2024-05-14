from typing import List, NoReturn

import maya.cmds as mc
import maya.api.OpenMaya as om2

#beginCode

def mPick(inList:om2.MSelectionList, index:int=0) -> om2.MSelectionList:
	"""
	mPick
	lazy utility for maya

	for quickly making single-item MSelectionList

	:param inList:	expects om2.MSelectionList - any
	:param index:	expects int - nth item in list

	:return:	om2.MSelectionList - with single item
	"""
	returnMSL = om2.MSelectionList()
	try:
		pickNode = inList.getSelectionStrings()[index]
	except:
		return ValueError (f"mPick - out of range: {index} index of {inList.length()-1} indices", )
	returnMSL.add(pickNode)
	return returnMSL