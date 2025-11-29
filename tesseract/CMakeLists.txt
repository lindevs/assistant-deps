cmake_minimum_required(VERSION 3.28)
project(tesseract VERSION 5.5.1 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)

option(GRAPHICS_DISABLED "Disable graphics (ScrollView)" OFF)
option(FAST_FLOAT "Enable float for LSTM" ON)
option(DISABLED_LEGACY_ENGINE "Disable the legacy OCR engine" OFF)

configure_file(config/version.h.in "${CMAKE_CURRENT_BINARY_DIR}/include/tesseract/version.h" @ONLY)
configure_file(config/config_auto.h.in "${CMAKE_CURRENT_BINARY_DIR}/include-private/config_auto.h" @ONLY)

set(PROJECT_AVX_SOURCES
        src/arch/dotproductavx.cpp
)

set(PROJECT_AVX2_SOURCES
        src/arch/intsimdmatrixavx2.cpp
)

set(PROJECT_AVX512_SOURCES
        src/arch/dotproductavx512.cpp
)

set(PROJECT_FMA_SOURCES
        src/arch/dotproductfma.cpp
)

set(PROJECT_SSE_SOURCES
        src/arch/dotproductsse.cpp
        src/arch/intsimdmatrixsse.cpp
)

set(PROJECT_NEON_SOURCES
        src/arch/dotproductneon.cpp
        src/arch/intsimdmatrixneon.cpp
)

