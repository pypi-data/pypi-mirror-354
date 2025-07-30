"""
optimalgiv
==========

Thin Python wrapper around the registered Julia package **OptimalGIV**.

`giv` and `GIVModel` are re-exported from `. _bridge`.
"""
import juliapkg
from juliacall import Main as jl
import os

juliapkg.resolve()
_pkg_root = os.path.dirname(__file__)
_project_dir = os.path.abspath(os.path.join(_pkg_root, ".."))
jl.seval(f"using Pkg; Pkg.activate(\"{_project_dir}\"); Pkg.instantiate()")
jl.seval("using PythonCall, OptimalGIV, DataFrames, StatsModels, Tables")

from ._bridge import giv, GIVModel

__all__ = ["giv", "GIVModel"]
__version__ = "0.1.3"
