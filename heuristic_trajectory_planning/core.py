import sys
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Any, Type, Optional

BUILD_SCHEMA_DIR = Path(__file__).parent.parent / "build" / "schema"
SCRIPT_DIR = Path(__file__).parent
sys.path.append(str(BUILD_SCHEMA_DIR))
sys.path.append(str(SCRIPT_DIR))

from google.protobuf import json_format
import config_pb2
from map_handler import MapHandler


# ==========================================
# Individual Base Class
# ==========================================
class BaseIndividual(ABC):
    def __init__(self):
        self.fitness: Optional[float] = None

    @abstractmethod
    def get_path_coordinates(self) -> tuple[list[float], list[float]]:
        """
        Must return a tuple of (x_coordinates, y_coordinates) for plotting and analysis.
        """
        pass


# ==========================================
# Abstract Base Classes
# ==========================================
class InitializationStrategy(ABC):
    @abstractmethod
    def __init__(self, payload: Any, global_config: Any):
        pass

    @abstractmethod
    def __call__(self) -> list[BaseIndividual]:
        pass


class TerminationStrategy(ABC):
    @abstractmethod
    def __init__(self, payload: Any, global_config: Any):
        pass

    @abstractmethod
    def __call__(self, generation_n: int, population: list[BaseIndividual]) -> bool:
        pass


class RecombinationStrategy(ABC):
    @abstractmethod
    def __init__(self, payload: Any, global_config: Any):
        pass

    @abstractmethod
    def __call__(self, population: list[BaseIndividual]) -> list[BaseIndividual]:
        pass


class MutationStrategy(ABC):
    @abstractmethod
    def __init__(self, payload: Any, global_config: Any):
        pass

    @abstractmethod
    def __call__(self, population: list[BaseIndividual]) -> list[BaseIndividual]:
        pass


class SelectionStrategy(ABC):
    @abstractmethod
    def __init__(self, payload: Any, global_config: Any):
        pass

    @abstractmethod
    def __call__(
        self,
        population: list[BaseIndividual],
        recombination: list[BaseIndividual],
        mutation: list[BaseIndividual],
    ) -> list[BaseIndividual]:
        pass


class AnalysisClass(ABC):
    @abstractmethod
    def __init__(self, payload: Any, global_config: Any):
        pass

    @abstractmethod
    def __call__(self, generation_n: int, population: list[BaseIndividual]):
        pass


# ==========================================
# Registries and Decorators
# ==========================================
INIT_REGISTRY: dict[str, Type[InitializationStrategy]] = {}
TERM_REGISTRY: dict[str, Type[TerminationStrategy]] = {}
RECOMB_REGISTRY: dict[str, Type[RecombinationStrategy]] = {}
MUTATION_REGISTRY: dict[str, Type[MutationStrategy]] = {}
SELECT_REGISTRY: dict[str, Type[SelectionStrategy]] = {}
ANALYSIS_REGISTRY: dict[str, Type[AnalysisClass]] = {}


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


def register_analysis(type_url: str):
    def decorator(cls):
        ANALYSIS_REGISTRY[type_url] = cls
        return cls

    return decorator


# ==========================================
# Default (Fallback) Implementations
# ==========================================
#


class DummyIndividual(BaseIndividual):
    def __init__(self, xy_coords: list[tuple[float, float]]):
        super().__init__()
        self.xy = xy_coords

    def get_path_coordinates(self) -> tuple[list[float], list[float]]:
        return map(list, zip(*self.xy))


class DummyInitialization(InitializationStrategy):
    def __init__(self, payload=None, global_config=None):
        self.start_config = global_config.start_config
        self.end_config = global_config.end_config
        pass

    def __call__(self) -> list[BaseIndividual]:
        print("[Init] Generating initial dummy population")
        # Return dummy trajectories in the center of the map
        return [
            DummyIndividual(
                [
                    (self.start_config[0], self.start_config[1]),
                    (0.0, 0.0),
                    (1.0, 0.0),
                    (2.0, 0.0),
                    (self.end_config[0], self.end_config[1]),
                ]
            ),
            DummyIndividual(
                [
                    (self.start_config[0], self.start_config[1]),
                    (0.0, 0.5),
                    (1.5, 1.5),
                    (0.5, 0.5),
                    (self.end_config[0], self.end_config[1]),
                ]
            ),
        ]


