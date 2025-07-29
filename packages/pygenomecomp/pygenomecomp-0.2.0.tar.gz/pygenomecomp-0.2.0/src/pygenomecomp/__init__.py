"""
PyGenomeComp: A Python tool for circular visualization of genome comparisons.

This package provides utilities for running BLAST comparisons, parsing annotations,
and generating SVG plots to visualize the results.
"""

# Define the package version. It's a good practice to have a single source of truth.
# This should match the version in your pyproject.toml.
__version__ = "0.2.0"

# Import key functions and classes to make them accessible at the package level.
# This creates a clean, user-friendly API for anyone using pygenomecomp as a library.
from .main import main
from .blast import make_blast_db, run_blastn, parse_blast_output
from .annotation import parse_annotations, AnnotationFeature
from .plot import generate_plot

# The __all__ variable defines the public API of the package.
# When a user does `from pygenomecomp import *`, only these names will be imported.
__all__ = [
    # From main.py
    "main",
    
    # From blast.py
    "make_blast_db",
    "run_blastn",
    "parse_blast_output",

    # From annotation.py
    "parse_annotations",
    "AnnotationFeature",

    # From plot.py
    "generate_plot",
]
