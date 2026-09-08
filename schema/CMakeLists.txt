file(MAKE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/cpp)
file(MAKE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/python)

find_package(Protobuf CONFIG REQUIRED)

# Enable compatibility mode so protobuf_generate works out-of-the-box
set(protobuf_MODULE_COMPATIBLE TRUE)

# generate C++ headers (.pb.h / .pb.cc) from config.proto
protobuf_generate(
    LANGUAGE cpp
    PROTOS config.proto
    OUT_VAR PROTO_CXX_FILES
)

# generate Python modules (_pb2.py) from config.proto
protobuf_generate(
    LANGUAGE python
    PROTOS config.proto
    OUT_VAR PROTO_PY_FILES
)

# Target to trigger code generation during the build
add_custom_target(generate_schemas ALL
    DEPENDS ${PROTO_CXX_FILES} ${PROTO_PY_FILES}
)
