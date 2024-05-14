from typing import List, NoReturn

import maya.cmds as mc
import maya.api.OpenMaya as om2

"""
see: rigStu/nodeNamingConvention.md
"""

"""
om2.MNamespace.getNamespaces(recurse=False)
# Result: [':UI', ':a0', ':b0', ':mesh', ':rig', ':shared'] # 
om2.MNamespace.getNamespaces(recurse=True)
# Result: [':UI', ':a0', ':a0:a1', ':b0', ':mesh', ':rig', ':rig:ug', ':shared'] # 
om2.MNamespace.getNamespaces("a0",recurse=True)
# Result: [':a0:a1'] # 
"""

class rigStu(): # see 00*.py
	def __init__(self):
		self.rigRoot = om2.MFnDagNode()
		self.jointRoot = om2.MFnDagNode()
		pass



#beginCode

	def nAutoRename(inNode, inRigSpace, newName:str, appendName:str = ""):
		"""
		nAutoRename
		utility function for maya

		wrapper for maya's rename function, to conform to desired namespace
		and keep mind off
		"""