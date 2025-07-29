from unittest import TestCase

import numpy

from mullerpy import muller


def f(x: complex, n: int = 2, p: int = 612) -> complex:
    return x**n - p


def g(x: float) -> float:
    return numpy.exp(-x) * numpy.sin(x)


class TestMuller(TestCase):
    def test_quadratic_roots(self) -> None:
        x = (10, 20, 30)
        res = muller(f, x)
        self.assertAlmostEqual(res.root, 612 ** (1 / 2), delta=1e-5)

        x = (-10, -20, -30)
        res = muller(f, x)
        self.assertAlmostEqual(res.root, -(612 ** (1 / 2)), delta=1e-5)

    def test_sine_roots(self) -> None:
        x = (1, 2, 3)
        res = muller(numpy.sin, x)
        self.assertAlmostEqual(res.root, numpy.pi, delta=1e-5)

        x = (2, 4, 6)
        res = muller(numpy.sin, x)
        self.assertAlmostEqual(res.root, 2 * numpy.pi, delta=1e-5)

    def test_exp_sine_roots(self) -> None:
        x = (-2, -3, -4)
        res = muller(g, x)
        self.assertAlmostEqual(res.root, -numpy.pi, delta=1e-5)

        x = (-1, 0, 1 / 2)
        res = muller(g, x)
        self.assertAlmostEqual(res.root, 0, delta=1e-5)

        x = (-1, 0, 1)
        res = muller(g, x)
        self.assertAlmostEqual(res.root, numpy.pi, delta=1e-5)

    def test_args(self) -> None:
        n, p = 2, 612

        x = (10, 20, 30)
        res = muller(f, x, args=(n, p))
        self.assertAlmostEqual(res.root, 612 ** (1 / 2), delta=1e-5)

        x = (-10, -20, -30)
        res = muller(f, x, args=(n, p))
        self.assertAlmostEqual(res.root, -(612 ** (1 / 2)), delta=1e-5)

    def test_complex_roots(self) -> None:
        n, p = 3, 1

        x = (-1, (-1 + 1j) / 2, 1j)
        res = muller(f, x, args=(n, p))
        self.assertAlmostEqual(
            res.root, (-1 + 3 ** (1 / 2) * 1j) / 2, delta=1e-5
        )

        x = (-1, -(1 + 1j) / 2, -1j)
        res = muller(f, x, args=(n, p))
        self.assertAlmostEqual(
            res.root, -(1 + 3 ** (1 / 2) * 1j) / 2, delta=1e-5
        )

    def test_tol(self) -> None:
        x = (10, 20, 30)

        res = muller(f, x, xtol=0)
        self.assertTrue(res.converged)
        self.assertIn("function", res.flag)

        res = muller(f, x, ftol=0)
        self.assertTrue(res.converged)
        self.assertIn("root", res.flag)

    def test_errors(self) -> None:
        x = (10, 20)

        with self.assertRaises(ValueError):
            muller(f, x)

        x = (10, 20, 30)

        with self.assertRaises(ValueError):
            muller(f, x, xtol=-1e-5)

        with self.assertRaises(ValueError):
            muller(f, x, ftol=-1e-5)

        with self.assertRaises(ValueError):
            muller(f, x, maxiter=0)

    def test_iterable(self) -> None:
        n, p = 2, 612

        x = [10, 20, 30]
        res = muller(f, x, args=(n, p))
        self.assertAlmostEqual(res.root, 612 ** (1 / 2), delta=1e-5)

        x = {10, 20, 30}
        res = muller(f, x, args=(n, p))
        self.assertAlmostEqual(res.root, 612 ** (1 / 2), delta=1e-5)

        x = range(10, 31, 10)
        res = muller(f, x, args=(n, p))
        self.assertAlmostEqual(res.root, 612 ** (1 / 2), delta=1e-5)

        x = numpy.array([10, 20, 30], dtype=numpy.int64)
        res = muller(f, x, args=(n, p))
        self.assertAlmostEqual(res.root, 612 ** (1 / 2), delta=1e-5)

        x = (10, 20, 30)

        res = muller(f, x, args=[n, p])
        self.assertAlmostEqual(res.root, 612 ** (1 / 2), delta=1e-5)

        res = muller(f, x, args={n, p})
        self.assertAlmostEqual(res.root, 612 ** (1 / 2), delta=1e-5)

        res = muller(f, x, args=numpy.array([n, p], dtype=numpy.int64))
        self.assertAlmostEqual(res.root, 612 ** (1 / 2), delta=1e-5)
