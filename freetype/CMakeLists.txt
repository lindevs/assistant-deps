cmake_minimum_required(VERSION 3.28)
project(freetype VERSION 2.13.3 LANGUAGES C)

set(CMAKE_C_STANDARD 99)

set(CMAKE_REQUIRED_QUIET TRUE)
include(CheckIncludeFile)

check_include_file(unistd.h HAVE_UNISTD_H)
check_include_file(fcntl.h HAVE_FCNTL_H)

configure_file(config/ftconfig.h.in "${CMAKE_CURRENT_BINARY_DIR}/include/freetype/config/ftconfig.h" @ONLY)
configure_file(pkgconfig/freetype2.pc.in "${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/freetype2.pc" @ONLY)

set(PROJECT_UNIX_SOURCES
        src/unix/ftsystem.c
)

set(PROJECT_SOURCES
        src/autofit/autofit.c
        src/base/ftbase.c
        src/base/ftbbox.c
        src/base/ftbdf.c
        src/base/ftbitmap.c
        src/base/ftcid.c
        src/base/ftfstype.c
        src/base/ftgasp.c
        src/base/ftglyph.c
        src/base/ftgxval.c
        src/base/ftinit.c
        src/base/ftmm.c
        src/base/ftotval.c
        src/base/ftpatent.c
        src/base/ftpfr.c
        src/base/ftstroke.c
        src/base/ftsynth.c
        src/base/fttype1.c
        src/base/ftwinfnt.c
        src/base/ftdebug.c
        src/bdf/bdf.c
        src/bzip2/ftbzip2.c
        src/cache/ftcache.c
        src/cff/cff.c
        src/cid/type1cid.c
        src/gzip/ftgzip.c
        src/lzw/ftlzw.c
        src/pcf/pcf.c
        src/pfr/pfr.c
        src/psaux/psaux.c
        src/pshinter/pshinter.c
        src/psnames/psnames.c
        src/raster/raster.c
        src/sdf/sdf.c
        src/sfnt/sfnt.c
        src/smooth/smooth.c
        src/svg/svg.c
        src/truetype/truetype.c
        src/type1/type1.c
        src/type42/type42.c
        src/winfonts/winfnt.c
)

if (UNIX)
    list(APPEND PROJECT_SOURCES ${PROJECT_UNIX_SOURCES})
endif ()

add_library(${PROJECT_NAME} ${PROJECT_SOURCES})

target_include_directories(${PROJECT_NAME}
        PUBLIC include
        PRIVATE include-private ${CMAKE_CURRENT_BINARY_DIR}/include include-private/autofit include-private/base
        include-private/bdf include-private/cache include-private/cff include-private/cid include-private/lzw
        include-private/pcf include-private/pfr include-private/psaux include-private/pshinter include-private/psnames
        include-private/raster include-private/sdf include-private/sfnt include-private/smooth include-private/svg
        include-private/truetype include-private/type1 include-private/type42 include-private/winfonts
)

target_link_libraries(${PROJECT_NAME} z png)

set_target_properties(${PROJECT_NAME} PROPERTIES POSITION_INDEPENDENT_CODE TRUE)
set_target_properties(${PROJECT_NAME} PROPERTIES C_VISIBILITY_PRESET hidden)

target_compile_definitions(${PROJECT_NAME} PRIVATE FT2_BUILD_LIBRARY)

install(TARGETS ${PROJECT_NAME} COMPONENT ${PROJECT_NAME})
install(DIRECTORY include/ DESTINATION include/freetype2 COMPONENT ${PROJECT_NAME})
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/include/ DESTINATION include/freetype2 COMPONENT ${PROJECT_NAME})
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/ DESTINATION lib/pkgconfig COMPONENT ${PROJECT_NAME})
