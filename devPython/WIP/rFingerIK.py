from typing import List, NoReturn

import maya.cmds as mc
import maya.api.OpenMaya as om2

"""
>> Finger IK

based on human hand -logy -thingy, consider adjustments on other factors

terminology:
joint0  ->  joint1  ->  joint2  ->  jointIK
|   Proximal   |   Middle   |   Distal   |
P-M-D

thumbs have no middle phalange (also thumb use regular noflip IK)

joint hierachy:

j0
	↳ j1
		↳ j2
			↳ j_IK
	↳ jCopy1
		↳ jCopy2

jCopy1 is positionally at j1
jCopy2 is positionally at j_IK
				
two cases:
- M+D shorter than P or equal
	- noflipIK j0-jCopy1-jCopy2
	- simpleIK j1-j2-j_IK
	- simple pole vector simpleIK, parent and offset to j1
	- noflip pole vector noflipIK
	- get bind position of IK controller (where translate = 0)
	- 
	- get distance from j0 to j_IK
		+ node: distanceBetween
		- if longer than rest position distance of j0-j_IK, add difference to jCopy2 joint distance
			- jCopy2 joint distance capped at M+D
		- if shorter than rest position distance of j0-j_IK, pass 
- M+D longer than P
	- see above, but:
	- get distance from j0 to j_IK
		- if longer than rest position distance of j0-j_IK, add difference to jCopy2 joint distance
			- jCopy2 joint distance capped at M+D
		- if shorter than rest position distance of j0-j_IK, lerp (P and M+D difference) and subtract from jCopy2 joint distance

to simplify:
	- get distance from j0 to j_IK 
		- get difference with rest position distance of j0-j_IK, offset difference to jCopy2 joint distance
			- jCopy2 joint distance maximum at M+D
			- jCopy2 joint distance minimum at 2(M+D) - P
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

	def rAutoFK(self,
				inJoint:om2.MSelectionList,
				parentGroup:om2.MSelectionList,
				auto:bool = True
				) -> om2.MSelectionList:
		pass # see rAutoFK.py

#beginCode

	def rFingerIK(inFinger:om2.MSelectionList) -> om2.MSelectionList:
		"""
		rFingerIK
		rigging operation for maya

		dual-IK driver, optimised for Proximal-Middle-Distal fingers (i.e. 3 rotational joints and 1 end effector joint)
		see code notes at rFingerIK.py for full theory


		:return:	om2.MSelectionList of created nodes
		"""

		# get joints, count them 4 [j0 j1 j2 j_IK]
		# make logic copy, reparent to opGroup
		# make new joints jCopy1 and jCopy2 (see code notes)
			# ensure orientation, use j2 as guide
	
	def rThumbIK(inFinger:om2.MSelectionList) -> om2.MSelectionList:
		"""
		rThumbIK
		rigging operation for maya

		turns out it's more complex than i've expected. oops
		
		:return:	om2.MSelectionList of created nodes
		"""