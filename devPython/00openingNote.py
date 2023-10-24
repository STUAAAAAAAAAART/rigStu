"""
TODO proper __init__ and workflow decision:

- base file: skeleton and mesh, bind skin
- workfile: base file (referenced)
- construction script (JSON?): flat rigging operations

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

		self.rigRoot = om2.MSelectionList() # expects transform/group "rigRoot"
		self.jointRoot = om2.MSelectionList() # expects joint ""

		try:
			self.jointRoot.add("j:jointRoot") # -> if missing, raises (kInvalidParameter): Object does not exist
		except:
			raise TypeError("class rigStu: jointRoot init fail - scene does not contain joint root 'j:jointRoot' ")
		try: # test if root is parent of world (i.e. not a child of another DAG object)
			self.jointRoot = self.jointRoot.getDagPath(0)
			self.jointRoot = om2.MFnDagNode(self.jointRoot)
			if self.jointRoot.parentCount() > 0:
				raise ValueError ("class rigStu: jointRoot init fail - j:jointRoot not child of World (unparented):")
		except:
			raise ValueError ("class rigStu: jointRoot init fail - MFnDagNode operation fail (j:jointRoot)")

		try:
			self.rigRoot.add("g:rigRoot") # -> if missing, raises (kInvalidParameter): Object does not exist
		except:
			if new:
				self.rigRoot.add( mc.createNode("transform", name="g:rigRoot") )
			else:
				raise TypeError("class rigStu: rigRoot init fail - scene does not contain 'g:rigRoot'")
		try: # test if root is parent of world (i.e. not a child of another DAG object)
			self.rigRoot = self.rigRoot.getDagPath(0)
			self.rigRoot = om2.MFnDagNode(self.rigRoot)
			if self.rigRoot.parentCount() > 0:
				raise ValueError ("class rigStu: rigRoot init fail - 'g:rigRoot' not child of World (unparented):")
		except:
			raise ValueError ("class rigStu: rigRoot init fail - MFnDagNode operation fail (g:rigRoot)")
		

	def rigRootName(self) -> str:
		return self.rigRoot.fullPathName()
	def jointRootName(self) -> str:
		return self.jointRoot.fullPathName()
