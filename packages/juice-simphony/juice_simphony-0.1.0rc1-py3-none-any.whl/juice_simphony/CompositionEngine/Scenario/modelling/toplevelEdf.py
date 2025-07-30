import os
from jinja2 import Template
from juice_simphony.CompositionEngine.Scenario.common.fileTemplate import fileTemplate
from juice_simphony.CompositionEngine.Scenario.common.fileName import fileName

class toplevelEdf(fileTemplate, fileName):

    def __init__(self, path, parameters=0):
        self.path = path
        self.parameters = parameters
        self.parameters["prefix"] = "EDF"
        self.parameters["type"] = "JUICE"
        self.parameters["desc"] = ""
        self.parameters["version"] = 0
        self.parameters["ext"] = "edf"
        self.fileName = ""
        self.template = 0
        fileName.__init__(self, parameters)