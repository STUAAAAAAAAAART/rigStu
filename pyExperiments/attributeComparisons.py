import maya.cmds as mc
import maya.api.OpenMaya as om2

# search engine description:
# maya compare two attributes if compatible for connection

"""
get attribute reference from MPlug

- om2.MSelectionList().getPlug(n) >> MObject # MPlug
- om2.MPlug().attribute() >> MObject # attribute
- om2.MFnAttribute( MPlug().attribute() ) >> MFnAttribute (class extractor)

test attributes for connection compatibility
attrA.acceptsAttribute(attrB) >> True/False or raise error if not MFnAttribute

"""

"""
links:
https://help.autodesk.com/view/MAYAUL/2022/ENU/?guid=Maya_SDK_py_ref_class_open_maya_1_1_m_plug_html
https://help.autodesk.com/view/MAYAUL/2022/ENU/?guid=Maya_SDK_py_ref_class_open_maya_1_1_m_fn_attribute_html
"""


mSelA = om2.MSelectionList().add("rigRoot.translateX")
mPlugA = mSelA.getPlug(0)
mAttrA = om2.MFnAttribute(mPlugA.attribute())

mSelB = om2.MSelectionList().add("rigRoot.translateZ")
mPlugB = mSelB.getPlug(0)
mAttrB = om2.MFnAttribute(mPlugB.attribute())

mAttrA.acceptsAttribute(mAttrB)