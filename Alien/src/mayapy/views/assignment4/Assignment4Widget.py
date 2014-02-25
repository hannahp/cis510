# Assignment1Widget.py
# (C)2013
# Scott Ernst

import nimble
from nimble import cmds
from pyglass.widgets.PyGlassWidget import PyGlassWidget
import random

#___________________________________________________________________________________________________ Assignment1Widget
class Assignment4Widget(PyGlassWidget):
    """A class for Assignment 1"""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        """Creates a new instance of Assignment1Widget."""
        super(Assignment4Widget, self).__init__(parent, **kwargs)
        self.homeBtn.clicked.connect(self._handleReturnHome)
        self.setUpButton.clicked.connect(self._handleSetup)
        self.blinkSlider.sliderMoved.connect(self._handleBlinkSlider)
        self.eyesSlider.valueChanged.connect(self._handleEyeSlider)


#===================================================================================================

#___________________________________________________________________________________________________ _handleReturnHome
    def _handleReturnHome(self):
        self.mainWindow.setActiveWidget('home')

#___________________________________________________________________________________________________ _handleReturnHome
    #------Get slider value and update the 'blink' values
    def _handleBlinkSlider(self):
        value = self.blinkSlider.value()
        cmds.setAttr("eyeTargets.blinkLeft", value)
        cmds.setAttr("eyeTargets.blinkMiddle", value)
        cmds.setAttr("eyeTargets.blinkRight", value)
#___________________________________________________________________________________________________ _handleReturnHome
    #-------Get slider value and move the eye targets
    def _handleEyeSlider(self):
        value = self.eyesSlider.value()
        EYE_START_POS = 137
        cmds.setAttr("eyeTargets.translateY", EYE_START_POS+value)

#--------------------------------------------------------------------------------------------------- _handleSetup
    ####Set up set-driven keys and rig. THIS SHOULD ONLY HAPPEN ONCE!!!!
    def _handleSetup(self):
        #----Set up dictionary for later use. Numbers are creation order from my modeling (important for NURBS naming)-
        direction = {"Left":2, "Middle":1, "Right":3}
        BLINK_LENGTH =6
        EYE_TARGET_LOW_BOUND = -11.038498
        EYE_TARGET_UPPER_BOUND = 16.118241
        EYE_START_POS = 137

        #----Add attrs for each eyelid
        for dir in direction:
            #------Put in "blink" attributes on the eye target------
            cmds.select("eyeTargets")

            #---Add the attribute "blink" for each eye onto the target
            cmds.addAttr(ln="blink"+dir, at="double", min=0, max=6, dv=0 )
            cmds.setAttr("eyeTargets.blink"+dir, keyable=True)

            #----Key the blinks----
            cmds.select("eyelid"+dir, r=True)
            cmds.select("makeNurbSphere"+str(direction[dir]), addFirst=True)
            #---Make sure the eyelid is in the correct start position----
            cmds.setAttr("makeNurbSphere"+str(direction[dir])+".startSweep", 10)
            cmds.setAttr("makeNurbSphere"+str(direction[dir])+".endSweep", 300)
            #---Set init key
            cmds.setDrivenKeyframe("makeNurbSphere"+str(direction[dir])+".startSweep", cd="eyeTargets.blink"+dir)
            cmds.setDrivenKeyframe("makeNurbSphere"+str(direction[dir])+".endSweep", cd="eyeTargets.blink"+dir)
            #----Clear selection and move driver for next key
            cmds.select(cl=True)
            cmds.setAttr("eyeTargets.blink"+dir, BLINK_LENGTH)
            #~~~move eyelid
            cmds.setAttr("makeNurbSphere"+str(direction[dir])+".startSweep", 0)
            cmds.setAttr("makeNurbSphere"+str(direction[dir])+".endSweep", 360)
            #---Set key
            cmds.setDrivenKeyframe("makeNurbSphere"+str(direction[dir])+".startSweep", cd="eyeTargets.blink"+dir)
            cmds.setDrivenKeyframe("makeNurbSphere"+str(direction[dir])+".endSweep", cd="eyeTargets.blink"+dir)
            #---reset our blink value, so it starts back at 0 once we set up
            cmds.setAttr("eyeTargets.blink"+dir, 0)

            #----Key the eyelid movement----
            #---Set key
            cmds.setAttr("eyeTargets.translateY", EYE_START_POS)
            cmds.setDrivenKeyframe("makeNurbSphere"+str(direction[dir])+".startSweep", cd="eyeTargets.translateY")
            cmds.setDrivenKeyframe("makeNurbSphere"+str(direction[dir])+".endSweep", cd="eyeTargets.translateY")
            #~~~Move eye target down
            cmds.setAttr("eyeTargets.translateY", EYE_START_POS+EYE_TARGET_LOW_BOUND)
            #---adjust eyelid sweep
            cmds.setAttr("makeNurbSphere"+str(direction[dir])+".startSweep", 35)
            cmds.setAttr("makeNurbSphere"+str(direction[dir])+".endSweep", 340)
            #---Set key
            cmds.setDrivenKeyframe("makeNurbSphere"+str(direction[dir])+".startSweep", cd="eyeTargets.translateY")
            cmds.setDrivenKeyframe("makeNurbSphere"+str(direction[dir])+".endSweep", cd="eyeTargets.translateY")
            #------
            #-----
            #~~~~Move Eye target up
            cmds.setAttr("eyeTargets.translateY", EYE_START_POS+EYE_TARGET_UPPER_BOUND)
            #---adjust eyelid sweep
            cmds.setAttr("makeNurbSphere"+str(direction[dir])+".startSweep", -20)
            cmds.setAttr("makeNurbSphere"+str(direction[dir])+".endSweep", 260)
            #---Set key
            cmds.setDrivenKeyframe("makeNurbSphere"+str(direction[dir])+".startSweep", cd="eyeTargets.translateY")
            cmds.setDrivenKeyframe("makeNurbSphere"+str(direction[dir])+".endSweep", cd="eyeTargets.translateY")
            #------Reset target
            cmds.setAttr("eyeTargets.translateY", EYE_START_POS)
            #-----
