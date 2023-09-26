"""
code sourced from
https://ehsanhm.wordpress.com/2022/02/02/maya-api-notes-click-for-more/
https://web.archive.org/web/20181017223955/http://www.chadvernon.com/blog/resources/maya-api-programming/introduction-to-the-maya-api/
"""

import maya.api.OpenMaya as om2

a = 'pCube1'
b = 'pCube2'

sel = om2.MSelectionList()
sel.add(a)
sel.add(b)

print('.' * 100)
print('selected nodes', sel.getSelectionStrings())

a_dag = sel.getDagPath(0)
a_dag_fn = om2.MFnDagNode(a_dag)
print('name with namespace (absoluteName)', a_dag_fn.absoluteName())
# a_dag_fn.addChild()
# a_dag_fn.attribute()
print('attr count', a_dag_fn.attributeCount())
print('Bounding Box', a_dag_fn.boundingBox)
# a_dag_fn.create()
# a_dag_fn.dagPath()
# a_dag_fn.dagRoot()
# print('duplicate', a_dag_fn.duplicate())
# a_dag_fn.findPlug()
print('full name', a_dag_fn.fullPathName())
# a_dag_fn.getConnections()
# a_dag_fn.getPath()
print('has attr foo', a_dag_fn.hasAttribute('foo'))

b_depend = sel.getDependNode(1)
print('has child pCube2', a_dag_fn.hasChild(b_depend))
# a_dag_fn.hasObj()
print('has parent pCube2', a_dag_fn.hasParent(b_depend))
print('has unique name', a_dag_fn.hasUniqueName())
# a_dag_fn.isChildOf(b_depend)
print('is intermediate', a_dag_fn.isIntermediateObject)
# a_dag_fn.isParentOf()
print('name', a_dag_fn.name())
print('partial name', a_dag_fn.partialPathName())
print('namespace', a_dag_fn.namespace)