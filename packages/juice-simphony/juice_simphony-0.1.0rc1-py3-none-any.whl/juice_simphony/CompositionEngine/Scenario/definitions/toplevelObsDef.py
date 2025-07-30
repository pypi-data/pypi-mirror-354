from jinja2 import Template
import os
from juice_simphony.CompositionEngine.Scenario.common.fileTemplate import fileTemplate
from juice_simphony.CompositionEngine.Scenario.common.fileName import fileName

class toplevelObsDef(fileTemplate, fileName):

    def __init__(self, path, parameters=0):
        self.path = path
        self.parameters = parameters
        self.parameters["prefix"]  = "ODF"
        self.parameters["type"]    = "TOP_LEVEL"
        self.parameters["desc"]    = ""
        self.parameters["version"] = 0
        self.parameters["ext"]     = "def"
        self.fileName = ""
        self.template = 0
        fileName.__init__(self, parameters)