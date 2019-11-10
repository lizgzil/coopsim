import os

import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="Cooperation Simulation",
    version="",
    author="Liz Gallagher",
    author_email="lizgzil@hotmail.com",
    description="Run a prisoner's dilemma game",
    long_description="Run a prisoner's dilemma game",
    long_description_content_type="text/markdown",
    url="",
    license="",
    packages=setuptools.find_packages(
        include=["coopsim"],
        exclude=["notebooks", "tests", "build"]
    ),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "jupyter",
        "matplotlib",
        "numpy",
        "openpyxl",
        "pandas",
        "xlrd",
    ],
    tests_require=[
        "pytest"
    ]
)