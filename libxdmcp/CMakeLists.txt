cmake_minimum_required(VERSION 3.28)
project(Xdmcp VERSION 1.1.5 LANGUAGES C)

set(CMAKE_C_STANDARD 99)

set(CMAKE_REQUIRED_QUIET TRUE)
include(CheckFunctionExists)

check_function_exists(arc4random_buf HAVE_ARC4RANDOM_BUF)
check_function_exists(getentropy HAVE_GETENTROPY)
check_function_exists(lrand48 HAVE_LRAND48)
check_function_exists(srand48 HAVE_SRAND48)
set(HASXDMAUTH 1)

configure_file(config/config-cmake.h.in "${CMAKE_CURRENT_BINARY_DIR}/include/config.h" @ONLY)
configure_file(pkgconfig/xdmcp.pc.in "${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/xdmcp.pc" @ONLY)

set(PROJECT_SOURCES
        src/Array.c
        src/Fill.c
        src/Flush.c
        src/Key.c
        src/Read.c
        src/Unwrap.c
        src/Wrap.c
        src/Wraphelp.c
        src/Write.c
)

add_library(${PROJECT_NAME} ${PROJECT_SOURCES})

target_include_directories(${PROJECT_NAME} PUBLIC include PRIVATE ${CMAKE_CURRENT_BINARY_DIR}/include include-private)

target_link_libraries(${PROJECT_NAME} xorgproto)

set_target_properties(${PROJECT_NAME} PROPERTIES POSITION_INDEPENDENT_CODE TRUE)

target_compile_definitions(${PROJECT_NAME} PRIVATE HAVE_CONFIG_H)
target_compile_options(${PROJECT_NAME} PRIVATE -fno-strict-aliasing)

install(TARGETS ${PROJECT_NAME} COMPONENT ${PROJECT_NAME})
install(DIRECTORY include/ DESTINATION include COMPONENT ${PROJECT_NAME})
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/ DESTINATION lib/pkgconfig COMPONENT ${PROJECT_NAME})
