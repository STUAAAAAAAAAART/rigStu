"""
TODO proper __init__ and workflow decision:

- base file: skeleton and mesh, bind skin
- workfile: base file (referenced)
- construction script (JSON?): flat rigging operations

"""

"""
TODO reconsider use of n:namespaces...?

unreal engine removes maya namespaces on FBX import
although this only affects bind joints and meshes in practice (export animated FBX)

also, a "soft namespace"(?) approach is already in use with transfrom groups
example outliner / DAG tree: (imagine n:something as n_something)
-------------
>>	rigRoot
>>		r:autoFK
			t:joint0_FK
				c:joint0_FK
			t:joint1_FK
				c:joint1_FK
>>		r:leftArm0_FKIK
			t:ikLogicJoints
				j:leftArm0_ikJoint0
					j:leftArm0_ikJoint1
						j:leftArm0_ikJoint2
				c:leftArm0_IK
					n:leftArm0_ikHandle
				c:leftArm0_PV
			t:shoulderLeft0
				c:shoulderLeft0_FK
			t:elbowLeft0
				c:elbowLeft0_FK
			t:forearmLeft0
				c:forearmLeft0_FK
-------------			


"""


#beginCode
"""
STUART LIM LEARNS TO RIG

written upon Maya 2022 (built-in python 3.7.7)
code not py 2.7.x ready, consider editing directly or use the future package



Dedications:
Jon Macey http://nccastaff.bournemouth.ac.uk/jmacey/
	for deeper insight into DCCs and the quirks of scripting/programming
	and the public resource that is all his lecture notes.
	even now after graduating I'm learning something new from his notes
Vlad Oancea
	for unreleating drive to figure out difficult code
Emma Moisuc
	for rigging talk and comisserating
Nim Mutti
	for showing chaos is not always a bad thing in code
Natalie, Nellie, Neliah
	three little reminders to keep learning


"""

from typing import List, NoReturn

import maya.cmds as mc
import maya.api.OpenMaya as om2

class rigStu():
	def __init__(self, new:bool=True):
		"""
		class rigStu

		__init__
		class expects the following baseline, either created new, or existing in scene


		:param new:	expects True/False: True make required nodes, or False get from scene  
		"""
		
		"""
		class initialisation
		self.rigRoot	<- om2.MFnDagNode - function of g:rigRoot transform/group DAG node
		self.jointRoot	<- om2.MFnDagNode - function of j:jointRoot transform/group DAG node
		"""
		
		self.jointRoot = om2.MSelectionList()	# expects joint "root"
		self.rigRoot = om2.MSelectionList()		# expects transform/group "rigRoot"
		self.autoFKgroup = om2.MSelectionList()	# expects transform/group "r:autoFK"

		initJointRoot = "root"
		initRigRoot = "rigRoot"
		initAutoFK = "r:autoFK"

		# ============= init jointRoot
		try:
			self.jointRoot.add(initJointRoot) # -> if missing, raises (kInvalidParameter): Object does not exist
			# check if joint, in case of multiple 
			if self.jointRoot.getDependNode(0).apiType() != om2.MFn.kJoint:
				raise TypeError(f"class rigStu: {initJointRoot} init fail - scene does not contain joint root 'root' ")
		except:
			raise TypeError(f"class rigStu: {initJointRoot} init fail - scene does not contain joint root 'root' ")
		try: # test if root is parent of world (i.e. not a child of another DAG object)
			self.jointRoot = self.jointRoot.getDagPath(0)
			self.jointRoot = om2.MFnDagNode(self.jointRoot)
			if self.jointRoot.parentCount() > 0:
				raise ValueError (f"class rigStu: {initJointRoot} init fail - {initJointRoot} not child of World (unparented):")
		except:
			raise ValueError (f"class rigStu: {initJointRoot} init fail - MFnDagNode operation fail ({initJointRoot})")

		# ============= init rigRoot
		try:
			self.rigRoot.add(initRigRoot) # -> if missing, raises (kInvalidParameter): Object does not exist
		except:
			if new:
				self.rigRoot.add( mc.createNode("transform", name=initRigRoot, ss=True) )
			else:
				raise TypeError(f"class rigStu: {initRigRoot} init fail - scene does not contain '{initRigRoot}'")
		try: # test if root is parent of world (i.e. not a child of another DAG object)
			self.rigRoot = self.rigRoot.getDagPath(0)
			self.rigRoot = om2.MFnDagNode(self.rigRoot)
			if self.rigRoot.parentCount() > 0:
				raise ValueError (f"class rigStu: {initRigRoot} init fail - '{initRigRoot}' not child of World (unparented):")
		except:
			raise ValueError (f"class rigStu: {initRigRoot} init fail - MFnDagNode operation fail ({initRigRoot})")
		
		# ============= init autoFKgroup
		try:
		#	self.autoFKgroup.add(       "rigRoot|autoFK"      )
			self.autoFKgroup.add(f"{initRigRoot}|{initAutoFK}")
		except:
			newNode = mc.createNode("transform", name=initAutoFK, ss=True)
			mc.parent(newNode,initRigRoot)
			self.autoFKgroup.add(f"{initRigRoot}|{initAutoFK}")
		try:
			self.autoFKgroup = self.autoFKgroup.getDagPath(0)
			self.autoFKgroup = om2.MFnDagNode(self.autoFKgroup)
		except:
			raise ValueError (f"class rigStu: {initAutoFK} init fail - MFnDagNode operation fail, check scene again ({initRigRoot})")

	# ============= functions
	def rigRootName(self) -> str:
		return self.rigRoot.fullPathName()
	def jointRootName(self) -> str:
		return self.jointRoot.fullPathName()
	def autoFKName(self) -> str:
		return self.autoFKgroup.fullPathName()
