<div align="center">
    <img src="assets/logo.png" alt="mullerpy logo" width="300">
</div>

[![PyPI version](https://img.shields.io/pypi/v/mullerpy.svg)](https://pypi.org/project/mullerpy/)

# mullerpy

A Python implementation of Muller's method.

---

## Usage

This library requires no dependencies beyond the Python standard library.

Here is a quick example to show how it is used:

```python
from mullerpy import muller
from math import exp, sin

def f(x):
    return exp(-x) * sin(x)

xguesses = (-1, 0, 1)
res = muller(f, xguesses)

print(res.root)
```

This finds a root of the function

$$
f(x) = e^{-x} \sin(x),
$$

which has roots at $x = n \pi$ for integer $n$. The result object has a `.root` attribute storing the estimated solution.

## Installation

It is easy to install `mullerpy` with `pip`:

```
pip install mullerpy
```

## Testing

To test, run

```
python -m unittest tests.test_muller
```

in the root directory. I like to use `pytest`, where you can simply enter

```
pytest
```
