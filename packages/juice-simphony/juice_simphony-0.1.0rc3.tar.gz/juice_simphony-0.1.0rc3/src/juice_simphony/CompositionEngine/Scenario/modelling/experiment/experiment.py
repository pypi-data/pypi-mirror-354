import os
from juice_simphony.CompositionEngine.Scenario.common import utils
from juice_simphony.CompositionEngine.Scenario.modelling.experiment.topLevelExpEdf import toplevelExpEdf


class experiment:

    def __init__(self, root_path, instName, parameters=0):
        self.root_path = root_path
        self.instName = instName
        self.parameters = parameters
        self.mainFolderPath = ""
        self.structure = dict()

    def build(self):
        self.createMainFolder(self.instName)
        self.structure         = self.addRootContent()
        self.structure["path"] = self.mainFolderPath;
        return self.structure

    def createMainFolder(self, folderName):
        self.mainFolderPath = utils.createFolder(self.root_path, folderName)
    
    def addRootContent(self):
        structure = dict()

        # Observation definition top level
        # --------------------------------
        tlEdfParams = dict()
        tlEdfParams["scenarioID"] = self.parameters["scenarioID"]
        tlEdfParams["edfRootPath"] = self.root_path
        tlEdfExp = toplevelExpEdf(self.mainFolderPath, self.instName, tlEdfParams)
        structure["toplevelExpEdf"] = tlEdfExp.genFile()
        return structure
