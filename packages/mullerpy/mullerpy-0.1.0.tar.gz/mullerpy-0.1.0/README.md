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

You can install `mullerpy` in one of the following ways:

### From source (locally)

Clone the repository and install using `pip`:

```
git clone https://github.com/fgittins/mullerpy.git
cd mullerpy
pip install .
```

### Directly from GitHub

Or you can install directly from GitHub:

```
pip install git+https://github.com/fgittins/mullerpy.git
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
