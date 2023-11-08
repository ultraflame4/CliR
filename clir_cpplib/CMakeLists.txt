cmake_minimum_required(VERSION 3.26)
project(clir_cpp)

find_package(Python3 REQUIRED COMPONENTS Interpreter Development)

execute_process(
        COMMAND "${Python3_EXECUTABLE}"
        -c "import numpy; print(numpy.get_include())"
        OUTPUT_VARIABLE NumPy_INCLUDE_DIRS
        OUTPUT_STRIP_TRAILING_WHITESPACE
)

add_library(
        clir_cpplib MODULE
        src/testmodule.cc
        src/charcolor.cc
        src/main.cc
)

if (SKBUILD)
    find_package(PythonExtensions REQUIRED)
    python_extension_module(clir_cpplib)
    install(TARGETS clir_cpplib LIBRARY DESTINATION clir_cpp)
endif ()

MESSAGE(STATUS ${NumPy_INCLUDE_DIRS} " <-- NUMPY INCLUDES")
include_directories(${Python3_INCLUDE_DIRS} ${NumPy_INCLUDE_DIRS})
target_link_libraries(clir_cpplib ${Python3_LIBRARIES})
