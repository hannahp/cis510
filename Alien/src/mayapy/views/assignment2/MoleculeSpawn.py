#-----------------------------------
# Author: Hannah Pruse
# Purpose: Generate 100 randomly-oriented randomly-placed
#           molecules. Animate them in random motion
#           and have the assemblies move symmetrically.
# NOTE: I also have a function to move the assemblies asymmetrically.
#       I just have not called that code anywhere.
#-----------------------------------

import random
import nimble
from nimble import cmds

#-----Constants---------
#Time between oscillations for hydrogen
OSC_RATE = 5
#Time between oscillations for hydrogen
OSC_RATE_ASSEMBLY = 7
#How many frames for total animation
ANIM_LENGTH=300
#How far the assemblies bend
BEND_SWING=20
#brownian motion offset
BROWNIAN_OFFSET=10
#number of molecules to spawn
num_molecules=150
#the max distance from origin molecules can spawn
MAX_DIST=200
#The maximum rotation of molecules (in degrees)
MAX_ROT=90
#start position of hydrogen for oscillation
HYDRO_OSC_START_POS=14
#end position of hydrogen for oscillation
HYDRO_OSC_END_POS=11
#------------------------

def setUpMolecule():
    #Adjust time slider
    cmds.playbackOptions( minTime='1', maxTime='300', mps=1)

    # Create the oxygen part of the larger bond (cylinder)
    cmds.polyCylinder(n='oxyCylinder', r=1, h=2, sx=20, sy=1, sz=1, ax=(1, 0, 0), rcp=0, cuv=3, ch=1)

    #Set scale for oxyCylinder
    cmds.setAttr("oxyCylinder.translateX", 6)
    cmds.setAttr("oxyCylinder.scaleZ", 2)
    cmds.setAttr("oxyCylinder.scaleX", 2)
    cmds.setAttr("oxyCylinder.scaleY", 2)

    #-------Set up shader and shade cylinder----------
    redShader = cmds.shadingNode('blinn', asShader=True, n='redBlinn')
    cmds.setAttr("redBlinn.color", 0.772, 0, 0, type="double3")

    cmds.select('oxyCylinder')

    cmds.hyperShade(assign=redShader)

    #--------------White Cylinder-------------

    # Create the oxygen part of the larger bond (cylinder)
    cmds.polyCylinder(n='hydroCylinder', r=1, h=2, sx=20, sy=1, sz=1, ax=(1, 0, 0), rcp=0, cuv=3, ch=1)

    #Set scale for oxyCylinder
    cmds.setAttr("hydroCylinder.translateX", 10)
    cmds.setAttr("hydroCylinder.scaleZ", 2)
    cmds.setAttr("hydroCylinder.scaleX", 2)
    cmds.setAttr("hydroCylinder.scaleY", 2)

    #-------Set up shader and shade cylinder----------
    whiteShader = cmds.shadingNode('blinn', asShader=True, n='whiteBlinn')
    cmds.setAttr("whiteBlinn.color", 1, 1, 1, type="double3")

    #Select the cylinder to color
    cmds.select('hydroCylinder')
    # Assign shader
    cmds.hyperShade(assign=whiteShader)

    #----------------------------------------------------------
    #-----------Group two cylinders together as "cylinder"-----
    #----------------------------------------------------------
    cmds.group(em=True, n='cylinder')
    cmds.parent('oxyCylinder', 'cylinder')
    cmds.parent('hydroCylinder', 'cylinder')

    #------------Oxygen-------------

    # Create the Oxygen sphere
    cmds.polySphere(n='oxygen', r=1, sx=20, sy=20, ax=(0, 1, 0), cuv=2, ch=1)

    #Set scale for oxygen
    cmds.setAttr("oxygen.scaleZ", 5)
    cmds.setAttr("oxygen.scaleX", 5)
    cmds.setAttr("oxygen.scaleY", 5)

    #-------Assign shader--------
    cmds.select('oxygen')

    cmds.hyperShade(assign=redShader)

    #------------Hydrogen-------------

    # Create the Hydrogen sphere
    cmds.polySphere(n='hydrogen', r=1, sx=20, sy=20, ax=(0, 1, 0), cuv=2, ch=1)

    #Set scale for oxygen
    cmds.setAttr("hydrogen.translateX", 14)
    cmds.setAttr("hydrogen.scaleZ", 4)
    cmds.setAttr("hydrogen.scaleX", 4)
    cmds.setAttr("hydrogen.scaleY", 4)

    #-------Assign shader--------
    cmds.select('hydrogen')

    cmds.hyperShade(assign=whiteShader)

    #----------------------------------------------------------
    #-----------Group 'cylinder' and hydrogen together as "hydroAssembly"-----
    #----------------------------------------------------------
    cmds.group(em=True, n='hydroAssembly1')
    cmds.parent('cylinder', 'hydroAssembly1')
    cmds.parent('hydrogen', 'hydroAssembly1')

    #----------------------------------------------------------
    #-----------Group into realign group
    #----------------------------------------------------------
    cmds.group(em=True, n='realignGroup1')
    cmds.parent('hydroAssembly1', 'realignGroup1')

    #-------------------------------------------------------------
    #------------Duplicate the assembly--------------------------
    #-------------------------------------------------------------
    cmds.duplicate('realignGroup1', n='realignGroup2')
    cmds.setAttr('realignGroup2.rotateZ', 180)
    cmds.rename('realignGroup2|hydroAssembly1','hydroAssembly2')

    #----------------------------------------------------------
    #-----------Make entire thing a group "molecule"-----
    #----------------------------------------------------------
    cmds.group(em=True, n='molecule')
    cmds.parent('oxygen', 'molecule')
    cmds.parent('realignGroup1', 'molecule')
    cmds.parent('realignGroup2', 'molecule')

    #-------Move entire molecule up-------
    cmds.setAttr("molecule.translateY", 10)

