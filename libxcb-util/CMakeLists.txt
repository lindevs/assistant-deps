cmake_minimum_required(VERSION 3.28)
project(xcb-util VERSION 0.4.1 LANGUAGES C)

set(CMAKE_C_STANDARD 99)

set(CMAKE_REQUIRED_QUIET TRUE)
include(CheckFunctionExists)

check_function_exists(vasprintf HAVE_VASPRINTF)

configure_file(config/config-cmake.h.in "${CMAKE_CURRENT_BINARY_DIR}/include/config.h" @ONLY)
configure_file(pkgconfig/xcb-atom.pc.in "${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/xcb-atom.pc" @ONLY)
configure_file(pkgconfig/xcb-aux.pc.in "${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/xcb-aux.pc" @ONLY)
configure_file(pkgconfig/xcb-event.pc.in "${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/xcb-event.pc" @ONLY)
configure_file(pkgconfig/xcb-util.pc.in "${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/xcb-util.pc" @ONLY)

set(PROJECT_SOURCES
        src/atoms.c
        src/event.c
        src/xcb_aux.c
)

add_library(${PROJECT_NAME} ${PROJECT_SOURCES})

target_include_directories(${PROJECT_NAME} PUBLIC include PRIVATE ${CMAKE_CURRENT_BINARY_DIR}/include include/xcb)

target_link_libraries(${PROJECT_NAME} xcb)

set_target_properties(${PROJECT_NAME} PROPERTIES POSITION_INDEPENDENT_CODE TRUE)

target_compile_definitions(${PROJECT_NAME} PRIVATE HAVE_CONFIG_H)
target_compile_options(${PROJECT_NAME} PRIVATE -fno-strict-aliasing)

install(TARGETS ${PROJECT_NAME} COMPONENT ${PROJECT_NAME})
install(DIRECTORY include/ DESTINATION include COMPONENT ${PROJECT_NAME})
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/ DESTINATION lib/pkgconfig COMPONENT ${PROJECT_NAME})
