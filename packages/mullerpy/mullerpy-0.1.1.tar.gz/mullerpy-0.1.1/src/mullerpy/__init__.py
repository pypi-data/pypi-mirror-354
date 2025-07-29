"""A Python implementation of Muller's method."""

from importlib.metadata import version

from .muller import muller

__all__ = ["muller"]
__version__ = version("mullerpy")
