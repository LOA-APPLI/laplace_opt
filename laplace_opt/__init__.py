# libraries
from importlib.metadata import version, PackageNotFoundError

# project
from .interface import OptWindow


try:
    __version__ = version("laplace-opt")
except PackageNotFoundError:
    __version__ = "0.0.0"


__all__ = [
    "__version__",
    "OptWindow",
]

__doc__ = """
Laplace optimization code (laplace_opt)

Usage
-----
See the laplace_opt.main file to get an example.
"""