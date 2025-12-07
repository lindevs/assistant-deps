cmake_minimum_required(VERSION 3.28)
project(webp VERSION 1.6.0 LANGUAGES C)

set(CMAKE_C_STANDARD 99)

option(WEBP_NEAR_LOSSLESS "Enable near-lossless encoding" ON)
option(WEBP_USE_THREAD "Enable threading support" ON)

set(CMAKE_REQUIRED_QUIET TRUE)
include(CheckIncludeFile)
include(CheckSourceCompiles)

check_include_file(GLUT/glut.h HAVE_GLUT_GLUT_H)
check_include_file(unistd.h HAVE_UNISTD_H)
check_include_file(wincodec.h HAVE_WINCODEC_H)
check_source_compiles(C "int main(void) {(void)__builtin_bswap16(0);return 0;}" HAVE_BUILTIN_BSWAP16)
check_source_compiles(C "int main(void) {(void)__builtin_bswap32(0);return 0;}" HAVE_BUILTIN_BSWAP32)
check_source_compiles(C "int main(void) {(void)__builtin_bswap64(0);return 0;}" HAVE_BUILTIN_BSWAP64)

if (CMAKE_SYSTEM_PROCESSOR MATCHES "x64|x86_64|AMD64|amd64")
    set(WEBP_HAVE_SSE2 1)
    set(WEBP_HAVE_SSE41 1)
    set(WEBP_HAVE_AVX2 1)
elseif (CMAKE_SYSTEM_PROCESSOR MATCHES "aarch64|ARM64|arm64")
    set(WEBP_HAVE_NEON 1)
endif ()

configure_file(config/config.h.in "${CMAKE_CURRENT_BINARY_DIR}/include/webp/config.h" @ONLY)

set(PROJECT_SSE_SOURCES
        src/dsp/alpha_processing_sse41.c
        src/dsp/dec_sse41.c
        src/dsp/enc_sse41.c
        src/dsp/lossless_enc_sse41.c
        src/dsp/lossless_sse41.c
        src/dsp/upsampling_sse41.c
        src/dsp/yuv_sse41.c
)

set(PROJECT_AVX2_SOURCES
        src/dsp/lossless_avx2.c
        src/dsp/lossless_enc_avx2.c
)

set(PROJECT_SHARPYUV_SOURCES
        src/sharpyuv/sharpyuv.c
        src/sharpyuv/sharpyuv_cpu.c
        src/sharpyuv/sharpyuv_csp.c
        src/sharpyuv/sharpyuv_dsp.c
        src/sharpyuv/sharpyuv_gamma.c
        src/sharpyuv/sharpyuv_neon.c
        src/sharpyuv/sharpyuv_sse2.c
)

set(PROJECT_MUX_SOURCES
        src/mux/anim_encode.c
        src/mux/muxedit.c
        src/mux/muxinternal.c
        src/mux/muxread.c
)

set(PROJECT_DEMUX_SOURCES
        src/demux/anim_decode.c
        src/demux/demux.c
)

set(PROJECT_DECODER_SOURCES
        src/dec/alpha_dec.c
        src/dec/buffer_dec.c
        src/dec/frame_dec.c
        src/dec/idec_dec.c
        src/dec/io_dec.c
        src/dec/quant_dec.c
        src/dec/tree_dec.c
        src/dec/vp8_dec.c
        src/dec/vp8l_dec.c
        src/dec/webp_dec.c
        src/utils/bit_reader_utils.c
        src/utils/color_cache_utils.c
        src/utils/filters_utils.c
        src/utils/huffman_utils.c
        src/utils/palette.c
        src/utils/quant_levels_dec_utils.c
        src/utils/random_utils.c
        src/utils/rescaler_utils.c
        src/utils/thread_utils.c
        src/utils/utils.c
        src/dsp/alpha_processing.c
        src/dsp/alpha_processing_mips_dsp_r2.c
        src/dsp/cpu.c
        src/dsp/dec.c
        src/dsp/dec_clip_tables.c
        src/dsp/dec_mips32.c
        src/dsp/dec_mips_dsp_r2.c
        src/dsp/dec_msa.c
        src/dsp/filters.c
        src/dsp/filters_mips_dsp_r2.c
        src/dsp/filters_msa.c
        src/dsp/lossless.c
        src/dsp/lossless_mips_dsp_r2.c
        src/dsp/lossless_msa.c
        src/dsp/rescaler.c
        src/dsp/rescaler_mips32.c
        src/dsp/rescaler_mips_dsp_r2.c
        src/dsp/rescaler_msa.c
        src/dsp/upsampling.c
        src/dsp/upsampling_mips_dsp_r2.c
        src/dsp/upsampling_msa.c
        src/dsp/yuv.c
        src/dsp/yuv_mips32.c
        src/dsp/yuv_mips_dsp_r2.c
        src/dsp/alpha_processing_sse2.c
        src/dsp/dec_sse2.c
        src/dsp/filters_sse2.c
        src/dsp/lossless_sse2.c
        src/dsp/rescaler_sse2.c
        src/dsp/upsampling_sse2.c
        src/dsp/yuv_sse2.c
        src/dsp/alpha_processing_neon.c
        src/dsp/dec_neon.c
        src/dsp/filters_neon.c
        src/dsp/lossless_neon.c
        src/dsp/rescaler_neon.c
        src/dsp/upsampling_neon.c
        src/dsp/yuv_neon.c
        src/dsp/alpha_processing_sse41.c
        src/dsp/dec_sse41.c
        src/dsp/lossless_sse41.c
        src/dsp/upsampling_sse41.c
        src/dsp/yuv_sse41.c
        src/dsp/lossless_avx2.c
)

