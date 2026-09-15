import sys
from pathlib import Path

script_dir = Path(__file__).resolve().parent
example_config_dir = script_dir.parent
project_root = example_config_dir.parent.parent

core_build_schema = project_root / "build" / "schema"
sys.path.append(str(core_build_schema))

plugin_schema_build = project_root / "build" / "examples" / "example_config" / "schema"
sys.path.append(str(plugin_schema_build))

import heuristic_trajectory_planning as htp
import config_pb2
import super_mutation_pb2
from google.protobuf import json_format


@htp.register_mutation("type.googleapis.com/htp.plugins.SuperMutationParams")
class SuperMutation(htp.MutationStrategy):
    def __init__(self, payload, global_config):
        params = super_mutation_pb2.SuperMutationParams()
        payload.Unpack(params)

        self.rate = params.adaptive_rate
        self.crossover = params.chromosomal_crossover

    def __call__(self, population: list) -> list:
        print(
            f"[Mutate] Running SuperMutation (Rate: {self.rate}, Crossover: {self.crossover})"
        )
        return population


def load_and_run():
    config_path = example_config_dir / "config" / "super_mutation_config.json"

    config = config_pb2.OptimizationConfig()
    with open(config_path, "r") as f:
        json_format.Parse(f.read(), config)

    print(f"[Main] Loaded OptimizationConfig with {config.iterations} iterations.")

    [init_s, term_s, recomb_s, select_s, mut_s, anal_s] = htp.build_and_get_strategies(
        config
    )

    ga = htp.GeneticAlgorithm(
        initialization_fn=init_s,
        termination_fn=term_s,
        recombination_fn=recomb_s,
        selection_fn=select_s,
        mutation_fn=mut_s,
        analysis_fn=anal_s,
    )

    final_pop = ga.run()
    print(f"\nFinal Population: {final_pop}")


if __name__ == "__main__":
    load_and_run()
