from typing import List, NoReturn

import maya.cmds as mc
import maya.api.OpenMaya as om2

class rigStu():
	def __init__(self):
		pass # see 00*.py

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
		#============= check if Joint already has been autoFK

		# get rig root group
		gRoot = om2.MSelectionList()
		gRoot.add("rigStu0")
			# TODO change this when main class defines/holds rig root 
		gRootName = gRoot.getSelectionStrings()[0]
		# new gc_ group ->
		# parent to rig root group
		gControl = om2.MSelectionList()
			# TODO just make the createnode wrapper
			# seperate the parent operation to make it a conscious decision
			#	rather than to piggyback on the cmds.creadeNode command
		gControl.add(mc.createNode("transform",n="",p=gRootName))
		
		# new c_ control shape/curve ->
		# parent to gc_ group
		# om2.MSL: A [rigRoot.worldInverse, joint.worldMatrix]
		# om2.MSL: B [gc_group.offsetParentMatrix]
		# invoke nAutoMultMatrix with input MSL A result MSL B ->
		# connect c_control.rotate to joint.rotate
		# connect c_control.scale to joint.scale
		
		#============= cleanup
		# lock and hide:
		#	- c_control.translate
		#	- gc_group .translate .rotate .scale
		
		self.nSetAttr()
		