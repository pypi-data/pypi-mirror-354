
class fileName():

    def __init__(self, params=0):
        if params!= 0: self.params.update(params)
        if "addScenarioID" not in self.params: self.params["addScenarioID"] = True

    # Base File Name Generator
    # ------------------------
    def genBaseFileName(self):
        # General scenario file name structure
        # {prefix}_{type}_{scenarioID}_{desc}_{version}
        type = ""
        desc = ""
        version = ""
        sceID = ""
        if self.params["type"] != "":    type    = "_" + self.params["type"].upper()
        if self.params["desc"] != "":    desc    = "_" + self.params["desc"]
        if self.params["version"] != "":  version = "_" + str(self.params["version"])
        if self.params["addScenarioID"]: sceID   = "_" + self.params["scenarioID"]
        return "{}{}{}{}{}".format(self.params["prefix"],
                                    type,
                                    desc,                                    
                                    sceID,
                                    version)

    # Base File Name Without version Generator
    # ----------------------------------------
    def genBaseFileNameNoV(self):
        # General scenario file name structure
        # {prefix}_{type}_{scenarioID}_{desc}_{version}
        type = ""
        desc = ""
        if self.params["type"] != "":    type    = "_" + self.params["type"].upper()
        if self.params["desc"] != "":    desc    = "_" + self.params["desc"]
        return "{}{}{}".format(self.params["prefix"],
                                    type,
                                    desc)


    # Reference File Name Generator
    # -----------------------------
    def genRefFileName(self):
        # General scenario file name structure
        # {prefix}_{type}_{desc}_{refScenarioID}_{version}
        type = ""
        desc = ""
        version = ""
        sceID = ""
        if self.params["type"] != "": type = "_" + self.params["type"].upper()
        if self.params["desc"] != "": desc = "_" + self.params["desc"]
        if self.params["version"] != "": version = "_" + self.params["version"]
        if self.params["addScenarioID"]: sceID  = "_" + self.params["refScenarioID"]
        return "{}{}{}{}{}".format(self.params["prefix"],
                                   type,
                                   desc,                                   
                                   sceID,
                                   version)