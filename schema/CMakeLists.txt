file(MAKE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/cpp)
file(MAKE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/python)

add_custom_command(
    OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/cpp/OptimizationConfig.hpp
    COMMAND quicktype -s schema ${CMAKE_CURRENT_SOURCE_DIR}/main_config.yaml -o ${CMAKE_CURRENT_BINARY_DIR}/cpp/OptimizationConfig.hpp --lang cpp
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/main_config.yaml ${CMAKE_CURRENT_SOURCE_DIR}/models.yaml
)

add_custom_command(
    OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/python/config_models.py
    COMMAND uv run datamodel-codegen --input ${CMAKE_CURRENT_SOURCE_DIR}/main_config.yaml --input-file-type jsonschema --output ${CMAKE_CURRENT_BINARY_DIR}/python/config_models.py
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/main_config.yaml ${CMAKE_CURRENT_SOURCE_DIR}/models.yaml
)

add_custom_target(generate_schemas ALL
    DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/cpp/OptimizationConfig.hpp
            ${CMAKE_CURRENT_BINARY_DIR}/python/config_models.py
)
