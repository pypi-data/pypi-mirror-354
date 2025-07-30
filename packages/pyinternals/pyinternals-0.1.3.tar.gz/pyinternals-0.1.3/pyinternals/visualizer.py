# coding: utf-8
import ctypes

from .cpy_layouts import PyObject, PyLongObject, PyUnicodeObject, PyDictObject
from .cpy_layouts import PyFloatObject, PyListObject, PyTupleObject, PySetObject

def inspect_int(obj):
    assert isinstance(obj, int), "Pass a Integer!"
    addr = id(obj)
    obj = ctypes.cast(addr, ctypes.POINTER(PyLongObject)).contents
    print(f"\n---> Int at {hex(addr)}:")
    print("-" * 40)
    print(f"{'Field':<15} | {'Value'}") 
    print("-" * 40)    
    print(f"{'Reference count':<15} | {obj.ob_refcnt}")
    print(f"{'Type address':<15} | {hex(obj.ob_type)}")    
    print(f"{'Size': <15} | {obj.ob_size}")
    print("\nDigits (base 2^30):")
    for i in range(abs(obj.ob_size)):
        print(f"  ob_digit[{i}]   | {obj.ob_digit[i]}")
    print("-" * 40)
    
def inspect_float(value):
    assert isinstance(value, float), "Pass a Float!"
    addr = id(value)
    obj = ctypes.cast(addr, ctypes.POINTER(PyFloatObject)).contents

    print(f"\n---> Float at {hex(addr)}:")
    print("-" * 40)
    print(f"{'Field':<15} | {'Value'}") 
    print("-" * 40)    
    print(f"{'Reference count':<15} | {obj.ob_refcnt}")
    print(f"{'Type address':<15} | {hex(obj.ob_type)}")    
    print(f"{'Value':<15} | {obj.ob_fval}")
    print("-" * 40)
    

def inspect_str(s: str):
    assert isinstance(s, str), "Pass a String!"
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
    print(f"{'Reference count':<15} | {obj.ob_refcnt}")
    print(f"{'Type address':<15} | {hex(obj.ob_type)}")    
    print(f"{'Hash':<15} | {obj.hash}")
    Int_MAP = {
    0: " Not Interned",
    1: "Interned",
    2: "Interned and Immortal",
    3: "Interned, Immortal, and Static"
    }
    print(f"{'Tnterned':<15} | {Int_MAP[interned]}")
    KIND_MAP = {
    0: "INVALID",
    1: "1BYTE",
    2: "2BYTE",
    4: "4BYTE"
}
    print(f"{'Kind':<15} | {kind} → {KIND_MAP.get(kind, 'UNKNOWN')}")
    print(f"{'Compact':<15} | {bool(compact)}")
    print(f"{'Ascii':<15} | {bool(ascii)}")
    print(f"{'Utf8_length':<15} | {len(s.encode('utf-8'))}")
    print("-" * 40)
    

def inspect_dict(dobj):
    assert isinstance(dobj, dict), "Pass a Dict!"
    addr = id(dobj)
    obj = ctypes.cast(addr, ctypes.POINTER(PyDictObject)).contents
    pk, pv = obj.ma_keys, obj.ma_values
    print(f"\n---> Dict at {hex(addr)}:")
    print("-" * 40)    
    print(f"{'Field':<15} | {'Value'}") 
    print("-" * 40)    
    print(f"{'Reference count':<15} | {obj.ob_refcnt}")
    print(f"{'Type address':<15} | {hex(obj.ob_type)}")    
    print(f"{'Used':<15} | {obj.ma_used}")
    print(f"{'Keys':<15} | {hex(pk) if pk is not None else None}")
    if pv:
        print(f"{'Values (split)':<15} | {hex(pv)}") # keys are shared
    else:
        print(f"{'Values (combined)':<15} | {pv}") # keys and values are stored in the dict

    # Visual mapping (not raw memory)
    print("\n  Contents:")
    if len(dobj) == 0: print("    empty")
    for k, v in dobj.items():
        print(f"    {repr(k)}: {repr(v)}")
    print("-" * 40)
    

def inspect_list(lst):
    assert isinstance(lst, list), "Pass a List!"
    addr = id(lst)
    obj = ctypes.cast(addr, ctypes.POINTER(PyListObject)).contents

    print(f"\n---> List at {hex(addr)}:")
    print("-" * 40)
    print(f"{'Field':<15} | {'Value'}") 
    print("-" * 40)    
    print(f"{'Reference count':<15} | {obj.ob_refcnt}")
    print(f"{'Type address':<15} | {hex(obj.ob_type)}")    
    print(f"{'Size':<15} | {obj.ob_size}")
    print(f"{'Allocated':<15} | {obj.ob_allocated}")
    print(f"{'Items':<15} | {hex(ctypes.addressof(obj.ob_items.contents))}")

    print("\nElements:")
    for i in range(obj.ob_size):
        ptr = obj.ob_items[i]  # this is a PyObject* (just an address)
        val = ctypes.cast(ptr, ctypes.py_object).value
        print(f"    {i}] @ {hex(ptr)}: {repr(val):<10} | {val.__class__.__name__}")
    print("-" * 40)
    
