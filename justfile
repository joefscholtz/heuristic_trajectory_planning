alias i:= init
alias b:= build
alias c:= clean
# alias e:= enter
alias r:=run

container_name:='heuristic_trajectory_planning'
docker-compose-service:='heuristic_trajectory_planning-app'

default:
  just --list

init:
  git submodule update --init --recursive
  uv sync
  external/vcpkg/bootstrap-vcpkg.sh

# pre-commit-init:
#   uv run pre-commit install --hook-type pre-commit --hook-type pre-push

build:
  cmake --preset default
  cmake --build --preset default --parallel
  ln -sf build/compile_commands.json .

run:
  @echo "Not implemented yet."

clean:
  @echo "Not implemented yet."

hard-clean: && clean
  @echo "Not implemented yet."

reset:
  @echo "Not implemented yet."

# test:
#   @echo "Not implemented yet."
#
# test-all:
#   @echo "Not implemented yet."#
#
# lint:
#   @echo "Not implemented yet."#
#
# format:
#   find app components -name "*.c" -o -name "*.h" | xargs clang-format -i
#
# qa:
#   just format
#   just lint
#   just test
#   just build

# Using Docker

# down:
#   docker stop {{container_name}} || true
#   docker rm {{container_name}} || true
#   docker compose -f docker-compose.yml down || true
#
# build-image args="--progress='auto'": down
#   @echo "Use 'just build-image --progress=\"plain\"' for more information. Options: auto (default), tty, plain, json, quiet"
#   docker compose {{args}} -f docker-compose.yml build;
#
# enter: down && down
#   docker compose -f docker-compose.yml run -it --rm --name {{container_name}} {{docker-compose-service}} bash
#
# dev target: down && down
#     docker-compose run --rm {{docker-compose-service}} just {{target}}
