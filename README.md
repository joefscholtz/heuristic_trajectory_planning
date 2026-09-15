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

## Requirements:

### Using Docker

- Docker
- Docker Compose

### Without Docker

- git
- [uv](https://docs.astral.sh/uv/) (Required, Python manager)
- [just](https://github.com/casey/just) (Optional, Recipes)

## Initialization

### Using Docker

Build image:

```bash
docker compose -f docker-compose.yml build;
```

Enter image:

```bash
docker compose -f docker-compose.yml run -it --rm --name heuristic_trajectory_planning heuristic_trajectory_planning-app bash
```

Once in the docker container you can proceed as follows

### Without Docker or after entering the image

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

### Building only protobuf parsing for Python

```bash
just gen-base-py-proto
```

```bash
just gen-example-py-proto examples/example_config/schema
```

## Running examples

using just:

```bash
just run
```

without just

```bash
uv run examples/example_config/python/main.py
uv run examples/example_map/python/main.py
```

## How to use the library

## TODO

### schema:

- [ ]

### Docker

- [] Fix matplotlib not showing one Docker container
