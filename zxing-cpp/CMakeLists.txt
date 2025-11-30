cmake_minimum_required(VERSION 3.28)
project(ZXing VERSION 2.3.0 LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_EXTENSIONS OFF)

set(ZXING_READERS 1)
set(ZXING_WRITERS 1)

configure_file(config/Version.h.in "${CMAKE_CURRENT_BINARY_DIR}/include/ZXing/Version.h" @ONLY)

set(PROJECT_SOURCES
        src/Barcode.cpp
        src/BarcodeFormat.cpp
        src/BinaryBitmap.cpp
        src/BitArray.cpp
        src/BitMatrix.cpp
        src/BitMatrixIO.cpp
        src/BitSource.cpp
        src/CharacterSet.cpp
        src/ConcentricFinder.cpp
        src/Content.cpp
        src/ECI.cpp
        src/Error.cpp
        src/GenericGF.cpp
        src/GenericGFPoly.cpp
        src/GlobalHistogramBinarizer.cpp
        src/GridSampler.cpp
        src/GTIN.cpp
        src/HRI.cpp
        src/HybridBinarizer.cpp
        src/MultiFormatReader.cpp
        src/MultiFormatWriter.cpp
        src/PerspectiveTransform.cpp
        src/ReadBarcode.cpp
        src/ReedSolomonDecoder.cpp
        src/ReedSolomonEncoder.cpp
        src/ResultPoint.cpp
        src/TextDecoder.cpp
        src/TextEncoder.cpp
        src/TextUtfEncoding.cpp
        src/Utf.cpp
        src/WhiteRectDetector.cpp
        src/WriteBarcode.cpp
        src/ZXingCpp.cpp
        src/aztec/AZDecoder.cpp
        src/aztec/AZDetector.cpp
        src/aztec/AZEncoder.cpp
        src/aztec/AZHighLevelEncoder.cpp
        src/aztec/AZReader.cpp
        src/aztec/AZToken.cpp
        src/aztec/AZWriter.cpp
        src/datamatrix/DMBitLayout.cpp
        src/datamatrix/DMDataBlock.cpp
        src/datamatrix/DMDecoder.cpp
        src/datamatrix/DMDetector.cpp
        src/datamatrix/DMECEncoder.cpp
        src/datamatrix/DMHighLevelEncoder.cpp
        src/datamatrix/DMReader.cpp
        src/datamatrix/DMSymbolInfo.cpp
        src/datamatrix/DMVersion.cpp
        src/datamatrix/DMWriter.cpp
        src/maxicode/MCBitMatrixParser.cpp
        src/maxicode/MCDecoder.cpp
        src/maxicode/MCReader.cpp
        src/oned/ODCodabarReader.cpp
        src/oned/ODCodabarWriter.cpp
        src/oned/ODCode39Reader.cpp
        src/oned/ODCode39Writer.cpp
        src/oned/ODCode93Reader.cpp
        src/oned/ODCode93Writer.cpp
        src/oned/ODCode128Patterns.cpp
        src/oned/ODCode128Reader.cpp
        src/oned/ODCode128Writer.cpp
        src/oned/ODDataBarCommon.cpp
        src/oned/ODDataBarExpandedBitDecoder.cpp
        src/oned/ODDataBarExpandedReader.cpp
        src/oned/ODDataBarLimitedReader.cpp
        src/oned/ODDataBarReader.cpp
        src/oned/ODDXFilmEdgeReader.cpp
        src/oned/ODEAN8Writer.cpp
        src/oned/ODEAN13Writer.cpp
        src/oned/ODITFReader.cpp
        src/oned/ODITFWriter.cpp
        src/oned/ODMultiUPCEANReader.cpp
        src/oned/ODReader.cpp
        src/oned/ODUPCAWriter.cpp
        src/oned/ODUPCEANCommon.cpp
        src/oned/ODUPCEWriter.cpp
        src/oned/ODWriterHelper.cpp
        src/pdf417/PDFBarcodeValue.cpp
        src/pdf417/PDFBoundingBox.cpp
        src/pdf417/PDFCodewordDecoder.cpp
        src/pdf417/PDFDecoder.cpp
        src/pdf417/PDFDetectionResult.cpp
        src/pdf417/PDFDetectionResultColumn.cpp
        src/pdf417/PDFDetector.cpp
        src/pdf417/PDFEncoder.cpp
        src/pdf417/PDFHighLevelEncoder.cpp
        src/pdf417/PDFModulusGF.cpp
        src/pdf417/PDFModulusPoly.cpp
        src/pdf417/PDFReader.cpp
        src/pdf417/PDFScanningDecoder.cpp
        src/pdf417/PDFWriter.cpp
        src/pdf417/ZXBigInteger.cpp
        src/qrcode/QRBitMatrixParser.cpp
        src/qrcode/QRCodecMode.cpp
        src/qrcode/QRDataBlock.cpp
        src/qrcode/QRDecoder.cpp
        src/qrcode/QRDetector.cpp
        src/qrcode/QREncoder.cpp
        src/qrcode/QRErrorCorrectionLevel.cpp
        src/qrcode/QRFormatInformation.cpp
        src/qrcode/QRMaskUtil.cpp
        src/qrcode/QRMatrixUtil.cpp
        src/qrcode/QRReader.cpp
        src/qrcode/QRVersion.cpp
        src/qrcode/QRWriter.cpp
        src/libzueci/zueci.c
)

add_library(${PROJECT_NAME} ${PROJECT_SOURCES})

target_include_directories(${PROJECT_NAME}
        PUBLIC include ${CMAKE_CURRENT_BINARY_DIR}/include
        PRIVATE include/ZXing ${CMAKE_CURRENT_BINARY_DIR}/include/ZXing include-private include-private/aztec
        include-private/datamatrix include-private/libzueci include-private/maxicode include-private/oned
        include-private/pdf417 include-private/qrcode
)

set_target_properties(${PROJECT_NAME} PROPERTIES POSITION_INDEPENDENT_CODE TRUE)

install(TARGETS ${PROJECT_NAME} COMPONENT ${PROJECT_NAME})
install(DIRECTORY include/ DESTINATION include COMPONENT ${PROJECT_NAME})
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/include/ DESTINATION include COMPONENT ${PROJECT_NAME})
