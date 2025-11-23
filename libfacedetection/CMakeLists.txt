cmake_minimum_required(VERSION 3.28)
project(facedetection LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_EXTENSIONS OFF)

option(ENABLE_AVX2 "Enable AVX2 support" ON)
option(ENABLE_NEON "Enable NEON support" ON)
option(ENABLE_OPENMP "Enable OpenMP support" ON)

set(CMAKE_REQUIRED_QUIET TRUE)
include(GenerateExportHeader)

set(PROJECT_SOURCES
        src/facedetectcnn.cpp
        src/facedetectcnn-data.cpp
        src/facedetectcnn-model.cpp
)

add_library(${PROJECT_NAME} ${PROJECT_SOURCES})

target_include_directories(${PROJECT_NAME}
        PUBLIC include ${CMAKE_CURRENT_BINARY_DIR}/include
        PRIVATE include/facedetection ${CMAKE_CURRENT_BINARY_DIR}/include/facedetection
)

set_target_properties(${PROJECT_NAME} PROPERTIES POSITION_INDEPENDENT_CODE TRUE)

if (ENABLE_AVX2 AND CMAKE_SYSTEM_PROCESSOR MATCHES "x64|x86_64|AMD64|amd64")
    target_compile_definitions(${PROJECT_NAME} PRIVATE _ENABLE_AVX2)
    target_compile_options(${PROJECT_NAME} PRIVATE -mavx2 -mfma)
endif ()
if (ENABLE_NEON AND CMAKE_SYSTEM_PROCESSOR MATCHES "aarch64|ARM64|arm64")
    target_compile_definitions(${PROJECT_NAME} PRIVATE _ENABLE_NEON)
endif ()
if (ENABLE_OPENMP)
    find_package(OpenMP REQUIRED QUIET)
    target_link_libraries(${PROJECT_NAME} OpenMP::OpenMP_CXX)
endif ()

generate_export_header(${PROJECT_NAME} EXPORT_FILE_NAME ${CMAKE_CURRENT_BINARY_DIR}/include/facedetection/facedetection_export.h)

install(TARGETS ${PROJECT_NAME} COMPONENT ${PROJECT_NAME})
install(DIRECTORY include/ DESTINATION include COMPONENT ${PROJECT_NAME})
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/include/ DESTINATION include COMPONENT ${PROJECT_NAME})
