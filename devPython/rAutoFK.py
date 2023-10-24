from typing import List, NoReturn

import maya.cmds as mc
import maya.api.OpenMaya as om2

"""
namespace
:c:[joint]FK0
:c:[joint]FK1 [...]

:r:simpleFK:
	t:[joint]FK0
	n:[joint]FK0_multMatrix

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

	def nCreateNode(self, *argv:str, ignoreLastOdd=False) -> om2.MSelectionList:
		pass # see function file
	def nAutoMultMatrix(self, inputList:om2.MSelectionList = None, reverseEval=False) -> om2.MSelectionList:
		pass # see function file
	def nSetAttr(self, inputlist:om2.MSelectionList = None, attr="") -> None:
		pass # see function file

#beginCode

	def rAutoFK(self,
			inJoint:om2.MSelectionList,
			parentGroup:om2.MSelectionList,
			auto:bool = True
			) -> om2.MSelectionList:
		"""
		rAutoFK
		rigging operation for maya

		simple FK controller, separate in DAG hierachy from the joint chain

		return is om2.MSelectionList of the following order:
			c:[joint] - control
			t:[joint] - group
			r:[namespace group]:n:multMatrix - node

		:param inJoint:		expects om2.MSeletionList - list of joints to apply
		:param parentGroup:	expects om2.MSeletionList - object to parent to
		:param auto:		expects True/False - flag to either group this to autoFK, or 
		:return:	om2.MSelectionlist of created nodes, see above
		"""
		#============= TODO 1 check if inJoint has already been autoFK?
		# dumb way: make string attribute in joint and insert namespace of rig operation group
		# hard way: crawl DG network from joint to see connections to transforms and from matrices
			# difficulty: working backwards from MPlugs to DG nodes is not straightforward

		om2.MFnData().

		#============= TODO 2 self.autoFK mobject?
		autoFKgroup = om2.MSelectionList()
		try:
			# self.rigRootName() + "r:autoFK"
			autoFKgroup.add("g:rigRoot|r:autoFK")
		except:
			newNode = mc.createNode("transform", name="r:autoFK", ss=True)
			# newNode self.rigRootName()
			mc.parent(newNode, "g:rigRoot")
			autoFKgroup.add("g:rigRoot|r:autoFK")
		
		autoFKgroup = autoFKgroup.getDagPath(0)
		autoFKgroup = om2.MFnDagNode(autoFKgroup)
		#============= TODO 3 factor in for function being used for a switching system (not necessairly for autoFK)
		# get parent group
		# 	this is either "r:autoFK", or the rig operation namespace group
		# gRootName = self.rigRootName()
		gRootName = "g:rigRoot"


		#=============


		
		
		# get joint
		jointObject = om2.MFnDagNode(inJoint.getDagPath()[0])		
		jointName = jointObject.partialPathName()
		# Returns the minimum path string necessary to uniquely identify the attached object.
		
		"""
		joint:          j:elbow0   :bindRoot| [....] |j:elbow0
		- DAG
		group(control): t:elbow0    :rigRoot|r:autoFK|t:elbow0_FK
		control:        c:elbow0_FK  :rigRoot|r:autoFK|t:elbow0|c:elbow0_FK
		
		- non-DAG
		multMatrix:     r:autoFK:n:elbowFK_mxm
		"""


		# new t:group ->
		# gControl = self.nCreateNode( "transform", "t:"+jointName )
		gControl = mc.createNode("transform", name="t:"+jointName ,ss=True)
		
		# parent to rig root group
		# self.mParent()
		mc.parent(  )

		# new c:control shape/curve ->
		# parent to t: group
		# om2.MSL: A [rigRoot.worldInverse, joint.worldMatrix]
		# om2.MSL: B [t:group.offsetParentMatrix]
		# invoke nAutoMultMatrix with input MSL A result MSL B ->
		# connect c:control.rotate to joint.rotate
		# connect c:control.scale to joint.scale
		
		#============= cleanup
		# lock and hide:
		#	- c_control.translate
		#	- gc_group .translate .rotate .scale
		
		
		self.nSetAttr()
		
