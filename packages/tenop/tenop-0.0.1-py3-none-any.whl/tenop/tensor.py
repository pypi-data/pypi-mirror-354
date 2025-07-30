from __future__ import annotations
from typing import Type, Union, Sequence, Tuple
from .buffers import Buffer, LazyBuffer
from .dtypes import *
from .helpers import reshape
from .shape import Shape

Scalar = Union[int, float, complex, bool, DType]
TensorType = Union[Scalar, Sequence["TensorType"]]

class Tensor:
  def __init__(self, tensor:Union[Scalar, TensorType], dtype:Union[Type,DType,None]=None, device:str="cpu:0", requires_grad:bool=False, const:bool=False, lazy:bool=False):
    self.__lazy = lazy
    if self.__lazy: self.__buffer = LazyBuffer(tensor, dtype, device, requires_grad, const)
    else: self.__buffer = Buffer(tensor, dtype, device, requires_grad, const)
  def __repr__(self): return f"<Tensor({self.__buffer})>"
  @property
  def device(self): return self.__buffer.device
  @property
  def dtype(self): return self.__buffer.dtype
  @property
  def ndim(self): return self.__buffer.ndim
  @property
  def strides(self): return self.__buffer.stride
  @property
  def requires_grad(self): return self.__buffer.requires_grad
  @property
  def isconst(self): return self.__buffer.is_const
  @property
  def islazy(self): return self.__lazy
  @property
  def iseager(self): return not self.__lazy
  def numel(self): return self.__buffer.numel()
  def shape(self, dim:Union[int,None]=None):
    if dim is None: return self.__buffer.shape
    if not 0 <= dim < len(self.__buffer.shape): raise IndentationError("Index out of range")
    return self.__buffer.shape[dim]
  def pointer(self): return self.__buffer.ptr
  def sizeof(self): return self.__buffer.sizeof()
  def numpy(self): return self.__buffer.numpy()
  def astype(self, dtype:Union[DType, Type]):
    return Tensor(self.__buffer.data(), dtype=dtype, device=f"{self.device.type_}:{self.device.index}", requires_grad=self.requires_grad, const=self.isconst, lazy=self.islazy)
  def clone(self): return Tensor(self.__buffer.data(), device=f"{self.device.type_}:{self.device.index}", requires_grad=self.requires_grad, const=self.isconst, lazy=self.islazy)
  def lazy(self):
    if self.islazy: return self
    return Tensor(self.__buffer.data(), device=f"{self.device.type_}:{self.device.index}", requires_grad=self.requires_grad, const=self.isconst, lazy=True)
  def eager(self):
    if not self.lazy: return self
    return Tensor(self.__buffer.data(), device=f"{self.device.type_}:{self.device.index}", requires_grad=self.requires_grad, const=self.isconst, lazy=False)
  def const(self):
    if self.isconst: return self
    return Tensor(self.__buffer.data(), device=f"{self.device.type_}:{self.device.index}", requires_grad=self.requires_grad, const=True, lazy=self.islazy)
  @staticmethod
  def ones(shape:Union[Shape,Tuple], device:str="cpu:0", requires_grad:bool=False, const:bool=False, lazy:bool=False):
    if not isinstance(shape, Shape): shape = Shape(shape)
    length = shape.numel()
    return Tensor(reshape([1] * length, shape.totuple()), device=device, requires_grad=requires_grad, const=const, lazy=lazy)
  @staticmethod
  def zeros(shape:Union[Shape,Tuple], device:str="cpu:0", requires_grad:bool=False, const:bool=False, lazy:bool=False):
    if not isinstance(shape, Shape): shape = Shape(shape)
    length = shape.numel()
    return Tensor(reshape([0] * length, shape.totuple()), device=device, requires_grad=requires_grad, const=const, lazy=lazy)
  @staticmethod
  def fill(value:Scalar, shape:Union[Shape,Tuple], device:str="cpu:0", requires_grad:bool=False, const:bool=False, lazy:bool=False):
    if not isinstance(shape, Shape): shape = Shape(shape)
    length = shape.numel()
    return Tensor(reshape([value] * length, shape.totuple()), device=device, requires_grad=requires_grad, const=const, lazy=lazy)
  def __getitem__(self, index:Union[int, slice]): return Tensor(self.__buffer.__getitem__(index), device=f"{self.device.type_}:{self.device.index}", requires_grad=self.requires_grad, const=self.isconst, lazy=self.islazy)
