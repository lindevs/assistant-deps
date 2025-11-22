cmake_minimum_required(VERSION 3.28)
project(xcb-render-util VERSION 0.3.10 LANGUAGES C)

set(CMAKE_C_STANDARD 99)

configure_file(pkgconfig/xcb-renderutil.pc.in "${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/xcb-renderutil.pc" @ONLY)

set(PROJECT_SOURCES
        src/cache.c
        src/util.c
        src/glyph.c
)

add_library(${PROJECT_NAME} ${PROJECT_SOURCES})

target_include_directories(${PROJECT_NAME} PUBLIC include PRIVATE include/xcb)

target_link_libraries(${PROJECT_NAME} xcb)

set_target_properties(${PROJECT_NAME} PROPERTIES POSITION_INDEPENDENT_CODE TRUE)

install(TARGETS ${PROJECT_NAME} COMPONENT ${PROJECT_NAME})
install(DIRECTORY include/ DESTINATION include COMPONENT ${PROJECT_NAME})
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/ DESTINATION lib/pkgconfig COMPONENT ${PROJECT_NAME})
