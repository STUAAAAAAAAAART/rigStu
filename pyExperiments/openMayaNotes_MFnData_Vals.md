
```py
import maya.api.OpenMaya as om2

om2.MFnData

# inherits:
om2.MFnBase

# inheritors:
om2.MFnComponentListData
om2.MFnDoubleArrayData
om2.MFnGeometryData
om2.MFnIntArrayData
om2.MFnMatrixArrayData
om2.MFnMatrixData
om2.MFnNumericData
om2.MFnPluginData
om2.MFnPointArrayData
om2.MFnStringArrayData
om2.MFnStringData
om2.MFnUInt64ArrayData
om2.MFnVectorArrayData

# querying an MPlug / .attribute
om2.MPlug().asMDataHandle() # >> returns MDataHandle
om2.MDataHandle().type() # >> returns one of the following ints

```

https://help.autodesk.com/view/MAYAUL/2022/ENU/?guid=Maya_SDK_py_ref_class_open_maya_1_1_m_fn_html

with thanks to ThE_JacO on the CGSociety Forums for leading into search inquiry to this file <br>
https://forums.cgsociety.org/t/python-access-connected-nodes-through-attributes/1677515/4

### SORTED BY INT VALUE

|int|MFn data type| extractor |
|:---:|:---|:---|
| 0 | kInvalid |  |
| 1 | `kNumeric` | `MFnNumericData` |
| 2 | `kPlugin` | `MFnPluginData` |
| 3 | `kPluginGeometry` | `MFnGeometryData` |
| 4 | `kString` | `MFnStringData` |
| 5 | `kMatrix` | `MFnMatrixData` |
| 6 | `kStringArray` | `MFnStringArrayData` |
| 7 | `kDoubleArray` | `MFnDoubleArrayData` |
| 8 | **kFloatArray** |  |
| 9 | `kIntArray` | `MFnIntArrayData` |
| 10 | `kPointArray` | `MFnPointArrayData` |
| 11 | `kVectorArray` | `MFnVectorArrayData` |
| 12 | **kMatrixArray** |  |
| 13 | `kComponentList` | `MFnComponentListData` |
| 14 | `kMesh` | `MFnMeshData` |
| 15 | `kLattice` | `MFnLatticeData` |
| 16 | `kNurbsCurve` | `MFnNurbsCurveData` |
| 17 | `kNurbsSurface` | `MFnNurbsSurfaceData` |
| 18 | `kSphere` | `MFnSphereData` |
| 19 | `kDynArrayAttrs` | `MFnArrayAttrsData` |
| 20 | `kDynSweptGeometry` | `MFnDynSweptGeometryData` |
| 21 | `kSubdSurface` | `MFnSubdData` |
| 22 | `kNObject` | `MFnNObjectData` |
| 23 | `kNId` | `MFnNIdData` |
| 24 | **kAny** |  |
| 25 | **kFalloffFunction** |  |
| 26 | kLast |  |