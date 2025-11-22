cmake_minimum_required(VERSION 3.28)
project(pcre2 VERSION 10.45 LANGUAGES C)

set(CMAKE_C_STANDARD 99)

set(PCRE2_LINK_SIZE "2" CACHE STRING "Internal link size (2, 3 or 4 allowed)")
set(PCRE2_HEAP_LIMIT "20000000" CACHE STRING "Default limit on heap memory (kibibytes)")
set(PCRE2_MATCH_LIMIT "10000000" CACHE STRING "Default limit on internal looping")
set(PCRE2_MATCH_LIMIT_DEPTH "MATCH_LIMIT" CACHE STRING "Default limit on internal depth of search")
set(PCRE2_MAX_VARLOOKBEHIND "255" CACHE STRING "Default limit on variable lookbehinds")
set(PCRE2_NEWLINE "LF" CACHE STRING "What to recognize as a newline (one of CR, LF, CRLF, ANY, ANYCRLF, NUL)")
set(PCRE2_PARENS_NEST_LIMIT "250" CACHE STRING "Default nested parentheses limit")
set(PCRE2GREP_BUFSIZE "20480" CACHE STRING "Buffer starting size parameter for pcre2grep")
set(PCRE2GREP_MAX_BUFSIZE "1048576" CACHE STRING "Buffer maximum size parameter for pcre2grep")

set(CMAKE_REQUIRED_QUIET TRUE)
include(CheckIncludeFile)
include(CheckSymbolExists)
include(CheckSourceCompiles)

