from __future__ import annotations
from typing import Tuple, Union

class Shape:
  def __init__(self, shape:Tuple[int, ...]) -> None:
    if not all(isinstance(x,int) for x in shape): raise TypeError("Dimension must be an integer")
    self.__shape = list(shape)
  def __repr__(self) -> str: return f"Shape({self.__shape})"
  def __len__(self) -> int: return len(self.__shape)
  def tolist(self) -> list: return self.__shape
  def totuple(self) -> tuple: return tuple(self.__shape)
  def __iter__(self): return iter(self.__shape)
  def __getitem__(self, index:int) -> int:
    if not 0 <= index < len(self): raise IndexError("Index out of range")
    return self.__shape[index]
  def numel(self):
    elements = 1
    for dim in self: elements *= dim
    return elements
  def __eq__(self, other:Union[Shape,Tuple]) -> bool: # type: ignore
    if not isinstance(other, Shape): other = Shape(other)
    if len(self.__shape) != len(other.__shape): return False
    return all(x == y for x,y in zip(self.__shape,other.__shape))
  def __ne__(self, other:Union[Shape,Tuple]) -> bool: return not self == other  # type: ignore
