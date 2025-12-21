cmake_minimum_required(VERSION 3.28)
project(openjp2 VERSION 2.5.4 LANGUAGES C)

set(CMAKE_C_STANDARD 99)

option(OPJ_USE_THREAD "Build with thread/mutex support" ON)

set(CMAKE_REQUIRED_QUIET TRUE)
include(CheckIncludeFile)
include(CheckSymbolExists)
include(CheckSourceCompiles)

check_include_file(malloc.h OPJ_HAVE_MALLOC_H)
check_symbol_exists(_aligned_malloc malloc.h OPJ_HAVE__ALIGNED_MALLOC)
check_symbol_exists(memalign malloc.h OPJ_HAVE_MEMALIGN)
check_symbol_exists(posix_memalign stdlib.h OPJ_HAVE_POSIX_MEMALIGN)
check_source_compiles(C "
#include <sys/types.h>
#include <stdio.h>
int main(int argc, char **argv) {
#define LARGE_OFF_T (((off_t) 1 << 62) - 1 + ((off_t) 1 << 62))
    int off_t_is_large[(LARGE_OFF_T % 2147483629 == 721 && LARGE_OFF_T % 2147483647 == 1) ? 1 : -1];
    FILE *fp = fopen(argv[0], \"r\");
    off_t offset = ftello(fp);
    fseeko(fp, offset, SEEK_CUR);
    fclose(fp);
    return 0;
}
" OPJ_HAVE_FSEEKO)

configure_file(config/opj_config.h.cmake.in "${CMAKE_CURRENT_BINARY_DIR}/include/openjpeg/opj_config.h" @ONLY)
configure_file(config/opj_config_private.h.cmake.in "${CMAKE_CURRENT_BINARY_DIR}/include-private/opj_config_private.h" @ONLY)

set(PROJECT_SOURCES
        src/bio.c
        src/cio.c
        src/dwt.c
        src/event.c
        src/function_list.c
        src/ht_dec.c
        src/image.c
        src/invert.c
        src/j2k.c
        src/jp2.c
        src/mct.c
        src/mqc.c
        src/openjpeg.c
        src/opj_clock.c
        src/opj_malloc.c
        src/pi.c
        src/sparse_array.c
        src/t1.c
        src/t2.c
        src/tcd.c
        src/tgt.c
        src/thread.c
)

add_library(${PROJECT_NAME} ${PROJECT_SOURCES})

target_include_directories(${PROJECT_NAME}
        PUBLIC include/openjpeg ${CMAKE_CURRENT_BINARY_DIR}/include/openjpeg
        PRIVATE include-private ${CMAKE_CURRENT_BINARY_DIR}/include-private
)

set_target_properties(${PROJECT_NAME} PROPERTIES POSITION_INDEPENDENT_CODE TRUE)

if (OPJ_USE_THREAD)
    target_compile_definitions(${PROJECT_NAME} PRIVATE MUTEX_pthread)
endif ()

target_compile_options(${PROJECT_NAME} PRIVATE -ffast-math)

install(TARGETS ${PROJECT_NAME} COMPONENT ${PROJECT_NAME})
install(DIRECTORY include/ DESTINATION include COMPONENT ${PROJECT_NAME})
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/include/ DESTINATION include COMPONENT ${PROJECT_NAME})
