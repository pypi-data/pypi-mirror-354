from jinja2 import Template
import os

from juice_simphony.CompositionEngine.SegmentationImporter.mapps_io import common
from juice_simphony.CompositionEngine.SegmentationImporter.mapps_io.common.fileHandleEps import fileHandleEps

class instToplevel(fileHandleEps):

    def __init__(self, rootPath, path, parameters=0):
        self.path = path
        self.rootPath = rootPath
        self.params = {}
        if parameters!=0:
            self.params.update(parameters)
        self.params["prefix"]  = "ITL"
        self.params["type"]    = "TOP_LEVEL"
        self.params["desc"]    = "INSTRUMENTS"
        self.params["version"] = "1"
        self.params["ext"]     = "itl"
        self.fileName = ""
        self.template = 0
        fileHandleEps.__init__(self)
    
    def writeContent(self):
        self.writeHeader(self.params["scenarioID"], "TOP LEVEL INSTRUMENTS TIMELINE")
        self.insertEmptyLine()
        self.insertComment("Instruments include files")
        self.insertComment("-------------------------")
        self.insertEmptyLine()

        # REMOVED
        #for includeFileTmp in self.params["includeFiles"]:
        #    includeFile = {}
        #    includeFile["filePath"] = includeFileTmp
        #    self.insertIncludeFile(includeFile)