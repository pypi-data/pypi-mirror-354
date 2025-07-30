import importlib.metadata

__author__ = "Ivan Zanardi"
__email__ = "zanardi3@illinois.edu"
__url__ = "https://github.com/ivanZanardi/pyharmx"
__license__ = "MIT License"
__version__ = importlib.metadata.version("pyharmx")
__all__ = ["PolyHarmInterpolator"]

from .interpolator import PolyHarmInterpolator
