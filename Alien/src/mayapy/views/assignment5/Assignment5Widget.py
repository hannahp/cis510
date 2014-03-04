# Assignment1Widget.py
# (C)2013
# Scott Ernst

import nimble
from nimble import cmds
from pyglass.widgets.PyGlassWidget import PyGlassWidget
import random

#___________________________________________________________________________________________________ Assignment1Widget
class Assignment5Widget(PyGlassWidget):
    """A class for Assignment 1"""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        """Creates a new instance of Assignment1Widget."""
        super(Assignment5Widget, self).__init__(parent, **kwargs)
        self.homeBtn.clicked.connect(self._handleReturnHome)
        self.oohSlider.valueChanged.connect(self._handleOohSlider)
        self.smileSlider.valueChanged.connect(self._handleSmileSlider)
        self.screamSlider.valueChanged.connect(self._handleScreamSlider)
        self.eyesSlider.valueChanged.connect(self._handleEyeSlider)
        self.cameraSlider.valueChanged.connect(self._handleCameraSlider)
        self.dollySlider.valueChanged.connect(self._handleDollySlider)
        self.eyesUDSlider.valueChanged.connect(self._handleEyeUDSlider)
        self.blinkSlider.valueChanged.connect(self._handleBlinkSlider)
        self.resetButton.clicked.connect(self._handleReset)
        self.keyAll.clicked.connect(self._handleKeyAll)

        #----Handle Key buttons
        self.keyOoh.clicked.connect(self._handleKeyOoh)
        self.keySmile.clicked.connect(self._handleKeySmile)
        self.keyScream.clicked.connect(self._handleKeyScream)
        self.keyBlink.clicked.connect(self._handleKeyBlink)
        self.keyEyesLR.clicked.connect(self._handleKeyEyesLR)
        self.keyEyesUD.clicked.connect(self._handleKeyEyesUD)
        self.keyPan.clicked.connect(self._handleKeyCameraPan)
        self.keyDolly.clicked.connect(self._handleKeyCameraDolly)


#===================================================================================================

#___________________________________________________________________________________________________ _handleReturnHome
    def _handleReturnHome(self):
        self.mainWindow.setActiveWidget('home')

#___________________________________________________________________________________________________
    #------Get slider value and update blend shape
    def _handleOohSlider(self):
        value = float(self.oohSlider.value())/100.0
        cmds.setAttr("blendShape1.oohHead", value)

#___________________________________________________________________________________________________
    #------Get slider value and update blend shape
    def _handleSmileSlider(self):
        value = float(self.smileSlider.value())/100.0
        cmds.setAttr("blendShape3.smile", value)
#___________________________________________________________________________________________________
    #------Get slider value and update blend shape
    def _handleScreamSlider(self):
        value = float(self.screamSlider.value())/100.0
        cmds.setAttr("blendShape2.screamHead", value)
#___________________________________________________________________________________________________
    #------Get slider value and update blend shape
    def _handleCameraSlider(self):
        value = self.cameraSlider.value()
        cmds.setAttr("camera1.translateX", value)
#___________________________________________________________________________________________________
    #------Get slider value and update blend shape
    def _handleDollySlider(self):
        value = self.dollySlider.value()
        cmds.dolly( 'camera1', abs=True, d=value )

#___________________________________________________________________________________________________
    #-------Get slider value and move the eye targets
    def _handleEyeSlider(self):
        value = self.eyesSlider.value()
        cmds.setAttr("eyeTargets.translateX", value)
#___________________________________________________________________________________________________ _handleReturnHome
    #------Get slider value and update the 'blink' values
    def _handleBlinkSlider(self):
        value = self.blinkSlider.value()
        cmds.setAttr("eyeTargets.blinkLeft", value)
        cmds.setAttr("eyeTargets.blinkMiddle", value)
        cmds.setAttr("eyeTargets.blinkRight", value)
#___________________________________________________________________________________________________ _handleReturnHome
    #-------Get slider value and move the eye targets
    def _handleEyeUDSlider(self):
        value = self.eyesUDSlider.value()
        EYE_START_POS = 137
        cmds.setAttr("eyeTargets.translateY", EYE_START_POS+value)

#___________________________________________________________________________________________________ _handleReturnHome
    #-------Reset the face
    def _handleReset(self):
        EYE_START_POS = 137
        cmds.setAttr("eyeTargets.translateY", EYE_START_POS)
        cmds.setAttr("eyeTargets.blinkLeft", 0)
        cmds.setAttr("eyeTargets.blinkMiddle", 0)
        cmds.setAttr("eyeTargets.blinkRight", 0)
        cmds.setAttr("eyeTargets.translateX", 0)
        cmds.setAttr("blendShape2.screamHead", 0)
        cmds.setAttr("blendShape3.smile", 0)
        cmds.setAttr("blendShape1.oohHead", 0)

        #----reset slider positions
        self.blinkSlider.setValue(0)
        self.screamSlider.setValue(0)
        self.oohSlider.setValue(0)
        self.smileSlider.setValue(0)
        self.eyesSlider.setValue(0)
        self.cameraSlider.setValue(230)
        self.dollySlider.setValue(250)
        self.eyesUDSlider.setValue(0)

#------------Key handlers-------------------
#___________________________________________________________________________________________________
    #-------Key Ooh face
    def _handleKeyOoh(self):
        cmds.setKeyframe('blendShape1', attribute='oohHead')
#___________________________________________________________________________________________________
    #-------Key scream face
    def _handleKeyScream(self):
        cmds.setKeyframe('blendShape2', attribute='screamHead')
#___________________________________________________________________________________________________
    #-------Key smile face
    def _handleKeySmile(self):
        cmds.setKeyframe('blendShape3', attribute='smile')
#___________________________________________________________________________________________________
    #-------Key blink face
    def _handleKeyBlink(self):
        cmds.setKeyframe('eyeTargets', attribute='blinkLeft')
        cmds.setKeyframe('eyeTargets', attribute='blinkRight')
        cmds.setKeyframe('eyeTargets', attribute='blinkMiddle')
#___________________________________________________________________________________________________
    #-------Key eye LR movement
    def _handleKeyEyesLR(self):
        cmds.setKeyframe('eyeTargets', attribute='translateX')
#___________________________________________________________________________________________________
    #-------Key eye UD movement
    def _handleKeyEyesUD(self):
        cmds.setKeyframe('eyeTargets', attribute='translateY')
#___________________________________________________________________________________________________
    #-------Key camera pan
    def _handleKeyCameraPan(self):
        cmds.setKeyframe("camera1", attribute='translateX')
#___________________________________________________________________________________________________
    #-------Key camera pan
    def _handleKeyCameraDolly(self):
        cmds.setKeyframe("camera1", attribute='translateX')
        cmds.setKeyframe("camera1", attribute='translateY')
        cmds.setKeyframe("camera1", attribute='translateZ')
#___________________________________________________________________________________________________
    #-------Key all the things!
    def _handleKeyAll(self):
        self._handleKeyCameraDolly()
        self._handleKeyCameraPan()
        self._handleKeyEyesUD()
        self._handleKeyEyesLR()
        self._handleKeyBlink()
        self._handleKeySmile()
        self._handleKeyScream()
        self._handleKeyOoh()

