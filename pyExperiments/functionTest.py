import maya.cmds as mc
import maya.api.OpenMaya as om2

def nAutoMultMatrix(
					inputList:om2.MSelectionList, 
					resultAttr:om2.MSelectionList,
					reverseEval=False,
					noOutput=False
					) -> om2.MSelectionList:
	
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
			print(f"DEBUG: {attr} >-->  {multMatInput}[{intDex}]")
			mc.connectAttr(attr, f"{multMatInput}[{intDex}]")
			intDex += 1
		except:
			raise TypeError( "nAutoMultMatrix - cmds.connectAttr to multMatrix operation failed:", attr)


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
		# test output MSL to ensure all of them are plugs of matrix type
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

def rAutoFK(
		inJoint:om2.MSelectionList,
		) -> om2.MSelectionList:

	gRootName = "rigRoot"
	opGroup = "rigRoot|r:autoFK"

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
		mc.parent(gControl , opGroup )

		# == new c:control shape/curve ->
		cControl = mc.circle(name = f":c:{jointName}_FK", nr=[1,0,0], ch = False)
		cControl = cControl[0] #TODO: investigate list return for mc.circle
		# parent to t:gControl
		mc.parent( cControl , gControl )
		returnMSL.add(cControl)
		returnMSL.add(gControl)

		# om2.MSL: A [rigRoot.worldInverse, joint.worldMatrix]
		# om2.MSL: B [t:group.offsetParentMatrix]
		# == invoke nAutoMultMatrix with input MSL A result MSL B ->
		mxmInput = om2.MSelectionList()
		mxmInput.add(f"{gRootName}.worldInverseMatrix")
		mxmInput.add(f"{jointName}.worldMatrix")

		mxmOutput = om2.MSelectionList()
		mxmOutput.add(f"{gControl}.offsetParentMatrix")

		print("DEBUG >> COMMENCE MULTMATRIX")
		nMultiply = nAutoMultMatrix(mxmInput,mxmOutput) # >> om2.MSL of multMatrixNode
		nMultName = (nMultiply.getSelectionStrings()[0])
		mc.rename(nMultName,f"n:{jointName}_mxm")
		returnMSL.merge(nMultiply)

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