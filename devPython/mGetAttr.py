from typing import List, NoReturn

import maya.cmds as mc
import maya.api.OpenMaya as om2

#beginCode

def mGetAttr(inList:om2.MSelectionList, attr:str) -> om2.MSelectionList:
	"""
	mGetAttr
	utility function for maya

	attempts running list of nodes in MSL to get attributes
	and returns MSL with node.attribute MObjects

	parse failures of inList will raise an error
	to prevent propagation of errors down the process

	:param inList:	expects MSelectionList of nodes, NOT MPlugs (refer to mConnect for explanation)
	:param attr:	expects string - to query and gather attributes
	
	:return:	om2.MSelectionList

	"""
	
	mReturn = om2.MSelectionList()
	mSelIter = om2.MItSelectionList(inList)
	
	getAttrErrors = []
	while not mSelIter.isDone():
		try:
			DGFn = om2.MFnDependencyNode(mSelIter.getDependNode())
			DGNodeName = mSelIter.getStrings()[0]
			if not DGFn.hasAttribute("attr"):
				getAttrErrors.append(DGNodeName)
				mSelIter.next()
				continue
			else:
				mReturn.add(DGNodeName + attr) # <- MObject "Node.attr"
			mSelIter.next()

		except:
			raise TypeError("mGetAttr: MFnDependencyNode operation failed:",
							mSelIter.getStrings())
	
	if len(getAttrErrors) > 0:
		errorMsg = "mGetAttr: Attributes not found in the following:"
		for i in getAttrErrors:
			errorMsg += "\n" + i
		raise(errorMsg)
	
	del(mSelIter)
	return mReturn