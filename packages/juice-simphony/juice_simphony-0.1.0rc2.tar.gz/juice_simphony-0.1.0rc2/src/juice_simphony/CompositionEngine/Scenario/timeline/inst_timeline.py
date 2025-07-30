from jinja2 import Template
import os

from juice_simphony.CompositionEngine.Scenario.common.fileHandleEps1 import fileHandleEps1
from juice_simphony.CompositionEngine.Scenario.common.fileName import fileName




class timelineFile(fileHandleEps1):
     
    def __init__(self, path, exp_name, params = 0):
        self.params = {}
        if params!=0: 
            self.params.update(params)
        self.path = path
        self.rootPath = path
        self.exp_name = exp_name
        self.params["prefix"]  = "ITL"
        self.params["type"]    = self.exp_name
        self.params["desc"]    = ""
        self.params["version"] = "SXXPYY"
        self.params["ext"]     = "json"
        self.fileName = ""
        self.template = 0
        self.writeVersion    = False
        self.writeTimeWindow = False
        fileName.__init__(self, self.params)


    def writeTimelineHeader(self, writeVersion, writeTimeWindow):
        self.writeHeader(self.params["scenarioID"], "JUICE " + self.exp_name + " SCENARIO TIMELINE")
        self.insertEmptyLine()

        if writeVersion == True:
            self.insertVersion()
            self.insertEmptyLine()

        if writeTimeWindow == True:
            self.insertTimeWindow(self.params["timeline"]["startTime"], self.params["timeline"]["endTime"])

    def writeContent(self):
        self.writeTimelineHeader(self.writeVersion, self.writeTimeWindow)


if __name__ == "__main__":
    params = {}
    params["scenarioID"] = "SJS0003C30A"
    tml = timelineFile(path="Z:\VALIDATION\simphony\pcm\phs_pcm_test_001\scenario_generator\output",exp_name="MAJIS",params=params)
    tml.genFile()