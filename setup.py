import setuptools
import os

setuptools.setup(
    name="mizore",
    version="0.1.0",
    description="A framework for hybrid quantum computing machine learning",
    packages=setuptools.find_namespace_packages(exclude=["venv"]),
    install_requires=[
        "openfermion",
        "projectq",
        "openfermionpyscf",
        "pyscf",
        "multiprocess",
        "numpy",
        "scipy"
    ]
)
