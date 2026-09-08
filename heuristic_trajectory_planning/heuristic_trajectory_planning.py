import sys
from pathlib import Path

BUILD_SCHEMA_DIR = Path(__file__).parent.parent / "build" / "schema"
SCRIPT_DIR = Path(__file__).parent
sys.path.append(str(BUILD_SCHEMA_DIR))

from google.protobuf import json_format
import config_pb2


def load_config(path):
    config = config_pb2.OptimizationConfig()
    with open(path, "r") as f:
        json_format.Parse(f.read(), config)
    print(f"Successfully loaded config: {config}")
    return config


if __name__ == "__main__":
    print("Hello from heuristic_trajectory_planning.py!")
    load_config(SCRIPT_DIR / "config" / "ex_config.json")
