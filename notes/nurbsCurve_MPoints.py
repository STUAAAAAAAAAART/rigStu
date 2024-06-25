# source: https://gaidachevrigs.com/2020/03/17/openmaya-mfnnurbscurve-create/
	# by Alexei Gaidachev
# relevant links:
# https://github.com/AlexGaida/Python/blob/1a07980a6fd632d3a3f48f468793e0c9729a25ee/maya_utils/curve_utils.py
	# missing functions in script below exist within above curve_utils.py repo


# WARNING: script based on openMaya 1.0. CONSULT AND CONVERT BEFORE USING

import maya.OpenMaya as OpenMaya



def get_point_array(points_array, equal_distance=False):
	"""
	calculate the positional array object.

	:param points_array:
	:param equal_distance: <bool> calculate the equal distance of CV's
	:return:
	"""
	m_array = OpenMaya.MPointArray()
	if equal_distance:
		array_length = len(points_array)
		for idx, point in enumerate(points_array):
			if idx == 0:
				m_array.append(OpenMaya.MPoint(*point))
				m_array.append(OpenMaya.MPoint(*point))
			elif idx >= 1 and idx != array_length - 1:
				prev_p, cur_p, next_p = list_scanner(points_array, idx)
				cur_v = math_utils.Vector(*cur_p)
				prev_v = math_utils.Vector(*prev_p)
				new_vec = math_utils.Vector(cur_v - prev_v)
				new_vec = math_utils.Vector(new_vec * 0.5)
				new_vec = math_utils.Vector(prev_v + new_vec)
				m_array.append(OpenMaya.MPoint(*new_vec.position))
			elif idx == array_length - 1:
				prev_p, cur_p, next_p = list_scanner(points_array, idx)
				prev_v = math_utils.Vector(*prev_p)
				next_v = math_utils.Vector(*next_p)
				new_vec = math_utils.Vector(next_v - prev_v)
				new_vec = math_utils.Vector(new_vec * 0.5)
				new_vec = math_utils.Vector(prev_v + new_vec)
				# add two points in the same spot
				m_array.append(OpenMaya.MPoint(*new_vec.position))
				m_array.append(OpenMaya.MPoint(*point))
	else:
		for idx, point in enumerate(points_array):
			if idx == 1:
				prev_p, cur_p, next_p = list_scanner(points_array, idx)
				cur_v = math_utils.Vector(*cur_p)
				prev_v = math_utils.Vector(*prev_p)
				new_vec = math_utils.Vector(cur_v - prev_v)
				new_vec = math_utils.Vector(new_vec * 0.5)
				new_vec = math_utils.Vector(prev_v + new_vec)
				m_array.append(OpenMaya.MPoint(*new_vec.position))
			elif idx == len(points_array) - 1:
				prev_p, cur_p, next_p = list_scanner(points_array, idx)
				prev_v = math_utils.Vector(*prev_p)
				next_v = math_utils.Vector(*next_p)
				new_vec = math_utils.Vector(next_v - prev_v)
				new_vec = math_utils.Vector(new_vec * 0.5)
				new_vec = math_utils.Vector(prev_v + new_vec)
				m_array.append(OpenMaya.MPoint(*new_vec.position))
			m_array.append(OpenMaya.MPoint(*point))
	return m_array

