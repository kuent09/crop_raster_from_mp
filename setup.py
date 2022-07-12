# coding: utf-8

"""
Installation setup
"""

# Third party
from setuptools import find_packages
from setuptools import setup

VERSION = "0.0.0"

setup(
    name="crop-raster-from-mp",
    version=VERSION,
    description="Crop a raster with microplots",
    author="Alteia Data Team",
    author_email="data@alteia.com",
    url="http://srvdev.delair.local/delair-stack/data/crop-raster-from-mp",
    packages=find_packages(exclude=["docs", "tests"]),
    install_requires=[
        "click==7.1.2",
        "rasterio==1.2.10"
    ],
)
