from typing import List, NoReturn

import maya.cmds as mc
import maya.api.OpenMaya as om2

#beginCode

def mGetNode(nodeName:str) -> om2.MSelectionList:
	"""
	mGetNode
	lazy function for maya
	
	returns node in MSelectionList
	(reminder: add nodes to MSL by using MSL.add())

	:param nodeName:	expects string, name of node

	:return:	Node in om2.MObject in MSelectionList

	"""
	mSel = om2.MSelectionList()
	mSel.add(nodeName)
	return mSel

def mGetNodeMany(inList) -> om2.MSelectionList:
	"""
	mGetNodeMany
	lazy function for maya
	
	attempts multiple selection calls (see mGetNode())
	skips and prints 

	om2.MSelectionList unfortunately does not allow strings in lists, so this is that option
	
	:param inList:	expects (tuple,) or [list] of strings, name of nodes

	:return:	om2.MSelectionList - list of nodes
	"""
	mSel = om2.MSelectionList()
	try:
		for i in inList:
			try:
				mSel.add(i)
			except:
				print("mGetNodeMany: invalid input or no MObject selected; skipped:", str(i))
	except:
		raise TypeError("mGetNodeMany: tuple or list expected; if singular or iterating please use mGetNode(). input:", str(input))

	return mSel