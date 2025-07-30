import os
import juliapkg
from juliacall import Main as jl
import pathlib

# 1) Compute the path to this package directory
_pkg_dir = pathlib.Path(__file__).parent.resolve()

# 2) Tell JuliaPkg to use _pkg_dir as *the* project
os.environ["PYTHON_JULIAPKG_PROJECT"] = str(_pkg_dir)

# 3) Now resolve (reads juliapkg.json in _pkg_dir)
juliapkg.resolve()

# 4) Activate & instantiate that project
jl.seval(f'''
    import Pkg
    Pkg.activate("{_pkg_dir}")
    Pkg.instantiate()
''')

# 5) Finally load OptimalGIV & friends
jl.seval("using PythonCall, OptimalGIV, DataFrames, StatsModels, Tables")

from ._bridge import giv, GIVModel

__all__ = ["giv", "GIVModel"]
__version__ = "0.1.3"
