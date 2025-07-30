from typing import Optional, Union, Sequence
from .dtypes import DType

Scalar = Union[int, float, complex, bool, DType]
TensorType = Union[Scalar, Sequence["TensorType"]]

def colored(string, color:Optional[str], background=False): return f"\u001b[{10*background+60*(color.upper() == color)+30+['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'].index(color.lower())}m{string}\u001b[0m" if color is not None else string

def flatten(data:TensorType):
  if not isinstance(data, list): return [data]
  flat = []
  for x in data: flat.extend(flatten(x))
  return flat

def infer_shape(lst) -> tuple:
  if not isinstance(lst, list):return ()
  if len(lst) == 0:return (0,)
  return (len(lst),) + infer_shape(lst[0])

def has_uniform_shape(lst):
  if not isinstance(lst, list): return True
  lengths = [len(x) if isinstance(x, list) else -1 for x in lst]
  if len(set(lengths)) != 1: return False
  return all(has_uniform_shape(x) for x in lst)

def reshape(array, shape):
  if len(shape) == 0: return array
  def build(shape, index):
    if len(shape) == 0:
      val = array[index[0]]
      index[0] += 1
      return val
    return [build(shape[1:], index) for _ in range(shape[0])]
  return build(shape, [0])
