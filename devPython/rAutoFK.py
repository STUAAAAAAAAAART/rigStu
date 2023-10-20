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
	n:[joint]

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

	def rAutoFK(self, inJoint:om2.MSelectionList) -> om2.MSelectionList:
		"""
		rAutoFK
		rigging operation for maya

		simple FK controller, separate in DAG hierachy from the joint chain

		:param inJoint:	expects om2.MSeletionList - list of joints to apply
		
		:return:	om2.MSelectionlist of created nodes, in consecutive order
		"""
		#============= TODO check if Joint already has been autoFK

		

		# get rig root group
		gRootName = self.rigRootName() # ->MFnDAG
		# get joint
		jointObject = om2.MFnDagNode(inJoint.getDagPath()[0])
		
		jointName = jointObject.partialPathName()
		# Returns the minimum path string necessary to uniquely identify the attached object.
		
		# new t:group ->
		"""
		joint:			j:elbow0
		control:		c:elbow0
		group(control):	t:elbow0
		"""
		gControl = self.nCreateNode()
		
		# parent to rig root group
		mc.parent()

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
		
		