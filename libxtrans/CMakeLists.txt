cmake_minimum_required(VERSION 3.28)
project(xtrans VERSION 1.4.0 LANGUAGES C)

set(CMAKE_C_STANDARD 99)

configure_file(pkgconfig/xtrans.pc.in "${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/xtrans.pc" @ONLY)

add_library(${PROJECT_NAME} INTERFACE)

target_include_directories(${PROJECT_NAME} INTERFACE include)

install(DIRECTORY include/ DESTINATION include COMPONENT ${PROJECT_NAME})
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/ DESTINATION share/pkgconfig COMPONENT ${PROJECT_NAME})
