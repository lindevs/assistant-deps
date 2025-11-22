cmake_minimum_required(VERSION 3.28)
project(xcb-wm VERSION 0.4.2 LANGUAGES C)

set(CMAKE_C_STANDARD 99)

configure_file(pkgconfig/xcb-ewmh.pc.in "${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/xcb-ewmh.pc" @ONLY)
configure_file(pkgconfig/xcb-icccm.pc.in "${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/xcb-icccm.pc" @ONLY)

add_library(xcb-ewmh src/ewmh.c)
add_library(xcb-icccm src/icccm.c)

target_include_directories(xcb-ewmh PUBLIC include PRIVATE include/xcb)
target_include_directories(xcb-icccm PUBLIC include PRIVATE include/xcb)

target_link_libraries(xcb-ewmh xcb)
target_link_libraries(xcb-icccm xcb)

set_target_properties(xcb-ewmh PROPERTIES POSITION_INDEPENDENT_CODE TRUE)
set_target_properties(xcb-icccm PROPERTIES POSITION_INDEPENDENT_CODE TRUE)

install(TARGETS xcb-ewmh xcb-icccm COMPONENT ${PROJECT_NAME})
install(DIRECTORY include/ DESTINATION include COMPONENT ${PROJECT_NAME})
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/ DESTINATION lib/pkgconfig COMPONENT ${PROJECT_NAME})
