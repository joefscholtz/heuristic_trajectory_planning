# heuristic_trajectory_planning/heuristic_trajectory_planning.py
import sys
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Any, Type

BUILD_SCHEMA_DIR = Path(__file__).parent.parent / "build" / "schema"
SCRIPT_DIR = Path(__file__).parent
sys.path.append(str(BUILD_SCHEMA_DIR))
sys.path.append(str(SCRIPT_DIR))

from google.protobuf import json_format
import config_pb2
from map_handler import MapHandler


# ==========================================
# Abstract Base Classes
# ==========================================
class InitializationStrategy(ABC):
    @abstractmethod
    def __call__(self) -> list:
        pass


class TerminationStrategy(ABC):
    @abstractmethod
    def __call__(self, generation: int, population: list) -> bool:
        pass


class RecombinationStrategy(ABC):
    @abstractmethod
    def __call__(self, population: list) -> list:
        pass


class MutationStrategy(ABC):
    @abstractmethod
    def __init__(self, payload: Any):
        pass

    @abstractmethod
    def __call__(self, population: list) -> list:
        pass


class SelectionStrategy(ABC):
    @abstractmethod
    def __call__(self, population: list, recombination: list, mutation: list) -> list:
        pass


# ==========================================
# Registries and Decorators
# ==========================================
MUTATION_REGISTRY: dict[str, Type[MutationStrategy]] = {}


def register_mutation(type_url: str):
    def decorator(cls: Type[MutationStrategy]):
        if not issubclass(cls, MutationStrategy):
            raise TypeError(f"{cls.__name__} must inherit from MutationStrategy")
        MUTATION_REGISTRY[type_url] = cls
        return cls

    return decorator


def build_mutation_strategy(config) -> MutationStrategy:
    payload = config.mutation_params
    type_url = payload.type_url

    if type_url not in MUTATION_REGISTRY:
        raise KeyError(f"No mutation strategy registered for '{type_url}'.")

    return MUTATION_REGISTRY[type_url](payload)


# ==========================================
# Default Implementations
# ==========================================
class DummyInitialization(InitializationStrategy):
    def __call__(self) -> list:
        print("[Init] Generating initial dummy population")
        return [1.0, 2.0, 3.0]


class TerminateAtMaxIter(TerminationStrategy):
    def __init__(self, max_iter: int):
        self.max_iter = max_iter

    def __call__(self, generation: int, population: list) -> bool:
        return generation >= self.max_iter


class DummyRecombination(RecombinationStrategy):
    def __call__(self, population: list) -> list:
        print("[Recombine] Recombining population")
        return population


class DummySelection(SelectionStrategy):
    def __call__(self, population: list, recombination: list, mutation: list) -> list:
        print("[Select] Selecting next generation")
        return mutation  # Simplistic dummy logic


# ==========================================
class GeneticAlgorithm:
    def __init__(
        self,
        initialization_fn: InitializationStrategy,
        termination_fn: TerminationStrategy,
        recombination_fn: RecombinationStrategy,
        mutation_fn: MutationStrategy,
        selection_fn: SelectionStrategy,
        analysis_fn=None,
    ):
        self.initialization_fn = initialization_fn
        self.termination_fn = termination_fn
        self.recombination_fn = recombination_fn
        self.mutation_fn = mutation_fn
        self.selection_fn = selection_fn
        self.analysis_fn = analysis_fn

    def run(self):
        generation = 0
        population = self.initialization_fn()

        while not self.termination_fn(generation, population):
            print(f"\n--- Generation {generation} ---")
            if self.analysis_fn is not None:
                self.analysis_fn(population)
            recombination = self.recombination_fn(population)
            mutation = self.mutation_fn(population)
            population = self.selection_fn(population, recombination, mutation)
            generation += 1

        return population


def load_config(path):
    config = config_pb2.OptimizationConfig()
    with open(path, "r") as f:
        json_format.Parse(f.read(), config)
    return config
