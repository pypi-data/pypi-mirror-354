from juice_simphony.CompositionEngine.Scenario.common import utils
import configparser
from jinja2 import Template
from juice_simphony.CompositionEngine.Scenario.common.fileTemplate import fileTemplate
from juice_simphony.CompositionEngine.Scenario.common.fileName import fileName

class agmCfgFile(fileTemplate, fileName):

    def __init__(self, path, params=0):
        self.path = path
        self.params = {}
        self.params["prefix"]  = "CFG"
        self.params["type"]    = "AGM"
        self.params["desc"]    = ""
        self.params["version"] = ""
        self.params["ext"]     = "xml"
        self.params.update(params)
        self.fileName = ""
        self.template = 0
        fileName.__init__(self, self.params)