set(PROJECT_SOURCES
        src/api/altorenderer.cpp
        src/api/baseapi.cpp
        src/api/capi.cpp
        src/api/hocrrenderer.cpp
        src/api/lstmboxrenderer.cpp
        src/api/pagerenderer.cpp
        src/api/pdfrenderer.cpp
        src/api/renderer.cpp
        src/api/wordstrboxrenderer.cpp
        src/arch/dotproduct.cpp
        src/arch/intsimdmatrix.cpp
        src/arch/simddetect.cpp
        src/ccmain/adaptions.cpp
        src/ccmain/applybox.cpp
        src/ccmain/control.cpp
        src/ccmain/docqual.cpp
        src/ccmain/equationdetect.cpp
        src/ccmain/fixspace.cpp
        src/ccmain/fixxht.cpp
        src/ccmain/linerec.cpp
        src/ccmain/ltrresultiterator.cpp
        src/ccmain/mutableiterator.cpp
        src/ccmain/osdetect.cpp
        src/ccmain/output.cpp
        src/ccmain/pageiterator.cpp
        src/ccmain/pagesegmain.cpp
        src/ccmain/pagewalk.cpp
        src/ccmain/par_control.cpp
        src/ccmain/paragraphs.cpp
        src/ccmain/paramsd.cpp
        src/ccmain/pgedit.cpp
        src/ccmain/recogtraining.cpp
        src/ccmain/reject.cpp
        src/ccmain/resultiterator.cpp
        src/ccmain/superscript.cpp
        src/ccmain/tessbox.cpp
        src/ccmain/tessedit.cpp
        src/ccmain/tesseractclass.cpp
        src/ccmain/tessvars.cpp
        src/ccmain/tfacepp.cpp
        src/ccmain/thresholder.cpp
        src/ccmain/werdit.cpp
        src/ccstruct/blamer.cpp
        src/ccstruct/blobbox.cpp
        src/ccstruct/blobs.cpp
        src/ccstruct/blread.cpp
        src/ccstruct/boxread.cpp
        src/ccstruct/boxword.cpp
        src/ccstruct/ccstruct.cpp
        src/ccstruct/coutln.cpp
        src/ccstruct/detlinefit.cpp
        src/ccstruct/dppoint.cpp
        src/ccstruct/fontinfo.cpp
        src/ccstruct/image.cpp
        src/ccstruct/imagedata.cpp
        src/ccstruct/linlsq.cpp
        src/ccstruct/matrix.cpp
        src/ccstruct/mod128.cpp
        src/ccstruct/normalis.cpp
        src/ccstruct/ocrblock.cpp
        src/ccstruct/ocrpara.cpp
        src/ccstruct/ocrrow.cpp
        src/ccstruct/otsuthr.cpp
        src/ccstruct/pageres.cpp
        src/ccstruct/params_training_featdef.cpp
        src/ccstruct/pdblock.cpp
        src/ccstruct/points.cpp
        src/ccstruct/polyaprx.cpp
        src/ccstruct/polyblk.cpp
        src/ccstruct/quadlsq.cpp
        src/ccstruct/quspline.cpp
        src/ccstruct/ratngs.cpp
        src/ccstruct/rect.cpp
        src/ccstruct/rejctmap.cpp
        src/ccstruct/seam.cpp
        src/ccstruct/split.cpp
        src/ccstruct/statistc.cpp
        src/ccstruct/stepblob.cpp
        src/ccstruct/werd.cpp
        src/ccutil/ambigs.cpp
        src/ccutil/bitvector.cpp
        src/ccutil/ccutil.cpp
        src/ccutil/errcode.cpp
        src/ccutil/indexmapbidi.cpp
        src/ccutil/params.cpp
        src/ccutil/scanutils.cpp
        src/ccutil/serialis.cpp
        src/ccutil/tessdatamanager.cpp
        src/ccutil/tprintf.cpp
        src/ccutil/unichar.cpp
        src/ccutil/unicharcompress.cpp
        src/ccutil/unicharmap.cpp
        src/ccutil/unicharset.cpp
        src/classify/adaptive.cpp
        src/classify/adaptmatch.cpp
        src/classify/blobclass.cpp
        src/classify/classify.cpp
        src/classify/cluster.cpp
        src/classify/clusttool.cpp
        src/classify/cutoffs.cpp
        src/classify/featdefs.cpp
        src/classify/float2int.cpp
        src/classify/fpoint.cpp
        src/classify/intfeaturespace.cpp
        src/classify/intfx.cpp
        src/classify/intmatcher.cpp
        src/classify/intproto.cpp
        src/classify/kdtree.cpp
        src/classify/mf.cpp
        src/classify/mfoutline.cpp
        src/classify/mfx.cpp
        src/classify/normfeat.cpp
        src/classify/normmatch.cpp
        src/classify/ocrfeatures.cpp
        src/classify/outfeat.cpp
        src/classify/picofeat.cpp
        src/classify/protos.cpp
        src/classify/shapeclassifier.cpp
        src/classify/shapetable.cpp
        src/classify/tessclassifier.cpp
        src/classify/trainingsample.cpp
        src/cutil/oldlist.cpp
        src/dict/context.cpp
        src/dict/dawg.cpp
        src/dict/dawg_cache.cpp
        src/dict/dict.cpp
        src/dict/hyphen.cpp
        src/dict/permdawg.cpp
        src/dict/stopper.cpp
        src/dict/trie.cpp
        src/lstm/convolve.cpp
        src/lstm/fullyconnected.cpp
        src/lstm/functions.cpp
        src/lstm/generate_lut.py
        src/lstm/input.cpp
        src/lstm/lstm.cpp
        src/lstm/lstmrecognizer.cpp
        src/lstm/maxpool.cpp
        src/lstm/network.cpp
        src/lstm/networkio.cpp
        src/lstm/parallel.cpp
        src/lstm/plumbing.cpp
        src/lstm/recodebeam.cpp
        src/lstm/reconfig.cpp
        src/lstm/reversed.cpp
        src/lstm/series.cpp
        src/lstm/stridemap.cpp
        src/lstm/weightmatrix.cpp
        src/textord/alignedblob.cpp
        src/textord/baselinedetect.cpp
        src/textord/bbgrid.cpp
        src/textord/blkocc.cpp
        src/textord/blobgrid.cpp
        src/textord/ccnontextdetect.cpp
        src/textord/cjkpitch.cpp
        src/textord/colfind.cpp
        src/textord/colpartition.cpp
        src/textord/colpartitiongrid.cpp
        src/textord/colpartitionset.cpp
        src/textord/devanagari_processing.cpp
        src/textord/drawtord.cpp
        src/textord/edgblob.cpp
        src/textord/edgloop.cpp
        src/textord/equationdetectbase.cpp
        src/textord/fpchop.cpp
        src/textord/gap_map.cpp
        src/textord/imagefind.cpp
        src/textord/linefind.cpp
        src/textord/makerow.cpp
        src/textord/oldbasel.cpp
        src/textord/pithsync.cpp
        src/textord/pitsync1.cpp
        src/textord/scanedg.cpp
        src/textord/sortflts.cpp
        src/textord/strokewidth.cpp
        src/textord/tabfind.cpp
        src/textord/tablefind.cpp
        src/textord/tablerecog.cpp
        src/textord/tabvector.cpp
        src/textord/textlineprojection.cpp
        src/textord/textord.cpp
        src/textord/topitch.cpp
        src/textord/tordmain.cpp
        src/textord/tospace.cpp
        src/textord/tovars.cpp
        src/textord/underlin.cpp
        src/textord/wordseg.cpp
        src/textord/workingpartset.cpp
        src/viewer/scrollview.cpp
        src/viewer/svmnode.cpp
        src/viewer/svutil.cpp
        src/wordrec/associate.cpp
        src/wordrec/chop.cpp
        src/wordrec/chopper.cpp
        src/wordrec/drawfx.cpp
        src/wordrec/findseam.cpp
        src/wordrec/gradechop.cpp
        src/wordrec/language_model.cpp
        src/wordrec/lm_consistency.cpp
        src/wordrec/lm_pain_points.cpp
        src/wordrec/lm_state.cpp
        src/wordrec/outlines.cpp
        src/wordrec/params_model.cpp
        src/wordrec/pieces.cpp
        src/wordrec/plotedges.cpp
        src/wordrec/render.cpp
        src/wordrec/segsearch.cpp
        src/wordrec/tface.cpp
        src/wordrec/wordclass.cpp
        src/wordrec/wordrec.cpp
)

