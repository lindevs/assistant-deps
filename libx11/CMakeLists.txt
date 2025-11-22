cmake_minimum_required(VERSION 3.28)
project(X11 VERSION 1.8.9 LANGUAGES C)

set(CMAKE_C_STANDARD 99)

option(XTHREADS "Enable X11 support for multithreading" ON)
option(USE_DYNAMIC_XCURSOR "Use the X cursor library to load cursors" ON)
option(XCMS "Include support for XCMS" ON)
option(XKB "Include support for XKB" ON)
option(XLOCALE "Include support for Internationalization" ON)
option(XF86BIGFONT "Enable XF86BIGFONT extension" ON)
option(USE_THREAD_SAFETY_CONSTRUCTOR "Use thread safety constructor" ON)
set(XCMSDIR "/usr/share/X11" CACHE STRING "Location of XCMS files")
set(XERRORDB "/usr/share/X11/XErrorDB" CACHE STRING "Location of error message database")
set(XKEYSYMDB "/usr/share/X11/XKeysymDB" CACHE STRING "Location of keysym database")
set(XLOCALEDIR "/usr/share/X11/locale" CACHE STRING "Location of locale data")
set(XLOCALELIBDIR "/usr/lib/X11/locale" CACHE STRING "Location of locale libraries")

set(CMAKE_REQUIRED_QUIET TRUE)
include(CheckFunctionExists)
include(CheckIncludeFile)
include(CheckSourceCompiles)

set(HAVE_REALLOCARRAY 1)
set(IPv6 1)
set(TCPCONN 1)
set(UNIXCONN 1)
set(_GNU_SOURCE 1)
set(XIM_t 1)
set(TRANS_CLIENT 1)
check_function_exists(nl_langinfo COMPOSECACHE)
check_function_exists(getresuid HASGETRESUID)
check_function_exists(issetugid HASSETUGID)
check_function_exists(shmat HAS_SHM)
check_function_exists(seteuid HAVE_SETEUID)
check_function_exists(strcasecmp HAVE_STRCASECMP)
check_function_exists(poll USE_POLL)
check_include_file(sys/filio.h HAVE_SYS_FILIO_H)
check_include_file(sys/ioctl.h HAVE_SYS_IOCTL_H)
check_include_file(sys/select.h HAVE_SYS_SELECT_H)
check_include_file(sys/socket.h HAVE_SYS_SOCKET_H)
check_source_compiles(C "int main() {return __builtin_popcountl(0);}" HAVE___BUILTIN_POPCOUNTL)

if (XTHREADS)
    check_function_exists(getpwuid_r XUSE_MTSAFE_API)
endif ()

configure_file(config/config-cmake.h.in "${CMAKE_CURRENT_BINARY_DIR}/include-private/config.h" @ONLY)
configure_file(config/XlibConf.h.in "${CMAKE_CURRENT_BINARY_DIR}/include/X11/XlibConf.h")
configure_file(pkgconfig/x11.pc.in "${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/x11.pc" @ONLY)
configure_file(pkgconfig/x11-xcb.pc.in "${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/x11-xcb.pc" @ONLY)

