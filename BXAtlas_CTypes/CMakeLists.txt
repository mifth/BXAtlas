cmake_minimum_required(VERSION 3.5)

project (BXAtlasCPP)
set(CMAKE_BUILD_TYPE Release)

set(CMAKE_CXX_STANDARD 20)

# Find source files
file(GLOB SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/sources/*.cpp)

# Include header files
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)

add_library(BXAtlas SHARED
    sources/xatlas.cpp
    sources/bxatlas.cpp
)


