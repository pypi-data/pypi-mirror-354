import re

import numpy
from Cython.Build import cythonize
from setuptools import Extension, setup

ext = Extension(
    name="recfast4py._recfast",
    ext_modules=cythonize("src/recfast4py/_recfast.pyx", language="c++"),
    sources=[
        "src/recfast4py/_recfast.cpp",
        "src/recfast4py/cosmology.Recfast.cpp",
        "src/recfast4py/evalode.Recfast.cpp",
        "src/recfast4py/recombination.Recfast.cpp",
        "src/recfast4py/ODE_solver.Recfast.cpp",
        "src/recfast4py/DM_annihilation.Recfast.cpp",
        "src/recfast4py/Rec_corrs_CT.Recfast.cpp",
    ],
    include_dirs=[numpy.get_include()],
    export_symbols=["_installPath"],
)

print(dir(ext))
print(ext.sources)
print(ext.export_symbols)

for p in ext.sources:
    if p.endswith("/_recfast.cpp"):
        with open(p) as fh:
            content = fh.read()
        content = re.sub(
            r"__PYX_EXTERN_C DL_EXPORT\(std::string\) installPath",
            "extern DL_EXPORT(std::string) installPath",
            content,
        )
        with open(p, "w") as fh:
            fh.write(content)

setup(ext_modules=[ext])
