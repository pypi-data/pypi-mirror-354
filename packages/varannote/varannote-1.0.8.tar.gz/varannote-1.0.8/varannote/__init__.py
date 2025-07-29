"""
VarAnnote - Comprehensive Variant Analysis & Annotation Suite

A powerful toolkit for genomic variant annotation and clinical interpretation.
Developed for bioinformatics researchers and clinical genomics applications.

Author: Ata Umut ÖZSOY
License: MIT
"""

__version__ = "1.0.8"
__author__ = "Ata Umut ÖZSOY"
__email__ = "ataumut7@gmail.com"

# Core modules
from .core import VariantAnnotator, PathogenicityPredictor
from .utils import VCFParser, AnnotationDatabase
from .cli import main

__all__ = [
    "VariantAnnotator",
    "PathogenicityPredictor", 
    "VCFParser",
    "AnnotationDatabase",
    "main"
] 