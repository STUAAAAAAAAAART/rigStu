from typing import List, NoReturn

import maya.cmds as mc
import maya.api.OpenMaya as om2

"""
https://help.autodesk.com/view/MAYAUL/2022/ENU/?guid=Maya_SDK_py_ref_class_open_maya_1_1_m_fn_nurbs_curve_html

.createWithEditPoints() , for creating a curve that will pass through each input point

MPoint description
https://help.autodesk.com/view/MAYAUL/2022/ENU/?guid=Maya_SDK_py_ref_class_open_maya_1_1_m_point_html
https://download.autodesk.com/us/maya/docs/maya85/API/MPoint.html
added because the function expects xyzw, was wondering why w-component is needed


additional function guidance around MFnNurbsCurve()
https://gaidachevrigs.com/2020/03/17/openmaya-mfnnurbscurve-create/
THANK YOU VERY MUCH ALEXEI GAIDACHEV

"""

class rigStu(): # see 00*.py
	def __init__(self):
		self.rigRoot = om2.MFnDagNode()
		self.jointRoot = om2.MFnDagNode()
		pass 

#beginCode

	# !! CONVERT FUNCTION TO mc.createCurve
	def mCurveType(self, type:str="open") -> int:
		"""
		mCurveType
		utility function for maya

		just to reduce having to type om2.MFnNurbsCurve.kOpen etc

		:param type:	expects string - "open" / "closed" / "periodic". shorthand 'o'/'c'/'p'
		:return:		enum ints corresponding to om2.MFnNurbsCurve curve types
		"""

		if type[0]=='o':
			return om2.MFnNurbsCurve.kOpen
		if type[0]=='c':
			return om2.MFnNurbsCurve.kClosed
		if type[0]=='p':
			return om2.MFnNurbsCurve.kPeriodic
		#shh
		
		# no valid inputs
		raise ValueError(f"mCurveType: string not recognised, keywords are open/closed/periodic | got: {str(type)}")

	# !! CONVERT FUNCTION TO mc.createCurve
	def mConvertToMPoint(self, points:list) -> om2.MPointArray:
		"""
		mConvertToMPoint
		utility function for maya

		converts regular list of points to MPoint
		:param points:	expects list of 3D points, e.g. [ [1,2,3], [4,5,6], ... ]
		:return:	om2.MPointArray
		"""
		returnList = om2.MPointArray()
		
		for i in points:
			if len(i) < 3:
				raise ValueError(f"mConvertToMPoint - MPoint(): not enough variables to cast to MPoint, 3 floats expected | got: {str(i)} , check input list")
			returnList.append(om2.MPoint(i[0], i[1], i[2], 1.0)) # reminder: MPoint constructor expects XYZW

		return returnList

	# !! CONVERT FUNCTION TO mc.createCurve
	def nCreateCurveCV(self, points:om2.MPointArray, form:int=om2.MFnNurbsCurve.kPeriodic, owner:om2.MSelectionList = None) -> om2.MSelectionList:
		"""
		nCreateCurveCV
		utility function for maya

		creates a low-level data class, and returns a DG attribute
		to be assigned or connected to a nurbsCurve's curveShape.create attribute

		:param points:			expects list of points, absolute to world space
		:param form:			expects enum int, use mCurveType()
		:param owner:			expects MSelecionList of DAG curves to receive the new curve; if None, nothing will be copied to 
		:param isEditPoints:	expects True/False - to query and gather attributes
		
		:return:	om2.MSelectionList of curveShape with nurbsCurve attribute that can be setAttr'd to curveShape.create

		"""
		
		eps = points
		eps = [[1,2,3],[2,3,4],[3,4,5],[4,5,6],[5,6,7],[6,7,8]]

		om2.MFnNurbsCurve.createWithEditPoints()
		newCurve = om2.MFnNurbsCurve.createWithEditPoints(eps, degree, )	



		# return 
		return
	
	# !! CONVERT FUNCTION TO mc.createCurve
	def nCreateCurveEP(self, points:list, owner:om2.MSelectionList = None) -> om2.MSelectionList:
		"""
		nCreateCurve
		utility function for maya

		creates a low-level data class, and returns a DG attribute
		to be assigned or connected to a nurbsCurve's curveShape.create attribute

		:param points:			expects list of points, absolute to world space
		:param owner:			expects MSelecionList of DAG curves to receive the new curve; if None, nothing will be copied to 
		:param isEditPoints:	expects True/False - to query and gather attributes
		
		:return:	om2.MSelectionList of curveShape with nurbsCurve attribute that can be setAttr'd to curveShape.create

		"""
	
	# !! CONVERT FUNCTION TO mc.createCurve
	def nCreateCurve(self, points:list, owner:om2.MSelectionList = None) -> om2.MSelectionList:
		"""
		nCreateCurve
		utility function for maya
		
		call function with nCreateCurveCV or nCreateCurveEP

		:param points:			expects list of points, absolute to world space
		:param owner:			expects MSelecionList of DAG curves to receive the new curve; if None, nothing will be copied to 
		:param isEditPoints:	expects True/False - to query and gather attributes
		
		:return:	om2.MSelectionList of curveShape with nurbsCurve attribute that can be setAttr'd to curveShape.create

		"""