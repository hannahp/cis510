# Assignment1Widget.py
# (C)2013
# Scott Ernst

import nimble
from nimble import cmds
import SpawnAliens
from pyglass.widgets.PyGlassWidget import PyGlassWidget
import random

#___________________________________________________________________________________________________ Assignment1Widget
class FinalProjWidget(PyGlassWidget):
    """A class for Assignment 1"""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        """Creates a new instance of Assignment1Widget."""
        super(FinalProjWidget, self).__init__(parent, **kwargs)
        self.homeBtn.clicked.connect(self._handleReturnHome)
        self.spawnButton.clicked.connect(self._handleSpawn)
        self.dropButton.clicked.connect(self._handleDropClaw)
        self.releaseButton.clicked.connect(self._handleReleaseClaw)
        self.clawHorizSlide.valueChanged.connect(self._handleHorizMove)
        self.clawVertSlide.valueChanged.connect(self._handleDepthMove)

        #---Key buttons-----
        self.keyClawPos.clicked.connect(self._handleKeyClawPos)


#===================================================================================================

#___________________________________________________________________________________________________ _handleReturnHome
    def _handleReturnHome(self):
        self.mainWindow.setActiveWidget('home')

#___________________________________________________________________________________________________ _handleSpawn
    #------Spawn all the aliens!
    def _handleSpawn(self):
        numAliens = self.numAliensSpinBox.value()
        SpawnAliens.spawnAliens(numAliens)
#___________________________________________________________________________________________________
    #------Move the claw L/R
    def _handleHorizMove(self):
        horizPos = self.clawHorizSlide.value()
        cmds.setAttr('claw.translateX', horizPos)
#___________________________________________________________________________________________________
    #------Move the claw forward/back
    def _handleDepthMove(self):
        vertPos = self.clawVertSlide.value()
        cmds.setAttr('claw.translateZ', vertPos)
#___________________________________________________________________________________________________
    #------Move the claw forward/back
    def _handleReleaseClaw(self):
        #Get the current time
        lastKeyTime = cmds.currentTime(query=True)

        #---Keyframe claw opening----
        #---Loop over the 3 claw fingers
        for i in range (1,4):
            #---current finger we are looking at
            fingerName = 'clawFinger'+str(i)
            #---initial keyframe
            cmds.setKeyframe('claw|'+fingerName+'Realign|'+fingerName, attribute='rotateZ', t=lastKeyTime)
            #----After 1.5 seconds, rotate finger to -110 Z
            cmds.setKeyframe('claw|'+fingerName+'Realign|'+fingerName, attribute='rotateZ', t=lastKeyTime+36, v=-110)

        lastKeyTime = lastKeyTime+36

        #------------------------------------
        #----UNPARENT the alien to the claw.
        #------------------------------------

        #-------Get the alien selected
        selectedAlien = cmds.ls(selection=True)[0]
        #------Get the alien's rigidBody name
        #selRB = cmds.listRelatives(selectedAlien, s=True)[0]


        #-----get the constraint node name
        transform = selectedAlien
        constraintNode = cmds.listConnections('%s.rotateOrder' % transform, source=True)[0]
        if not cmds.nodeType(constraintNode) == 'parentConstraint':
            raise RuntimeError('Node %s is not of type constraint' % constraintNode)

        #----Key the swap of weights from the base
        cmds.setKeyframe(constraintNode+".clawBaseW0", t=lastKeyTime, v=1)
        cmds.setKeyframe(constraintNode+".clawBaseW0", t=lastKeyTime+1, v=0)
        #---Keyframe the swap of weights to the locator
        cmds.setKeyframe(constraintNode+"."+selectedAlien+"LocW1", t=lastKeyTime, v=0)
        cmds.setKeyframe(constraintNode+"."+selectedAlien+"LocW1", t=lastKeyTime+1, v=1)

        lastKeyTime = lastKeyTime+1 #AFTER swapping weights

        #---Keyframe the blend parent
        cmds.setKeyframe(selectedAlien+".blendParent1", t=lastKeyTime, v=1)
        cmds.setKeyframe(selectedAlien+".blendParent1", t=lastKeyTime+1, v=0)

        #-------Key the Active attribute to be on----
        #cmds.setKeyframe(selRB, attribute='act', t=lastKeyTime, v=0)
        #cmds.setKeyframe(selRB, attribute='act', t=lastKeyTime+1, v=1)