set(PROJECT_SOURCES
        src/enc/alpha_enc.c
        src/enc/analysis_enc.c
        src/enc/backward_references_cost_enc.c
        src/enc/backward_references_enc.c
        src/enc/config_enc.c
        src/enc/cost_enc.c
        src/enc/filter_enc.c
        src/enc/frame_enc.c
        src/enc/histogram_enc.c
        src/enc/iterator_enc.c
        src/enc/near_lossless_enc.c
        src/enc/picture_csp_enc.c
        src/enc/picture_enc.c
        src/enc/picture_psnr_enc.c
        src/enc/picture_rescale_enc.c
        src/enc/picture_tools_enc.c
        src/enc/predictor_enc.c
        src/enc/quant_enc.c
        src/enc/syntax_enc.c
        src/enc/token_enc.c
        src/enc/tree_enc.c
        src/enc/vp8l_enc.c
        src/enc/webp_enc.c
        src/dec/alpha_dec.c
        src/dec/buffer_dec.c
        src/dec/frame_dec.c
        src/dec/idec_dec.c
        src/dec/io_dec.c
        src/dec/quant_dec.c
        src/dec/tree_dec.c
        src/dec/vp8_dec.c
        src/dec/vp8l_dec.c
        src/dec/webp_dec.c
        src/utils/bit_reader_utils.c
        src/utils/bit_writer_utils.c
        src/utils/color_cache_utils.c
        src/utils/filters_utils.c
        src/utils/huffman_encode_utils.c
        src/utils/huffman_utils.c
        src/utils/palette.c
        src/utils/quant_levels_dec_utils.c
        src/utils/quant_levels_utils.c
        src/utils/random_utils.c
        src/utils/rescaler_utils.c
        src/utils/thread_utils.c
        src/utils/utils.c
        src/dsp/alpha_processing.c
        src/dsp/alpha_processing_mips_dsp_r2.c
        src/dsp/cost.c
        src/dsp/cost_mips32.c
        src/dsp/cost_mips_dsp_r2.c
        src/dsp/cpu.c
        src/dsp/dec.c
        src/dsp/dec_clip_tables.c
        src/dsp/dec_mips32.c
        src/dsp/dec_mips_dsp_r2.c
        src/dsp/dec_msa.c
        src/dsp/enc.c
        src/dsp/enc_mips32.c
        src/dsp/enc_mips_dsp_r2.c
        src/dsp/enc_msa.c
        src/dsp/filters.c
        src/dsp/filters_mips_dsp_r2.c
        src/dsp/filters_msa.c
        src/dsp/lossless.c
        src/dsp/lossless_enc.c
        src/dsp/lossless_enc_mips32.c
        src/dsp/lossless_enc_mips_dsp_r2.c
        src/dsp/lossless_enc_msa.c
        src/dsp/lossless_mips_dsp_r2.c
        src/dsp/lossless_msa.c
        src/dsp/rescaler.c
        src/dsp/rescaler_mips32.c
        src/dsp/rescaler_mips_dsp_r2.c
        src/dsp/rescaler_msa.c
        src/dsp/ssim.c
        src/dsp/upsampling.c
        src/dsp/upsampling_mips_dsp_r2.c
        src/dsp/upsampling_msa.c
        src/dsp/yuv.c
        src/dsp/yuv_mips32.c
        src/dsp/yuv_mips_dsp_r2.c
        src/dsp/alpha_processing_sse2.c
        src/dsp/cost_sse2.c
        src/dsp/dec_sse2.c
        src/dsp/enc_sse2.c
        src/dsp/filters_sse2.c
        src/dsp/lossless_enc_sse2.c
        src/dsp/lossless_sse2.c
        src/dsp/rescaler_sse2.c
        src/dsp/ssim_sse2.c
        src/dsp/upsampling_sse2.c
        src/dsp/yuv_sse2.c
        src/dsp/alpha_processing_neon.c
        src/dsp/cost_neon.c
        src/dsp/dec_neon.c
        src/dsp/enc_neon.c
        src/dsp/filters_neon.c
        src/dsp/lossless_enc_neon.c
        src/dsp/lossless_neon.c
        src/dsp/rescaler_neon.c
        src/dsp/upsampling_neon.c
        src/dsp/yuv_neon.c
)

