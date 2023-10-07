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

# You can use both Maya Python API 1.0 and Maya Python API 2.0 in the same script.
# However, you cannot pass an API 1.0 object to an API 2.0 method and vice versa.


class rigStu():
	def __init__(self):
		pass


def mGetNode(nodeName:str) -> om2.MSelectionList:
	"""
	mGetNode
	lazy function for maya
	
	returns node in MSelectionList
	(reminder: add nodes to MSL by using MSL.add())

	:param nodeName:	expects string, name of node

	:return:	Node in om2.MObject in MSelectionList

	"""
	mSel = om2.MSelectionList()
	mSel.add(nodeName)
	return mSel

def mGetNodeMany(inList) -> om2.MSelectionList:
	"""
	mGetNodeMany
	lazy function for maya
	
	attempts multiple selection calls (see mGetNode())
	skips and prints 

	om2.MSelectionList unfortunately does not allow strings in lists, so this is that option
	
	:param inList:	expects (tuple,) or [list] of strings, name of nodes

	:return:	om2.MSelectionList - list of nodes
	"""
	mSel = om2.MSelectionList()
	try:
		for i in inList:
			try:
				mSel.add(i)
			except:
				print("mGetNodeMany: invalid input or no MObject selected; skipped:", str(i))
	except:
		raise TypeError("mGetNodeMany: tuple or list expected; if singular or iterating please use mGetNode(). input:", str(input))

	return mSel

def mGetAttr(inList:om2.MSelectionList, attr:str) -> om2.MSelectionList:
	"""
	mGetAttr
	utility function for maya

	attempts running list of nodes in MSL to get attributes
	and returns MSL with node.attribute MObjects

	parse failures of inList will raise an error
	to prevent propagation of errors down the process

	:param inList:	expects MSelectionList of nodes, NOT MPlugs (refer to mConnect for explanation)
	:param attr:	expects string - to query and gather attributes
	
	:return:	om2.MSelectionList

	"""
	
	mReturn = om2.MSelectionList()
	mSelIter = om2.MItSelectionList(inList)
	
	getAttrErrors = []
	while not mSelIter.isDone():
		try:
			DGFn = om2.MFnDependencyNode(mSelIter.getDependNode())
			DGNodeName = mSelIter.getStrings()[0]
			if not DGFn.hasAttribute("attr"):
				getAttrErrors.append(DGNodeName)
				mSelIter.next()
				continue
			else:
				mReturn.add(DGNodeName + attr) # <- MObject "Node.attr"
			mSelIter.next()

		except:
			raise TypeError("mGetAttr: MFnDependencyNode operation failed:",
							mSelIter.getStrings())
	
	if len(getAttrErrors) > 0:
		errorMsg = "mGetAttr: Attributes not found in the following:"
		for i in getAttrErrors:
			errorMsg += "\n" + i
		raise(errorMsg)
	
	del(mSelIter)
	return mReturn

def mConnect(list:om2.MSelectionList) -> NoReturn:
	"""
	mConnect
	utility function for maya

	connects two MObjects holding attributes,
	according to default mc.connectAttr() settings

	a longer MSelectionList will chain multiple connection commands
	[from, to, from, to, from, to, ... ]

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

""" TODO
when querying connections, the plug may belong to a multi-attribute
joint4.matrix -> mxmTestAttr0.matrixIn[0]
joint5.matrix -> mxmTestAttr0.matrixIn[1] 
consider situations where breaking specific connections may be needed
or breaking all connections to the multi-attribute