#-------------Define animation functions--------------
# Param stringName should be the name of a transform node
def rotX(stringName, timeEnd, valEnd):
    curRotation = cmds.getAttr(stringName+"|realignGroup1|hydroAssembly1.rotateX")
    #cmds.setKeyframe(stringName, at="rotateX", t=timeStart, v=curRotation)
    cmds.setKeyframe(stringName, at="rotateX", t=timeEnd, v=valEnd)
#--------------------------------------------------------------------------------------------------------------------

def rotY(stringName, timeEnd, valEnd):
    curRotation = cmds.getAttr(stringName+"|realignGroup1|hydroAssembly1.rotateY")
    #cmds.setKeyframe(stringName, at="rotateY", t=timeStart, v=curRotation)
    cmds.setKeyframe(stringName, at="rotateY", t=timeEnd, v=valEnd)
#--------------------------------------------------------------------------------------------------------------------

def rotZ(stringName, timeEnd, valEnd):
    curRotation = cmds.getAttr(stringName+"|realignGroup1|hydroAssembly1.rotateZ")
    #cmds.setKeyframe(stringName, at="rotateZ", t=timeStart, v=curRotation)
    cmds.setKeyframe(stringName, at="rotateZ", t=timeEnd, v=valEnd)
#--------------------------------------------------------------------------------------------------------------------

def symStretch(stringName):
    #Keyframe Hydrogen on assembly 2
    cmds.setKeyframe(stringName+"|realignGroup2|hydroAssembly2|hydrogen", at="translateX", t=0, v=HYDRO_OSC_START_POS)
    cmds.setKeyframe(stringName+"|realignGroup2|hydroAssembly2|hydrogen", at="translateX", t=OSC_RATE, v=HYDRO_OSC_END_POS)
    cmds.selectKey(stringName+"|realignGroup2|hydroAssembly2|hydrogen", at="translateX")#, t=('0sec', OSC_RATE))
    cmds.setInfinity(stringName+"|realignGroup2|hydroAssembly2|hydrogen", at="translateX", pri='oscillate', poi='oscillate')
    cmds.keyTangent(stringName+"|realignGroup2|hydroAssembly2|hydrogen", itt='plateau')#, time=(0, OSC_RATE))
    
    #Keyframe the cylinder movement on assembly 2
    cmds.setKeyframe(stringName+"|realignGroup2|hydroAssembly2", at="translateX", t=0, v=0)
    cmds.setKeyframe(stringName+"|realignGroup2|hydroAssembly2", at="translateX", t=OSC_RATE_ASSEMBLY, v=-1)
    cmds.selectKey(stringName+"|realignGroup2|hydroAssembly2", at="translateX")#, t=('0sec', OSC_RATE_ASSEMBLY))
    cmds.setInfinity(stringName+"|realignGroup2|hydroAssembly2", at="translateX", pri='oscillate', poi='oscillate')
    cmds.keyTangent(stringName+"|realignGroup2|hydroAssembly2", itt='plateau')#, time=(0, OSC_RATE_ASSEMBLY))
    
    #Keyframe Hydrogen on assembly 1
    cmds.setKeyframe(stringName+"|realignGroup1|hydroAssembly1|hydrogen", at="translateX", t=0, v=HYDRO_OSC_START_POS)
    cmds.setKeyframe(stringName+"|realignGroup1|hydroAssembly1|hydrogen", at="translateX", t=OSC_RATE, v=HYDRO_OSC_END_POS)
    cmds.selectKey(stringName+"|realignGroup1|hydroAssembly1|hydrogen", at="translateX")#, t=['0sec', OSC_RATE+'sec'])
    cmds.setInfinity(stringName+"|realignGroup1|hydroAssembly1|hydrogen", at="translateX", pri='oscillate', poi='oscillate')
    cmds.keyTangent(stringName+"|realignGroup1|hydroAssembly1|hydrogen", itt='plateau')#, time=(0, OSC_RATE))
    
    #Keyframe the cylinder movement on assembly 2
    cmds.setKeyframe(stringName+"|realignGroup1|hydroAssembly1", at="translateX", t=0, v=0)
    cmds.setKeyframe(stringName+"|realignGroup1|hydroAssembly1", at="translateX", t=OSC_RATE_ASSEMBLY, v=-1)
    cmds.selectKey(stringName+"|realignGroup1|hydroAssembly1", at="translateX")#, t=['0sec', OSC_RATE_ASSEMBLY+'sec'])
    cmds.setInfinity(stringName+"|realignGroup1|hydroAssembly1", at="translateX", pri='oscillate', poi='oscillate')
    cmds.keyTangent(stringName+"|realignGroup1|hydroAssembly1", itt='plateau')#, time=(0, OSC_RATE_ASSEMBLY))
