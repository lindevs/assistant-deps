cmake_minimum_required(VERSION 3.28)
project(SM VERSION 1.2.4 LANGUAGES C)

set(CMAKE_C_STANDARD 99)

set(IPv6 1)
set(TCPCONN 1)

configure_file(config/config-cmake.h.in "${CMAKE_CURRENT_BINARY_DIR}/include/config.h" @ONLY)
configure_file(pkgconfig/sm.pc.in "${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/sm.pc" @ONLY)

set(PROJECT_SOURCES
        src/sm_client.c
        src/sm_error.c
        src/sm_genid.c
        src/sm_manager.c
        src/sm_misc.c
        src/sm_process.c
)

add_library(${PROJECT_NAME} ${PROJECT_SOURCES})

target_include_directories(${PROJECT_NAME} PUBLIC include PRIVATE ${CMAKE_CURRENT_BINARY_DIR}/include include-private)

target_link_libraries(${PROJECT_NAME} ICE)

set_target_properties(${PROJECT_NAME} PROPERTIES POSITION_INDEPENDENT_CODE TRUE)

target_compile_definitions(${PROJECT_NAME} PRIVATE HAVE_CONFIG_H)
target_compile_options(${PROJECT_NAME} PRIVATE -fno-strict-aliasing)

install(TARGETS ${PROJECT_NAME} COMPONENT ${PROJECT_NAME})
install(DIRECTORY include/ DESTINATION include COMPONENT ${PROJECT_NAME})
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/ DESTINATION lib/pkgconfig COMPONENT ${PROJECT_NAME})
