cmake_minimum_required(VERSION 3.28)
project(z VERSION 1.3.1 LANGUAGES C)

set(CMAKE_C_STANDARD 99)

set(CMAKE_REQUIRED_QUIET TRUE)
include(CheckIncludeFile)
include(CheckTypeSize)
include(CMakePushCheckState)

check_include_file(unistd.h Z_HAVE_UNISTD_H)

configure_file(config/zconf.h.cmakein "${CMAKE_CURRENT_BINARY_DIR}/include/zconf.h" @ONLY)
configure_file(pkgconfig/zlib.pc.in "${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/zlib.pc" @ONLY)

set(PROJECT_SOURCES
        src/adler32.c
        src/compress.c
        src/crc32.c
        src/deflate.c
        src/gzclose.c
        src/gzlib.c
        src/gzread.c
        src/gzwrite.c
        src/inflate.c
        src/infback.c
        src/inftrees.c
        src/inffast.c
        src/trees.c
        src/uncompr.c
        src/zutil.c
)

add_library(${PROJECT_NAME} ${PROJECT_SOURCES})

target_include_directories(${PROJECT_NAME} PUBLIC include ${CMAKE_CURRENT_BINARY_DIR}/include PRIVATE include-private)

set_target_properties(${PROJECT_NAME} PROPERTIES POSITION_INDEPENDENT_CODE TRUE)

cmake_push_check_state(RESET)
set(CMAKE_REQUIRED_QUIET TRUE)
set(CMAKE_REQUIRED_DEFINITIONS -D_LARGEFILE64_SOURCE)
check_type_size(off64_t OFF64_T)
cmake_pop_check_state()
if (HAVE_OFF64_T)
    target_compile_definitions(${PROJECT_NAME} PRIVATE _LARGEFILE64_SOURCE)
endif ()

install(TARGETS ${PROJECT_NAME} COMPONENT ${PROJECT_NAME})
install(DIRECTORY include/ DESTINATION include COMPONENT ${PROJECT_NAME})
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/include/ DESTINATION include COMPONENT ${PROJECT_NAME})
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/ DESTINATION share/pkgconfig COMPONENT ${PROJECT_NAME})
