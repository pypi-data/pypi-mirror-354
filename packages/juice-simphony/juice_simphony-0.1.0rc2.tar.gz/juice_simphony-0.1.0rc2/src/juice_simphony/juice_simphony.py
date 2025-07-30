import os
import json
from pathlib import Path
import shutil
from importlib import resources
from juice_simphony.CompositionEngine.Scenario.scenario import scenario
from juice_simphony.CompositionEngine.SegmentationImporter.restApiPlan import RestApiPlan

#BASE_DIR = Path(__file__).resolve().parents[2]
#config_file_path = BASE_DIR / "data" / "simphony"
#default_config_path = config_file_path / "config_scenario.json"

base_package = (__package__ or "").split(".")[0]
config_file_path = resources.files(base_package) / "data"
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




def load_app_params(config):
    scenario_output = os.path.expandvars(config["scenario_output_area_abs_path"])
    kernel_path = os.path.expandvars(config["kernel_abs_path"])

    return {
        "conf_repo": {"juice_conf": os.path.expandvars(config["juice_conf"])},
        "scenario_generator": {"scenario_output_area_abs_path": scenario_output},
        "spice_info": {
            "kernel_abs_path": kernel_path,
            "spice_kernels_abs_path": kernel_path,
            "spice_tmp_abs_path": f"{scenario_output}/spice_kernels"
        }
    }

def resolve_segment_id(config):
    if "segment_id" in config:
        return config["segment_id"]

    if "trajectory" in config and "mnemonic" in config:
        apiPlan = RestApiPlan("https://juicesoc.esac.esa.int/rest_api/")
        events_plan = apiPlan.get_trajectory(config["trajectory"], config["mnemonic"])
        if events_plan and isinstance(events_plan, list) and "id" in events_plan[0]:
            return events_plan[0]["id"]
        raise ValueError("No valid segment ID found in API response.")

    raise KeyError("Either 'segment_id' or both 'trajectory' and 'mnemonic' must be specified.")

def main(config, mapps=False):
    segment_id = resolve_segment_id(config)
    print(f"Segment ID: {segment_id}")

    appParams = load_app_params(config)
    appParams.update({
        "scenario_id": config["scenario_id"],
        "main_target": config["main_target"],
        "segmentID": segment_id,
        "shortDesc": config["shortDesc"],
        "startTime": config["startTime"],
        "endTime": config["endTime"],
        "iniAbsolutePath": config["iniAbsolutePath"]
    })

    print("MAPPS mode enabled" if mapps else "MAPPS mode not enabled")

    scen = scenario(
        appParams["scenario_generator"]["scenario_output_area_abs_path"],
        appParams,
        True,
        mapps=mapps
    )
    scenario_path = scen.buildScenario()
    print(f"Scenario built at: {scenario_path}")

    spice_tmp_folder = appParams["spice_info"]["spice_tmp_abs_path"]
    if os.path.exists(spice_tmp_folder):
        shutil.rmtree(spice_tmp_folder)