class TerminateAtMaxIter(TerminationStrategy):
    def __init__(self, payload=None, global_config=None):
        self.max_iter = global_config.iterations if global_config else 1000

    def __call__(self, generation_n: int, population: list[BaseIndividual]) -> bool:
        return generation_n >= self.max_iter


class DummyRecombination(RecombinationStrategy):
    def __init__(self, payload=None, global_config=None):
        pass

    def __call__(self, population: list[BaseIndividual]) -> list[BaseIndividual]:
        print("[Recombine] Recombining population")
        return population


class DummyMutation(MutationStrategy):
    def __init__(self, payload=None, global_config=None):
        pass

    def __call__(self, population: list[BaseIndividual]) -> list[BaseIndividual]:
        print("[Mutate] Dummy mutation")
        return population


class DummySelection(SelectionStrategy):
    def __init__(self, payload=None, global_config=None):
        pass

    def __call__(
        self,
        population: list[BaseIndividual],
        recombination: list[BaseIndividual],
        mutation: list[BaseIndividual],
    ) -> list[BaseIndividual]:
        print("[Select] Selecting next generation_n")
        return mutation


class PrintGen(AnalysisClass):
    def __init__(self, payload=None, global_config=None):
        pass

    def __call__(self, generation_n: int, population: list[BaseIndividual]):
        print(f"\n--- Generation {generation_n} ---")


# ==========================================
def build_and_get_strategies(config):
    def _instantiate(field_name: str, registry: dict, default_class: type):
        if config.HasField(field_name):
            payload = getattr(config, field_name)
            if payload.type_url not in registry:
                raise KeyError(
                    f"No strategy registered for '{payload.type_url}' in {field_name}"
                )
            return registry[payload.type_url](payload, global_config=config)

        # Fallback to default class, passing the full config for context
        return default_class(payload=None, global_config=config)

    init_s = _instantiate("initialization_params", INIT_REGISTRY, DummyInitialization)
    term_s = _instantiate("termination_params", TERM_REGISTRY, TerminateAtMaxIter)
    recomb_s = _instantiate("recombination_params", RECOMB_REGISTRY, DummyRecombination)
    select_s = _instantiate("selection_params", SELECT_REGISTRY, DummySelection)
    mut_s = _instantiate("mutation_params", MUTATION_REGISTRY, DummyMutation)
    anal_s = _instantiate("analysis_params", ANALYSIS_REGISTRY, PrintGen)

    return [init_s, term_s, recomb_s, select_s, mut_s, anal_s]


# ==========================================
class GeneticAlgorithm:
    def __init__(
        self,
        initialization_fn: InitializationStrategy,
        termination_fn: TerminationStrategy,
        recombination_fn: RecombinationStrategy,
        mutation_fn: MutationStrategy,
        selection_fn: SelectionStrategy,
        analysis_fn: Optional[AnalysisClass] = None,
    ):
        self.initialization_fn = initialization_fn
        self.termination_fn = termination_fn
        self.recombination_fn = recombination_fn
        self.mutation_fn = mutation_fn
        self.selection_fn = selection_fn
        self.analysis_fn = analysis_fn

    def run(self):
        generation_n = 0
        population = self.initialization_fn()

        while not self.termination_fn(generation_n, population):
            if self.analysis_fn is not None:
                self.analysis_fn(generation_n, population)
            recombination = self.recombination_fn(population)
            mutation = self.mutation_fn(population)
            population = self.selection_fn(population, recombination, mutation)
            generation_n += 1

        return population
