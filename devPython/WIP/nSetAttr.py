from typing import List, NoReturn

import maya.cmds as mc
import maya.api.OpenMaya as om2

"""
syntax based on grok:
	node.attr = value
	nSetAttr( MSel, attr, value )

do not use om2.MPlugs, !!working backwards is hard!!
	because mc.connectAttr requires valid distinct DAG paths
	and getting full paths of items with identical shortNames
	is hard to do from an MPlug
om2.MObject is much much easier to work forwards with

cast inputs as om2.MSelectionList().add("node.attr")
preferbably using:
	MSL.getSelectionStrings()[n] + "." + "attributeName"
and .add() the above string

.add(node.attr) WILL raise kInvalidParameter if attribute does not exist
so that's the validator settled

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

def nSetAttr(inList:om2.MSelectionList , inAttr, inValue, skipMissing=False) -> NoReturn:
	"""

	gets attributes of


	:param *args:	expects run of om2.
	"""
def nSetAttrDAG()