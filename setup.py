import setuptools
import os
from setuptools import setup, find_packages
setup(
    name="mizore",
    version="0.1.0",
    description="A framework for adaptive quantum circuit construction",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "openfermion",
        "projectq",
        "openfermionpyscf",
        # "pyscf",
        "multiprocess",
        "numpy",
        "scipy",
        "networkx",
        "matplotlib==2.2.3",
        "minorminer",
        "infomap"
    ]
)
