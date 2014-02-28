# Assignment1Widget.py
# (C)2013
# Scott Ernst

import nimble
from nimble import cmds
from pyglass.widgets.PyGlassWidget import PyGlassWidget
import random

#___________________________________________________________________________________________________ Assignment1Widget
class ColorChangeWidget(PyGlassWidget):
    """A class for Assignment 1"""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        """Creates a new instance of Assignment1Widget."""
        super(ColorChangeWidget, self).__init__(parent, **kwargs)
        #self.homeBtn.clicked.connect(self._handleReturnHome)
        self.changeColorButton.clicked.connect(self._handleChangeColor)
        #self.redSlider.sliderMoved.connect(self._handleRedSlider)
        #self.greenSlider.sliderMoved.connect(self._handleGreenSlider)
        self.blueSlider.valueChanged.connect(self._handleBlueSlider)


#===================================================================================================

#___________________________________________________________________________________________________ _handleReturnHome
    #def _handleReturnHome(self):
    #    self.mainWindow.setActiveWidget('home')

#___________________________________________________________________________________________________ _handleReturnHome
    #------Get slider value and update the 'blink' values
    def _handleChangeColor(self):
        red = self.redSlider.value()
        green = self.greenSlider.value()
        blue = self.blueSlider.value()

        #---Normalize----
        normRed = (float(red))*(1.0/(255.0-0))
        normGreen = (float(green))*(1.0/(255.0-0))
        normBlue = (float(blue))*(1.0/(255.0-0))

        cmds.setAttr("phong2.color", normRed, normGreen, normBlue, type="double3")
        cmds.setAttr("phong3.color", normRed, normGreen, normBlue, type="double3")
        cmds.setAttr("phong8.color", normRed, normGreen, normBlue, type="double3")
        cmds.setAttr("phong14.color", normRed, normGreen, normBlue, type="double3")


    def _handleBlueSlider(self):
        print "test"
        red = self.redSlider.value()
        green = self.greenSlider.value()
        blue = self.blueSlider.value()
        skinVal = self.skinCheck.value()
        print skinVal

        self.display.setRgb(red, green, blue)
    #
    #     #---Normalize----
    #     normRed = (float(red))*(1.0/(255.0-0))
    #     normGreen = (float(green))*(1.0/(255.0-0))
    #     normBlue = (float(blue))*(1.0/(255.0-0))


