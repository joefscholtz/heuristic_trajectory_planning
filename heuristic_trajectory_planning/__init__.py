import sys
from pathlib import Path

BUILD_SCHEMA_DIR = Path(__file__).parent.parent / "build" / "schema"
SCRIPT_DIR = Path(__file__).parent
sys.path.append(str(BUILD_SCHEMA_DIR))
sys.path.append(str(SCRIPT_DIR))

from .core import (
    GeneticAlgorithm,
    build_and_get_strategies,
    register_initialization,
    register_termination,
    register_recombination,
    register_mutation,
    register_selection,
    # Abstract Base Classes
    InitializationStrategy,
    TerminationStrategy,
    RecombinationStrategy,
    MutationStrategy,
    SelectionStrategy,
)

from . import initialization
from . import termination
from . import recombination
from . import mutation
from . import selection
