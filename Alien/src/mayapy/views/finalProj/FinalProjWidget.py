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



#===================================================================================================

#___________________________________________________________________________________________________ _handleReturnHome
    def _handleReturnHome(self):
        self.mainWindow.setActiveWidget('home')

#___________________________________________________________________________________________________ _handleReturnHome
    #------Spawn all the aliens!
    def _handleSpawn(self):
        numAliens = self.numAliensSpinBox.value()
        SpawnAliens.spawnAliens(numAliens)
