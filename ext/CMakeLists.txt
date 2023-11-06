cmake_minimum_required(VERSION 3.26)
project(clir_cpp)

add_library(
        clir_cpplib SHARED
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

find_package(Python3 REQUIRED COMPONENTS Interpreter Development)

include_directories(${Python3_INCLUDE_DIRS})
target_link_libraries(clir_cpplib ${Python3_LIBRARIES})

