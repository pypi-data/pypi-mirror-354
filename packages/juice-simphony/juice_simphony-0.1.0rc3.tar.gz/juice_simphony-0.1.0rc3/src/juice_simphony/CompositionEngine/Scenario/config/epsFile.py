from jinja2 import Template
import os

from juice_simphony.CompositionEngine.Scenario.common.fileTemplate import fileTemplate
from juice_simphony.CompositionEngine.Scenario.common.fileName import fileName

class epsFile(fileTemplate, fileName):

    def __init__(self, path, params=0):
        self.path = path
        self.params = params
        self.params["prefix"]  = "CFG"
        self.params["type"]    = "EPS"
        self.params["desc"]    = ""
        self.params["version"] = ""
        self.params["ext"]     = "cfg"
        self.fileName = ""
        self.template = 0
        fileName.__init__(self, params)