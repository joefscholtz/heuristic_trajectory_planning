# examples/example_config/python/main.py
import sys
from pathlib import Path

script_dir = Path(__file__).resolve().parent
example_config_dir = script_dir.parent
project_root = example_config_dir.parent.parent

core_build_schema = project_root / "build" / "schema"
sys.path.append(str(core_build_schema))

plugin_schema_build = project_root / "build" / "examples" / "example_config" / "schema"
sys.path.append(str(plugin_schema_build))

from heuristic_trajectory_planning import heuristic_trajectory_planning as htp
import config_pb2
import super_mutation_pb2
from google.protobuf import json_format


# ==========================================
# User Defined Plugin via Registry
# ==========================================
@htp.register_mutation("type.googleapis.com/htp.plugins.SuperMutationParams")
class SuperMutation(htp.MutationStrategy):
    def __init__(self, payload):
        params = super_mutation_pb2.SuperMutationParams()
        payload.Unpack(params)

        # Store configuration locally in the instance
        self.rate = params.adaptive_rate
        self.crossover = params.chromosomal_crossover

    def __call__(self, population: list) -> list:
        print(
            f"[Mutate] Running SuperMutation (Rate: {self.rate}, Crossover: {self.crossover})"
        )
        # In a real scenario, modify the population here
        return population


# ==========================================
def load_and_run():
    config_path = example_config_dir / "config" / "super_mutation_config.json"

    # Load configuration
    config = config_pb2.OptimizationConfig()
    with open(config_path, "r") as f:
        json_format.Parse(f.read(), config)

    print(f"[Main] Loaded OptimizationConfig with {config.iterations} iterations.")

    mutation_strategy = htp.build_mutation_strategy(config)
    init_strategy = htp.DummyInitialization()
    term_strategy = htp.TerminateAtMaxIter(
        config.iterations
    )  # Usually 1000, keep small for tests if desired
    recomb_strategy = htp.DummyRecombination()
    select_strategy = htp.DummySelection()

    ga = htp.GeneticAlgorithm(
        initialization_fn=init_strategy,
        termination_fn=term_strategy,
        recombination_fn=recomb_strategy,
        mutation_fn=mutation_strategy,
        selection_fn=select_strategy,
    )

    ga.termination_fn = htp.TerminateAtMaxIter(3)

    final_pop = ga.run()
    print(f"\nFinal Population: {final_pop}")


if __name__ == "__main__":
    load_and_run()
