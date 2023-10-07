from typing import List, NoReturn

import maya.cmds as mc
import maya.api.OpenMaya as om2

"""TODO
consider two possibilities:
1. input is of bare joints
2. input is of joints with existing FK nodes

would be easier to make #1 first, and run commands based on the kind of joint required
"""
"""
>> NoFlip IK and 2-point IK (the traditional way)

an IK system without a pole vector constraint will flip
	when the end effector moves past a certain point relative to the base joint
a traditional simple pole vector control and constraint will ensure
	that the elbow/knee will point in the intended direction,
	so long as the user would move that control to the intended spot
a noflip IK setup will ensure that the pole vector controller
	will point forward relative to where the base and end are,
	preventing flips on a polar region about the secondary vector,
	and reducing the amount of user intervention for common swing/walk cycles

NoFlipIK	: good for swing cycles (walking/running, strides)
2-pointIK	: good for direct middle-joint control (climbing overs, stances)

in addition to blending between FK and IK,
	this setup will blend between both kinds of pole vector controls 
"""

def rAutoFK(inJoint:om2.MSelectionList) -> om2.MSelectionList:
	pass # see rAutoFK.py

#beginCode

def rAutoPV(inIKHandle:om2.MSelectionList) -> om2.MSelectionList:
	"""
	rAutoPV
	rigging operation for maya
	split out due to complexity, will be used within rAutoFKIK()

	important note: see dev notes in devPython/nAutoRotateHelper.py

	:return:	om2.MSelectionList of created nodes
	"""

	# create pole vector constraint node
	# create c_control noflip
	# create c_control two-point IK (IK2)
	# 

def rAutoFKIK(inJoints:om2.MSelectionList) -> om2.MSelectionList:
	"""
	rAutoIK
	rigging operation for maya

	makes an FKIK system (e.g. arms, legs)

	:param inJoints:	expects om2.MSelectionlist - 3 joints

	:return:	om2.MSelectionlist - all created nodes
		important connections first in MSL in the following order:
		- FKIK blend attribute MPlug
		- IK Evaluation Joints
		- IK Handle/Solver
		- Controllers: IK, PV, FK(s), IKFK Switch
		-
	"""
	# get joints
	# rAutoFK() each one ->
	# make blendMatrix node and connect FK to index 0 ->
	# make 

def rAutoAddIK(inJoints:om2.MSelectionList) -> om2.MSelectionList:
	"""
	"""