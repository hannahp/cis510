# Assignment1Widget.py
# (C)2013
# Scott Ernst

import nimble
from nimble import cmds
from pyglass.widgets.PyGlassWidget import PyGlassWidget
import random

#___________________________________________________________________________________________________ Assignment1Widget
class Assignment3Widget(PyGlassWidget):
    """A class for Assignment 1"""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        """Creates a new instance of Assignment1Widget."""
        super(Assignment3Widget, self).__init__(parent, **kwargs)
        self.homeBtn.clicked.connect(self._handleReturnHome)
        self.goButton.clicked.connect(self._handleGoButton)

#===================================================================================================

#___________________________________________________________________________________________________ _handleReturnHome
    def _handleReturnHome(self):
        self.mainWindow.setActiveWidget('home')

#___________________________________________________________________________________________________ _handleReturnHome
    def _handleGoButton(self):
        start = self.rangeStartSlide.value()    #get user-def range start
        end = self.rangeEndSlide.value()        #get user-def range end
        selObj = cmds.ls(sl=True)[0]            #Get selected object
        numVerts = cmds.polyEvaluate(selObj, v=True)

        #-----For each vertex...------
        for i in range(numVerts):
            pos = cmds.pointPosition(selObj+'.vtx['+str(i)+']')
            randX = random.randrange(start,end)
            randY = random.randrange(start,end)
            randZ = random.randrange(start,end)
            cmds.move(randX, randY, randZ, selObj+'.vtx['+str(i)+']', r=True)
            print cmds.pointPosition(selObj+'.vtx['+str(i)+']')