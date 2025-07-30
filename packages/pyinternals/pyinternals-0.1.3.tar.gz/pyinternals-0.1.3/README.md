# pyinternals

A visualizer for Python object layout in CPython.

This package provides tools to directly inspecting Python objects through their C-level structure using `ctypes`.
This is a powerful approach for deep object introspection, especially when you need to examine the internal memory representation of Python objects like `int`, `float`, `str`, `list`, `dict` and custom classes.


## Features

- Inspect memory layout of Python objects.
- Visualize CPython object internals like `__dict__`, `__slots__`, methods, and more.
- Great for learning how CPython manages memory.

## Installation

Install via pip:

```bash
pip install pyinternals
```
## Learning materials

- CPython implementation : https://github.com/python/cpython
- Cpython Internals repository: https://github.com/zpoint/CPython-Internals