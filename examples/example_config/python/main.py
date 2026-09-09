import sys
from pathlib import Path

# Locate paths relative to this script
script_dir = Path(__file__).resolve().parent
example_config_dir = script_dir.parent
project_root = example_config_dir.parent.parent

# 1. Add core build schema path (for config_pb2.py)
core_build_schema = project_root / "build" / "schema"
sys.path.append(str(core_build_schema))

# 2. Add plugin schema build path directly so we can import the module flatly
plugin_schema_build = project_root / "build" / "examples" / "example_config" / "schema"
sys.path.append(str(plugin_schema_build))

from google.protobuf import json_format
import config_pb2
import super_mutation_pb2  # Imported directly from build/examples/example_config/schema/


def load_and_run():
    config_path = example_config_dir / "config" / "super_mutation_config.json"

    config = config_pb2.OptimizationConfig()
    with open(config_path, "r") as f:
        json_format.Parse(f.read(), config)

    print(f"[Python] Loaded base iterations: {config.iterations}")

    # Unpack the Any field
    if config.HasField("mutation_params"):
        super_params = super_mutation_pb2.SuperMutationParams()
        if config.mutation_params.Unpack(super_params):
            print("[Python] Unpacked SuperMutationParams successfully!")
            print(f"[Python]   - Adaptive Rate: {super_params.adaptive_rate}")
            print(f"[Python]   - Cross-over: {super_params.chromosomal_crossover}")
        else:
            print("[Python] Failed to unpack Any message.")


if __name__ == "__main__":
    load_and_run()
