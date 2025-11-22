cmake_minimum_required(VERSION 3.28)
project(xorgproto C)

set(CMAKE_C_STANDARD 99)

set(CMAKE_REQUIRED_QUIET TRUE)
include(CheckStructHasMember)

set(FD_SET_HEADERS "sys/param.h;sys/types.h;sys/time.h;sys/select.h")
check_struct_has_member(fd_set fds_bits "${FD_SET_HEADERS}" HAVE_FD_SET_FDS_BITS)
check_struct_has_member(fd_set __fds_bits "${FD_SET_HEADERS}" HAVE_FD_SET___FDS_BITS)

if (HAVE_FD_SET_FDS_BITS)
    set(USE_FDS_BITS fds_bits)
elseif (HAVE_FD_SET___FDS_BITS)
    set(USE_FDS_BITS __fds_bits)
else ()
    message(FATAL_ERROR "fd_set not found in the headers.")
endif ()

configure_file(config/Xpoll.h.in "${CMAKE_CURRENT_BINARY_DIR}/include/X11/Xpoll.h" @ONLY)

set(PKGCONFIG_FILES
        pkgconfig/applewmproto
        pkgconfig/bigreqsproto
        pkgconfig/compositeproto
        pkgconfig/damageproto
        pkgconfig/dmxproto
        pkgconfig/dpmsproto
        pkgconfig/dri2proto
        pkgconfig/dri3proto
        pkgconfig/fixesproto
        pkgconfig/fontsproto
        pkgconfig/glproto
        pkgconfig/inputproto
        pkgconfig/kbproto
        pkgconfig/presentproto
        pkgconfig/randrproto
        pkgconfig/recordproto
        pkgconfig/renderproto
        pkgconfig/resourceproto
        pkgconfig/scrnsaverproto
        pkgconfig/videoproto
        pkgconfig/xcmiscproto
        pkgconfig/xextproto
        pkgconfig/xf86bigfontproto
        pkgconfig/xf86dgaproto
        pkgconfig/xf86driproto
        pkgconfig/xf86vidmodeproto
        pkgconfig/xineramaproto
        pkgconfig/xproto
        pkgconfig/xwaylandproto
)

foreach (pkgconfig_file ${PKGCONFIG_FILES})
    configure_file(${pkgconfig_file}.pc.in "${CMAKE_CURRENT_BINARY_DIR}/${pkgconfig_file}.pc" @ONLY)
endforeach ()

add_library(${PROJECT_NAME} INTERFACE)

target_include_directories(${PROJECT_NAME} INTERFACE include ${CMAKE_CURRENT_BINARY_DIR}/include)

install(DIRECTORY include/ DESTINATION include COMPONENT ${PROJECT_NAME})
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/include/ DESTINATION include COMPONENT ${PROJECT_NAME})
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/ DESTINATION share/pkgconfig COMPONENT ${PROJECT_NAME})
