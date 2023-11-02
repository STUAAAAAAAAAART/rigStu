UE4 Mannequin model

```
root
	pelvis
	|	spine_01
	|		spine_02
	|			spine_03
	|			|	clavicle_l
	|			|		upperarm_l
	|			|			upperarm_twist_01_l
	|			|			lowerarm_l
	|			|				lowerarm_twist_01_l
	|			|				handl_l
	|			|					index_01_l
	|			|						index_02_l
	|			|							index_03_l
	|			|					middle_01_l
	|			|						middile_02_l
	|			|							middle_03_l
	|			|					pinky_01_l
	|			|						pinky_02_l
	|			|							pinky_03_l
	|			|					ring_01_l
	|			|						ring_02_l
	|			|							ring_03_l
	|			|					thumb_01_l
	|			|						thumb_02_l
	|			(spine_03)
	|			|	clavicle_r
	|			|		upperarm_r
	|			|			upperarm_twist_01_r						
	|			|			lowerarm_r
	|			|				lowerarm_twist_01_r
	|			|				handl_r
	|			|					index_01_r
	|			|						index_02_r
	|			|							index_03_r
	|			|					middle_01_r
	|			|						middile_02_r
	|			|							middle_03_r
	|			|					pinky_01_r
	|			|						pinky_02_r
	|			|							pinky_03_r
	|			|					ring_01_r
	|			|						ring_02_r
	|			|							ring_03_r
	|			|					thumb_01_r
	|			|						thumb_02_r
	|			(spine_03)
	|				neck_01
	|					head
	|						[... facerig ...]
	(pelvis)
		thigh_l
			thigh_twist_01_l
			calf_l
				calf_twist_01_l
				foot_l
					ball_l
		thigh_r
			thigh_twist_01_r
			calf_r
				calf_twist_01_r
				foot_r
					ball_r
(root)
	ik_foot_root
		ik_foot_l
		ik_foot_r
	ik_hand_root
		ik_hand_tool
			ik_hand_l
			ik_hand_r

```