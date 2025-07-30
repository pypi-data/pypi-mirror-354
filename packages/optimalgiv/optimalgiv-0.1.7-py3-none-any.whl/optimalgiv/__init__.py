import os
import pathlib
import sys

# 1) Compute path FIRST
_pkg_dir = pathlib.Path(__file__).parent.resolve()

# 2) Set environment variable BEFORE importing Julia-related modules
os.environ["PYTHON_JULIAPKG_PROJECT"] = str(_pkg_dir)

# 3) Now import Julia modules
import juliapkg
from juliacall import Main as jl

# 4) Resolve and setup Julia environment
if not hasattr(sys, "_julia_env_initialized"):
    juliapkg.resolve()  # Reads juliapkg.json

    jl.seval(f"""
        import Pkg
        Pkg.activate("{_pkg_dir}")
        Pkg.instantiate()  # Downloads dependencies
    """)

    jl.seval("using PythonCall, OptimalGIV, DataFrames, StatsModels, Tables")
    sys._julia_env_initialized = True  # Prevent re-initialization

# 5) Import Python API
from ._bridge import giv, GIVModel

__all__ = ["giv", "GIVModel"]
__version__ = "0.1.7"