"""


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


def mResilverConnections(inPlug):
	"""
	mResilverConnections
	utility function for maya

	gets attribute that has multiple inputs and re-connects all the plugs
	to remove gaps in connections

	maya currently does not correct or cleanup plug removals in attributes
	containing multiple inputs, 
	"""

def mParent(list, firstIsParent=False):
	"""
	mParent
	utility function for maya

	gets MSelection List of DAG nodes, making the end of the list the parent of the rest

	
	:param list:			expects MSelectionList - pipe input through getDAG() before invoking this function
	:param firstIsParent:	expects True/False - if first item should be the Parent instead

	"""


def mCreate(node, name=None) -> om2.MSelectionList:
	"""
	mCreate
	utility function for maya

	series of function calls: creates and returns DG node
	"""


def mGetNodeConnection(inNode, direction, excludeSelf=False) ->  om2.MSelectionList:
	"""
	mGetNodeConnection
	utility function for maya

	returns list of nodes connected to selected node, querying direction required
	
	code re-wrap based on om2.MItDependencyGraph
		https://help.autodesk.com/view/MAYAUL/2022/ENU/?guid=Maya_SDK_cpp_ref_class_m_plug_html
		https://download.autodesk.com/us/maya/2011help/API/class_m_it_dependency_graph.html
		https://help.autodesk.com/view/MAYAUL/2022/ENU/?guid=Maya_SDK_py_ref_class_open_maya_1_1_m_it_dependency_graph_html
	
	code based on:
		https://stackoverflow.com/a/18738405
		https://ehsanhm.wordpress.com/2022/02/02/maya-api-notes-click-for-more/
			- for getting MPlugs of both ends of a node connection (especially the downstream one)
			- ( for cnn in cnns: ) 
		https://web.archive.org/web/20181017223955/http://www.chadvernon.com/blog/resources/maya-api-programming/introduction-to-the-maya-api/

	:param inNode:		expects om2.MObject, has soft fallback for om2.MSelectionList (no string, use select function first)
	:param direction:	expects "upstream", "downstream", or just "up" or "down" - for querying up- or down-stream connections
	:param excludeSelf:	expects True/False - exclude connections that originate from and connects to itself

	:return: om2.MSelectionList of resultant plugs, or =None if empty
		- return structure is listed in the form of plug(0), plug(1), plug(2), plug(3), plug(4), plug(5)...
		- where plug(0) -> plug(1); plug(2) -> plug(3); plug(4) -> plug(5)...
		- if upstream query, return list is expected to be otherNode.attr -> queryNode.attr etc
		- if downstream query, return list is expected to be queryNode.attr -> otherNode.attr etc
		- "queryNode" refers/relates to the input node "inNode" in param
	"""
	# ============= setup
	nodeDir = 'Z'
	if str(direction[0]) in "uU1":
		nodeDir = om2.MItDependencyGraph.kUpstream # -> int 1, 
	if str(direction[0]) in "dD0":
		nodeDir = om2.MItDependencyGraph.kDownstream # -> int 0
	if str(nodeDir) not in "01":
		raise ValueError('invalid node direction specified; expected: "upwards", "downwards')

	queryMObject = None
	# irrational sanity: soft fail if input is MSelectionList instead of MObject
	if type(inNode) == type(om2.MSelectionList()):
		print("caution: function designed for single MObject and not a list of. First item used instead")
		try:
			queryMObject = inNode.getDependNode(0)
		except:
			raise TypeError("mGetNodeConnection 01 - attempt to pull om2.MSelectionList failed")
	else:
		queryMObject = inNode

	# ============= function
	returnNodes = om2.MSelectionList() # -> MSelectionList: create return object

	print("nodeDirection: ", nodeDir)
	# Create a dependency graph iterator for our current object:
	print("")

	# existing value reminders from above:
#	nodeDir # 1 = upstream; 0 = downstream
#	queryMObject # holds input node
#	queryNodeName # has name of input node
	
	queryNodeFn = om2.MFnDependencyNode(queryMObject)
	queryNodeConnections = queryNodeFn.getConnections()
	for i in queryNodeConnections:
		if nodeDir: # upstream -> queryNode -> downstream
			# UPSTREAM QUERY: otherNode -> queryNode
			in_plugs = i.connectedTo(True, False)  #asDst, asSrc - query node as ->destination, or as source->
			for in_plug in in_plugs:
				print('{} -> {}'.format(in_plug.name(), i.name()))
				if excludeSelf and in_plug.name().split(sep=".")[0] == i.name().split(sep=".")[0]:
					continue
				returnNodes.add(in_plug)
				returnNodes.add(i)
		else:
			# DOWNSTREAM QUERY: queryNode -> otherNode
			out_plugs = i.connectedTo(False, True)  #asDst, asSrc
			for out_plug in out_plugs:
				print('{} -> {}'.format(i.name(), out_plug.name()))
				if excludeSelf and out_plug.name().split(sep=".")[0] == i.name().split(sep=".")[0]:
					continue
				returnNodes.add(i)
				returnNodes.add(out_plug)
	
	if returnNodes.length() == 0: return None
	return returnNodes



def rControlCastShape(inShape, targetCurve):
	"""
	
	"""




def rQuickHuman():
	"""
	UE5 metahuman
	5 spine bones from base of back hip to before base of neck
	2 neck bones


	"""




# main program
if __name__ == "__main__":
	rigStu()