#--------------------------------------------------------------------------------------------------------------------

def asymStretch(stringName):
    #Keyframe Hydrogen on assembly 2
    cmds.setKeyframe(stringName+"|realignGroup2|hydroAssembly2|hydrogen", at="translateX", t=0, v=HYDRO_OSC_START_POS)
    cmds.setKeyframe(stringName+"|realignGroup2|hydroAssembly2|hydrogen", at="translateX", t=OSC_RATE, v=HYDRO_OSC_END_POS)
    cmds.selectKey(stringName+"|realignGroup2|hydroAssembly2|hydrogen", at="translateX")#, t=['0sec', OSC_RATE+'sec'])
    cmds.setInfinity(stringName+"|realignGroup2|hydroAssembly2|hydrogen", at="translateX", pri='oscillate', poi='oscillate')
    cmds.keyTangent(stringName+"|realignGroup2|hydroAssembly2|hydrogen", itt='plateau')#, time=(0, OSC_RATE))
    
    #Keyframe the cylinder movement on assembly 2
    cmds.setKeyframe(stringName+"|realignGroup2|hydroAssembly2", at="translateX", t=0, v=0)
    cmds.setKeyframe(stringName+"|realignGroup2|hydroAssembly2", at="translateX", t=OSC_RATE_ASSEMBLY, v=-1)
    cmds.selectKey(stringName+"|realignGroup2|hydroAssembly2", at="translateX")#, t=['0sec', OSC_RATE_ASSEMBLY+'sec'])
    cmds.setInfinity(stringName+"|realignGroup2|hydroAssembly2", at="translateX", pri='oscillate', poi='oscillate')
    cmds.keyTangent(stringName+"|realignGroup2|hydroAssembly2", itt='plateau')#, time=(0, OSC_RATE_ASSEMBLY))
    
    #Keyframe the hydrogen on assembly 1
    cmds.setKeyframe(stringName+"|realignGroup1|hydroAssembly1|hydrogen", at="translateX", t=0, v=HYDRO_OSC_END_POS)
    cmds.setKeyframe(stringName+"|realignGroup1|hydroAssembly1|hydrogen", at="translateX", t=OSC_RATE, v=HYDRO_OSC_START_POS)
    cmds.selectKey(stringName+"|realignGroup1|hydroAssembly1|hydrogen", at="translateX")#, t=['0sec', OSC_RATE+'sec'])
    cmds.setInfinity(stringName+"|realignGroup1|hydroAssembly1|hydrogen", at="translateX", pri='oscillate', poi='oscillate')
    cmds.keyTangent(stringName+"|realignGroup1|hydroAssembly1|hydrogen", itt='plateau')#, time=(0, OSC_RATE))
    
    #Keyframe the cylinder movement on assembly 2
    cmds.setKeyframe(stringName+"|realignGroup1|hydroAssembly1", at="translateX", t=0, v=-1)
    cmds.setKeyframe(stringName+"|realignGroup1|hydroAssembly1", at="translateX", t=OSC_RATE_ASSEMBLY, v=0)
    cmds.selectKey(stringName+"|realignGroup1|hydroAssembly1", at="translateX")#, t=['0sec', OSC_RATE_ASSEMBLY+'sec'])
    cmds.setInfinity(stringName+"|realignGroup1|hydroAssembly1", at="translateX", pri='oscillate', poi='oscillate')
    cmds.keyTangent(stringName+"|realignGroup1|hydroAssembly1", itt='plateau')#, time=(0, OSC_RATE_ASSEMBLY))
