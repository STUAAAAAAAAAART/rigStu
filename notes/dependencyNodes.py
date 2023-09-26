"""
code sourced from
https://ehsanhm.wordpress.com/2022/02/02/maya-api-notes-click-for-more/
https://web.archive.org/web/20181017223955/http://www.chadvernon.com/blog/resources/maya-api-programming/introduction-to-the-maya-api/
"""

import maya.cmds as mc
import maya.api.OpenMaya as om2

# create a few cubes in a new scene and connect some of their attributes 
mc.file(new=True, f=True)
mc.polyCube()
mc.polyCube()
mc.polyCube()
mc.connectAttr('pCube1.r', 'pCube2.r')
mc.connectAttr('pCube2.sx', 'pCube3.sx')

# create a selection-list and add 2 of created cubes to this list
# selection lists can help find the dagPath and dependNode of given objects quickly
sel = om2.MSelectionList()
sel.add('pCube1')
sel.add('pCube2')

print('.' * 100)

# get depend node
b_depend = sel.getDependNode(1)

# create function-set that can manipulate depend node
b_depend_fn = om2.MFnDependencyNode(b_depend)

# name with namespace (absoluteName)
print(b_depend_fn.absoluteName())

# create an attribute 
n_attr_fn = om2.MFnNumericAttribute()
test_attr = n_attr_fn.create('test', 'test', om2.MFnNumericData.kFloat)
n_attr_fn.keyable = True
n_attr_fn.setMin(5.5)
b_depend_fn.addAttribute(test_attr)

# find attr class (default attribute or user created one?)
b_depend_fn.attributeClass(at)

# number of all attributes on given depend node
attr_count = b_depend_fn.attributeCount()

# access the last created attribute
at = b_depend_fn.attribute(int(attr_count) - 1)

# create function-set to work with the attribute
n_attr_fn_2 = om2.MFnNumericAttribute(at)
print(n_attr_fn_2.name)

# get a mel command that can be used to create an attribute just like this one
n_attr_fn_2.getAddAttrCmd(True)

# create new node
depend_fn = om2.MFnDependencyNode()
mdn_obj = depend_fn.create('multiplyDivide')
print('created a new node', depend_fn.name())

# access plug
plug = b_depend_fn.findPlug('tx', False)

# get and set plug, ie: lock, channelbox, get value, set value
plug.asFloat()
plug.name()
plug.parent().name()
plug.partialName()
plug.setFloat(5.0)



# b_depend_fn = om2.MFnDependencyNode(b_depend)
# get out connections 
cnns = b_depend_fn.getConnections()
for cnn in cnns:
    # find out connections
    out_plugs = cnn.connectedTo(False, True)  #asDst, asSrc
    for out_plug in out_plugs:
        print('{} -> {}'.format(cnn.name(), out_plug.name()))
    # find in connections
    in_plugs = cnn.connectedTo(True, False)  #asDst, asSrc
    for in_plug in in_plugs:
        print('{} -> {}'.format(in_plug.name(), cnn.name()))

# some other useful functions and properties of depend fn
b_depend_fn.hasAttribute('tx')
b_depend_fn.hasUniqueName()
b_depend_fn.isDefaultNode
b_depend_fn.isFromReferencedFile
b_depend_fn.isLocked
b_depend_fn.namespace
b_obj = b_depend_fn.object()

# get dag from mObject
if obj.hasFn(om2.MFn.kDagNode):
    dag_fn = om2.MFnDagNode(obj)
    dag_fn.getPath()

# find plugin of given node
b_depend_fn.pluginName

# remove attr
test_plug = b_depend_fn.findPlug('test', False)
b_depend_fn.removeAttribute(test_plug.attribute())

# find type of the depend node attached to this function-set
b_depend_fn.type()
b_depend_fn.typeId
b_depend_fn.typeName