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
    def __init__(self, payload: Any):
        pass

    @abstractmethod
    def __call__(self) -> list:
        pass


class TerminationStrategy(ABC):
    @abstractmethod
    def __init__(self, payload: Any):
        pass

    @abstractmethod
    def __call__(self, generation: int, population: list) -> bool:
        pass


class RecombinationStrategy(ABC):
    @abstractmethod
    def __init__(self, payload: Any):
        pass

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
    def __init__(self, payload: Any):
        pass

    @abstractmethod
    def __call__(self, population: list, recombination: list, mutation: list) -> list:
        pass


# ==========================================
# Registries and Decorators
# ==========================================
INIT_REGISTRY: dict[str, Type[InitializationStrategy]] = {}
TERM_REGISTRY: dict[str, Type[TerminationStrategy]] = {}
RECOMB_REGISTRY: dict[str, Type[RecombinationStrategy]] = {}
MUTATION_REGISTRY: dict[str, Type[MutationStrategy]] = {}
SELECT_REGISTRY: dict[str, Type[SelectionStrategy]] = {}


def register_initialization(type_url: str):
    def decorator(cls):
        INIT_REGISTRY[type_url] = cls
        return cls

    return decorator


def register_termination(type_url: str):
    def decorator(cls):
        TERM_REGISTRY[type_url] = cls
        return cls

    return decorator


def register_recombination(type_url: str):
    def decorator(cls):
        RECOMB_REGISTRY[type_url] = cls
        return cls

    return decorator


def register_mutation(type_url: str):
    def decorator(cls):
        MUTATION_REGISTRY[type_url] = cls
        return cls

    return decorator


def register_selection(type_url: str):
    def decorator(cls):
        SELECT_REGISTRY[type_url] = cls
        return cls

    return decorator


# ==========================================
# Default (Fallback) Implementations
# ==========================================
class DummyInitialization(InitializationStrategy):
    def __init__(self, config=None):
        pass

    def __call__(self) -> list:
        print("[Init] Generating initial dummy population")
        return [1.0, 2.0, 3.0]


class TerminateAtMaxIter(TerminationStrategy):
    def __init__(self, config):
        self.max_iter = config.iterations if config else 1000

    def __call__(self, generation: int, population: list) -> bool:
        return generation >= self.max_iter


class DummyRecombination(RecombinationStrategy):
    def __init__(self, config=None):
        pass

    def __call__(self, population: list) -> list:
        print("[Recombine] Recombining population")
        return population


class DummyMutation(MutationStrategy):
    def __init__(self, config=None):
        pass

    def __call__(self, population: list) -> list:
        print("[Mutate] Dummy mutation")
        return population


class DummySelection(SelectionStrategy):
    def __init__(self, config=None):
        pass

    def __call__(self, population: list, recombination: list, mutation: list) -> list:
        print("[Select] Selecting next generation")
        return mutation


# ==========================================
def build_and_get_strategies(config):
    def _instantiate(field_name: str, registry: dict, default_class: type):
        if config.HasField(field_name):
            payload = getattr(config, field_name)
            if payload.type_url not in registry:
                raise KeyError(
                    f"No strategy registered for '{payload.type_url}' in {field_name}"
                )
            return registry[payload.type_url](payload)

        # Fallback to default class, passing the full config for context
        return default_class(config)

    init_s = _instantiate("initialization_params", INIT_REGISTRY, DummyInitialization)
    term_s = _instantiate("termination_params", TERM_REGISTRY, TerminateAtMaxIter)
    recomb_s = _instantiate("recombination_params", RECOMB_REGISTRY, DummyRecombination)
    select_s = _instantiate("selection_params", SELECT_REGISTRY, DummySelection)
    mut_s = _instantiate("mutation_params", MUTATION_REGISTRY, DummyMutation)

    return [init_s, term_s, recomb_s, select_s, mut_s]


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
