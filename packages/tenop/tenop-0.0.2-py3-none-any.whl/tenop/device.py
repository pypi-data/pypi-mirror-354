from .engine import cuda, cpu

DEVICES = ["cpu", "cuda"]

class Device:
  def __init__(self, device: str):
    parts = device.lower().split(":")
    if parts[0] not in DEVICES: raise ValueError(f"Unknown device type '{parts[0]}'")
    self.__type = parts[0]
    self.__index = 0
    if len(parts) == 2:
      try: self.__index = abs(int(parts[1]))
      except ValueError: raise ValueError(f"Invalid device index in '{device}'")
    if self.__type == "cpu":
      if self.__index != 0: raise ValueError("CPU does not support indexing other than 0")
    elif self.__type == "cuda":
      available = cuda.count()
      if abs(self.__index) >= available: raise RuntimeError(f"CUDA device index {self.__index} exceeds available devices ({available})")
  def __repr__(self): return f"<Device(device='{self.__type}', index={self.__index})>"
  @property
  def type_(self): return self.__type
  @property
  def index(self): return self.__index
  @property
  def name(self):
    if self.__type == "cuda": return cuda.get_device_name(self.__index)
    elif self.__type == "cpu": return cpu.get_device_name()[2:]
