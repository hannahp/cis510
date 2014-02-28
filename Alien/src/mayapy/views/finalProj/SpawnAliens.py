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

MAX_DIST = 500

def spawnAliens(num_aliens):
    #----------------------Generate X-amount of molecules-------------------
    for i in range(0, num_aliens):

        #Give each a unique name
        curName = "alien"
        curName = curName+str(i)
        cmds.duplicate('alien', n=curName)

        #---Place in random location
        cmds.setAttr(curName+".translateX", random.randrange(MAX_DIST))
        #cmds.setAttr(curName+".translateY", random.randrange(MAX_DIST))
        cmds.setAttr(curName+".translateZ", random.randrange(MAX_DIST))

        #Random orientation
        cmds.setAttr(curName+".rotateX", random.randrange(360))
        cmds.setAttr(curName+".rotateY", random.randrange(360))
        cmds.setAttr(curName+".rotateZ", random.randrange(360))

