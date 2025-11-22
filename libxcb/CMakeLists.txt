cmake_minimum_required(VERSION 3.28)
project(xcb VERSION 1.17.0 LANGUAGES C)

set(CMAKE_C_STANDARD 99)

set(XCB_QUEUE_BUFFER_SIZE 16384 CACHE STRING "XCB buffer size")

set(CMAKE_REQUIRED_QUIET TRUE)
include(CheckFunctionExists)
include(CheckSymbolExists)
include(CheckCompilerFlag)

check_function_exists(getaddrinfo HAVE_GETADDRINFO)
check_function_exists(sendmsg HAVE_SENDMSG)
check_function_exists(poll USE_POLL)
check_compiler_flag(C -fvisibility=hidden GCC_HAS_VISIBILITY)

check_symbol_exists(IOV_MAX limits.h HAVE_IOV_MAX)
if (NOT HAVE_IOV_MAX)
    check_symbol_exists(UIO_MAXIOV sys/uio.h HAVE_UIO_MAXIOV)
    if (HAVE_UIO_MAXIOV)
        set(IOV_MAX UIO_MAXIOV)
    else ()
        set(IOV_MAX 16)
    endif ()
endif ()

if (UNIX AND NOT APPLE)
    set(HAVE_ABSTRACT_SOCKETS 1)
endif ()

configure_file(config/config-cmake.h.in "${CMAKE_CURRENT_BINARY_DIR}/include/config.h" @ONLY)

set(PKGCONFIG_FILES
        pkgconfig/xcb
        pkgconfig/xcb-composite
        pkgconfig/xcb-damage
        pkgconfig/xcb-dbe
        pkgconfig/xcb-dpms
        pkgconfig/xcb-dri2
        pkgconfig/xcb-dri3
        pkgconfig/xcb-glx
        pkgconfig/xcb-present
        pkgconfig/xcb-randr
        pkgconfig/xcb-record
        pkgconfig/xcb-render
        pkgconfig/xcb-res
        pkgconfig/xcb-screensaver
        pkgconfig/xcb-shape
        pkgconfig/xcb-shm
        pkgconfig/xcb-sync
        pkgconfig/xcb-xf86dri
        pkgconfig/xcb-xfixes
        pkgconfig/xcb-xinerama
        pkgconfig/xcb-xinput
        pkgconfig/xcb-xkb
        pkgconfig/xcb-xtest
        pkgconfig/xcb-xv
        pkgconfig/xcb-xvmc
)

foreach (pkgconfig_file ${PKGCONFIG_FILES})
    configure_file(${pkgconfig_file}.pc.in "${CMAKE_CURRENT_BINARY_DIR}/${pkgconfig_file}.pc" @ONLY)
endforeach ()

set(PROJECT_COMPONENTS
        composite
        damage
        dbe
        dpms
        dri2
        dri3
        glx
        present
        randr
        record
        render
        res
        screensaver
        shape
        shm
        sync
        xf86dri
        xfixes
        xinerama
        xinput
        xkb
        xtest
        xv
        xvmc
)

foreach (component ${PROJECT_COMPONENTS})
    add_library(${PROJECT_NAME}-${component} src/${component}.c)
    target_include_directories(${PROJECT_NAME}-${component} PRIVATE include/xcb)
    set_target_properties(${PROJECT_NAME}-${component} PROPERTIES POSITION_INDEPENDENT_CODE TRUE)
    install(TARGETS ${PROJECT_NAME}-${component} COMPONENT ${PROJECT_NAME})
endforeach ()

set(PROJECT_SOURCES
        src/xcb_conn.c
        src/xcb_out.c
        src/xcb_in.c
        src/xcb_ext.c
        src/xcb_xid.c
        src/xcb_list.c
        src/xcb_util.c
        src/xcb_auth.c
        src/xproto.c
        src/bigreq.c
        src/xc_misc.c
)

add_library(${PROJECT_NAME} ${PROJECT_SOURCES})

target_include_directories(${PROJECT_NAME} PUBLIC include PRIVATE ${CMAKE_CURRENT_BINARY_DIR}/include include-private include/xcb)

target_link_libraries(${PROJECT_NAME} Xau
        ${PROJECT_NAME}-composite ${PROJECT_NAME}-damage ${PROJECT_NAME}-dbe ${PROJECT_NAME}-dpms ${PROJECT_NAME}-dri2
        ${PROJECT_NAME}-dri3 ${PROJECT_NAME}-glx ${PROJECT_NAME}-present ${PROJECT_NAME}-randr ${PROJECT_NAME}-record
        ${PROJECT_NAME}-render ${PROJECT_NAME}-res ${PROJECT_NAME}-screensaver ${PROJECT_NAME}-shape ${PROJECT_NAME}-shm
        ${PROJECT_NAME}-sync ${PROJECT_NAME}-xf86dri ${PROJECT_NAME}-xfixes ${PROJECT_NAME}-xinerama ${PROJECT_NAME}-xinput
        ${PROJECT_NAME}-xkb ${PROJECT_NAME}-xtest ${PROJECT_NAME}-xv ${PROJECT_NAME}-xvmc
)

set_target_properties(${PROJECT_NAME} PROPERTIES POSITION_INDEPENDENT_CODE TRUE)

target_compile_definitions(${PROJECT_NAME} PRIVATE HAVE_CONFIG_H)
target_compile_options(${PROJECT_NAME} PRIVATE -Wno-unused-result)

install(TARGETS ${PROJECT_NAME} COMPONENT ${PROJECT_NAME})
install(DIRECTORY include/ DESTINATION include COMPONENT ${PROJECT_NAME})
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/ DESTINATION lib/pkgconfig COMPONENT ${PROJECT_NAME})
