cmake_minimum_required(VERSION 3.28)
project(png VERSION 1.6.50 LANGUAGES C)

set(CMAKE_C_STANDARD 99)

set(CMAKE_REQUIRED_QUIET TRUE)
include(CheckSourceCompiles)

set(PROJECT_INTEL_SOURCES
        src/intel/filter_sse2_intrinsics.c
        src/intel/intel_init.c
)

set(PROJECT_ARM_SOURCES
        src/arm/arm_init.c
        src/arm/filter_neon_intrinsics.c
        src/arm/palette_neon_intrinsics.c
)

set(PROJECT_MIPS_SOURCES
        src/mips/mips_init.c
        src/mips/filter_msa_intrinsics.c
        src/mips/filter_mmi_inline_assembly.c
)

set(PROJECT_POWERPC_SOURCES
        src/powerpc/powerpc_init.c
        src/powerpc/filter_vsx_intrinsics.c
)

set(PROJECT_LOONGARCH_SOURCES
        src/loongarch/loongarch_lsx_init.c
        src/loongarch/filter_lsx_intrinsics.c
)

set(PROJECT_RISCV_SOURCES
        src/riscv/filter_rvv_intrinsics.c
        src/riscv/riscv_init.c
)

set(PROJECT_SOURCES
        src/png.c
        src/pngerror.c
        src/pngget.c
        src/pngmem.c
        src/pngpread.c
        src/pngread.c
        src/pngrio.c
        src/pngrtran.c
        src/pngrutil.c
        src/pngset.c
        src/pngtrans.c
        src/pngwio.c
        src/pngwrite.c
        src/pngwtran.c
        src/pngwutil.c
)

if (CMAKE_SYSTEM_PROCESSOR MATCHES "^(i[3-6]86|x86|amd64)")
    list(APPEND PROJECT_SOURCES ${PROJECT_INTEL_SOURCES})
    set(PNG_OPTIMIZATION PNG_INTEL_SSE_OPT=1)
elseif (CMAKE_SYSTEM_PROCESSOR MATCHES "^(arm64|aarch64)")
    list(APPEND PROJECT_SOURCES ${PROJECT_ARM_SOURCES})
    set(PNG_OPTIMIZATION PNG_ARM_NEON_OPT=1)
elseif (CMAKE_SYSTEM_PROCESSOR MATCHES "^(mipsel|mips64el)")
    list(APPEND PROJECT_SOURCES ${PROJECT_MIPS_SOURCES})
    set(PNG_OPTIMIZATION PNG_MIPS_MSA_OPT=2 PNG_MIPS_MMI_OPT=1)
elseif (CMAKE_SYSTEM_PROCESSOR MATCHES "^(powerpc|ppc64)")
    list(APPEND PROJECT_SOURCES ${PROJECT_POWERPC_SOURCES})
    set(PNG_OPTIMIZATION PNG_POWERPC_VSX_OPT=2)
elseif (CMAKE_SYSTEM_PROCESSOR MATCHES "^(loongarch)")
    list(APPEND PROJECT_SOURCES ${PROJECT_LOONGARCH_SOURCES})
    set(PNG_OPTIMIZATION PNG_LOONGARCH_LSX_OPT=1)
    set_source_files_properties(${PROJECT_LOONGARCH_SOURCES} PROPERTIES COMPILE_OPTIONS "-mlsx")
elseif (CMAKE_SYSTEM_PROCESSOR MATCHES "^(riscv)")
    check_source_compiles(C "
        #include <riscv_vector.h>
        #include <asm/hwcap.h>
        #ifndef COMPAT_HWCAP_ISA_V
        #error \"COMPAT_HWCAP_ISA_V is not available\"
        #endif
        int main() {
          const float src[] = { 0.0f, 0.0f, 0.0f, 0.0f };
          uint64_t ptr[2] = {0x0908060504020100, 0xFFFFFFFF0E0D0C0A};
          vuint8m1_t a = __riscv_vreinterpret_v_u64m1_u8m1(__riscv_vle64_v_u64m1(ptr, 2));
          vfloat32m1_t val = __riscv_vle32_v_f32m1((const float*)(src), 4);
          return (int)__riscv_vfmv_f_s_f32m1_f32(val);
      }" COMPILER_SUPPORTS_RVV)
    if (COMPILER_SUPPORTS_RVV)
        list(APPEND PROJECT_SOURCES ${PROJECT_RISCV_SOURCES})
        set(PNG_OPTIMIZATION PNG_RISCV_RVV_OPT=2)
    endif ()
endif ()

add_library(${PROJECT_NAME} ${PROJECT_SOURCES})

target_include_directories(${PROJECT_NAME} PUBLIC include PRIVATE include-private)

target_link_libraries(${PROJECT_NAME} z)

set_target_properties(${PROJECT_NAME} PROPERTIES POSITION_INDEPENDENT_CODE TRUE)

target_compile_definitions(${PROJECT_NAME} PRIVATE ${PNG_OPTIMIZATION})

install(TARGETS ${PROJECT_NAME} COMPONENT ${PROJECT_NAME})
install(DIRECTORY include/ DESTINATION include COMPONENT ${PROJECT_NAME})
