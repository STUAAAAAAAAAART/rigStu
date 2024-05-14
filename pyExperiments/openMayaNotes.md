# openMaya 2.0 Notes

The primary idea is to utilise openMaya for keeping track of lists of objects, and using maya.cmds to create and adjust nodes/objects.

pointers in openMaya automatically update when there are changes in names, especially in cases where cmds.rename() adjusts the new name to avoid name collisions. doing this in lists of names in strings will require a lot of functions to re-query and re-validate names, along with many more checks that's already covered in openMaya

executing in maya.cmds is desired for undo history purposes. for this to be done in openMaya, the script will have to be written as a proper plugin for maya, which is out of personal scope at the moment

```
maya.api.OpenMaya as om2 | selection and pointer management
--------------------------------------------------------------------
maya.cmds         as mc  | creating, connecting, and adjusting nodes
```


## Selection-sided tasks
### Select Objects in python (making a list)
assign objects to python variables, not to be confused with selecting in maya scene
```
var = om2.MSelectionList()
var.add(nodeNameStr)
```
most node creation functions in maya cmds return the DAG path (the scene name) of the string, so pipe the outputs to war.add() .<br>
this unfortunately is done one by one, so loops may be required for multiple new objects
```
newCircle = mc.circle()
var.add(newCircle)
# or
var.add( mc.circle() )
```

### adding a list to another
akin to list.append()
```
list1 = om2.MSelectionList()
list2 = om2.MSelectionList()

list1.merge( list2 )
```

### getting specific objects in context
common wants include:
- objects appearing in the scene (Direct A-cyclic Graph / DAG nodes)
- nodes in the node editor (Dependency Graph / DG nodes)
- attributes of either of the above two, via Plugs


## Execution-sided tasks



# command list
```
om2.MGlobal.getActiveSelectionList()
	:return: om2.MSelectionList - selected nodes (MObject) in scene

class
om2.MSelectionList
	# https://help.autodesk.com/view/MAYAUL/2022/ENU/?guid=Maya_SDK_py_ref_class_open_maya_1_1_m_selection_list_html
__init__()
__init__(om2.MSelectionList)
	:return: copy of input MSelectionList
.add(str)
.add(MObject)
.add(MDagPath)
.getDagPath(n)
	:return: MObject pointer to nth node with DAG Path
	>> extractor om2.MFnDagNode()
.getDependNode(n)
	:return: MObject pointer to nth Dependency Node
	>> extractor om2.MFnDependencyNode()
.getPlug(n)
	:return: MObject pointer to nth MPlug
	note: add() object.attribute name (e.g. "pSphere.translateX")
	>> extractor: MFnAttribute()
.getSelectionStrings(n)
	:return: Tuple: (str, str, str, ...)

om2.MFnDagNode()
__init__(MObject)
__init__(om2.MDagPath)
.dagRoot()
	:return: MObject pointer to root parent node

class
om2.MItSelectionList
__init__(om2.MSelectionList)

om2.MFnDependencyNode()
__init__(MObject)

om2.MItDependencyNode()
__init__(MObject)

om2.MItDependencyGraph()

class
om2.MPlug
__init__()


om2.MFnAttribute
__init__(MPlug.getAttribute())
.acceptsAttribute(om2.MFnAttribute)
	:return: True/False - are both attributes compatible with each other?

```