from typing import List, NoReturn

import maya.cmds as mc
import maya.api.OpenMaya as om2

"""
namespace
:c:[joint]FK0
:c:[joint]FK1 [...]

:r:autoFK:
	n:[rigGroup][joint]FK0_multMatrix

connection recipe:
[rigRoot].worldInverseMatrix >--> [multMatrix].matrixIn[]
[joint].worldMatrix >--> [multMatrix].matrixIn[]
[controller].inverseMatrix >--> [multMatrix].matrixIn[]

[multMatrix].matrixSum >--> t:[joint]FK0.offsetParentMatrix
"""


class rigStu(): # see 00*.py
	def __init__(self):
		self.rigRoot = om2.MFnDagNode()
		self.jointRoot = om2.MFnDagNode()
		self.autoFKgroup = om2.MFnDagNode()
		pass
	def rigRootName(self) -> str:
		return self.rigRoot.fullPathName()
	def jointRootName(self) -> str:
		return self.jointRoot.fullPathName()
	def autoFKName(self) -> str:
		return self.autoFKgroup.fullPathName()
	
	def nCreateNode(self, *argv:str, ignoreLastOdd=False) -> om2.MSelectionList:
		pass # see function file
	def nAutoMultMatrix(self,
						inputList:om2.MSelectionList, 
						resultAttr:om2.MSelectionList,
						reverseEval=False,
						noOutput=False) -> om2.MSelectionList:
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

		return is a [list] of om2.MSelectionList, depending on number of joint inputs
		om2.MSelectionList of the following order:
			c:[joint] - control
			t:[joint] - group
			r:[namespace group]:n:multMatrix - node

		:param inJoint:		expects om2.MSeletionList - list of joints to apply
		:param parentGroup:	expects om2.MSeletionList - operation group (DAG transform) to parent under
		:param auto:		expects True/False - flag to either group this to autoFK, or 
		:return:	[list] of om2.MSelectionlist of created nodes, see above
		"""
		# ============= TODO 1 check if inJoint has already been autoFK?
		# dumb way: make string attribute in joint and insert namespace of rig operation group
		# hard way: crawl DG network from joint to see connections to transforms and from matrices
			# difficulty: working backwards from MPlugs to DG nodes is not straightforward


		# ============= rigging operation name
		# ============= TODO 2 factor that autoFK will also be used for utility joints
		# ============= TODO 3 factor in for function being used for a switching system (not necessairly for autoFK)
		gRootName = "rigRoot"
		# get parent group
		# 	this is either "r:autoFK", or the rig operation namespace group
		# gRootName = self.rigRootName()
		opGroupShort = ""
		opGroupDagPath = ""
		if auto:
			opGroupDagPath = self.autoFKName()
			opGroupShort = self.autoFKName().split(":")[-1]
		else:
			# reminder: make opGroup node then add to this function
			opGroupDagPath = parentGroup.getDagPath(0).partialPathName()
			opGroupShort = opGroupDagPath.split(":")[-1]
		# =============


		# ============= test for joints from input list
		# TODO - consider function to check items for type
		jointListIter = om2.MItSelectionList(inJoint)
		errorList = []
		while not jointListIter.isDone():
			try:
				# joint test
				if jointListIter.getDependNode().apiType() != om2.MFn.kJoint:
					# node not a joint
					errorList.append(jointListIter.getStrings()[0])
			except:
				# failed getDependNode or apiType
				errorList.append(jointListIter.getStrings()[0])
			# tests passed, continue
			jointListIter.next()
		# if errors occured, raise error
		if len(errorList) > 0:
			raise TypeError ("rAutoFK - following input object(s) not a joint:", str(errorList))
		
		del errorList
		
		"""
		joint:          elbow0   root| [....] |elbow0
		- DAG
		group(control): t:elbow0_FK  :rigRoot|r:autoFK|t:elbow0_FK
		control:        c:elbow0_FK  :rigRoot|r:autoFK|t:elbow0_FK|c:elbow0_FK
		
		- non-DAG
		multMatrix:     n:elbowFK_mxm
		"""
		# all clear
		# ============= do the thing  
		jointListIter.reset()
		returnList = []
		while not jointListIter.isDone():
			returnMSL = om2.MSelectionList()

			jointName = om2.MFnDagNode(jointListIter.getDagPath()).partialPathName()
			# == new t:group ->
			# gControl = self.nCreateNode( "transform", "t:"+jointName )
			gControl = mc.createNode("transform", name=f":t:{jointName}_FK",ss=True)	

			# == parent to operation group
			# self.mParent()
			mc.parent(gControl , opGroupDagPath )

			# == new c:control shape/curve ->
			cControl = mc.circle(name = f":c:{jointName}_FK", nr=[1,0,0], ch = False)
			cControl = cControl[0] #TODO: investigate list return for mc.circle
			# parent to t:gControl
			mc.parent( cControl , gControl )
			returnMSL.add(cControl)
			returnMSL.add(gControl)

			# TODO: replace string formatting with mGetAttr()
			# om2.MSL: A [rigRoot.worldInverse, joint.worldMatrix, control.inverseMatrix]
			# om2.MSL: B [t:group.offsetParentMatrix]
			# == invoke nAutoMultMatrix with input MSL A result MSL B ->
			mxmInput = om2.MSelectionList()
			mxmInput.add(f"{gRootName}.worldInverseMatrix")
			mxmInput.add(f"{jointName}.worldMatrix")
			mxmInput.add(f"{cControl}.inverseMatrix")

			mxmOutput = om2.MSelectionList()
			mxmOutput.add(f"{gControl}.offsetParentMatrix")

			nMultiply = self.nAutoMultMatrix(mxmInput,mxmOutput) # >> om2.MSL of multMatrixNode
			nMultName = (nMultiply.getSelectionStrings()[0])
			mc.rename(nMultName,f":n:{opGroupShort}_{jointName}_mxm")
			returnMSL.merge(nMultiply)

			#TODO nGetAttribute nConnect 
			# connect c:control.rotate to joint.rotate
			# connect c:control.scale to joint.scale
			mc.connectAttr(f"{cControl}.rotate", f"{jointName}.rotate")
			mc.connectAttr(f"{cControl}.scale",  f"{jointName}.scale" )

			#============= cleanup
			# lock and hide:
			#	- c_control.translate
			#	- gc_group .translate .rotate .scale
			# TODO - nSetAttr (just make be following a lot more parametric)
			# self.nSetAttr()
			quickList = [
				f"{cControl}.tx", f"{cControl}.ty", f"{cControl}.tz",
				f"{gControl}.tx", f"{gControl}.ty", f"{gControl}.tz",
				f"{gControl}.rx", f"{gControl}.ry", f"{gControl}.rz",
				f"{gControl}.sx", f"{gControl}.sy", f"{gControl}.sz"
			] # because channel box only displays separate axes and maya isn't that smart 
			for attr in quickList:
				mc.setAttr(attr, lock = True, keyable = False, channelBox = False)

			returnList.append(returnMSL)
			jointListIter.next()

		# everything done
		return returnList