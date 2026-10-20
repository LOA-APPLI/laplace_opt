# libraries
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("laplace-opt")
except PackageNotFoundError:
    __version__ = "0.0.0"

# project
from .interface import OptWindow

__all__ = [
    "__version__",
    "OptWindow",
]

__doc__ = """
Laplace optimizer (laplace_opt)

Usage
-----
See the laplace_opt.main file to get an example of entry point.
"""