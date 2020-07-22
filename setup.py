import setuptools
import os

setuptools.setup(
    name="mizore",
    version="0.1.0",
    description="A framework for hybrid quantum computing machine learning",
    packages=setuptools.find_namespace_packages(),
    install_requires=[
        'numpy>=1.18.1',
    ]
)
