
class fileName():

    def __init__(self, params = 0):
        if params!=0: self.params.updates(params)
        if "addScenarioID" not in self.params: self.params["addScenarioID"] = True

    # Base File Name Generator
    # ------------------------
    def genBaseFileName(self):
        # General scenario file name structure
        # {prefix}_{scenarioID}_{type}_{desc}_{version}
        type = ""
        desc = ""
        version = ""
        sceID = ""
        if self.params["type"] != "":    type   = "_" + self.params["type"].upper()
        if self.params["desc"] != "":    desc    = "_" + self.params["desc"]
        if self.params["version"] != 0 and self.params["version"] != 'SXXPYY': version = "_V{}".format(self.params["version"])
        elif self.params["version"] == 'SXXPYY': version = f"_{self.params['version']}"
        if self.params["addScenarioID"]: sceID   = "_" + self.params["scenarioID"]
        return "{}{}{}{}{}".format(self.params["prefix"],
                                    type,
                                    desc,
                                    sceID,
                                    version)

    # Reference File Name Generator
    # -----------------------------
    def genRefFileName(self):
        # General scenario file name structure
        # {prefix}_{refScenarioID}_{type}_{desc}_{version}
        type = ""
        desc = ""
        version = ""
        sceID = ""
        if self.params["type"] != "": type = "_" + self.params["type"].upper()
        if self.params["desc"] != "": desc = "_" + self.params["desc"]
        if self.params["version"] != 0 and self.params["version"] != 'SXXPYY': version = "_V{}".format(self.params["version"])
        elif self.params["version"] == 'SXXPYY': version = f"_{self.params['version']}"
        if self.params["addScenarioID"]: sceID  = "_" + self.params["refScenarioID"]
        return "{}{}{}{}{}".format(self.params["prefix"],
                                   type,
                                   desc,
                                   sceID,
                                   version)