#include <Python.h>
#include <cstdint>
#include <string>

static const char* CSI = "\33[";

static void get_ansi_color(uint8_t r, uint8_t g, uint8_t b, std::string out_s, bool fore){
    out_s.append(CSI);
    if (fore) {
        out_s.append("38;2");
    }
    else{
        out_s.append("48;2");
    }
    out_s.append(std::to_string(r) + ";");
    out_s.append(std::to_string(g) + ";");
    out_s.append(std::to_string(b) + "m");
}

static PyObject *pyAnsiColor(PyObject * self, PyObject * args){
    uint8_t red;
    uint8_t green;
    uint8_t blue;
    int fore;
    if (!PyArg_ParseTuple(args, "b", &red))
        return nullptr;
    if (!PyArg_ParseTuple(args, "b", &green))
        return nullptr;
    if (!PyArg_ParseTuple(args, "b", &blue))
        return nullptr;
    if (!PyArg_ParseTuple(args, "p", &fore))
        return nullptr;


    std::string ansi_ = "";
    get_ansi_color(red, green, blue, ansi_, fore == 1);
    return Py_BuildValue("s", ansi_.data());
}



