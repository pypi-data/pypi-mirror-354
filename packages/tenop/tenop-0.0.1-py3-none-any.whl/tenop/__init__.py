from typing import Union, Sequence, Type
from .tensor import Tensor
from .shape import Shape
from .dtypes import (
  DType,
  boolean,
  bool_,
  uint8,
  uint16,
  uint32,
  uint64,
  uchar,
  ushort,
  uint,
  ulong,
  ulonglong,
  int8,
  int16,
  int32,
  int64,
  char,
  short,
  int_,
  long,
  longlong,
  float32,
  float64,
  float_,
  double,
  longdouble,
  floatcomplex,
  doublecomplex,
  longdoublecomplex,
  complex64,
  complex128,
  complex256
)

Scalar = Union[int, float, complex, bool, DType]
TensorType = Union[Scalar, Sequence["TensorType"]]

def tensor(array:TensorType, dtype:Union[DType,Type,None]=None, device:str="cpu:0", requires_grad:bool=False, const:bool=False, lazy:bool=False):
  return Tensor(array, dtype=dtype, device=device, requires_grad=requires_grad, const=const, lazy=lazy)

__all__ = [
  "Scalar",
  "TensorType",
  "Tensor",
  "Shape",
  "tensor",
  "boolean",
  "bool_",
  "uint8",
  "uint16",
  "uint32",
  "uint64",
  "uchar",
  "ushort",
  "uint",
  "ulong",
  "ulonglong",
  "int8",
  "int16",
  "int32",
  "int64",
  "char",
  "short",
  "int_",
  "long",
  "longlong",
  "float32",
  "float64",
  "float_",
  "double",
  "longdouble",
  "floatcomplex",
  "doublecomplex",
  "longdoublecomplex",
  "complex64",
  "complex128",
  "complex256"
]
