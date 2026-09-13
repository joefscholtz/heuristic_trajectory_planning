# heuristic_trajectory_planning

DESCRIPTION HERE!!

## Project structure

```
.
├── examples/                             # Use-cases
│   ├── 2D/                               #
│       └── .../                          #
│   └── 3D/                               #
│       └── .../                          #
├── external/                             # External dependencies
├── heuristic_trajectory_planning/        # Python module
│   └── __init__.py                       #
│   └── core.py                           #
├── heuristic_trajectory_planning_lib/    # C++ library
├── presentation/                         # LaTeX Beamer presentation
├── schema/                               # Configuration Schema
└── justfile                              # Recipes
```

## Installation

Requirements:

- git
- [uv](https://docs.astral.sh/uv/) (Required, Python manager)
- [just](https://github.com/casey/just) (Optional, Recipes)

using just:

```bash
just init
```

without just

```bash
git submodule update --init --recursive
uv sync
external/vcpkg/bootstrap-vcpkg.sh # or .bat if on windows
```

## Build

using just:

```bash
just build
```

without just

```bash
  cmake --preset default
  cmake --build --preset default --parallel
  ln -sf build/compile_commands.json .
```

## Running examples

using just:

```bash
just run
```

without just

```bash
# Not implemented yet
```

## How to use the library

## TODO

### schema:

- [ ]
