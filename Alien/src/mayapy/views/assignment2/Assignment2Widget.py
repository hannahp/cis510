# Assignment1Widget.py
# (C)2013
# Scott Ernst

import nimble
from nimble import cmds
from pyglass.widgets.PyGlassWidget import PyGlassWidget
import MoleculeSpawn

#___________________________________________________________________________________________________ Assignment1Widget
class Assignment2Widget(PyGlassWidget):
    """A class for Assignment 1"""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        """Creates a new instance of Assignment1Widget."""
        super(Assignment2Widget, self).__init__(parent, **kwargs)
        self.spawnButton.clicked.connect(self._handleSpawnButton)
        self.deleteAllButton.clicked.connect(self._handleDeleteAllButton)
        self.homeBtn.clicked.connect(self._handleReturnHome)

#===================================================================================================
#                                                                                 H A N D L E R S
    #def _handleSlide(self):
    #    print numMolecSlider.getValue()
#___________________________________________________________________________________________________ _handleReturnHome
    def _handleSpawnButton(self):
        """
        This callback creates a polygonal cylinder in the Maya scene.

        """
        #Grab the names of all molecules in a scene
        allObj=cmds.ls('molecule*', assemblies=True)
        #If there aren't any molecules yet, make them
        if not allObj:
            numMolec=self.numMolecSpin.value()
            MoleculeSpawn.spawnMolecules(numMolec)
            response = nimble.createRemoteResponse(globals())
        # Otherwise, tell user to delete all before making more
        else:
            self.spawnButton.setText ("Please delete before making more molecules")
#___________________________________________________________________________________________________ _handleDeleteAll
    def _handleDeleteAllButton(self):
        """
        This callback creates a polygonal cylinder in the Maya scene.

        """
        allObj=cmds.ls('molecule*', assemblies=True)
        for i in allObj:
            cmds.delete(i)
        cmds.delete ("redBlinnSG")
        cmds.delete ("whiteBlinnSG")
        cmds.delete ("redBlinn")
        cmds.delete ("whiteBlinn")
        self.spawnButton.setText ("Spawn Molecules")

#___________________________________________________________________________________________________ _handleReturnHome
    def _handleReturnHome(self):
        self.mainWindow.setActiveWidget('home')
