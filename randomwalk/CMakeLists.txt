cmake_minimum_required(VERSION 2.8)

PROJECT(MitoRandomWalk CXX)

FIND_PACKAGE(VTK REQUIRED)

INCLUDE(${VTK_USE_FILE})

ADD_EXECUTABLE(MitoRandomWalk MitoRandomWalk.cxx)

TARGET_LINK_LIBRARIES(MitoRandomWalk  ${VTK_LIBRARIES})
