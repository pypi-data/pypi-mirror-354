import argparse
import json
from pathlib import Path
from juice_simphony.juice_simphony import main as main_runner

# Define default config path
BASE_DIR = Path(__file__).resolve().parents[2]
config_file_path = BASE_DIR / "data" / "simphony"
default_config_path = config_file_path / "config_scenario.json"

def run():
    parser = argparse.ArgumentParser(description="Standalone Simphony Scenario Generator")
    parser.add_argument('--config', type=str, default=default_config_path, help="Path to JSON config file")
    parser.add_argument('--mapps', action='store_true', help='Optional flag to enable MAPPS-specific behavior')
    args = parser.parse_args()

    # Load config
    with open(args.config, 'r') as f:
        config = json.load(f)

    main_runner(config, mapps=args.mapps)