list(APPEND PROJECT_SOURCES ${PROJECT_SSE_SOURCES} ${PROJECT_AVX2_SOURCES})

if (CMAKE_SYSTEM_PROCESSOR MATCHES "x64|x86_64|AMD64|amd64")
    set_source_files_properties(${PROJECT_SSE_SOURCES} PROPERTIES COMPILE_OPTIONS -msse4.1)
    set_source_files_properties(${PROJECT_AVX2_SOURCES} PROPERTIES COMPILE_OPTIONS -mavx2)
endif ()

add_library(sharpyuv ${PROJECT_SHARPYUV_SOURCES})
add_library(${PROJECT_NAME}mux ${PROJECT_MUX_SOURCES})
add_library(${PROJECT_NAME}demux ${PROJECT_DEMUX_SOURCES})
add_library(${PROJECT_NAME}decoder ${PROJECT_DECODER_SOURCES})
add_library(${PROJECT_NAME} ${PROJECT_SOURCES})

target_include_directories(sharpyuv PUBLIC include PRIVATE include/webp include-private ${CMAKE_CURRENT_BINARY_DIR}/include src)
target_include_directories(${PROJECT_NAME}mux PUBLIC include PRIVATE include/webp include-private ${CMAKE_CURRENT_BINARY_DIR}/include)
target_include_directories(${PROJECT_NAME}demux PUBLIC include PRIVATE include/webp include-private ${CMAKE_CURRENT_BINARY_DIR}/include)
target_include_directories(${PROJECT_NAME}decoder PUBLIC include PRIVATE include/webp include-private ${CMAKE_CURRENT_BINARY_DIR}/include)
target_include_directories(${PROJECT_NAME} PUBLIC include PRIVATE include/webp include-private ${CMAKE_CURRENT_BINARY_DIR}/include)

target_link_libraries(${PROJECT_NAME} sharpyuv ${PROJECT_NAME}mux ${PROJECT_NAME}demux ${PROJECT_NAME}decoder)

set_target_properties(sharpyuv PROPERTIES POSITION_INDEPENDENT_CODE TRUE)
set_target_properties(sharpyuv PROPERTIES C_VISIBILITY_PRESET hidden)
set_target_properties(${PROJECT_NAME}mux PROPERTIES POSITION_INDEPENDENT_CODE TRUE)
set_target_properties(${PROJECT_NAME}mux PROPERTIES C_VISIBILITY_PRESET hidden)
set_target_properties(${PROJECT_NAME}demux PROPERTIES POSITION_INDEPENDENT_CODE TRUE)
set_target_properties(${PROJECT_NAME}demux PROPERTIES C_VISIBILITY_PRESET hidden)
set_target_properties(${PROJECT_NAME}decoder PROPERTIES POSITION_INDEPENDENT_CODE TRUE)
set_target_properties(${PROJECT_NAME}decoder PROPERTIES C_VISIBILITY_PRESET hidden)
set_target_properties(${PROJECT_NAME} PROPERTIES POSITION_INDEPENDENT_CODE TRUE)
set_target_properties(${PROJECT_NAME} PROPERTIES C_VISIBILITY_PRESET hidden)

target_compile_definitions(sharpyuv PRIVATE HAVE_CONFIG_H)
target_compile_definitions(${PROJECT_NAME}mux PRIVATE HAVE_CONFIG_H)
target_compile_definitions(${PROJECT_NAME}demux PRIVATE HAVE_CONFIG_H)
target_compile_definitions(${PROJECT_NAME}decoder PRIVATE HAVE_CONFIG_H)
target_compile_definitions(${PROJECT_NAME} PRIVATE HAVE_CONFIG_H)

install(TARGETS sharpyuv COMPONENT ${PROJECT_NAME})
install(TARGETS ${PROJECT_NAME}mux COMPONENT ${PROJECT_NAME})
install(TARGETS ${PROJECT_NAME}demux COMPONENT ${PROJECT_NAME})
install(TARGETS ${PROJECT_NAME}decoder COMPONENT ${PROJECT_NAME})
install(TARGETS ${PROJECT_NAME} COMPONENT ${PROJECT_NAME})
install(DIRECTORY include/ DESTINATION include COMPONENT ${PROJECT_NAME})
