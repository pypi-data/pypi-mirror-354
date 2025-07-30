<p align="center">
  <img src="./docs/tenop.png" alt="Tenop Logo" width="300">
</p>

<div align="center">
  <a href="https://pypi.org/project/tenop/">
    <img src="https://img.shields.io/pypi/v/tenop" alt="PyPI - Version">
  </a>
  <a href="https://pypi.org/project/tenop/">
    <img src="https://img.shields.io/pypi/pyversions/tenop" alt="PyPI - Python Version">
  </a>
  <a href="https://github.com/0xhilSa/tenop/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/0xhilSa/tenop" alt="License">
  </a>
</div>


<p align="center">
  <strong>TenOp</strong> is a lightweight and minimalist tensor computation library with CUDA acceleration, designed for high-performance numerical computing.
</p>

---

## 🚀 Features

- Simple tensor operations with a clean API
- Optimized backend with CPU and CUDA support
- Written in Python with compiled C/CUDA extensions

## 📦 Installation
```bash
pip install tenop
```

## Or install from source
```bash
git clone https://github.com/0xhilSa/tenop.git
cd tenop
pip install .
```

## Usage
```python
from tenop import Tensor

x = Tensor([1,2,3,4,5], device="cpu:0")
print(x)
print(x.device, x.device.name)
print(x.lazy()) # make Tensor lazy

y = x.cuda()    # store Tensor on CUDA device
print(y)
print(y.device, y.device.name)
print(y.lazy())
```
See [./tests/test.py](./tests/test.py) and [./tests/testing.ipynb](./tests/testing.ipynb) for more examples

---

## LICENSE
[MIT](./LICENSE)
