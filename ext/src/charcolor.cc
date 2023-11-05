#include <Python.h>
#include <cstdint>
#include <string>
#include <iostream>

static const char* CSI = "\33[";

static void get_ansi_color(uint8_t r, uint8_t g, uint8_t b, std::string& out_s, bool fore){
    out_s+=CSI;
    if (fore) {
        out_s+="38;2;";
    }
    else{
        out_s+="48;2;";
    }
    out_s+=std::to_string(r) + ";";
    out_s+=std::to_string(g) + ";";
    out_s+=std::to_string(b) + "m";
}

static PyObject *pyAnsiColor(PyObject * self, PyObject * args){
    uint8_t red;
    uint8_t green;
    uint8_t blue;
    int fore;
    if (!PyArg_ParseTuple(args, "bbbp", &red, &green, &blue,&fore))
        return nullptr;

    std::string ansi_ = "";
    get_ansi_color(red, green, blue, ansi_, fore == 1);
    return PyUnicode_FromString(ansi_.c_str());
}