def inspect_tuple(tpl):
    assert isinstance(tpl, tuple), "Pass a Tuple!"
    addr = id(tpl)
    obj = ctypes.cast(addr, ctypes.POINTER(PyTupleObject)).contents

    print(f"\n---> Tuple at {hex(addr)}:")
    print("-" * 40)
    print(f"{'Field':<15} | {'Value'}") 
    print("-" * 40)    
    print(f"{'Reference count':<15} | {obj.ob_refcnt}")
    print(f"{'Type address':<15} | {hex(obj.ob_type)}")    
    print(f"{'Size':<15} | {obj.ob_size}")
    print(f"{'Items':<15} | {hex(ctypes.addressof(obj.ob_items.contents))}")

    print("\nElements:")
    for i, elm in enumerate(tpl):
        print(f"    {i}] @ {hex(id(elm))}: {elm:<10} | {elm.__class__.__name__}")
    print("-" * 40)
    
def inspect_set(sobj):
    assert isinstance(sobj, set), "Pass a Set!"
    addr = id(sobj)
    obj = ctypes.cast(addr, ctypes.POINTER(PySetObject)).contents

    print(f"\n---> Tuple at {hex(addr)}:")
    print("-" * 40)
    print(f"{'Field':<15} | {'Value'}") 
    print("-" * 40)    
    print(f"{'Reference count':<15} | {obj.ob_refcnt}")
    print(f"{'Type address':<15} | {hex(obj.ob_type)}")    
    print(f"{'Fill':<15} | {obj.fill}")
    print(f"{'Used':<15} | {obj.used}")
    print(f"{'Mask':<15} | {obj.mask}")
    print(f"{'Table':<15} | {hex(ctypes.addressof(obj.table))}")
    print(f"{'Hash':<15} | {obj.hash}")
    print(f"{'Weakreflist':<15} | {obj.weakreflist}")

    print("\nElements:")
    for i, elm in enumerate(sobj):
        print(f"    {i}] @ {hex(id(elm))}: {elm:<10} | {elm.__class__.__name__}")


def hexdump(obj, size=64):
    addr = id(obj)
    raw = (ctypes.c_ubyte * size).from_address(addr)
    return ' '.join(f'{b:02x}' for b in raw)

def inspect_instance(iobj):
    assert hasattr(iobj, '__dict__') or hasattr(iobj, '__slots__'), "Pass Instance has dict or slots!"    
    addr = id(iobj)
    obj = ctypes.cast(addr, ctypes.POINTER(PyObject)).contents
    print(f"\n---> Instancs at {hex(addr)}:")
    print("-" * 40)
    print(f"{'Field':<15} | {'Value'}") 
    print("-" * 40)    
    print(f"{'Reference count':<15} | {obj.ob_refcnt}")
    print(f"{'Type address':<15} | {hex(obj.ob_type)}")
    if hasattr(iobj, '__dict__'):
        print("-" * 40)
        print("\nThe Instance dict inspection :")
        inspect_dict(iobj.__dict__)
    elif hasattr(iobj, '__slots__'):
        print("-" * 40)
        print("\nThe Instance slots inspection :")
        print("-" * 40)                
        print(f"\n---> Slots at {hex(id(iobj.__slots__))}:")
        print("\n  Contents:")
        for s in type(iobj).__slots__:
            if hasattr(iobj, s):
                print(f"    '{s}' : {getattr(iobj, s)}")
        print("-" * 40)
        
    else:
        print("\nThe Instance attributes maybe implemented in C")
        print("-" * 40)
        

def inspect_obj(obj):
    if isinstance(obj, int):
        inspect_int(obj)
    elif isinstance(obj, float):
        inspect_float(obj)
    elif isinstance(obj, str):
        inspect_str(obj)
    elif isinstance(obj, tuple):
        inspect_tuple(obj)
    elif isinstance(obj, list):
        inspect_list(obj)
    elif isinstance(obj, set):
        inspect_set(obj)
    elif isinstance(obj, dict):
        inspect_dict(obj)
    elif hasattr(obj, '__dict__') or hasattr(obj, '__slots__'):
        inspect_instance(obj)
    else: print("The object inspection not implemented yet!")