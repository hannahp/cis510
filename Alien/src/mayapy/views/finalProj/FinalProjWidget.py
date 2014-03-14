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

        #---Keyframe claw closing----
        #---Loop over the 3 claw fingers
        for i in range (1,4):
            #---current finger we are looking at
            fingerName = 'clawFinger'+str(i)
            #---initial keyframe
            cmds.setKeyframe(fingerName+"Group|"+fingerName+"Joint", attribute='rotateZ', t=lastKeyTime)
            #----After 1.5 seconds, rotate finger to -70 Z
            cmds.setKeyframe(fingerName+"Group|"+fingerName+"Joint", attribute='rotateZ', t=lastKeyTime+36, v=40)

#___________________________________________________________________________________________________ _handleDrop Claw
    #------drop the claw
    def _handleDropClaw(self):

        #Get the current time
        lastKeyTime = cmds.currentTime(query=True)
        print lastKeyTime

        #-------------------------
        #------Drop the claw------
        #-------------------------
        #Set initial status keyframe
        cmds.setKeyframe('claw', attribute='translateY', t=lastKeyTime, v=345)
        #----set keyframe for dropped claw
        cmds.setKeyframe('claw', attribute='translateY', t=lastKeyTime+72, v=20)

        #---change curTime to be time at last keyframe
        lastKeyTime = lastKeyTime+72

        #---Keyframe claw closing----
        #---Loop over the 3 claw fingers
        for i in range (1,4):
            #---current finger we are looking at
            fingerName = 'clawFinger'+str(i)
            #---initial keyframe
            cmds.setKeyframe(fingerName+"Group|"+fingerName+"Joint", attribute='rotateZ', t=lastKeyTime)
            #----After 1.5 seconds, rotate finger to -70 Z
            cmds.setKeyframe(fingerName+"Group|"+fingerName+"Joint", attribute='rotateZ', t=lastKeyTime+36, v=40)

        #--last keyframe was at lastKey+36
        lastKeyTime = lastKeyTime+36

        #-----Raise the claw----------
        #Set initial status keyframe
        cmds.setKeyframe('claw', attribute='translateY', t=lastKeyTime, v=20)
        #--raise it back to the start position of Y
        cmds.setKeyframe('claw', attribute='translateY', t=lastKeyTime+72, v=345)


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