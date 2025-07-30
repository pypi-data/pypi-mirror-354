"""
optimalgiv
==========

Thin Python wrapper around the registered Julia package **OptimalGIV**.

`giv` and `GIVModel` are re-exported from `. _bridge`.
"""
import juliapkg
from juliacall import Main as jl

juliapkg.resolve()
jl.seval("using Pkg; Pkg.activate(); Pkg.instantiate()")
jl.seval("using PythonCall, OptimalGIV, DataFrames, StatsModels, Tables")

from ._bridge import giv, GIVModel

__all__ = ["giv", "GIVModel"]
__version__ = "0.1.2"
