"""
optimalgiv
==========

Thin Python wrapper around the registered Julia package **OptimalGIV**.

Upon importing the package:
1. JuliaPkg resolves (installs) any JSON-declared deps into your project folder.
2. The Julia project (adjacent to this Python package) is activated and instantiated.
3. Required packages are loaded exactly once.
"""
import os
import juliapkg
from juliacall import Main as jl

# ─────────────────────────────────────────────────────────────────────────────
# Determine our project directory (one level up from this __init__)
# ─────────────────────────────────────────────────────────────────────────────
_pkg_root = os.path.dirname(__file__)
_project_dir = os.path.abspath(os.path.join(_pkg_root, ".."))

# ─────────────────────────────────────────────────────────────────────────────
# Bootstrap Julia environment on package import
# ─────────────────────────────────────────────────────────────────────────────
# 1) Ensure Julia & declared JSON dependencies are installed into our project
juliapkg.resolve(target=_project_dir)

# 2) Activate & instantiate that local Julia project (reads its Project.toml or JSON)
jl.seval(
    f"using Pkg; Pkg.activate(\"{_project_dir}\"); Pkg.instantiate()"
)

# 3) Load modules needed for GIV
jl.seval("using PythonCall, OptimalGIV, DataFrames, StatsModels, Tables")

# Re-export API
from ._bridge import giv, GIVModel

__all__ = ["giv", "GIVModel"]
__version__ = "0.1.2"
