cmake_minimum_required(VERSION 3.26)
project(clir_cpp)

find_package(Python3 REQUIRED COMPONENTS Interpreter Development)


add_library(
        clir_cpplib SHARED
        src/testmodule.cc
        src/charcolor.cc
        src/main.cc
)

if (SKBUILD)
    find_package(PythonExtensions REQUIRED)
    python_extension_module(clir_cpplib)
    install(TARGETS clir_cpplib LIBRARY DESTINATION clir_cpp)
endif ()

include_directories(${Python3_INCLUDE_DIRS})
target_link_libraries(clir_cpplib ${Python3_LIBRARIES})