set_source_files_properties(src/arch/dotproduct.cpp PROPERTIES COMPILE_OPTIONS "-fopenmp-simd;-ffast-math")

if (CMAKE_SYSTEM_PROCESSOR MATCHES "x86|x86_64|AMD64|amd64|i386|i686")
    list(APPEND PROJECT_SOURCES ${PROJECT_AVX_SOURCES} ${PROJECT_AVX2_SOURCES}
            ${PROJECT_AVX512_SOURCES} ${PROJECT_FMA_SOURCES} ${PROJECT_SSE_SOURCES})

    set_source_files_properties(${PROJECT_AVX_SOURCES} PROPERTIES COMPILE_OPTIONS -mavx)
    set_source_files_properties(${PROJECT_AVX2_SOURCES} PROPERTIES COMPILE_OPTIONS -mavx2)
    set_source_files_properties(${PROJECT_AVX512_SOURCES} PROPERTIES COMPILE_OPTIONS -mavx512f)
    set_source_files_properties(${PROJECT_FMA_SOURCES} PROPERTIES COMPILE_OPTIONS -mfma)
    set_source_files_properties(${PROJECT_SSE_SOURCES} PROPERTIES COMPILE_OPTIONS -msse4.1)

    set(ARCH_OPTIONS HAVE_AVX HAVE_AVX2 HAVE_AVX512F HAVE_FMA HAVE_SSE4_1 OPENMP_SIMD)
elseif (CMAKE_SYSTEM_PROCESSOR MATCHES "arm64|aarch64.*|AARCH64.*")
    list(APPEND PROJECT_SOURCES ${PROJECT_NEON_SOURCES})
    set(ARCH_OPTIONS HAVE_NEON)
endif ()

add_library(${PROJECT_NAME} ${PROJECT_SOURCES})

target_include_directories(${PROJECT_NAME}
        PUBLIC include ${CMAKE_CURRENT_BINARY_DIR}/include
        PRIVATE ${CMAKE_CURRENT_BINARY_DIR}/include-private include-private/api include-private/arch
        include-private/ccmain include-private/ccstruct include-private/ccutil include-private/classify
        include-private/cutil include-private/dict include-private/lstm include-private/textord include-private/viewer
        include-private/wordrec
)

target_link_libraries(${PROJECT_NAME} leptonica)

set_target_properties(${PROJECT_NAME} PROPERTIES POSITION_INDEPENDENT_CODE TRUE)

target_compile_definitions(${PROJECT_NAME} PRIVATE HAVE_CONFIG_H)
target_compile_definitions(${PROJECT_NAME} PRIVATE ${ARCH_OPTIONS})

install(TARGETS ${PROJECT_NAME} COMPONENT ${PROJECT_NAME})
install(DIRECTORY include/ DESTINATION include COMPONENT ${PROJECT_NAME})
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/include/ DESTINATION include COMPONENT ${PROJECT_NAME})
