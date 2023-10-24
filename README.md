# rigStu
 one person's journey into maya's rigging and scripting ecosystem - more exploratory than complete

### dev environment
Windows 10
Maya 2022
Python (mayapy) 3.7.7

## about this project

the commands are based on frequent tasks encountered during the rigging masterclass in uni. this project aims to turn them into smaller commands, as a means to describe rig construction methods down to a series of (hopefully) readable scripts.

i've read from the industry's experience that the rigs are usually (re)generated programmatically during the later stages of the process, and i've taken a bit of inspiration from that to help with compartmentalisation of control groups, automation of repetitive and otherwise menial tasks, and replication of complex designs when applied on other characters

additionally i'm hoping that this would help with focus by reverting the scene to an unrigged state to focus on a set of controls without being overwhelmed with the node editor

## use of Maya's API 2.0 (openMaya 2) vs maya.cmds

this project uses a mix of both, with openMaya mainly used for pointing to nodes, and maya.cmds for actual actions on the scene.

while it is possible for action commands to be written in openMaya, my current understanding is that the script has to be registered and properly accomodated as a plugin to maya, for the commands to be registered into the environment's undo queue (mc.undoInfo)

as of now, making this into a proper plugin is a lower priority, possibly would be the phase after making a more complete set of commands, and also after making an in-maya window for it.

## node naming convention

as of now i've been using short underscored_ prefixes to tag nodes, but i'm still looking into maya's namespace editor and am contemplating on its possible use in this project. it gets more difficult if i end up grouping control node networks using a namespace, or at the very least figuring out the hierachy for them (completely flat? grouped according to outliner/DAG hierachy?). 

|prefix (old)|namespace|description|
|:---:|:---:|-----|
|g_|g:|group|
|c_|c:|control|
|r_|r:|rig group (superspace for grouping rigs in parts)|
| |r:leftArm:|example namespace for a rigging operation|
|uj_|r:"...":j:|joint (not skin bind joints, for )|
|n_|r:"...":n:|DG-only node|
|t_|r:"..."t:|pre-transform group|

examples and more detail in [rigStu/devPython/nAutoRename.py](devPython/nAutoRename.py)

## code acknowledgements

sourced code and guidance from the internet are mentioned in the separate dev python files in rigStu/devPython, primarily within files that contains said code and methods. if using this repository, consider crediting or referencing them instead where appropriate