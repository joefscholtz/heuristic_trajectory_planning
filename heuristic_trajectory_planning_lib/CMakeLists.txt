find_package(nlohmann_json CONFIG REQUIRED)
find_package(yaml-cpp CONFIG REQUIRED)

add_library(heuristic_trajectory_planning_lib INTERFACE)

add_dependencies(heuristic_trajectory_planning_lib generate_schemas)


target_include_directories(heuristic_trajectory_planning_lib 
    INTERFACE
        ${CMAKE_CURRENT_SOURCE_DIR}/include

    INTERFACE
        ${CMAKE_CURRENT_BINARY_DIR}
        ${CMAKE_BINARY_DIR}/schema/cpp
)

add_custom_command(
    OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/config/ex_config.json
    COMMAND uv run yq "." ${CMAKE_CURRENT_SOURCE_DIR}/config/ex_config.yaml > ${CMAKE_CURRENT_BINARY_DIR}/config/ex_config.json
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/config/ex_config.yaml
)

add_custom_target(generate_ex_configs ALL
    DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/config/ex_config.json
)

target_link_libraries(heuristic_trajectory_planning_lib INTERFACE 
  nlohmann_json::nlohmann_json
  yaml-cpp::yaml-cpp
)
