# Node Naming Convention Notes
pass

## Considerations

### Unreal Engine ignores namespaces when importing maya FBX files
this mostly only affects stuff going into the FBX for import into unreal engine, so models and joints and baked animation data without rig information.<br>
there are pipelines out there that synce rig information between maya and UE5's control rig, so consider strategy on utilising namespaces

### programmetric selection/assignment of MObjects
pass

## editing the rig after handing off to animators
maya's reference editor looks for specific names in the referenced project file, so if it does nto find it, the edited data will remain but without the node it's looking for.

if there is a change in rig articulation or logic, consider how existing downstream animation would represent motion in the edited rig

## editng names of nodes in maya (cmds.rename)
`cmds.rename( existingNodeDagPath:str , newName:str )`
- if a new name is of the same as another name in the project (especially with the same DAG path), cmds.rename() will index and/or increment the name and assign 
- if a new name contains a namespace that does not currently exist in maya's namespace editor, a new namespace will be created automatically according to case-sensitive hierachy
- namespaces are also exclusive, in the sense that it cannot share the same name as a DG node

## example outliner list

```
root
	hip
		spine0
			[...]
		pelvis
			[...]
mesh

rigRoot
	r:autoFK
		t:joint0_FK
			c:joint0_FK
		t:joint1_FK
			c:joint1_FK
	r:leftArm0_FKIK
		t:ikLogicJoints
			j:leftArm0_ikJoint0
				j:leftArm0_ikJoint1
					j:leftArm0_ikJoint2
			c:leftArm0_IK
				n:leftArm0_ikHandle
			c:leftArm0_PV
		t:shoulderLeft0
			c:shoulderLeft0_FK
		t:elbowLeft0
			c:elbowLeft0_FK
		t:forearmLeft0
			c:forearmLeft0_FK
```

## Node Naming Convention
### joints (in main file before import/referencing)
- unreal engine removes namespaces of maya FBX imports, do not intentionally name a node in the rig space the same as any joint or mesh in the exportable asset space
- chains:
```
spine0
	spine1
		spine2
```
- chirality / sidedness / handedness<br>

```
"legLeft0"
	"kneeLeft0"
		"ankleLeft0"
"legRight0"
	"kneeRight0"
		ankleRight0"
```
- trees, e.g. extra limbs<br>
no hard and fast rule, just note for animation reuse
```
"shoulderLeft0"
	"elbowLeft0"
		"wristLeft0"
"shoulderLeft1"
	"elbowLeft1"
		"wristLeft1"
```

### control curves
- IMPORTANT: KEEP TRACK OF ALL CONTROL CURVES, AS ANIMATION DATA GOES IN HERE
- IF ADJUSTING RIG:
	- MAINTAIN NAMES
	- CONSIDER NEW CONTROL SCHEME, CLEANUP OR RE-KEYING ANIMS MAY BE NECESSARY
```
"c:[jointName]_[purpose]"
"c:handLeft0_FK"
```

### rigging operations
key name variables:
- [operation] - the name of the rigging group, e.g. nodes under an IKFK group

**pre-transforms**
```
"t:[operation]"
```

**non-skin joint logics**
- DO NOT NAME SIMILARLY TO MAIN BIND SKELETON, ESPECIALLY WITHOUT NAMESPACES
- take note of [jointLocation] and [index], as [jointLocation] may already contain an index
```
"j:[operation]_[jointLocation]_[purpose][index]"
"j:armLeftIKFK_arm0_logicIK" "j:armLeftIKFK_arm1_logicIK" "j:armLeftIKFK_arm2_logicIK"
```

**DG-only nodes (not appearing in the DAG)**
```
"n:[type]_[operation]_[purpose][index]"
"n:mxm_tailChain0_driver0"
```