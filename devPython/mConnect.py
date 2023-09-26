"""

motivation:
	MPlugs aren't used for inputs, because of limited ready name information
	from the available MPlug functions, without having to work backward to
	the DG node that owns the plug.

	this command works as such for DAG nodes:
	- MSelectionList.getSelectionList() -> tuple(str,str,...): full DAG paths
	- for each pair of the list ( using MItSelectionList() ):
		- MSelectionList.getPlug() -> MObject[MPlug]: will raise error if not a plug
		- if either fails, skip pair
		- otherwise mc.connectAttr(first, other)
	
	the path from an MPlug to a usable DAG-specific connectAttr command would be:
	- MPlug.name() -> str: "shortname.attr", not the FULL DAG name
	- MPlug.node() -> MObject
	- MSelectionList().add(MObject) -> MSL
	- MSelectionList.getSelectionList()[0] -> str: full DAG name of source node
	- string maths: (DAG name) - (source node shortname) + (MPlug.name())
		- repeat above for other plug, possibly with one MSL pass by .add()ing twice
	- mc.connectAttr(first, other)

	additional notes:
		while mc.connectAttr is used,
		the om2 implementation of that function is possible
		however it requires to be properly registed in maya's plugin system
		and an undo/redo function to be present
		https://jamesbdunlop.github.io/om2intro/2020/01/13/om2vscmds03.html

"""

""" TODO
when querying connections, the plug may belong to a multi-attribute
joint4.matrix -> mxmTestAttr0.matrixIn[0]
joint5.matrix -> mxmTestAttr0.matrixIn[1] 
consider situations where breaking specific connections may be needed
or breaking all connections to the multi-attribute

"""

from typing import List, NoReturn

import maya.cmds as mc
import maya.api.OpenMaya as om2

#beginCode

def mConnect(list:om2.MSelectionList) -> NoReturn:
	"""
	mConnect
	utility function for maya

	connects two MObjects holding attributes,
	according to default mc.connectAttr() settings

	a longer MSelectionList will chain multiple connection commands
	[from, to, from, to, from, to, ... ]

	:param list:	expects om2.MSelectionList - list of from-to pairs of MObjects containing MPlugs

	"""
	mIter = om2.MItSelectionList(list)
	while not mIter.isDone():
		# fromAttr->
		fromAttr = mIter.getStrings()[0]
		mIter.next()
		if mIter.isDone(): break # because there is nothing left to connect to
		# ->toAttr
		toAttr = mIter.getStrings()[0]
		try:
			mc.connectAttr(fromAttr, toAttr)
		except:
			raise("mConnect - mc.connectAttr operation failed, check work before debugging:", fromAttr,"->", toAttr)
		mIter.next()
		

	return


def mConnectStr(fromPlug:str, toPlug:str) -> NoReturn:
	"""
	mConnectStr
	lazy function for maya

	see mConnect
	this function is fall-forward to mConnect()
	by taking in name string to test for MPlug, and then passed to mc.connectAttr()

	:param fromPlug:	expects str - name of source plug
	:param toPlug:		expects str - name of destination plug

	"""
	testPlug = []
	for i in [fromPlug,toPlug]:
		getPlug = om2.MSelectionList().add(i)
			# new MSL
			# add MObject via string, !! raises error if not available
		try:
			getPlug.getPlug(0) # -> MPlug: just a test
			# get MPlug in MObject, !! raises error if not an MPlug
			# WARNING: MPlug NAME FUNCTIONS RETURNS RELATIVE NAME.ATTR, 
			# 	AND DOES NOT AUTORESOLVE FOR DAG PATH,
			#	MAKING THIS PRONE TO ERRORS WHEN DAG OBJECTS
			#	HAS IDENTICAL DAG SHORTNAMES
			# this is why i'm not utilising the MPlug
			#	and instead am falling back to the full DAG path
		except:
			raise TypeError("mConnectStr - MPlug not found from string:", i)
		testPlug.append(getPlug.getSelectionStrings()[0])
	try:
		mc.connectAttr(testPlug[0], testPlug[1])
	except:
		raise("mConnectStr - mc.connectAttr operation failed, check work before debugging:", testPlug[0],"->", testPlug[1])
