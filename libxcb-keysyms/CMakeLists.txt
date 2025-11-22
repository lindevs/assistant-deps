cmake_minimum_required(VERSION 3.28)
project(xcb-keysyms VERSION 0.4.1 LANGUAGES C)

set(CMAKE_C_STANDARD 99)

configure_file(pkgconfig/xcb-keysyms.pc.in "${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/xcb-keysyms.pc" @ONLY)

set(PROJECT_SOURCES
        src/keysyms.c
)

add_library(${PROJECT_NAME} ${PROJECT_SOURCES})

target_include_directories(${PROJECT_NAME} PUBLIC include PRIVATE include/xcb)

target_link_libraries(${PROJECT_NAME} xcb)

set_target_properties(${PROJECT_NAME} PROPERTIES POSITION_INDEPENDENT_CODE TRUE)

target_compile_options(${PROJECT_NAME} PRIVATE -fno-strict-aliasing)

install(TARGETS ${PROJECT_NAME} COMPONENT ${PROJECT_NAME})
install(DIRECTORY include/ DESTINATION include COMPONENT ${PROJECT_NAME})
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/ DESTINATION lib/pkgconfig COMPONENT ${PROJECT_NAME})