#--------------------------------------------------------------------------------------------------------------------
def bend(stringName):
    keyt = (0, OSC_RATE_ASSEMBLY)
    curRotation = cmds.getAttr(stringName+"|realignGroup1|hydroAssembly1.rotateZ")
    cmds.setKeyframe(stringName+"|realignGroup1|hydroAssembly1", at="rotateZ", t=0, v=-curRotation)
    cmds.setKeyframe(stringName+"|realignGroup1|hydroAssembly1", at="rotateZ", t=OSC_RATE_ASSEMBLY, v=BEND_SWING)
    cmds.selectKey(stringName+"|realignGroup1|hydroAssembly1", at="rotateZ")
    cmds.setInfinity(stringName+"|realignGroup1|hydroAssembly1", at="rotateZ", pri='oscillate', poi='oscillate')
    cmds.keyTangent(stringName+"|realignGroup1|hydroAssembly1", itt='plateau') #time=(0, OSC_RATE_ASSEMBLY))
    
    curRotation = cmds.getAttr(stringName+"|realignGroup2|hydroAssembly2.rotateZ")
    cmds.setKeyframe(stringName+"|realignGroup2|hydroAssembly2", at="rotateZ", t=0, v=-curRotation)
    cmds.setKeyframe(stringName+"|realignGroup2|hydroAssembly2", at="rotateZ", t=OSC_RATE_ASSEMBLY, v=-BEND_SWING)
    cmds.selectKey(stringName+"|realignGroup2|hydroAssembly2", at="rotateZ")
    cmds.setInfinity(stringName+"|realignGroup2|hydroAssembly2", at="rotateZ", pri='oscillate', poi='oscillate')
    cmds.keyTangent(stringName+"|realignGroup2|hydroAssembly2", itt='plateau') #time=(0, OSC_RATE_ASSEMBLY))


#---set up dictionary of animations to choose from
#---Right now only 3-6 are being called via this dictionary;
#--however, this can be expanded in the future to have the molecules
#--choose asym or sym stretching and bending every few seconds as well
#---The current configuration was chosen based on my understanding of molecule behavior

num = random.randrange(0,6)
animations = {0 : symStretch,
    1 : asymStretch,
    2 : bend,
    3 : rotX,
    4 : rotY,
    5 : rotZ
    }

def spawnMolecules(num_molecules):
    #----------------------Generate X-amount of molecules-------------------
    setUpMolecule()
    for i in range(0, num_molecules):

        #Give each a unique name
        curName = "molecule"
        curName = curName+str(i)
        cmds.duplicate('molecule', n=curName)

        #---Place in random location
        cmds.setAttr(curName+".translateX", random.randrange(MAX_DIST))
        cmds.setAttr(curName+".translateY", random.randrange(MAX_DIST))
        cmds.setAttr(curName+".translateZ", random.randrange(MAX_DIST))

        #Random orientation
        cmds.setAttr(curName+".rotateX", random.randrange(360))
        cmds.setAttr(curName+".rotateY", random.randrange(360))
        cmds.setAttr(curName+".rotateZ", random.randrange(360))

        #Set rotation of legs
        #These set numbers are arbitrary, but these locations looked good.
        cmds.setAttr(curName+"|realignGroup1.rotateZ", -39.4)#random.randrange(360))
        cmds.setAttr(curName+"|realignGroup2.rotateZ", 217.6)#cmds.getAttr(curName+"|hydroAssembly1.rotateZ")+104)

        #Get number from 0 to 1. 0=symmetrical 1= asymmetrical
        stretchType = random.randrange(0,2)

        #Set up stretching anims based on our assigned type
        if stretchType == 0:
            symStretch(curName)
        else:
            asymStretch(curName)

        #Set up bending motion (oscillating animation)
        bend(curName)

        #Set some random movement
        for i in range(1, ANIM_LENGTH):
            #--------Assign a random animation state----------
            #---Move molecule to new location every five frames
            if i % 5 == 0:
                curPosX = cmds.getAttr(curName+".translateX")
                curPosY = cmds.getAttr(curName+".translateY")
                curPosZ = cmds.getAttr(curName+".translateZ")

                #Move to random position and keyframe
                cmds.setKeyframe(curName, at="translateX", t=i, v=curPosX + random.randrange(BROWNIAN_OFFSET))
                cmds.setKeyframe(curName, at="translateY", t=i, v=curPosY + random.randrange(BROWNIAN_OFFSET))
                cmds.setKeyframe(curName, at="translateZ", t=i, v=curPosZ + random.randrange(BROWNIAN_OFFSET))

            #Every five frames, randomly rotate
            if i % 5 == 0 and i != 0:
                #Random rotation
                randNum = random.randrange(3,6)
                animations[randNum](curName, i, random.randrange(MAX_ROT))

    #--_Delete first molecule that we used to duplicate the rest
    cmds.delete('molecule')