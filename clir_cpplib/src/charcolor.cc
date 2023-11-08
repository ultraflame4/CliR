#include <Python.h>
#include <numpy/arrayobject.h>
#include <cstdint>
#include <string>
#include <iostream>

static const char *CSI = "\33[";

static void get_ansi_color(uint8_t r, uint8_t g, uint8_t b, std::string &out_s, bool fore) {
    out_s += CSI;
    if (fore) {
        out_s += "38;2;";
    } else {
        out_s += "48;2;";
    }
    out_s += std::to_string(r) + ";";
    out_s += std::to_string(g) + ";";
    out_s += std::to_string(b) + "m";
}

static PyObject *pyColorChars(PyObject * self, PyObject * args) {
    PyObject * chars;
    PyObject * _charcolors;
    if (!PyArg_ParseTuple(args, "OO", &chars, &_charcolors)) return nullptr;

    int chars_len = PyList_Size(chars);
    if (chars_len < 0) return nullptr;

    // todo further update and specify ndarray requirements later on
    if (!PyArray_Check(_charcolors)) {
        PyErr_SetString(PyExc_TypeError, "Argument at position 2 is not a numpy array!");
        return nullptr;
    }
    std::cout << "A passed a numpy array!";
    PyObject * charcolors = PyArray_FromObject(_charcolors, NPY_INT8, 0,4);
    if (charcolors == nullptr) return nullptr;
    std::cout << "Successfully passed a numpy array!";
    for (int y = 0; y < chars_len; ++y) {
        PyObject * row = PyList_GetItem(chars, y);
        void *raw_buffer = PyUnicode_DATA(row);
        int row_len = PyUnicode_GetLength(row);

        if (raw_buffer == nullptr || row_len < 0) return nullptr;

        for (int x = 0; x < row_len; ++x) {
            Py_UCS4 c = PyUnicode_READ_CHAR(row, x);

        }
    }


    Py_RETURN_NONE;
}

static PyObject *pyAnsiColor(PyObject * self, PyObject * args) {
    uint8_t red;
    uint8_t green;
    uint8_t blue;
    int fore;
    if (!PyArg_ParseTuple(args, "bbbp", &red, &green, &blue, &fore))
        return nullptr;

    std::string ansi_ = "";
    get_ansi_color(red, green, blue, ansi_, fore == 1);
    return PyUnicode_FromString(ansi_.c_str());
}



