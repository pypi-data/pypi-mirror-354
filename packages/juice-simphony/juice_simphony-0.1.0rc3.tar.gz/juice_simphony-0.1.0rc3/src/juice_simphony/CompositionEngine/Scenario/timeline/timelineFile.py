from jinja2 import Template
import os
from common.fileHandleEps1 import fileHandleEps1
from common.fileName import fileName
from commons.name2acronym import name2acronym


class timelineFile(fileHandleEps1):
     
    def __init__(self, path, exp_name, parameters = 0):
        self.parameters = {}
        if parameters!=0: 
            self.parameters.update(parameters)
        self.path = path
        self.rootPath = path
        self.parameters["prefix"]  = "ITL"
        self.parameters["type"]    = name2acronym(exp_name)
        self.parameters["desc"]    = ""
        self.parameters["version"] = "SXXPYY"
        self.parameters["ext"]     = "itl"
        self.fileName = ""
        self.template = 0
        self.includes = includes
        self.writeVersion    = False
        self.writeTimeWindow = False
        fileName.__init__(self, self.parameters)   


    def writeTimelineHeader(self, writeVersion, writeTimeWindow):
        self.writeHeader(self.parameters["scenarioID"], "JUICE " + exp_name + " SCENARIO TIMELINE")
        self.insertEmptyLine()

        if writeVersion == True:
            self.insertVersion()
            self.insertEmptyLine()

        if writeTimeWindow == True:
            self.insertTimeWindow(self.parameters["timeline"]["startTime"], self.parameters["timeline"]["endTime"])

    def writeContent(self):
        self.writeTimelineHeader(self.writeVersion, self.writeTimeWindow)
