# rigStu
 one man's journey into maya's rigging ecosystem - more exploratory than complete

### dev environment
Windows 10
Maya 2022
Python (mayapy) 3.7.7

## about this project

the commands are based on frequent tasks encountered during the rigging masterclass in uni. this project aims to turn them into smaller commands, as a means to describe rig construction methods down to a series of (hopefully) readable scripts.

## use of Maya's API 2.0 (openMaya 2) vs maya.cmds

this project uses a mix of both, with openMaya mainly used for pointing to nodes, and maya.cmds for actual actions on the scene.

while it is possible for action commands to be written in openMaya, my current understanding is that the script has to be registered and properly accomodated as a plugin to maya, for the commands to be registered into the environment's undo queue (mc.undoInfo)

as of now, making this into a proper plugin is a lower priority, possibly would be the phase after making a more complete set of commands, and also after making an in-maya window for it.

## code acknowledgements

sourced code and guidance from the internet are mentioned in the separate dev python files in rigStu/devPython, primarily within files that contains said code and methods. if using this repository, consider crediting or referencing them instead where appropriate