find_package(Protobuf CONFIG REQUIRED)

# Generate C++ and Python headers for the plugin proto
protobuf_generate(
    LANGUAGE cpp
    PROTOS schema/super_mutation.proto
    OUT_VAR PLUGIN_CXX_FILES
)

protobuf_generate(
    LANGUAGE python
    PROTOS schema/super_mutation.proto
    OUT_VAR PLUGIN_PY_FILES
)

add_custom_target(generate_super_mutation_python ALL
    DEPENDS ${PLUGIN_PY_FILES}
)

# Compile the generated plugin proto into a static library
add_library(super_mutation_proto STATIC ${PLUGIN_CXX_FILES})
target_link_libraries(super_mutation_proto PUBLIC config_proto protobuf::libprotobuf)
target_include_directories(super_mutation_proto PUBLIC ${CMAKE_CURRENT_BINARY_DIR})

# Build the example C++ executable
add_executable(example_super_mutation cpp/main.cpp)
target_link_libraries(example_super_mutation PRIVATE heuristic_trajectory_planning_lib super_mutation_proto protobuf::libprotobuf)
target_include_directories(example_super_mutation PRIVATE ${CMAKE_CURRENT_BINARY_DIR})
