cmake_minimum_required(VERSION 3.26)
project(clir_cpp)

find_package(Python3 REQUIRED COMPONENTS Interpreter Development)
find_package(PythonExtensions REQUIRED)

add_library(
        clir_cpplib MODULE
        src/testmodule.cc
        src/charcolor.cc
        src/main.cc
)
set_target_properties(
        clir_cpplib
        PROPERTIES
        PREFIX ""
        OUTPUT_NAME "${CLIR_MOD_NAME}"
        SUFFIX ""
        LINKER_LANGUAGE CPP
)


#if(WIN32)
#    set_target_properties(
#            clir_cpplib
#            PROPERTIES
#            SUFFIX ".pyd"
#    )
#endif ()

python_extension_module(clir_cpplib)
install(TARGETS clir_cpplib LIBRARY DESTINATION clir_cpp)

include_directories(${Python3_INCLUDE_DIRS})
target_link_libraries(clir_cpplib ${Python3_LIBRARIES})

