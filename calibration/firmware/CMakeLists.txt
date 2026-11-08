# == DO NOT EDIT THE FOLLOWING LINES for the Raspberry Pi Pico VS Code Extension to work ==
if(WIN32)
    set(USERHOME $ENV{USERPROFILE})
else()
    set(USERHOME $ENV{HOME})
endif()
set(sdkVersion 2.3.1)
set(toolchainVersion 15_2_Rel1)
set(picotoolVersion 2.3.1)
set(picoVscode ${USERHOME}/.pico-sdk/cmake/pico-vscode.cmake)
if (EXISTS ${picoVscode})
    include(${picoVscode})
endif()
# ====================================================================================
cmake_minimum_required(VERSION 3.13)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(PICO_BOARD pico2_w)

include(pico_sdk_import.cmake)

project(mullan_kosteusmittari C CXX ASM)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

pico_sdk_init()

add_executable(mullan_kosteusmittari
    main.c
)

target_link_libraries(mullan_kosteusmittari
    pico_stdlib
    hardware_adc
)

pico_enable_stdio_usb(mullan_kosteusmittari 1)
pico_enable_stdio_uart(mullan_kosteusmittari 0)

pico_add_extra_outputs(mullan_kosteusmittari)