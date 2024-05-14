# explainer the video.md
### Youtube: Stuart's uni rigging demoreel (2021-2023)

uploaded YYYYMMDD

⬅ [youtube link]()

## part 1: project spino

Part of Rigging Masterclass 2022/23, Bournemouth University <br/>
Spinosaurus Model provided by Frontier Studios via Bounremouth University

### the foot

one of the main challenges in producing a rig for a spinosaurus (as described by Frontier<sup>a1</sup>) was solving the digitigrade foot ("finger-walker"<sup>a2</sup>).

> <sup>a1</sup> part of talk by Frontier Studios rigging team at BFX 2022 hosted by Bournemouth University <br/>
> <sup>a2</sup> https://en.wikipedia.org/wiki/Digitigrade

an IK rig for a typical human foot involves side-roll and an inverse-foot IK solver, with the toes ("fingers") located at the tip of the foot. with

with the spinosaurus, the claw/toe is the main contact surface of the foot, which makes the inverse-foot system inadequate, as the toes need flexibility to animate

[]image: diagram of human foot vs spino digitigrade foot

### the tail

⬅ FK control: [rig reel 2023](landing_YT0001_controllerFK.md)

there was a suggestion to have additional controls to drive groups of multiple sections of the tail. for a 9-joint chain, each has an individual rotational FK controller; 3 additional controllers drive joints in that chan in consecutive groups of 3; a final overall controller drives all of them.

each joint is driven by adding the rotations together, with the node network ensuring the controllers still face the direction of the joint.

### postmortem and the rest

the biggest challenge for me during this 3-month long project is balancing between developing the most complex part of the rig, and enumerating the rest of the rig. the pressure of this has got me looking into possibly scripting most of the common nodework and tasks to a script native to maya. hopefully this would reclaim more time spent on addressing complexity away from enumerating the rest of the rig. 

⬅ github: [rigStu](https://github.com/STUAAAAAAAAAART/rigStu)

as for the spino rig itself, other anatomical considerations include its sail spine: while most known skeletons describe individual "sail bones" to be fused to the corresponding spinal section, animation consideration has to be made to have them articulate sideways for presentation purposes (also to consider if each spine should be segmented to articulate in a curve)

additionally there is the joint chain for the tongue, which could be a control scheme similar to the tail, or one with an additional spline IK switch to it.

other improvements that are either needed, or to expand functionality:
- individually blend the IK affector away from each toe while in IK mode (e.g. one toe in FK, other two in IK)
	- not sure if this is a possible scenario in animation, but if it crops up, the FK/IK blending system needs to be more grandular
- adjust the transform logic of the reverse foot system, so that the tip-of-toe point and the "ball-of-foot" point would better represent the upward peel of the foot
	- it's currently placed a bit too high, and the end of the toes are affected by the rotation of the peel too early
-  


## part 2: untitled project to generate keyframes for speech animation

⬅ github: [LINK](https://github.com/STUAAAAAAAAAART/)<br/>
attributions described in github repository

### the rig (2021-2023)

the scope of the rig was constrained to the mouth, without the rest of the emotive face. driven joints for

the rig was structured around the International Phonetic Alphabet, which describes the possible sounds a human vocal system can produce. the idea of using phonemes instead of viscemes is to provision to recieve other languages for speech animation

the driven face is condensed to the following controls:

- consonant space (2 floats, place and jaw rotation)
	- place of articulation for where the tongue would be placed for consonants made via oral obstruction
	- jaw rotation, simply lowering the law while maintaining place 
- vowel space (3 floats)
	- place of articulation, this time to complement the "backness" of the vowel
	- jaw rotation, independent to the consonant jaw, just for the sake of separation of representation between consonant-vowel transition
	- mouth roundness, the "aperture size" of the lips


- consonant-vowel blend (1 float) 


the controls drive the rig face, which consist of:

- a guide spline for the tongue
- two spline tracks, outlining:
	- the roof of the inner mouth, for consonant places
	- the lower articulation extents of the tongue, for vowel-backness
- vowel lip roundedness
	- ring of joint points representing the lips are distributed along a lofted surface of 3 sets of curves, representing the extents of vowel roundedness
- jaw rotation
- 



### the script (2022-2023)

in short:

0. [python - OS] <br/>audio is converted to a JSON file, containing detected words and timestamp of occurence
1. [python - OS] <br/>words are convered to an IPA definition through a dictionary lookup
2. [python - maya] <br/>file is read into  IPA symbols are convered to mouth articulation definitions, and keyframed consecutively between word timestamps

the IPA definitions have been taken from the IPA-Dict project<sup>b1</sup>, to serve as the basis of conversions from words to IPA. the project contains a few variants of certain languages to represent regional accents, especially when a word has differing accepted pronounciations by different peoples

<sup>b1</sup> https://github.com/open-dict-data/ipa-dict

the scope of this project is limited to the EN-GB definitions, but the only variance in choosing a different locale is pointing to another definition file. also this is to reflect the intent of the keyframer only accepting IPA, so that it's mostly language-agnostic as long as there is an IPA definition or transcription

### postmortem (2023 - )

- properly implement bilibial (lips) and labiodental (lip-and-jaw) stops
- make network nodes hold values to represent the various phonemes
	- script will still generate most timing, but symbol-to-value representation would be stored in the rig rather than relying on an external file (an external file would still be feasible, probably for purposes of syncing or external editing or transfer)
- need to device a proper way of editing word spacing/timing/stretch in maya to 
- add the following controls to abstract or adjust multiple driven actions:
	- loudness: scaling poses for larger mouth shapes, to help with shouting moments 
	- sideways rotation offset to jaw-lowering: for sideways-mouth moments, e.g. whispering

this project is not unique in any way: existing speech animation tools exist, including a toolset within Advanced Skeleton that converts audio to keyframe animation<sup>c1</sup>. I kinda saw it as an interesting topic at the time and tried to figure out as much as i could on my own

> <sup>c1</sup> LipSync example voice & Unreal export - Advanced Skeleton https://www.youtube.com/watch?v=73y3aJuScaY <br/>

## part 3: "Rigging Script Test"

⬅ github: [you're looking at it!](https://github.com/STUAAAAAAAAAART/rigStu)

see explainer in [README.md](../README.md)

but in short: it's me figuring out how does openMaya 2.0 (python) work, and how i could use it for scripting work, like node creation and networking, and rigging operations. this test is to apply a simple FK controller to every single joint in active selection