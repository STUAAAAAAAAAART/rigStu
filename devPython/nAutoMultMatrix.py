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

#beginCode

	def nAutoMultMatrix(self,
						inputList:om2.MSelectionList, 
						resultAttr:om2.MSelectionList,
						reverseEval=False,
						noOutput=False) -> om2.MSelectionList:
		"""
		nAutoMultMatrix
		utility function for maya

		selection syntax: [A,B,C,D...]
			reverseEval False -> equation notation
				("ABCD = M")
			reverseEval True  -> evaluation direction (Maya)
				(CD, then B, then A....)
				(Maya multMatrix default)
		
		no provisions for renaming in this function; cmds.rename() after calling this function
		
		use mGetAttr() to quickly get and validate attrs/plugs for this function
		the multMatrix node requires and outputs matrix values
		see also: cmds.connectAttr() 
		
		:param inputList:	expects om2.MSelectionlist - MObjects of matrix attributes only
		:param resultAttr:	expects om2.MSelectionList - MObjects containing result node.attr to connect to
		:param reverseEval:	expects True/False - see syntax
		:param noOutput:	expects True/False - verbose: flag True to skip connecting output items. invalid or empty list will raise error

		:return:	MSelectionList - MObject of multMatrix DG node
		"""
		
		# test input MSL to ensure all of them are plugs
		# TODO leave this check in? or expect in good faith that inputs are sanatised?
		inIter = om2.MItSelectionList(inputList)
		while not inIter.isDone():
			try: inIter.getPlug()
			except:
				raise TypeError ("nAutoMultMatrix - inputList item in MSList not an attribute: " + inIter.getStrings()[0])
			inIter.next()
		del inIter

		# do the thing
		sequence = inputList.getSelectionStrings()
		
		if not reverseEval: # inputList is not in maya's multMatrix order
			sequence = list(sequence)
			sequence.reverse()
		
		multMat = mc.createNode("multMatrix")
		multMatInput = f"{multMat}.matrixIn"
		intDex = 0
		
		for attr in sequence:
			# IMPORTANT FOR ATTRIBUTE-ARRAYS[n]: INDEX MUST BE SPECIFIED, connectAttr() IS NOT SMART
			# TODO: look into nextAvailable flag in connectAttr() and why it's refusing to work
			try:
				mc.connectAttr(attr, f"{multMatInput}[{intDex}]")
				intDex += 1
			except:
				raise TypeError( "nAutoMultMatrix - cmds.connectAttr to multMatrix operation failed:", attr)
		del intDex

		if noOutput:
			# no output. return node immediately
			return om2.MSelectionList().add(multMat) # >> MSelectionList


		# test for output
		errors = []
		attrList = []
		multOutAttr = om2.MSelectionList()
		multOutAttr.add(f"{multMat}.matrixSum")
		multOutAttr = om2.MFnAttribute(multOutAttr.getPlug(0).attribute())
		try:
			# test output MSL to ensure all of them can connect
			outIter = om2.MItSelectionList(resultAttr)
			while not outIter.isDone():
				hasError = False				
				try:
					# ============= see pyExperiments/openMayaNotes_MFnData_Vals.md
					plugAttr = om2.MFnAttribute(outIter.getPlug().attribute())
					if multOutAttr.acceptsAttribute(plugAttr):
						attrList.append( outIter.getStrings()[0] )
						# test passed, next item
						outIter.next()
						continue
					else:
						hasError = True # not matrix attribute type that .matrixSum expects

				except:
					hasError= True # om2 MPlug MDataHandle operation chain failed
					pass
				if hasError:
					errors.append( outIter.getStrings()[0] )
				outIter.next()
			del outIter
		except:	# MSL operation failed
			raise TypeError ("nAutoMultMatrix - om2.MSelectionList operation failed:", str(resultAttr))

		# check for any erros caught
		if len(errors) > 0: # raise error if there are attributes that aren't matrices
			raise TypeError ("nAutoMultMatrix - following attributes for output incompatible, stopping:", str(errors))
		
		# output list all good! connect them all!
		multMatOutput = f"{multMat}.matrixSum" # yes, this is what it's called
		for n in attrList:
			mc.connectAttr(multMatOutput, n)
		

		# finally
		return om2.MSelectionList().add(multMat) # >> MSelectionList