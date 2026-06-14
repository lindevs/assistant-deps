cmake_minimum_required(VERSION 3.28)
project(xkbcommon VERSION 1.10.0 LANGUAGES C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_EXTENSIONS OFF)

set(DEFAULT_XKB_LAYOUT "us" CACHE STRING "Default XKB layout")
set(DEFAULT_XKB_MODEL "pc105" CACHE STRING "Default XKB model")
set(DEFAULT_XKB_OPTIONS "NULL" CACHE STRING "Default XKB options")
set(DEFAULT_XKB_RULES "evdev" CACHE STRING "Default XKB ruleset")
set(DEFAULT_XKB_VARIANT "NULL" CACHE STRING "Default XKB variant")
set(DFLT_XKB_CONFIG_EXTRA_PATH "/usr/local/etc/xkb" CACHE STRING "Extra lookup path for system-wide XKB data")
set(DFLT_XKB_CONFIG_ROOT "/usr/share/X11/xkb" CACHE STRING "The XKB config root")
set(XLOCALEDIR "/usr/share/X11/locale" CACHE STRING "The X locale root")

set(CMAKE_REQUIRED_QUIET TRUE)
include(CheckIncludeFile)
include(CheckFunctionExists)
include(CheckSymbolExists)
include(CheckSourceCompiles)
include(CMakePushCheckState)

check_include_file(unistd.h HAVE_UNISTD_H)
check_function_exists(asprintf HAVE_ASPRINTF)
check_function_exists(mmap HAVE_MMAP)
check_function_exists(open_memstream HAVE_OPEN_MEMSTREAM)
check_function_exists(posix_fallocate HAVE_POSIX_FALLOCATE)
check_function_exists(strndup HAVE_STRNDUP)
check_source_compiles(C "int main(){if(__builtin_expect(1<0,0)){}}" HAVE___BUILTIN_EXPECT)

cmake_push_check_state(RESET)
set(CMAKE_REQUIRED_QUIET TRUE)
set(CMAKE_REQUIRED_DEFINITIONS -D_GNU_SOURCE)
check_symbol_exists(eaccess unistd.h HAVE_EACCESS)
check_symbol_exists(euidaccess unistd.h HAVE_EUIDACCESS)
check_symbol_exists(mkostemp stdlib.h HAVE_MKOSTEMP)
check_symbol_exists(secure_getenv stdlib.h HAVE_SECURE_GETENV)
cmake_pop_check_state()

set(EXIT_INVALID_USAGE 2)
set(_GNU_SOURCE 1)

configure_file(config/config.h.in "${CMAKE_CURRENT_BINARY_DIR}/include-private/config.h" @ONLY)
configure_file(pkgconfig/xkbcommon.pc.in "${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/xkbcommon.pc" @ONLY)
configure_file(pkgconfig/xkbcommon-x11.pc.in "${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/xkbcommon-x11.pc" @ONLY)

set(PROJECT_X11_SOURCES
        src/x11/keymap.c
        src/x11/state.c
        src/x11/util.c
        src/context-priv.c
        src/keymap-priv.c
        src/atom.c
)

set(PROJECT_SOURCES
        src/xkbcomp/action.c
        src/xkbcomp/keymap.c
        src/xkbcomp/xkbcomp.c
        src/xkbcomp/symbols.c
        src/xkbcomp/rules.c
        src/xkbcomp/keymap-dump.c
        src/xkbcomp/ast-build.c
        src/xkbcomp/types.c
        src/xkbcomp/expr.c
        src/xkbcomp/include.c
        src/xkbcomp/keycodes.c
        src/xkbcomp/compat.c
        src/xkbcomp/vmod.c
        src/xkbcomp/keywords.c
        src/xkbcomp/scanner.c
        src/compose/table.c
        src/compose/paths.c
        src/compose/state.c
        src/compose/parser.c
        src/atom.c
        src/context.c
        src/context-priv.c
        src/keymap.c
        src/keymap-priv.c
        src/keysym.c
        src/keysym-case-mappings.c
        src/keysym-utf.c
        src/scanner-utils.c
        src/state.c
        src/text.c
        src/utf8.c
        src/utf8-decoding.c
        src/utils.c
        src/utils-paths.c
)

list(PREPEND PROJECT_SOURCES generated/bison/parser.c)

add_library(${PROJECT_NAME}-x11 ${PROJECT_X11_SOURCES})
add_library(${PROJECT_NAME} ${PROJECT_SOURCES})

target_include_directories(${PROJECT_NAME}-x11
        PUBLIC include
        PRIVATE include-private ${CMAKE_CURRENT_BINARY_DIR}/include-private include-private/x11
)
target_include_directories(${PROJECT_NAME}
        PUBLIC include
        PRIVATE include-private ${CMAKE_CURRENT_BINARY_DIR}/include-private
        include-private/xkbcomp include-private/compose generated
)

target_link_libraries(${PROJECT_NAME}-x11 xcb)
target_link_libraries(${PROJECT_NAME} ${PROJECT_NAME}-x11)

set_target_properties(${PROJECT_NAME}-x11 PROPERTIES POSITION_INDEPENDENT_CODE TRUE)
set_target_properties(${PROJECT_NAME}-x11 PROPERTIES C_VISIBILITY_PRESET hidden)
set_target_properties(${PROJECT_NAME} PROPERTIES POSITION_INDEPENDENT_CODE TRUE)
set_target_properties(${PROJECT_NAME} PROPERTIES C_VISIBILITY_PRESET hidden)

target_compile_definitions(${PROJECT_NAME}-x11 PRIVATE _FILE_OFFSET_BITS=64)
target_compile_options(${PROJECT_NAME}-x11 PRIVATE -fno-strict-aliasing)
target_compile_definitions(${PROJECT_NAME} PRIVATE _FILE_OFFSET_BITS=64)
target_compile_options(${PROJECT_NAME} PRIVATE -fno-strict-aliasing)

install(TARGETS ${PROJECT_NAME}-x11 COMPONENT ${PROJECT_NAME})
install(TARGETS ${PROJECT_NAME} COMPONENT ${PROJECT_NAME})
install(DIRECTORY include/ DESTINATION include COMPONENT ${PROJECT_NAME})
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/ DESTINATION lib/pkgconfig COMPONENT ${PROJECT_NAME})
