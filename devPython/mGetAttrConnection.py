"""
see mGetNodeConnection()
"""

from typing import List, NoReturn

import maya.cmds as mc
import maya.api.OpenMaya as om2

""" TODO
e.g. a multMatrix node has an array of inputs
with only the name of the main attribute (.attr) and not of its elements (.attr[5])
find out how to get all the connections
and return as a list in index ascending order

note that maya does not resilver plugs on arrays with gaps in the indices
see mResilverConnections()
"""

#beginCode

def mGetAttrConnection(inPlug:om2.MSelectionList, direction) -> om2.MSelectionList:
	"""
	mGetAttrConnection
	utility function for maya

	returns list of attributes connected to selected node, querying direction required
	
	:param inNode:		expects om2.MObject, has soft fallback for om2.MSelectionList (no string, use select function first)
	:param direction:	expects "upstream", "downstream", or just "up" or "down" - for querying up- or down-stream connections
	
	:return: om2.MSelectionList of resultant plugs, or =None if empty
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
	if type(inPlug) == type(om2.MSelectionList()):
		print("caution: function designed for single MObject and not a list of. First item used instead")
		try:
			queryMObject = inPlug.getDependNode(0)
		except:
			raise TypeError("mGetNodeConnection 01 - attempt to pull om2.MSelectionList failed")
	else:
		queryMObject = inPlug

	# ============= function
	returnPlugs = om2.MSelectionList() # -> MSelectionList: create return object

	