from typing import List, NoReturn

import maya.cmds as mc
import maya.api.OpenMaya as om2

"""
the inputs of the multMatrix node in maya is arranged in evaluation order
e.g.
	for equation ABCDEFG = M
	multMatrix.matrixIn[] requires inputs to be:
		[G,F,E,D,C,B,A]
"""

class rigStu(): # see 00*.py
	def __init__(self):
		self.rigRoot = om2.MFnDagNode()
		self.jointRoot = om2.MFnDagNode()
		pass 

	def mGetAttr(self, inList:om2.MSelectionList, attr:str) -> om2.MSelectionList:
		pass # see function file

#beginCode

	def nAutoMultMatrix(self,
					 	inputList:om2.MSelectionList, 
						resultAttr:om2.MSelectionList,
						reverseEval=False) -> om2.MSelectionList:
		"""
		nAutoMultMatrix
		utility function for maya

		selection syntax: [A,B,C,D...]
			reverseEval False -> equation notation
				("ABCD = M")
			reverseEval True  -> evaluation direction
				(CD, then B, then A....)
				(Maya multMatrix default)
		
		no provisions for renaming in this function; cmds.rename() after calling this function
		
		use mGetAttr() to quickly get and validate attrs/plugs for this function
		the multMatrix node requires and outputs matrix values
		see also: cmds.connectAttr() 
		
		:param inputList:	expects om2.MSelectionlist - MObjects of matrix attributes only
		:param resultAttr:	expects om2.MSelectionList - single MObject containing result node.attr to connect to
		:param reverseEval:	expects True/False - see syntax

		:return:	MSelectionList - MObject of multMatrix DG node
		"""
		
		# test input MSL to ensure all of them are plugs
		# TODO leave this check in? or expect in good faith that inputs are sanatised?
		inIter = om2.MItSelectionList(inputList)
		while not inIter.isDone():
			try: inIter.getPlug()
			except:
				raise TypeError ("nAutoMultMatrix - item in MSList not an attribute: " + inIter.getStrings()[0])
		del inIter

		self.mGetAttr()

		

		# do the thing
		sequence = inputList.getSelectionStrings()
		
		if not reverseEval: # inputList is not in maya's multMatrix order
			sequence = list(sequence).reverse()
		
		multMat = mc.createNode("multMatrix")
		multMatInput = multMat + ".matrixIn"
		
		for attr in sequence:
			try: mc.connectAttr(attr, multMatInput)
			except:
				raise TypeError( "nAutoMultMatrix - cmds.connectAttr operation failed:" )

		# test for output
		try:
			resultAttr.getSelectionStrings()
			try:
				# test if plug
				testPlug = resultAttr.getPlug(0)
			except:
				print("nAutoMultMatrix - no valid attrs found in MSL, skipping output connection")
				return om2.MSelectionList().add(multMat)
			try:
				# is plug; test if matrix attribute
				testPlug.
			except:
				print( "nAutoMultMatrix - invalid output target, expected matrix attribute:", )
		except:
			print("nAutoMultMatrix - resultAttr MSL operation failed, skipping output connection")
			return om2.MSelectionList().add(multMat)
		
		# any attr found, test if matrix
		outAttr = resultAttr.getSelectionStrings()[0]
		if ".m" not in outAttr:
			print("nAutoMultMatrix - resultAttr not a matrix, skipping output connection")

		# valid attr found 
		
		mc.connectAttr(multMat+"matrixOut" , )
		return om2.MSelectionList().add(multMat)

		