set(PROJECT_SOURCES
        src/xcms/AddDIC.c
        src/xcms/AddSF.c
        src/xcms/CCC.c
        src/xcms/cmsAllCol.c
        src/xcms/cmsAllNCol.c
        src/xcms/cmsCmap.c
        src/xcms/cmsColNm.c
        src/xcms/cmsGlobls.c
        src/xcms/cmsInt.c
        src/xcms/cmsLkCol.c
        src/xcms/cmsMath.c
        src/xcms/cmsProp.c
        src/xcms/cmsTrig.c
        src/xcms/CvCols.c
        src/xcms/CvColW.c
        src/xcms/HVC.c
        src/xcms/HVCGcC.c
        src/xcms/HVCGcV.c
        src/xcms/HVCGcVC.c
        src/xcms/HVCMnV.c
        src/xcms/HVCMxC.c
        src/xcms/HVCMxV.c
        src/xcms/HVCMxVC.c
        src/xcms/HVCMxVs.c
        src/xcms/HVCWpAj.c
        src/xcms/IdOfPr.c
        src/xcms/Lab.c
        src/xcms/LabGcC.c
        src/xcms/LabGcL.c
        src/xcms/LabGcLC.c
        src/xcms/LabMnL.c
        src/xcms/LabMxC.c
        src/xcms/LabMxL.c
        src/xcms/LabMxLC.c
        src/xcms/LabWpAj.c
        src/xcms/LRGB.c
        src/xcms/Luv.c
        src/xcms/LuvGcC.c
        src/xcms/LuvGcL.c
        src/xcms/LuvGcLC.c
        src/xcms/LuvMnL.c
        src/xcms/LuvMxC.c
        src/xcms/LuvMxL.c
        src/xcms/LuvMxLC.c
        src/xcms/LuvWpAj.c
        src/xcms/OfCCC.c
        src/xcms/PrOfId.c
        src/xcms/QBlack.c
        src/xcms/QBlue.c
        src/xcms/QGreen.c
        src/xcms/QRed.c
        src/xcms/QuCol.c
        src/xcms/QuCols.c
        src/xcms/QWhite.c
        src/xcms/SetCCC.c
        src/xcms/SetGetCols.c
        src/xcms/StCol.c
        src/xcms/StCols.c
        src/xcms/UNDEFINED.c
        src/xcms/uvY.c
        src/xcms/XRGB.c
        src/xcms/xyY.c
        src/xcms/XYZ.c
        src/xkb/XKB.c
        src/xkb/XKBAlloc.c
        src/xkb/XKBBell.c
        src/xkb/XKBBind.c
        src/xkb/XKBCompat.c
        src/xkb/XKBCtrls.c
        src/xkb/XKBCvt.c
        src/xkb/XKBExtDev.c
        src/xkb/XKBGAlloc.c
        src/xkb/XKBGeom.c
        src/xkb/XKBGetByName.c
        src/xkb/XKBGetMap.c
        src/xkb/XKBleds.c
        src/xkb/XKBList.c
        src/xkb/XKBMAlloc.c
        src/xkb/XKBMisc.c
        src/xkb/XKBNames.c
        src/xkb/XKBRdBuf.c
        src/xkb/XKBSetGeom.c
        src/xkb/XKBSetMap.c
        src/xkb/XKBUse.c
        src/xlibi18n/ICWrap.c
        src/xlibi18n/imKStoUCS.c
        src/xlibi18n/IMWrap.c
        src/xlibi18n/lcCharSet.c
        src/xlibi18n/lcConv.c
        src/xlibi18n/lcCT.c
        src/xlibi18n/lcDB.c
        src/xlibi18n/lcDynamic.c
        src/xlibi18n/lcFile.c
        src/xlibi18n/lcGeneric.c
        src/xlibi18n/lcInit.c
        src/xlibi18n/lcPrTxt.c
        src/xlibi18n/lcPublic.c
        src/xlibi18n/lcPubWrap.c
        src/xlibi18n/lcRM.c
        src/xlibi18n/lcStd.c
        src/xlibi18n/lcTxtPr.c
        src/xlibi18n/lcUTF8.c
        src/xlibi18n/lcUtil.c
        src/xlibi18n/lcWrap.c
        src/xlibi18n/mbWMProps.c
        src/xlibi18n/mbWrap.c
        src/xlibi18n/utf8WMProps.c
        src/xlibi18n/utf8Wrap.c
        src/xlibi18n/wcWrap.c
        src/xlibi18n/XDefaultIMIF.c
        src/xlibi18n/XDefaultOMIF.c
        src/xlibi18n/xim_trans.c
        src/AllCells.c
        src/AllowEv.c
        src/AllPlanes.c
        src/AutoRep.c
        src/Backgnd.c
        src/BdrWidth.c
        src/Bell.c
        src/Border.c
        src/ChAccCon.c
        src/ChActPGb.c
        src/ChClMode.c
        src/ChCmap.c
        src/ChGC.c
        src/ChKeyCon.c
        src/ChkIfEv.c
        src/ChkMaskEv.c
        src/ChkTypEv.c
        src/ChkTypWEv.c
        src/ChkWinEv.c
        src/ChPntCon.c
        src/ChProp.c
        src/ChSaveSet.c
        src/ChWAttrs.c
        src/ChWindow.c
        src/CirWin.c
        src/CirWinDn.c
        src/CirWinUp.c
        src/ClDisplay.c
        src/Clear.c
        src/ClearArea.c
        src/ConfWind.c
        src/Context.c
        src/ConvSel.c
        src/CopyArea.c
        src/CopyCmap.c
        src/CopyGC.c
        src/CopyPlane.c
        src/CrBFData.c
        src/CrCmap.c
        src/CrCursor.c
        src/CrGC.c
        src/CrGlCur.c
        src/CrPFBData.c
        src/CrPixmap.c
        src/CrWindow.c
        src/Cursor.c
        src/DefCursor.c
        src/DelProp.c
        src/Depths.c
        src/DestSubs.c
        src/DestWind.c
        src/DisName.c
        src/DrArc.c
        src/DrArcs.c
        src/DrLine.c
        src/DrLines.c
        src/DrPoint.c
        src/DrPoints.c
        src/DrRect.c
        src/DrRects.c
        src/DrSegs.c
        src/ErrDes.c
        src/ErrHndlr.c
        src/evtomask.c
        src/EvToWire.c
        src/FetchName.c
        src/FillArc.c
        src/FillArcs.c
        src/FillPoly.c
        src/FillRct.c
        src/FillRcts.c
        src/FilterEv.c
        src/Flush.c
        src/Font.c
        src/FontInfo.c
        src/FontNames.c
        src/FreeCmap.c
        src/FreeCols.c
        src/FreeCurs.c
        src/FreeEData.c
        src/FreeEventData.c
        src/FreeGC.c
        src/FreePix.c
        src/FSSaver.c
        src/FSWrap.c
        src/GCMisc.c
        src/Geom.c
        src/GetAtomNm.c
        src/GetColor.c
        src/GetDflt.c
        src/GetEventData.c
        src/GetFPath.c
        src/GetFProp.c
        src/GetGCVals.c
        src/GetGeom.c
        src/GetHColor.c
        src/GetHints.c
        src/GetIFocus.c
        src/GetImage.c
        src/GetKCnt.c
        src/GetMoEv.c
        src/GetNrmHint.c
        src/GetPCnt.c
        src/GetPntMap.c
        src/GetProp.c
        src/GetRGBCMap.c
        src/GetSOwner.c
        src/GetSSaver.c
        src/GetStCmap.c
        src/GetTxtProp.c
        src/GetWAttrs.c
        src/GetWMCMapW.c
        src/GetWMProto.c
        src/globals.c
        src/GrButton.c
        src/GrKey.c
        src/GrKeybd.c
        src/GrPointer.c
        src/GrServer.c
        src/Host.c
        src/Iconify.c
        src/IfEvent.c
        src/imConv.c
        src/ImText.c
        src/ImText16.c
        src/ImUtil.c
        src/InitExt.c
        src/InsCmap.c
        src/IntAtom.c
        src/KeyBind.c
        src/KeysymStr.c
        src/KillCl.c
        src/LiHosts.c
        src/LiICmaps.c
        src/LiProps.c
        src/ListExt.c
        src/LoadFont.c
        src/LockDis.c
        src/locking.c
        src/LookupCol.c
        src/LowerWin.c
        src/Macros.c
        src/MapRaised.c
        src/MapSubs.c
        src/MapWindow.c
        src/MaskEvent.c
        src/Misc.c
        src/ModMap.c
        src/MoveWin.c
        src/NextEvent.c
        src/OCWrap.c
        src/OMWrap.c
        src/OpenDis.c
        src/ParseCmd.c
        src/ParseCol.c
        src/ParseGeom.c
        src/PeekEvent.c
        src/PeekIfEv.c
        src/Pending.c
        src/PixFormats.c
        src/PmapBgnd.c
        src/PmapBord.c
        src/PolyReg.c
        src/PolyTxt.c
        src/PolyTxt16.c
        src/PropAlloc.c
        src/PutBEvent.c
        src/PutImage.c
        src/Quarks.c
        src/QuBest.c
        src/QuColor.c
        src/QuColors.c
        src/QuCurShp.c
        src/QuExt.c
        src/QuKeybd.c
        src/QuPntr.c
        src/QuStipShp.c
        src/QuTextE16.c
        src/QuTextExt.c
        src/QuTileShp.c
        src/QuTree.c
        src/RaiseWin.c
        src/RdBitF.c
        src/RecolorC.c
        src/ReconfWin.c
        src/ReconfWM.c
        src/Region.c
        src/RegstFlt.c
        src/RepWindow.c
        src/RestackWs.c
        src/RotProp.c
        src/ScrResStr.c
        src/SelInput.c
        src/SendEvent.c
        src/SetBack.c
        src/SetClMask.c
        src/SetClOrig.c
        src/SetCRects.c
        src/SetDashes.c
        src/SetFont.c
        src/SetFore.c
        src/SetFPath.c
        src/SetFunc.c
        src/SetHints.c
        src/SetIFocus.c
        src/SetLocale.c
        src/SetLStyle.c
        src/SetNrmHint.c
        src/SetPMask.c
        src/SetPntMap.c
        src/SetRGBCMap.c
        src/SetSOwner.c
        src/SetSSaver.c
        src/SetState.c
        src/SetStCmap.c
        src/SetStip.c
        src/SetTile.c
        src/SetTSOrig.c
        src/SetTxtProp.c
        src/SetWMCMapW.c
        src/SetWMProto.c
        src/StBytes.c
        src/StColor.c
        src/StColors.c
        src/StName.c
        src/StNColor.c
        src/StrKeysym.c
        src/StrToText.c
        src/Sync.c
        src/Synchro.c
        src/Text.c
        src/Text16.c
        src/TextExt.c
        src/TextExt16.c
        src/TextToStr.c
        src/TrCoords.c
        src/UndefCurs.c
        src/UngrabBut.c
        src/UngrabKbd.c
        src/UngrabKey.c
        src/UngrabPtr.c
        src/UngrabSvr.c
        src/UninsCmap.c
        src/UnldFont.c
        src/UnmapSubs.c
        src/UnmapWin.c
        src/VisUtil.c
        src/WarpPtr.c
        src/Window.c
        src/WinEvent.c
        src/Withdraw.c
        src/WMGeom.c
        src/WMProps.c
        src/WrBitF.c
        src/xcb_disp.c
        src/xcb_io.c
        src/XlibAsync.c
        src/XlibInt.c
        src/Xrm.c
        src/modules/im/ximcp/imCallbk.c
        src/modules/im/ximcp/imDefFlt.c
        src/modules/im/ximcp/imDefIc.c
        src/modules/im/ximcp/imDefIm.c
        src/modules/im/ximcp/imDefLkup.c
        src/modules/im/ximcp/imDispch.c
        src/modules/im/ximcp/imEvToWire.c
        src/modules/im/ximcp/imExten.c
        src/modules/im/ximcp/imImSw.c
        src/modules/im/ximcp/imInsClbk.c
        src/modules/im/ximcp/imInt.c
        src/modules/im/ximcp/imLcFlt.c
        src/modules/im/ximcp/imLcGIc.c
        src/modules/im/ximcp/imLcIc.c
        src/modules/im/ximcp/imLcIm.c
        src/modules/im/ximcp/imLcLkup.c
        src/modules/im/ximcp/imLcPrs.c
        src/modules/im/ximcp/imLcSIc.c
        src/modules/im/ximcp/imRm.c
        src/modules/im/ximcp/imRmAttr.c
        src/modules/im/ximcp/imThaiFlt.c
        src/modules/im/ximcp/imThaiIc.c
        src/modules/im/ximcp/imThaiIm.c
        src/modules/im/ximcp/imTrans.c
        src/modules/im/ximcp/imTransR.c
        src/modules/im/ximcp/imTrX.c
        src/modules/lc/def/lcDefConv.c
        src/modules/lc/gen/lcGenConv.c
        src/modules/lc/Utf8/lcUTF8Load.c
        src/modules/om/generic/omDefault.c
        src/modules/om/generic/omGeneric.c
        src/modules/om/generic/omImText.c
        src/modules/om/generic/omText.c
        src/modules/om/generic/omTextEsc.c
        src/modules/om/generic/omTextExt.c
        src/modules/om/generic/omTextPer.c
        src/modules/om/generic/omXChar.c
)

