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



#===================================================================================================

#___________________________________________________________________________________________________ _handleReturnHome
    def _handleReturnHome(self):
        self.mainWindow.setActiveWidget('home')

#___________________________________________________________________________________________________ _handleSpawn
    #------Spawn all the aliens!
    def _handleSpawn(self):
        numAliens = self.numAliensSpinBox.value()
        SpawnAliens.spawnAliens(numAliens)
#___________________________________________________________________________________________________ _handleDrop Claw
    #------drop the claw
    def _handleDropClaw(self):
        #Get the current time
        lastKeyTime = cmds.currentTime(query=True)

        #Set initial status keyframe
        cmds.setKeyframe('claw', attribute='translateY')
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
            cmds.setKeyframe('claw|'+fingerName+'Realign|'+fingerName, attribute='rotateZ', t=lastKeyTime)
            #----After 1.5 seconds, rotate finger to -70 Z
            cmds.setKeyframe('claw|'+fingerName+'Realign|'+fingerName, attribute='rotateZ', t=lastKeyTime+36, v=-70)

        #--last keyframe was at lastKey+36
        lastKeyTime = lastKeyTime+36

        #-----Raise the claw----------
        #Set initial status keyframe
        cmds.setKeyframe('claw', attribute='translateY', t=lastKeyTime, v=20)
        #--raise it back to the start position of Y
        cmds.setKeyframe('claw', attribute='translateY', t=lastKeyTime+72, v=345)

