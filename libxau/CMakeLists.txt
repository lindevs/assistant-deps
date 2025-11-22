cmake_minimum_required(VERSION 3.28)
project(Xau VERSION 1.0.11 LANGUAGES C)

set(CMAKE_C_STANDARD 99)

option(XTHREADS "Enable libXau support for multithreading" ON)

set(CMAKE_REQUIRED_QUIET TRUE)
include(CheckFunctionExists)
include(CheckLibraryExists)

check_function_exists(explicit_bzero HAVE_EXPLICIT_BZERO)
check_function_exists(pathconf HAVE_PATHCONF)

if (XTHREADS)
    check_function_exists(gethostbyname_r HAVE_GETHOSTBYNAME_R)
    if (NOT HAVE_GETHOSTBYNAME_R)
        check_library_exists(nsl gethostbyname_r "" HAVE_NSL_GETHOSTBYNAME_R)
    endif ()
    if (HAVE_GETHOSTBYNAME_R OR HAVE_NSL_GETHOSTBYNAME_R)
        set(XUSE_MTSAFE_API 1)
    endif ()

    if (CMAKE_SYSTEM_NAME STREQUAL "SunOS")
        set(_POSIX_PTHREAD_SEMANTICS 1)
        set(_REENTRANT 1)
    endif ()
endif ()

configure_file(config/config-cmake.h.in "${CMAKE_CURRENT_BINARY_DIR}/include/config.h" @ONLY)
configure_file(pkgconfig/xau.pc.in "${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/xau.pc" @ONLY)

set(PROJECT_SOURCES
        src/AuDispose.c
        src/AuFileName.c
        src/AuGetAddr.c
        src/AuGetBest.c
        src/AuLock.c
        src/AuRead.c
        src/AuUnlock.c
        src/AuWrite.c
)

add_library(${PROJECT_NAME} ${PROJECT_SOURCES})

target_include_directories(${PROJECT_NAME} PUBLIC include PRIVATE ${CMAKE_CURRENT_BINARY_DIR}/include)

target_link_libraries(${PROJECT_NAME} xorgproto)

set_target_properties(${PROJECT_NAME} PROPERTIES POSITION_INDEPENDENT_CODE TRUE)

target_compile_definitions(${PROJECT_NAME} PRIVATE HAVE_CONFIG_H)
target_compile_options(${PROJECT_NAME} PRIVATE -fno-strict-aliasing)

install(TARGETS ${PROJECT_NAME} COMPONENT ${PROJECT_NAME})
install(DIRECTORY include/ DESTINATION include COMPONENT ${PROJECT_NAME})
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/ DESTINATION lib/pkgconfig COMPONENT ${PROJECT_NAME})