add_library(${PROJECT_NAME} ${PROJECT_SOURCES})
add_library(${PROJECT_NAME}-xcb src/x11_xcb.c)

target_include_directories(${PROJECT_NAME}
        PUBLIC include ${CMAKE_CURRENT_BINARY_DIR}/include
        PRIVATE include-private include-private/xcms include-private/xkb include-private/xlibi18n include/X11
        ${CMAKE_CURRENT_BINARY_DIR}/include-private
)
target_include_directories(${PROJECT_NAME}-xcb
        PUBLIC include ${CMAKE_CURRENT_BINARY_DIR}/include
        PRIVATE include-private include/X11
)

target_link_libraries(${PROJECT_NAME} xtrans xcb ${PROJECT_NAME}-xcb)
target_link_libraries(${PROJECT_NAME}-xcb xcb)

set_target_properties(${PROJECT_NAME} PROPERTIES POSITION_INDEPENDENT_CODE TRUE)
set_target_properties(${PROJECT_NAME}-xcb PROPERTIES POSITION_INDEPENDENT_CODE TRUE)

target_compile_definitions(${PROJECT_NAME} PRIVATE HAVE_CONFIG_H)
target_compile_options(${PROJECT_NAME} PRIVATE -fno-strict-aliasing -w)
target_compile_options(${PROJECT_NAME}-xcb PRIVATE -w)

check_source_compiles(C "#include <stdlib.h>\n int main() {return (int) (malloc(0) == NULL);}" MALLOC_0_RETURNS_NULL)
if (MALLOC_0_RETURNS_NULL)
    target_compile_definitions(${PROJECT_NAME} PRIVATE MALLOC_0_RETURNS_NULL)
    set_source_files_properties(src/modules/lc/gen/lcGenConv.c PROPERTIES COMPILE_OPTIONS -UMALLOC_0_RETURNS_NULL)
endif ()

install(TARGETS ${PROJECT_NAME} COMPONENT ${PROJECT_NAME})
install(TARGETS ${PROJECT_NAME}-xcb COMPONENT ${PROJECT_NAME})
install(DIRECTORY include/ DESTINATION include COMPONENT ${PROJECT_NAME})
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/include/ DESTINATION include COMPONENT ${PROJECT_NAME})
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/pkgconfig/ DESTINATION lib/pkgconfig COMPONENT ${PROJECT_NAME})
