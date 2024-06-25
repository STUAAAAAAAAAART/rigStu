from typing import List, NoReturn

import maya.cmds as mc
import maya.api.OpenMaya as om2

class rigStu(): # see 00*.py
	def __init__(self):
		self.rigRoot = om2.MFnDagNode()
		self.jointRoot = om2.MFnDagNode()
		pass 

#beginCode

	def mGetAttr(self, inList:om2.MSelectionList, attr:str) -> om2.MSelectionList:
		"""
		mGetAttr
		utility function for maya

		attempts running list of nodes in MSL to get attributes
		and returns MSL with node.attribute MObjects

		parse failures of inList will raise an error
		to prevent propagation of errors down the process

		:param inList:	expects MSelectionList of nodes, NOT MPlugs (refer to mConnect for explanation)
		:param attr:	expects string - to query and gather attributes
		
		:return:	om2.MSelectionList of attributes, use om2.MFnAttribute() on each

		"""
		
		mReturn = om2.MSelectionList()
		mSelIter = om2.MItSelectionList(inList)
		
		getAttrErrors = []
		while not mSelIter.isDone():
			try:
				# DG node extractor
				DGFn = om2.MFnDependencyNode(mSelIter.getDependNode())
				try:
					# playlist while coding:
						# https://www.youtube.com/watch?v=XN758QmTus0
					# om2.MFnDependencyNode().hasAttribute("name") -> bool
						# has attr: True
						# not attr: False
					# om2.MFnDependencyNode().findPlug("name",False) -> MPlug
						# has attr: MPlug class, access selection string with MPlug.name()
						# not attr: !! raise kInvalidParameter
					plugAttr = DGFn.findPlug(attr, False) # >> MObject, attribute
						# not attr: !! raise kInvalidParameter, go to except
					mReturn.add(plugAttr)
				except:
					getAttrErrors.append(mSelIter.getStrings()[0])
					mSelIter.next()
					continue
				mSelIter.next()
			except:
				raise TypeError("mGetAttr: MFnDependencyNode operation failed:",
								mSelIter.getStrings())
		
		if len(getAttrErrors) > 0:
			errorMsg = f"mGetAttr:  Attribute '.{attr}' not found in the following:"
			for i in getAttrErrors:
				errorMsg += "\n" + i
			raise(errorMsg)
		
		del(mSelIter)
		return mReturn