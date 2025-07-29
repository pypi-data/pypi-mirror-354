# coding: utf-8
import ctypes


class PyObject(ctypes.Structure):
    _fields_ = [
        ("ob_refcnt", ctypes.c_ssize_t),
        ("ob_type", ctypes.c_void_p),
    ]
    

class PyVarObject(PyObject):
    _fields_ = [
        ("ob_size", ctypes.c_ssize_t),
    ]
 

class PyLongObject(PyVarObject):
    _fields_ = [
        ("ob_digit", ctypes.c_uint32 * 10),
    ]
 

class PyFloatObject(PyObject):
    _fields_ = [
        ("ob_fval", ctypes.c_double),
    ]


class PyASCIIObject(PyObject):
    _fields_ = [
        ("length", ctypes.c_ssize_t),
        ("hash", ctypes.c_ssize_t),
        ("state", ctypes.c_uint),  # contains interned, kind, compact, ascii, etc.
    ]


class PyCompactUnicodeObject(PyASCIIObject):
    _fields_ = [
        ("utf8_length", ctypes.c_ssize_t),
        ("utf8", ctypes.c_char_p),
    ]


class PyUnicodeObject(PyCompactUnicodeObject):
    _fields_ = [
        ("data", ctypes.c_void_p),
    ]
    

class PyListObject(PyVarObject):
    _fields_ = [
        ("ob_items", ctypes.POINTER(ctypes.c_void_p)),  # pointer to array of PyObject*
        ("ob_allocated", ctypes.c_ssize_t),
    ]


class PyDictObject(PyObject):
    _fields_ = [
        ("ma_used", ctypes.c_ssize_t),
        ("ma_version_tag", ctypes.c_uint64),  # Optional
        ("ma_keys", ctypes.c_void_p),
        ("ma_values", ctypes.c_void_p),
    ]
