cmake_minimum_required(VERSION 3.28)
project(ffi VERSION 3.5.2 LANGUAGES C ASM)

set(CMAKE_C_STANDARD 11)

set(CMAKE_REQUIRED_QUIET TRUE)
include(CheckIncludeFile)
include(CheckFunctionExists)
include(CheckTypeSize)
include(CheckSourceCompiles)
include(CMakePushCheckState)

set(VERSION ${PROJECT_VERSION})
set(FFI_VERSION_STRING ${PROJECT_VERSION})
set(FFI_VERSION_NUMBER ${PROJECT_VERSION_MAJOR}0${PROJECT_VERSION_MINOR}0${PROJECT_VERSION_PATCH})
set(FFI_EXEC_TRAMPOLINE_TABLE 0)
set(FFI_EXEC_STATIC_TRAMP 1)
set(FFI_EXEC_LIB_DIR /../lib)

check_include_file(alloca.h HAVE_ALLOCA_H)
check_include_file(sys/memfd.h HAVE_SYS_MEMFD_H)
check_function_exists(memfd_create HAVE_MEMFD_CREATE)

check_source_compiles(C [=[
int foo(void) {
  __asm__(
      ".cfi_remember_state\n\t"
      ".cfi_restore_state\n\t"
  );
  return 0;
}
int main(void) { return foo(); }
]=] HAVE_AS_CFI_PSEUDO_OP)

check_source_compiles(C [=[
int __attribute__((visibility("hidden"))) foo(void) { return 1; }
int main(void) { return foo(); }
]=] HAVE_HIDDEN_VISIBILITY_ATTRIBUTE)

check_type_size("long double" SIZEOF_LONG_DOUBLE)
if (HAVE_SIZEOF_LONG_DOUBLE)
    set(HAVE_LONG_DOUBLE 1)
endif ()

if (CMAKE_SYSTEM_PROCESSOR MATCHES "x64|x86_64|AMD64|amd64")
    set(TARGET X86_64)
elseif (CMAKE_SYSTEM_PROCESSOR MATCHES "aarch64|ARM64|arm64")
    set(TARGET AARCH64)
elseif (CMAKE_SYSTEM_PROCESSOR MATCHES "riscv")
    set(TARGET RISCV)
endif ()

if (${TARGET} STREQUAL X86_64)
    cmake_push_check_state(RESET)
    set(CMAKE_REQUIRED_QUIET TRUE)
    set(CMAKE_REQUIRED_FLAGS "-Wa,--fatal-warnings")
    check_source_compiles(C [=[
    __asm__(
        ".text\n\t"
        ".globl foo\n\t"
        "foo:\n\t"
        "jmp bar\n\t"
        ".section .eh_frame,\"a\",@unwind\n\t"
        "bar:\n\t"
        ".text\n\t"
    );
    int main(void) { return 0; }
    ]=] HAVE_AS_X86_64_UNWIND_SECTION_TYPE)
    cmake_pop_check_state()

    check_source_compiles(C [=[
    __asm__(
        ".text\n\t"
        "foo: nop\n\t"
        ".data\n\t"
        ".long foo-.\n\t"
        ".text\n\t"
    );
    int main(void) { return 0; }
    ]=] HAVE_AS_X86_PCREL)
elseif (${TARGET} STREQUAL RISCV)
    set(FFI_EXEC_STATIC_TRAMP 0)
    set(FFI_EXEC_LIB_DIR "")
endif ()

configure_file(config/fficonfig-cmake.h.in "${CMAKE_CURRENT_BINARY_DIR}/include-private/fficonfig.h" @ONLY)
configure_file(config/ffi.h.in "${CMAKE_CURRENT_BINARY_DIR}/include/ffi.h" @ONLY)
configure_file(pkgconfig/libffi.pc.in "${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/libffi.pc" @ONLY)

set(PROJECT_X86_64_SOURCES
        src/x86/ffi64.c
        src/x86/ffiw64.c
        src/x86/unix64.S
        src/x86/win64.S
)

set(PROJECT_AARCH64_SOURCES
        src/aarch64/ffi.c
        src/aarch64/sysv.S
)

set(PROJECT_RISCV_SOURCES
        src/riscv/ffi.c
        src/riscv/sysv.S
)

set(PROJECT_SOURCES
        src/prep_cif.c
        src/types.c
        src/raw_api.c
        src/java_raw_api.c
        src/closures.c
        src/tramp.c
)

if (${TARGET} STREQUAL X86_64)
    list(APPEND PROJECT_SOURCES ${PROJECT_X86_64_SOURCES})
    set(TARGET_INCLUDE include/x86)
    set(TARGET_PRIVATE_INCLUDE include-private/x86)
elseif (${TARGET} STREQUAL AARCH64)
    list(APPEND PROJECT_SOURCES ${PROJECT_AARCH64_SOURCES})
    set(TARGET_INCLUDE include/aarch64)
    set(TARGET_PRIVATE_INCLUDE include-private/aarch64)
elseif (${TARGET} STREQUAL RISCV)
    list(APPEND PROJECT_SOURCES ${PROJECT_RISCV_SOURCES})
    set(TARGET_INCLUDE include/riscv)
    set(TARGET_PRIVATE_INCLUDE include-private/riscv)
endif ()

add_library(${PROJECT_NAME} ${PROJECT_SOURCES})

target_include_directories(${PROJECT_NAME}
        PUBLIC ${TARGET_INCLUDE} ${CMAKE_CURRENT_BINARY_DIR}/include
        PRIVATE ${TARGET_PRIVATE_INCLUDE} include-private ${CMAKE_CURRENT_BINARY_DIR}/include-private
)

target_compile_options(${PROJECT_NAME} PRIVATE -fomit-frame-pointer -fexceptions -Wno-deprecated-declarations)

install(TARGETS ${PROJECT_NAME} COMPONENT ${PROJECT_NAME})
install(DIRECTORY ${TARGET_INCLUDE}/ DESTINATION include COMPONENT ${PROJECT_NAME})
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/include/ DESTINATION include COMPONENT ${PROJECT_NAME})
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/ DESTINATION lib/pkgconfig COMPONENT ${PROJECT_NAME})
