import os
import json
from pathlib import Path
import shutil
from juice_simphony.CompositionEngine.Scenario.scenario import scenario
from juice_simphony.CompositionEngine.SegmentationImporter.restApiPlan import RestApiPlan

BASE_DIR = Path(__file__).resolve().parents[2]
config_file_path = BASE_DIR / "data" / "simphony"
default_config_path = config_file_path / "config_scenario.json"

def expand_paths(config):
    """Recursively expand user (~) and environment variables ($VAR) in string paths"""
    if isinstance(config, dict):
        return {k: expand_paths(v) for k, v in config.items()}
    elif isinstance(config, list):
        return [expand_paths(item) for item in config]
    elif isinstance(config, str):
        return os.path.expandvars(os.path.expanduser(config))
    else:
        return config

def load_parameters(file_name):
    with open(file_name) as json_file:
        raw_config = json.load(json_file)
    return expand_paths(raw_config)

def load_app_params():
    config_file = os.path.join(config_file_path, "cfg_simphony.json")
    config = load_parameters(config_file)

    appParams = {}
    appParams["conf_repo"] = config["inputs"]
    sg = config["scenario_generator"]
    appParams["scenario_generator"] = sg

    spice = config["spice"]
    spice["spice_kernels_abs_path"] = spice["kernel_abs_path"]
    spice["spice_tmp_abs_path"] = os.path.join(sg["scenario_output_area_abs_path"], "spice_kernels")
    appParams["spice_info"] = spice

    return appParams


def main(config, mapps=False):
    if "segment_id" not in config:
        if "trajectory" in config and "mnemonic" in config:
            apiPlan = RestApiPlan("https://juicesoc.esac.esa.int/rest_api/")
            events_plan = apiPlan.get_trajectory(config["trajectory"], config["mnemonic"])
            if events_plan and isinstance(events_plan, list) and "id" in events_plan[0]:
                segment_id = events_plan[0]["id"]
                print(f"Segment ID: {segment_id}")
            else:
                raise ValueError("No valid segment ID found in API response.")
        else:
            raise KeyError("Both 'trajectory' and 'mnemonic' must be specified in the config")
    else:
        segment_id = config["segment_id"]
        print(f"Segment ID: {segment_id}")

    appParams = load_app_params()

    appParams.update({
        "scenario_id": config["scenario_id"],
        "main_target": config["main_target"],
        "segmentID": segment_id,
        "shortDesc": config["shortDesc"],
        "startTime": config["startTime"],
        "endTime": config["endTime"],
        "iniAbsolutePath": config["iniAbsolutePath"]
    })

    #print(json.dumps(appParams, indent=4))

    if mapps:
        print("MAPPS mode enabled, doing MAPPS-specific operations")
    else:
        print("MAPPS mode not enabled")

    scen = scenario(appParams["scenario_generator"]["scenario_output_area_abs_path"], appParams, True, mapps=mapps)
    scenario_path = scen.buildScenario()

    print(f"Scenario built at: {scenario_path}")

    spice_tmp_folder = appParams["spice_info"]["spice_tmp_abs_path"]
    if os.path.exists(spice_tmp_folder):
        shutil.rmtree(spice_tmp_folder)
