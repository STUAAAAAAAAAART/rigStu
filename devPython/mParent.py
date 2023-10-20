from typing import List, NoReturn

import maya.cmds as mc
import maya.api.OpenMaya as om2

"""
Maya API terms work looking into:
- DAG Direct A-cyclic Graph
- DG Dependency Graph

cmds.parent() is a function exclusive to nodes on the DAG
DG nodes without a DAG function/representation cannot be parented

https://help.autodesk.com/cloudhelp/2022/ENU/Maya-Tech-Docs/CommandsPython/parent.html
cmds.parent() syntax:
parent( [dagObject...] [dagObject] ,
		[absolute=boolean],			
		[addObject=boolean],		# funky instancing function, probably avoid
		[noConnections=boolean],
		[noInvScale=boolean],		# specific to joints(.inverseScale)
		[relative=boolean],			# maintains transforms of children
		[removeObject=boolean],
		[shape=boolean],
		[world=boolean]				# unParent everything in list
		)

"""

"""
python: unpacking lists into arguments
https://stackoverflow.com/questions/3480184/pass-a-list-to-a-function-to-act-as-multiple-arguments
list = [a,b c,d]
function(*list)
# effectively does
function(a,b,c,d) 
"""

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

	def mParentMfnDAG(self, *args:om2.MFnDagNode, firstIsParent=False) -> NoReturn:
		"""
		mParentMfnDAG
		utility function for maya

		handler for getting a run of MFnDagNode pointers
		and parenting the DAG objects according to cmds.parent() syntax

		:param *args:	expects run of om2.MFnDagNode
		:param firstIsParent:	expects True/False - if first item should be the Parent instead
		"""
		doList = []
		for i in args:
			doList.append(i.fullpathName())
		
		if len(doList) < 2:
			raise ValueError ("mParentMfnDAG - not enough objects for operation: list length", len(doList))

		# do the thing
		try:
			self.mParentList(doList, firstIsParent)
		except:
			raise("mParentMfnDAG -> mParentList: error raised downstream")
		# yes i'm this lazy

	def mParentMSel(self, inList:om2.MSelectionList, firstIsParent=False) -> NoReturn:
		"""
		mParentMSel
		utility function for maya

		handler for getting DAG nodes in MSelectionList
		and parenting the DAG objects according to cmds.parent() syntax

		ensure MSL contains objects on the DAG only,
		function will raise error if 

		:param inList:	expects om2.MSeletionList of DAG nodes
		:param firstIsParent:	expects True/False - if first item should be the Parent instead
		"""
		mSelIter = om2.MItSelectionList(inList)
		doList = []
		while not mSelIter.isDone():
			doList.append( mSelIter.getDagPath().fullPathName() )
			# om2.MItSelectionList().getDagPath -> om2.MDagPath
			# om2.MDagPath.fullPathName() -> string
			mSelIter.next()
		
		if len(doList) < 2:
			raise ValueError ("mParentMSel - not enough objects for operation: list length", len(doList))

		# do the thing
		try:
			self.mParentList(doList, firstIsParent)
		except:
			raise("mParentMSel -> mParentList: error raised downstream")
		# yes i'm this lazy

	def mParent(self, *args:str, firstIsParent=False) -> NoReturn:
		"""
		mParent
		lazy function for maya
		
		valid DAG paths only, function does not check if paths are valid
		(consider pulling DAG paths from om2 API classes)

		:param *args:	expects run of strings
		:param firstIsParent:	expects True/False - if first item should be the Parent instead
		"""
		
		self.mParentList(args, firstIsParent)
		# yes i'm overthinking this
		

	def mParentList(self, inList, firstIsParent=False) -> NoReturn:
		"""
		mParent
		utility function for maya

		valid DAG paths only, function does not check if paths are valid
		(consider pulling DAG paths from om2 API classes)
		
		:param list:			expects List/Tuple of strings - DAG paths
		:param firstIsParent:	expects True/False - if first item should be the Parent instead
		"""
		doList = inList
		if firstIsParent:
			getParent = doList.pop(0)
			doList.append(getParent)
		mc.parent(*doList)