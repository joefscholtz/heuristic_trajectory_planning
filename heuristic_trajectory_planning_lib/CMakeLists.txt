find_package(Protobuf CONFIG REQUIRED)

add_library(heuristic_trajectory_planning_lib INTERFACE)

add_dependencies(heuristic_trajectory_planning_lib generate_schemas)

target_include_directories(heuristic_trajectory_planning_lib 
    INTERFACE
        ${CMAKE_CURRENT_SOURCE_DIR}/include
    INTERFACE
        ${CMAKE_CURRENT_BINARY_DIR}
        ${CMAKE_BINARY_DIR}/schema
)

target_link_libraries(heuristic_trajectory_planning_lib INTERFACE 
  protobuf::libprotobuf
)

add_executable(test_config examples/test_config.cpp)
target_link_libraries(test_config PRIVATE heuristic_trajectory_planning_lib protobuf::libprotobuf)
target_include_directories(test_config PRIVATE ${CMAKE_BINARY_DIR}/schema)
