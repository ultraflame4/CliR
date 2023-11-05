cmake_minimum_required(VERSION 3.10)
project(clir_cpp)

add_library(
        clir_cpplib SHARED
        src/testmodule.cc
)


find_package(PythonInterp 3.9 REQUIRED)

# This goes after, since it uses PythonInterp as hint
find_package(PythonLibs 3.9 REQUIRED)

include_directories(${PYTHON_INCLUDE_DIRS})
target_link_libraries(clir_cpplib ${PYTHON_LIBRARIES})