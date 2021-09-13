#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 11:12:10 2021
@author: set
"""
import setuptools

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

import glob
def recursive_dir_walker(dir):
    files = [recursive_dir_walker(directory) for directory in glob.glob(f'{dir}/*')]
    if len(files) == 0: files = [[dir]]
    return sum(files, [])

datafiles = []#recursive_dir_walker("ABC/*")

setuptools.setup(
    name="question answering dataloader",
    version="0.0.0",
    author="Hosu Lee",
    author_email="leehosu01@naver.com",
    description="question answering efficient dataloader based on pytorch, with multiple answer candidates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leehosu01/question-answering-dataloader",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=requirements,
    data_files = datafiles,
    include_package_data=True
)