set(SUPPORT_PCRE2_8 1)
set(SUPPORT_PCRE2_16 1)
set(SUPPORT_PCRE2_32 1)
set(SUPPORT_JIT 1)
set(SUPPORT_PCRE2GREP_JIT 1)
set(SUPPORT_PCRE2GREP_CALLOUT 1)
set(SUPPORT_PCRE2GREP_CALLOUT_FORK 1)
set(SUPPORT_UNICODE 1)
check_include_file(assert.h HAVE_ASSERT_H)
check_include_file(dirent.h HAVE_DIRENT_H)
check_include_file(sys/stat.h HAVE_SYS_STAT_H)
check_include_file(sys/types.h HAVE_SYS_TYPES_H)
check_include_file(unistd.h HAVE_UNISTD_H)
check_include_file(windows.h HAVE_WINDOWS_H)
check_symbol_exists(bcopy strings.h HAVE_BCOPY)
check_symbol_exists(memfd_create sys/mman.h HAVE_MEMFD_CREATE)
check_symbol_exists(memmove string.h HAVE_MEMMOVE)
check_symbol_exists(secure_getenv stdlib.h HAVE_SECURE_GETENV)
check_symbol_exists(strerror string.h HAVE_STRERROR)
check_source_compiles(C "
    #include <stddef.h>
    int main(void) { int a,b; size_t m; __builtin_mul_overflow(a,b,&m); return 0; }
" HAVE_BUILTIN_MUL_OVERFLOW)
check_source_compiles(C "
    int main(int c, char *v[]) { if (c) __builtin_unreachable(); return (int)(*v[0]); }
" HAVE_BUILTIN_UNREACHABLE)

check_source_compiles(C "
    extern __attribute__ ((visibility (\"default\"))) int f(void);
    int main(void) { return f(); }
    int f(void) { return 42; }
" HAVE_VISIBILITY)
if (HAVE_VISIBILITY)
    set(PCRE2_EXPORT "__attribute__ ((visibility (\"default\")))")
else ()
    set(PCRE2_EXPORT)
endif ()

if (PCRE2_NEWLINE STREQUAL "CR")
    set(NEWLINE_DEFAULT "1")
endif ()
if (PCRE2_NEWLINE STREQUAL "LF")
    set(NEWLINE_DEFAULT "2")
endif ()
if (PCRE2_NEWLINE STREQUAL "CRLF")
    set(NEWLINE_DEFAULT "3")
endif ()
if (PCRE2_NEWLINE STREQUAL "ANY")
    set(NEWLINE_DEFAULT "4")
endif ()
if (PCRE2_NEWLINE STREQUAL "ANYCRLF")
    set(NEWLINE_DEFAULT "5")
endif ()
if (PCRE2_NEWLINE STREQUAL "NUL")
    set(NEWLINE_DEFAULT "6")
endif ()

configure_file(config/config-cmake.h.in "${CMAKE_CURRENT_BINARY_DIR}/include/config.h" @ONLY)
configure_file(pkgconfig/libpcre2-posix.pc.in "${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/libpcre2-posix.pc" @ONLY)
configure_file(pkgconfig/libpcre2-8.pc.in "${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/libpcre2-8.pc" @ONLY)
configure_file(pkgconfig/libpcre2-16.pc.in "${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/libpcre2-16.pc" @ONLY)
configure_file(pkgconfig/libpcre2-32.pc.in "${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/libpcre2-32.pc" @ONLY)

set(PROJECT_POSIX_SOURCES
        src/pcre2posix.c
)

set(PROJECT_SOURCES
        src/pcre2_auto_possess.c
        src/pcre2_chartables.c
        src/pcre2_chkdint.c
        src/pcre2_compile.c
        src/pcre2_compile_class.c
        src/pcre2_config.c
        src/pcre2_context.c
        src/pcre2_convert.c
        src/pcre2_dfa_match.c
        src/pcre2_error.c
        src/pcre2_extuni.c
        src/pcre2_find_bracket.c
        src/pcre2_jit_compile.c
        src/pcre2_maketables.c
        src/pcre2_match.c
        src/pcre2_match_data.c
        src/pcre2_newline.c
        src/pcre2_ord2utf.c
        src/pcre2_pattern_info.c
        src/pcre2_script_run.c
        src/pcre2_serialize.c
        src/pcre2_string_utils.c
        src/pcre2_study.c
        src/pcre2_substitute.c
        src/pcre2_substring.c
        src/pcre2_tables.c
        src/pcre2_ucd.c
        src/pcre2_valid_utf.c
        src/pcre2_xclass.c
)

add_library(${PROJECT_NAME}-posix ${PROJECT_POSIX_SOURCES})
add_library(${PROJECT_NAME}-8 ${PROJECT_SOURCES})
add_library(${PROJECT_NAME}-16 ${PROJECT_SOURCES})
add_library(${PROJECT_NAME}-32 ${PROJECT_SOURCES})

target_include_directories(${PROJECT_NAME}-posix PUBLIC include PRIVATE ${CMAKE_CURRENT_BINARY_DIR}/include include-private)
target_include_directories(${PROJECT_NAME}-8 PUBLIC include PRIVATE ${CMAKE_CURRENT_BINARY_DIR}/include include-private)
target_include_directories(${PROJECT_NAME}-16 PUBLIC include PRIVATE ${CMAKE_CURRENT_BINARY_DIR}/include include-private)
target_include_directories(${PROJECT_NAME}-32 PUBLIC include PRIVATE ${CMAKE_CURRENT_BINARY_DIR}/include include-private)

set_target_properties(${PROJECT_NAME}-posix PROPERTIES POSITION_INDEPENDENT_CODE TRUE)
set_target_properties(${PROJECT_NAME}-posix PROPERTIES C_VISIBILITY_PRESET hidden)
set_target_properties(${PROJECT_NAME}-8 PROPERTIES POSITION_INDEPENDENT_CODE TRUE)
set_target_properties(${PROJECT_NAME}-8 PROPERTIES C_VISIBILITY_PRESET hidden)
set_target_properties(${PROJECT_NAME}-16 PROPERTIES POSITION_INDEPENDENT_CODE TRUE)
set_target_properties(${PROJECT_NAME}-16 PROPERTIES C_VISIBILITY_PRESET hidden)
set_target_properties(${PROJECT_NAME}-32 PROPERTIES POSITION_INDEPENDENT_CODE TRUE)
set_target_properties(${PROJECT_NAME}-32 PROPERTIES C_VISIBILITY_PRESET hidden)

target_compile_definitions(${PROJECT_NAME}-posix PRIVATE HAVE_CONFIG_H)
target_compile_definitions(${PROJECT_NAME}-posix PRIVATE PCRE2_CODE_UNIT_WIDTH=8)
target_compile_definitions(${PROJECT_NAME}-8 PRIVATE HAVE_CONFIG_H)
target_compile_definitions(${PROJECT_NAME}-8 PRIVATE PCRE2_CODE_UNIT_WIDTH=8)
target_compile_definitions(${PROJECT_NAME}-16 PRIVATE HAVE_CONFIG_H)
target_compile_definitions(${PROJECT_NAME}-16 PRIVATE PCRE2_CODE_UNIT_WIDTH=16)
target_compile_definitions(${PROJECT_NAME}-32 PRIVATE HAVE_CONFIG_H)
target_compile_definitions(${PROJECT_NAME}-32 PRIVATE PCRE2_CODE_UNIT_WIDTH=32)

check_source_compiles(C "
    #ifndef __CET__
    #error CET is not enabled
    #endif
    int main() { return 0; }
" INTEL_CET_ENABLED)
if (INTEL_CET_ENABLED)
    target_compile_options(${PROJECT_NAME}-8 PRIVATE -mshstk)
    target_compile_options(${PROJECT_NAME}-16 PRIVATE -mshstk)
    target_compile_options(${PROJECT_NAME}-32 PRIVATE -mshstk)
endif ()

install(TARGETS ${PROJECT_NAME}-posix COMPONENT ${PROJECT_NAME})
install(TARGETS ${PROJECT_NAME}-8 COMPONENT ${PROJECT_NAME})
install(TARGETS ${PROJECT_NAME}-16 COMPONENT ${PROJECT_NAME})
install(TARGETS ${PROJECT_NAME}-32 COMPONENT ${PROJECT_NAME})
install(DIRECTORY include/ DESTINATION include COMPONENT ${PROJECT_NAME})
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/ DESTINATION lib/pkgconfig COMPONENT ${PROJECT_NAME})
