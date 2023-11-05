#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <iostream>

extern  PyObject *testprint(PyObject *self, PyObject *args)
{
  std::cout << "Hello world!\n";
  return PyLong_FromLong(10);
}




static PyMethodDef testmodMethods [] = {
        {"test",testprint, METH_VARARGS, "Prints hello world"},
        {NULL}
};

static struct PyModuleDef testmodule = {
        PyModuleDef_HEAD_INIT,
        "ext",
        NULL,
        -1,
        testmodMethods
};

PyMODINIT_FUNC PyInit_ext(void){
    return PyModule_Create(&testmodule);
}