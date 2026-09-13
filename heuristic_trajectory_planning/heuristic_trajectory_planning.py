import sys
from pathlib import Path

BUILD_SCHEMA_DIR = Path(__file__).parent.parent / "build" / "schema"
SCRIPT_DIR = Path(__file__).parent
sys.path.append(str(BUILD_SCHEMA_DIR))

from google.protobuf import json_format
import config_pb2
from map_handler import MapHandler


def load_config(path):
    config = config_pb2.OptimizationConfig()
    with open(path, "r") as f:
        json_format.Parse(f.read(), config)
    print(f"Successfully loaded config: {config}")
    return config


class GeneticAlgorithm:
    def __init__(
        self,
        initialization_fn,
        termination_fn,
        recombination_fn,
        mutation_fn,
        selection_fn,
    ):
        self.initialization_fn = initialization_fn
        self.termination_fn = termination_fn
        self.recombination_fn = recombination_fn
        self.mutation_fn = mutation_fn
        self.selection_fn = selection_fn

    def run(self):
        generation = 0
        population = self.initialization_fn()

        while not self.termination_fn(generation, population):
            recombination = self.recombination_fn(population)
            mutation = self.mutation_fn(population)
            population = self.selection_fn(population, recombination, mutation)


if __name__ == "__main__":
    print("Hello from heuristic_trajectory_planning.py!")
    load_config(SCRIPT_DIR / "config" / "ex_config.json")
    map = MapHandler.load_map_from_yaml(SCRIPT_DIR / "config/map/turtlebot3_map.yaml")
    map.plot()
    downsampled_grid = map.discretize(factor=4)
    downsampled_grid.plot()
