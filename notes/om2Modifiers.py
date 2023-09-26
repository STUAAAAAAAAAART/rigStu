"""
code sourced from:
https://jamesbdunlop.github.io/om2intro/2020/01/13/om2vscmds03.html
"""


from maya.api import OpenMaya as om2
from maya import cmds
# mDagMod for creating / handling DGNodes
mdgmod = om2.MDGModifier()

# mDagMod for creating / handling DagNodes
mDagMod = om2.MDagModifier()

curSel = om2.MGlobal.getActiveSelectionList()
srcNode = curSel.getDependNode(0)
destNode = curSel.getDependNode(1)

# connect
# Find first source plug, find dest plug, use the modifier to connect them
mFn = om2.MFnDependencyNode(srcNode)
srcPlug = mFn.findPlug("translate", False)
mFn.setObject(destNode)
destPlug = mFn.findPlug("translate", False)
if destPlug.isConnected:
	# Find what it is connected to and disconnect it first!
	# Since this is a destination only one thing can be connected to it.
	# Else if we're looking for all connected to a source we can use connectedTo()
	src = destPlug.source()
	mDagMod.disconnect(srcPlug, destPlug)

mDagMod.connect(srcPlug, destPlug)
mDagMod.doIt()

# getAttr
# some plugs are compounds, some are arrays, some are floats / bool / shorts / double etc
srcTrans = [srcPlug.child(x).asFloat() for x in range(srcPlug.numChildren())]
print(srcTrans)

# setAttr
srcPlug.child(0).setFloat(10)

# createNode
# Depending on if you are making a DAGNode or DGNode you'll need to use either a
# MDagModifier or a MDGModifier() eg: you can't make a joint with a MDGModifier()
nodeName = "Fart"
# We can use cmds here to check for the node as the queries in cmds are pretty
# fast.
if not cmds.objExists(nodeName):
	newNode = mDagMod.createNode("transform")
	mDagMod.renameNode(newNode, nodeName)
	mDagMod.doIt()
# Note you might want to use the MFnDependencyNode.create() method, but this will
# create the node in scene as soon as you call this. Using the MDG or MDag modifiers
# lets you queue up xNum of operations and using the doIt() to perform them in one
# go. Which can be a HUGE time saver when building complex scenes.