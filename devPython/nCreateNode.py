from typing import List, NoReturn

import maya.cmds as mc
import maya.api.OpenMaya as om2

class rigStu(): # see 00*.py
	def __init__(self):
		self.rigRoot = om2.MFnDagNode()
		self.jointRoot = om2.MFnDagNode()
		pass 
	def rigRootName(self) -> str:
		return self.rigRoot.fullPathName()
	def jointRootName(self) -> str:
		return self.jointRoot.fullPathName()

#beginCode

	def nCreateNode(self, *argv:str, ignoreLastOdd=False) -> om2.MSelectionList:
		"""
		nCreateNode
		lazy function for maya

		series of function calls: creates and returns DG node
		utilises cmds.createNode() with skipSelect = True

		odd-lengths of arguments will raise error unless overridden
			by ignoreLastOdd=True

		syntax: nCreateNode(type, name, type, name, type, name ...)
		will fall back for string runs in [Lists] or (Tuples,), only in the same syntax

		if input already pre-paired, e.g. [[type,name] , [type,name] ...]
			use nCreateNodeList()

		:param *argv:	expects pairs of strings, comma-seperated (see python)
		:param ignoreLastOdd:	expects True/False, suppress odd-length list error and run up to last valid pair

		:return:	om2.MSelectionList - created nodes
		"""
		# prepare operation list
		# expect 1D list of strings
		inList = None
		if type(argv[0]) == type(list()) or type(argv[0]) == type(tuple()):
			inList = argv[0]
		else:
			inList = argv
		
		# even-numbered list check
		if len(inList) %2 == 1: # if odd numbered. TODO (in general) look into bit checks in python
			if ignoreLastOdd:
				inList.pop()
			else:
				raise ValueError ("nCreateNode: input list has odd-numbered length, check before running again:",len(inList))
		
		makeList = []
		# convert to 2D paired list
		for i in range(len(inList)/2):
			makeList.append([inList[i*2],inList[i*2+1]])

		# make that thing(s)
		return self.nCreateNodeList(makeList)
		# yes i'm this lazy
	
	def nCreateNodeList(self, inList) -> om2.MSelectionList:
		"""
		nCreateNode
		lazy function for maya

		see nCreateNode()
		syntax: nCreateNode(type, name, type, name, type, name ...)

		:param inList:	expects List/Tuple, pairs of strings
		:return:	om2.MSelectionList - created nodes
		"""
		returnList = om2.MSelectionList()
		# make that thing(s)
		for i in inList:
			returnList.add( mc.createNode(i[0] , n=i[1], ss=True) )
		return returnList