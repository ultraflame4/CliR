#include <Python.h>
#include <iostream>

static PyObject *testprint(PyObject *self, PyObject *args)
{
  std::cout << "Hello world! This is built with cmake!\n";
  return PyLong_FromLong(10);
}