#___________________________________________________________________________________________________ _handleDrop Claw
    #------drop the claw
    def _handleDropClaw(self):

        #-----------------------------------
        #-----CHECK IF ALIEN IS SELECTED----
        #-----------------------------------
        selItems = cmds.ls('alien*', selection=True)
        if selItems==[]:
            print "Please select an alien to pick up"
            return

        #---------If an alien is selected......
        else:

            #Get the current time
            lastKeyTime = cmds.currentTime(query=True)
            print lastKeyTime

            #Set initial status keyframe
            cmds.setKeyframe('claw', attribute='translateY', t=lastKeyTime, v=345)
            #-----Move the claw down so the parenting looks realistic
            cmds.setAttr('claw.translateY', 20)
            #----set keyframe for dropped claw
            cmds.setKeyframe('claw', attribute='translateY', t=lastKeyTime+72)


            #---change curTime to be time at last keyframe
            lastKeyTime = lastKeyTime+72

            #---Keyframe claw closing----
            #---Loop over the 3 claw fingers
            for i in range (1,4):
                #---current finger we are looking at
                fingerName = 'clawFinger'+str(i)
                #---initial keyframe
                cmds.setKeyframe('claw|'+fingerName+'Realign|'+fingerName, attribute='rotateZ', t=lastKeyTime)
                #----After 1.5 seconds, rotate finger to -70 Z
                cmds.setKeyframe('claw|'+fingerName+'Realign|'+fingerName, attribute='rotateZ', t=lastKeyTime+36, v=-70)

            #--last keyframe was at lastKey+36
            lastKeyTime = lastKeyTime+36

            #----Grab selected alien's name
            selectedAlien = cmds.ls(selection=True)[0]
            #------Get the alien's rigidBody name
            #selRB = cmds.listRelatives(selectedAlien, s=True)[0]

            #-------Key the Active attribute to be off----
            #cmds.setKeyframe(selRB, attribute='act', t=lastKeyTime-1, v=1)
            #cmds.setKeyframe(selRB, attribute='act', t=lastKeyTime, v=0)

            #----Create a locator where the alien is----
            existingAlienLoc = cmds.ls(selectedAlien+"Loc")
            alienLoc = selectedAlien+"Loc"
            alienPos = cmds.xform(selectedAlien, q=1, ws=1, t=1)
            if existingAlienLoc == []:
                cmds.spaceLocator(n=alienLoc)
                cmds.move(alienPos[0], alienPos[1], alienPos[2], alienLoc)

            #---------------------------------------------------------
            #-------Check to see if parent relationship already exists.
            #---------------------------------------------------------

            clawParent = cmds.ls(selectedAlien+"_parent*", type='constraint')

            #----If no parent yet, make one------
            if clawParent == []:
                #----PARENT the alien to the claw.
                cmds.parentConstraint('clawBase', selectedAlien, mo=True)
                #----PARENT the alien to the locator.
                cmds.parentConstraint(alienLoc, selectedAlien, mo=True)

            #---move the claw back, as we want it to start at the top. This was just for parenting purposes
            cmds.setAttr('claw.translateY', 345)

            #-----get the constraint node name
            transform = selectedAlien
            constraintNode = cmds.listConnections('%s.rotateOrder' % transform, source=True)[0]
            if not cmds.nodeType(constraintNode) == 'parentConstraint':
                raise RuntimeError('Node %s is not of type constraint' % constraintNode)

            #---Keyframe the blend parent
            cmds.setKeyframe(selectedAlien+".blendParent1", t=lastKeyTime, v=0)
            cmds.setKeyframe(selectedAlien+".blendParent1", t=lastKeyTime+1, v=1)
            #---Keyframe the swap between the weights of the two parents
            cmds.setKeyframe(constraintNode+".clawBaseW0", t=lastKeyTime, v=0)
            cmds.setKeyframe(constraintNode+".clawBaseW0", t=lastKeyTime+1, v=1)
            cmds.setKeyframe(constraintNode+"."+alienLoc+"W1", t=lastKeyTime, v=1)
            cmds.setKeyframe(constraintNode+"."+alienLoc+"W1", t=lastKeyTime+1, v=0)
            #---Make sure we start with this constraint off
            cmds.setAttr(constraintNode+".clawBaseW0", 0)

            lastKeyTime = lastKeyTime+1

            #-----Raise the claw----------
            #Set initial status keyframe
            cmds.setKeyframe('claw', attribute='translateY', t=lastKeyTime, v=20)
            #--raise it back to the start position of Y
            cmds.setKeyframe('claw', attribute='translateY', t=lastKeyTime+72, v=345)

            #-----Raise the Locator------
            #Set initial status keyframe
            cmds.setKeyframe(alienLoc, attribute='translateY', t=lastKeyTime, v=alienPos[1])
            #--raise it back to the start position of Y
            cmds.setKeyframe(alienLoc, attribute='translateY', t=lastKeyTime+72, v=345)
    # def _handleDropClaw(self):
    #
    #     #-----------------------------------
    #     #-----CHECK IF ALIEN IS SELECTED----
    #     #-----------------------------------
    #     selItems = cmds.ls('alien*', selection=True)
    #     if selItems==[]:
    #         print "Please select an alien to pick up"
    #         return
    #
    #     #---------If an alien is selected......
    #     else:
    #
    #         #Get the current time
    #         lastKeyTime = cmds.currentTime(query=True)
    #         print lastKeyTime
    #
    #         #Set initial status keyframe
    #         cmds.setKeyframe('claw', attribute='translateY', t=lastKeyTime, v=345)
    #         #-----Move the claw down so the parenting looks realistic
    #         cmds.setAttr('claw.translateY', 20)
    #         #----set keyframe for dropped claw
    #         cmds.setKeyframe('claw', attribute='translateY', t=lastKeyTime+72)
    #
    #
    #         #---change curTime to be time at last keyframe
    #         lastKeyTime = lastKeyTime+72
    #
    #         #---Keyframe claw closing----
    #         #---Loop over the 3 claw fingers
    #         for i in range (1,4):
    #             #---current finger we are looking at
    #             fingerName = 'clawFinger'+str(i)
    #             #---initial keyframe
    #             cmds.setKeyframe('claw|'+fingerName+'Realign|'+fingerName, attribute='rotateZ', t=lastKeyTime)
    #             #----After 1.5 seconds, rotate finger to -70 Z
    #             cmds.setKeyframe('claw|'+fingerName+'Realign|'+fingerName, attribute='rotateZ', t=lastKeyTime+36, v=-70)
    #
    #         #--last keyframe was at lastKey+36
    #         lastKeyTime = lastKeyTime+36
    #
    #         #----Grab selected alien's name
    #         selectedAlien = cmds.ls(selection=True)[0]
    #
    #         alienLoc = selectedAlien+"Loc"
    #         alienPos = cmds.xform(selectedAlien, q=1, ws=1, t=1)
    #
    #
    #         #---------------------------------------------------------
    #         #-------Check to see if parent relationship already exists.
    #         #---------------------------------------------------------
    #
    #         clawParent = cmds.ls(selectedAlien+"_parent*", type='constraint')
    #
    #         #-----Raise the claw----------
    #         #Set initial status keyframe
    #         cmds.setKeyframe('claw', attribute='translateY', t=lastKeyTime, v=20)
    #         #--raise it back to the start position of Y
    #         cmds.setKeyframe('claw', attribute='translateY', t=lastKeyTime+72, v=345)
    #
    #         #-----Raise the alien----------
    #         #Set initial status keyframe
    #         cmds.setKeyframe(selectedAlien, attribute='translateY', t=lastKeyTime, v=20)
    #         #--raise it back to the start position of Y
    #         cmds.setKeyframe(selectedAlien, attribute='translateY', t=lastKeyTime+72, v=345)
    #
    #         lastKeyTime = lastKeyTime +72
    #
    #         #----If no parent yet, make one------
    #         if clawParent == []:
    #             #----PARENT the alien to the claw.
    #             cmds.parentConstraint('clawBase', selectedAlien, mo=True)
    #
    #         #---move the claw back, as we want it to start at the top. This was just for parenting purposes
    #         cmds.setAttr('claw.translateY', 345)
    #
    #         #-----get the constraint node name
    #         transform = selectedAlien
    #         constraintNode = cmds.listConnections('%s.rotateOrder' % transform, source=True)[0]
    #         if not cmds.nodeType(constraintNode) == 'parentConstraint':
    #             raise RuntimeError('Node %s is not of type constraint' % constraintNode)
    #
    #         #---Keyframe the blend parent
    #         cmds.setKeyframe(selectedAlien+".blendParent1", t=lastKeyTime, v=0)
    #         cmds.setKeyframe(selectedAlien+".blendParent1", t=lastKeyTime+1, v=1)
    #         #---Keyframe the swap between the weights of the two parents
    #         cmds.setKeyframe(constraintNode+".clawBaseW0", t=lastKeyTime, v=0)
    #         cmds.setKeyframe(constraintNode+".clawBaseW0", t=lastKeyTime+1, v=1)
    #         #cmds.setKeyframe(constraintNode+"."+alienLoc+"W1", t=lastKeyTime, v=1)
    #         #cmds.setKeyframe(constraintNode+"."+alienLoc+"W1", t=lastKeyTime+1, v=0)
    #         #---Make sure we start with this constraint off
    #         cmds.setAttr(constraintNode+".clawBaseW0", 0)
    #
    #         lastKeyTime = lastKeyTime+1



#----------------------------------------------
#------Key button handlers---------------------
#----------------------------------------------

#___________________________________________________________________________________________________
    #-------Key horiz pos
    def keyHoriz(self):
        cmds.setKeyframe('claw', attribute='translateX')
#___________________________________________________________________________________________________
    #-------Key horiz pos
    def keyDepth(self):
        cmds.setKeyframe('claw', attribute='translateZ')
#___________________________________________________________________________________________________
    #-------Key horiz pos
    def _handleKeyClawPos(self):
        self.keyHoriz()
        self.keyDepth()