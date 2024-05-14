from typing import List, NoReturn

import maya.cmds as mc
import maya.api.OpenMaya as om2

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

#beginCode

	