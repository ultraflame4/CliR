#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "./testmodule.cc"
#include "./charcolor.cc"


static PyMethodDef methods [] = {
        {"ansi_color", pyAnsiColor, METH_VARARGS, "Returns ansi color"},
        {"test",testprint, METH_VARARGS, "Prints hello world"},
        {NULL}
};
static struct PyModuleDef module = {
        PyModuleDef_HEAD_INIT,
        "clir_cpplib",
        NULL,
        -1,
        methods
};

PyMODINIT_FUNC PyInit_clir_cpplib(void){
    return PyModule_Create(&module);
}