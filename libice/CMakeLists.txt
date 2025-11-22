cmake_minimum_required(VERSION 3.28)
project(ICE VERSION 1.1.1 LANGUAGES C)

set(CMAKE_C_STANDARD 99)

set(CMAKE_REQUIRED_QUIET TRUE)
include(CheckFunctionExists)
include(CheckSymbolExists)

check_function_exists(arc4random_buf HAVE_ARC4RANDOM_BUF)
check_function_exists(asprintf HAVE_ASPRINTF)
check_function_exists(getentropy HAVE_GETENTROPY)
check_function_exists(strcasecmp HAVE_STRCASECMP)
set(ICE_t 1)
set(IPv6 1)
set(TCPCONN 1)
set(TRANS_CLIENT 1)
set(TRANS_SERVER 1)
set(UNIXCONN 1)
set(_GNU_SOURCE 1)

configure_file(config/config-cmake.h.in "${CMAKE_CURRENT_BINARY_DIR}/include/config.h" @ONLY)
configure_file(pkgconfig/ice.pc.in "${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/ice.pc" @ONLY)

set(PROJECT_SOURCES
        src/accept.c
        src/authutil.c
        src/connect.c
        src/error.c
        src/getauth.c
        src/iceauth.c
        src/icetrans.c
        src/listen.c
        src/listenwk.c
        src/locking.c
        src/misc.c
        src/ping.c
        src/process.c
        src/protosetup.c
        src/register.c
        src/replywait.c
        src/setauth.c
        src/shutdown.c
        src/watch.c
)

add_library(${PROJECT_NAME} ${PROJECT_SOURCES})

target_include_directories(${PROJECT_NAME} PUBLIC include PRIVATE ${CMAKE_CURRENT_BINARY_DIR}/include include-private)

target_link_libraries(${PROJECT_NAME} xorgproto xtrans)

set_target_properties(${PROJECT_NAME} PROPERTIES POSITION_INDEPENDENT_CODE TRUE)

target_compile_definitions(${PROJECT_NAME} PRIVATE HAVE_CONFIG_H)
target_compile_options(${PROJECT_NAME} PRIVATE -fno-strict-aliasing -Wno-format-truncation)

check_function_exists(fchown HAVE_FCHOWN)
if (HAVE_FCHOWN)
    target_compile_definitions(${PROJECT_NAME} PRIVATE HAS_FCHOWN)
endif ()

check_symbol_exists(S_ISVTX sys/stat.h HAVE_S_ISVTX)
if (HAVE_S_ISVTX)
    target_compile_definitions(${PROJECT_NAME} PRIVATE HAS_STICKY_DIR_BIT)
endif ()

install(TARGETS ${PROJECT_NAME} COMPONENT ${PROJECT_NAME})
install(DIRECTORY include/ DESTINATION include COMPONENT ${PROJECT_NAME})
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/ DESTINATION lib/pkgconfig COMPONENT ${PROJECT_NAME})
