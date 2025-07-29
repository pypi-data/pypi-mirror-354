# -*- coding: utf-8 -*-
"""
Created on Sun Jun  8 15:01:48 2025

@author: admin
"""


from setuptools import setup, find_packages
import os

VERSION = '0.0.1'
DESCRIPTION = 'Calculation of Convertible Bond Value'

setup(
    name="convertbonds",
    version=VERSION,
    author="Taisen Zheng",
    author_email="jc3802201@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    #long_description=open('README.md',encoding="UTF8").read(),
    long_description="A simple tool for calculating convertible bond value.",

    packages=find_packages(),
    
    keywords=['python', 'convertbonds'],
    #data_files=[('', [''])],

    license="MIT",
    url="https://github.com/",
    #scripts=['convertbonds.py'],
    entry_points={'console_scripts': ['convertbonds=convertbonds:main',],
    },
    
    
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows"
    ],
    
    python_requires=">=3",
    install_requires=["matplotlib>=3.5.2","scipy>=1.9.1"]
    
    
    
)
