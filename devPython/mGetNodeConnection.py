"""
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
"""


from typing import List, NoReturn

import maya.cmds as mc
import maya.api.OpenMaya as om2

#beginCode

def mGetNodeConnection(inNode, direction, excludeSelf=False) ->  om2.MSelectionList:
	"""
	mGetNodeConnection
	utility function for maya

	returns list of connections to selected node, querying direction required
	
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