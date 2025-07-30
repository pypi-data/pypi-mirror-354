from juice_simphony.CompositionEngine.Scenario.common import utils
import configparser
from jinja2 import Template
from juice_simphony.CompositionEngine.Scenario.common.fileTemplate import fileTemplate
from juice_simphony.CompositionEngine.Scenario.common.fileName import fileName

class mappsIniFile(fileTemplate, fileName):

    def __init__(self, path, params=0):
        self.path = path
        self.params = params
        self.params["prefix"]  = "CFG"
        self.params["type"]    = "MAPPS"
        self.params["desc"]    = ""
        self.params["version"] = ""
        self.params["ext"]     = "ini"
        self.fileName = ""
        self.template = 0
        fileName.__init__(self, params)