"""
code sourced from
https://ehsanhm.wordpress.com/2022/02/02/maya-api-notes-click-for-more/
https://web.archive.org/web/20181017223955/http://www.chadvernon.com/blog/resources/maya-api-programming/introduction-to-the-maya-api/
"""

import maya.api.OpenMaya as om2

# store selected nodes
sel = om2.MGlobal.getActiveSelectionList() # -> MSelectionList

# create an iterator from selected objects
sel_it = om2.MItSelectionList(sel)

# go through selected items
while not sel_it.isDone():

    # get dag path
    dag = sel_it.getDagPath()

    # Full name
    print('Full name:', dag.fullPathName())

    # short name
    print('Short name:', dag.partialPathName())

    # get world and parent matrix
    print('world matrix', dag.inclusiveMatrix())
    print('parent world matrix', dag.exclusiveMatrix())
    print('parent world inverse matrix', dag.exclusiveMatrixInverse())

    # calculate local matrix from world and parent matrices
    local_matrix = dag.exclusiveMatrixInverse() * dag.inclusiveMatrix()
    print('local matrix', local_matrix)

    # get children of given nodes and if they're transform nodes, print their names
    children = []
    for i in range(dag.childCount()):
        child_obj = dag.child(i)
        if child_obj.apiTypeStr == 'kTransform':
            child_dag = om2.MDagPath.getAPathTo(child_obj)
            children.append(child_dag.partialPathName())
    print('children', children)

    # access shape node of current node
    dag.extendToShape()
    print('Shape node', dag.partialPathName())

    # go to next item
    sel_it.next()