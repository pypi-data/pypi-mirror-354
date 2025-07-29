# coding: utf-8
import ctypes

from .cpy_layouts import PyLongObject, PyUnicodeObject, PyDictObject
from .cpy_layouts import PyFloatObject, PyListObject
def inspect_int(obj):
    addr = id(obj)
    obj = ctypes.cast(addr, ctypes.POINTER(PyLongObject)).contents
    print(f"\n---> Int at {hex(addr)}:")
    print("-" * 40)
    print(f"{'Field':<15} | {'Value'}") 
    print("-" * 40)    
    print(f"{'ob_refcnt':<15} | {obj.ob_refcnt}")
    print(f"{'ob_type':<15} | {hex(obj.ob_type)}")    
    print(f"{'size': <15} | {obj.ob_size}")
    print("\ndigits (base 2^30):")
    for i in range(abs(obj.ob_size)):
        print(f"  ob_digit[{i}]   | {obj.ob_digit[i]}")

def inspect_float(value):
    assert isinstance(value, float), "Pass a float!"
    addr = id(value)
    obj = ctypes.cast(addr, ctypes.POINTER(PyFloatObject)).contents

    print(f"\n---> Float at {hex(addr)}:")
    print("-" * 40)
    print(f"{'Field':<15} | {'Value'}") 
    print("-" * 40)    
    print(f"{'ob_refcnt':<15} | {obj.ob_refcnt}")
    print(f"{'ob_type':<15} | {hex(obj.ob_type)}")    
    print(f"{'ob_fval':<15} | {obj.ob_fval}")


def inspect_str(s: str):
    assert isinstance(s, str)
    addr = id(s)
    obj = ctypes.cast(addr, ctypes.POINTER(PyUnicodeObject)).contents

    state = obj.state
    interned = state & 0b11
    kind = (state >> 2) & 0b111
    compact = (state >> 5) & 0b1
    ascii = (state >> 6) & 0b1

    print(f"\n---> String at {hex(addr)}:")
    print("-" * 40)    
    print(f"{'Field':<15} | {'Value'}") 
    print("-" * 40)    
    print(f"{'ob_refcnt':<15} | {obj.ob_refcnt}")
    print(f"{'ob_type':<15} | {hex(obj.ob_type)}")    
    print(f"{'hash':<15} | {obj.hash}")
    Int_MAP = {
    0: " Not Interned",
    1: "Interned",
    2: "Interned and Immortal",
    3: "Interned, Immortal, and Static"
    }
    print(f"{'interned':<15} | {Int_MAP[interned]}")
    KIND_MAP = {
    0: "INVALID",
    1: "1BYTE",
    2: "2BYTE",
    4: "4BYTE"
}
    print(f"{'kind':<15} | {kind} → {KIND_MAP.get(kind, 'UNKNOWN')}")
    print(f"{'compact':<15} | {bool(compact)}")
    print(f"{'ascii':<15} | {bool(ascii)}")
    print(f"{'utf8_length':<15} | {len(s.encode('utf-8'))}")


def inspect_dict(dobj):
    assert isinstance(dobj, dict)
    addr = id(dobj)
    obj = ctypes.cast(addr, ctypes.POINTER(PyDictObject)).contents
    pk, pv = obj.ma_keys, obj.ma_values
    print(f"\n---> Dict at {hex(addr)}:")
    print("-" * 40)    
    print(f"{'Field':<15} | {'Value'}") 
    print("-" * 40)    
    print(f"{'ob_refcnt':<15} | {obj.ob_refcnt}")
    print(f"{'ob_type':<15} | {hex(obj.ob_type)}")    
    print(f"{'used':<15} | {obj.ma_used}")
    print(f"{'ma_keys':<15} | {hex(pk) if pk is not None else None}")
    print(f"{'ma_values':<15} | {hex(pv) if pv is not None else None}")

    # Visual mapping (not raw memory)
    print("\n  Contents:")
    for k, v in dobj.items():
        print(f"    {repr(k)}: {repr(v)}")


def inspect_list(lst):
    addr = id(lst)
    obj = ctypes.cast(addr, ctypes.POINTER(PyListObject)).contents

    print(f"\n---> List at {hex(addr)}:")
    print("-" * 40)
    print(f"{'Field':<15} | {'Value'}") 
    print("-" * 40)    
    print(f"{'ob_refcnt':<15} | {obj.ob_refcnt}")
    print(f"{'ob_type':<15} | {hex(obj.ob_type)}")    
    print(f"{'size':<15} | {obj.ob_size}")
    print(f"{'allocated':<15} | {obj.ob_allocated}")
    print(f"{'ob_items':<15} | {hex(ctypes.addressof(obj.ob_items.contents))}")

    print("\n{'Elements':}")
    for i in range(obj.ob_size):
        ptr = obj.ob_items[i]  # this is a PyObject* (just an address)
        val = ctypes.cast(ptr, ctypes.py_object).value
        print(f"    {i}] @ {hex(ptr)}: {repr(val):<10} | {val.__class__.__name__}")


def hexdump(obj, size=64):
    addr = id(obj)
    raw = (ctypes.c_ubyte * size).from_address(addr)
    return ' '.join(f'{b:02x}' for b in raw)
