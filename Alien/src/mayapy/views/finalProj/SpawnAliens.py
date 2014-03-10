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

MAX_DIST = 400

def spawnAliens(num_aliens):
    #----------------------Generate X-amount of aliens-------------------
    #---make gravity field if it doesn't already exist
    gravName = cmds.ls( 'alienGrav*' )
    print gravName
    if gravName == []:
        print "make grav"
        cmds.gravity(n="alienGrav", pos = (0, 0, 0), m=980, att=0, dx=0, dy=-1, dz=0, mxd=-1, vsh="none", vex=0, vof=(0, 0, 0), vsw=360, tsr=0.5)

    for i in range(0, num_aliens):

        #Give each a unique name
        curName = "alien"
        curName = curName+str(i)
        cmds.duplicate('alien', n=curName)

        #---Place in random location
        cmds.setAttr(curName+".translateX", random.randrange(-MAX_DIST, MAX_DIST))
        cmds.setAttr(curName+".translateY", 200)
        cmds.setAttr(curName+".translateZ", random.randrange(-MAX_DIST, MAX_DIST))

        #Random orientation
        cmds.setAttr(curName+".rotateX", random.randrange(360))
        cmds.setAttr(curName+".rotateY", random.randrange(360))
        cmds.setAttr(curName+".rotateZ", random.randrange(360))

        #Connect up to gravity
        cmds.connectDynamic(curName, f="alienGrav")
    #Connect up to gravity
    cmds.connectDynamic("alien", f="alienGrav")



