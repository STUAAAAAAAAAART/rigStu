from typing import List, NoReturn

import maya.cmds as mc
import maya.api.OpenMaya as om2

"""
NAMING CONVENTION
rename calls in maya that includes a namespace that does not exist
	will automatically create a new namespace
-------------
joints:
- keep name in one all-lowercase word

skin bind joints (work upstream to ensure conformity, or rename in reference)
"j:[jointName - location - index]"
chains
"j:spine0"
"j:spine1"
"j:spine2"

chirality / sidedness / handedness
(TODO - consider, due to rigging operations depending on making left and right sided versions)
"j:legLeft0"  "j:kneeLeft0"  "j:ankleLeft0"
"j:legRight0" "j:kneeRight0" "j:ankleRight0"
- keep sidedness in capital: "Left" or "L"
- (TODO) A B C D convention could help, but be aware of 26 letter options
- (TODO)

trees, e.g. extra limbs (TODO - suggestion as of now)
"j:shoulderLeft0" "j:elbowLeft0" "j:wristLeft0"
"j:shoulderLeft1" "j:elbowLeft1" "j:wristLeft1"

-------------
control curves:
"c:[jointName][purpose]"
"c:handLeft0FK"
- IMPORTANT: KEEP TRACK OF ALL CONTROL CURVES,
	ANIMATION DATA GOES HERE
- IF ADJUSTING RIG:
	- MAINTAIN NAMES
	- CONSIDER NEW CONTROL SCHEME, CLEANUP OR RE-KEYING ANIMS MAY BE NECESSARY

-------------
rigging operations
pre-transforms
"r:[rigging group]:t:[purpose]"

non-skin joint logics
"r:[rigging op/group]:j:[purpose][index]"
"r:armLeftIKFK:j:ik0" "r:armLeftIKFK:j:ik3" "r:armLeftIKFK:j:ik3"

DG-only nodes (not appearing in the DAG)
"r:[rigging op/group]:n:[type and/or purpose][index]"
"r:tailChainFK:n:mxmTailDriver0"
"""

""" om2.MNamespace

om2.MNamespace.getNamespaces(recurse=False)
# Result: [':UI', ':a0', ':b0', ':mesh', ':rig', ':shared'] # 
om2.MNamespace.getNamespaces(recurse=True)
# Result: [':UI', ':a0', ':a0:a1', ':b0', ':mesh', ':rig', ':rig:ug', ':shared'] # 
om2.MNamespace.getNamespaces("a0",recurse=True)
# Result: [':a0:a1'] # 
"""

class rigStu(): # see 00*.py
	def __init__(self):
		self.rigRoot = om2.MFnDagNode()
		self.jointRoot = om2.MFnDagNode()
		pass



#beginCode

	def nAutoRename(inNode, inRigSpace, newName:str, appendName:str = ""):
		"""
		nAutoRename
		utility function for maya

		wrapper for maya's rename function, to conform to desired namespace
		and keep mind off
		"""