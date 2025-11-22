cmake_minimum_required(VERSION 3.28)
project(xcb-cursor VERSION 0.1.5 LANGUAGES C)

set(CMAKE_C_STANDARD 99)

set(XCURSORPATH "~/.icons:/usr/share/icons:/usr/share/pixmaps:/usr/X11R6/lib/X11/icons" CACHE STRING "Search path for cursors")

set(CMAKE_REQUIRED_QUIET TRUE)
include(CheckFunctionExists)
include(CheckIncludeFile)

configure_file(pkgconfig/xcb-cursor.pc.in "${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/xcb-cursor.pc" @ONLY)

set(PROJECT_SOURCES
        src/cursor.c
        src/load_cursor.c
        src/parse_cursor_file.c
        src/shape_to_id.c
)

add_library(${PROJECT_NAME} ${PROJECT_SOURCES})

target_include_directories(${PROJECT_NAME} PUBLIC include PRIVATE include-private include/xcb)

target_link_libraries(${PROJECT_NAME} xcb xcb-render-util xcb-image)

set_target_properties(${PROJECT_NAME} PROPERTIES POSITION_INDEPENDENT_CODE TRUE)

target_compile_definitions(${PROJECT_NAME} PRIVATE XCURSORPATH="${XCURSORPATH}")
target_compile_definitions(${PROJECT_NAME} PRIVATE _GNU_SOURCE)

check_function_exists(le32toh HAVE_LE32TOH)
if (HAVE_LE32TOH)
    target_compile_definitions(${PROJECT_NAME} PRIVATE HAVE_LE32TOH)
endif ()

check_include_file(endian.h HAVE_ENDIAN_H)
if (HAVE_ENDIAN_H)
    target_compile_definitions(${PROJECT_NAME} PRIVATE HAVE_ENDIAN_H)
endif ()

check_include_file(sys/endian.h HAVE_SYS_ENDIAN_H)
if (HAVE_SYS_ENDIAN_H)
    target_compile_definitions(${PROJECT_NAME} PRIVATE HAVE_SYS_ENDIAN_H)
endif ()

check_include_file(sys/byteorder.h HAVE_SYS_BYTEORDER_H)
if (HAVE_SYS_BYTEORDER_H)
    target_compile_definitions(${PROJECT_NAME} PRIVATE HAVE_SYS_BYTEORDER_H)
endif ()

check_include_file(libkern/OSByteOrder.h HAVE_LIBKERN_OSBYTEORDER_H)
if (HAVE_LIBKERN_OSBYTEORDER_H)
    target_compile_definitions(${PROJECT_NAME} PRIVATE HAVE_LIBKERN_OSBYTEORDER_H)
endif ()

target_compile_options(${PROJECT_NAME} PRIVATE -fno-strict-aliasing)

install(TARGETS ${PROJECT_NAME} COMPONENT ${PROJECT_NAME})
install(DIRECTORY include/ DESTINATION include COMPONENT ${PROJECT_NAME})
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/ DESTINATION lib/pkgconfig COMPONENT ${PROJECT_NAME})
