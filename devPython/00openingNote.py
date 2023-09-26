#beginCode
"""
STUART LIM LEARNS TO RIG

written upon Maya 2022 (built-in python 3.7.7)
code not py 2.7.x ready, consider editing directly or use the future package



Dedications:
Jon Macey http://nccastaff.bournemouth.ac.uk/jmacey/
	for deeper insight into DCCs and the quirks of scripting/programming
	and the public resource that is all his lecture notes.
	even now after graduating I'm learning something new from his notes
Vlad Oancea
	for unreleating drive to figure out difficult code
Emma Moisuc
	for rigging talk and comisserating
Nim Mutti
	for showing chaos is not always a bad thing in code
Natalie, Nellie, Neliah
	three little reminders to keep learning


"""

from typing import List, NoReturn

import maya.cmds as mc
import maya.api.OpenMaya as om2