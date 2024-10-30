cmake_minimum_required(VERSION 3.5)

project (BXAtlasCPP)
set(CMAKE_BUILD_TYPE Release)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED true)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Find source files
file(GLOB SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/sources/*.cpp)

# Include header files
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)

add_definitions(/D_DISABLE_CONSTEXPR_MUTEX_CONSTRUCTOR)

add_library(BXAtlas SHARED
    sources/xatlas.cpp
    sources/bxatlas.cpp
)


