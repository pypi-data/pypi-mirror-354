"""
VarAnnote Utilities Package

Common utilities for variant processing and annotation.
"""

from .vcf_parser import VCFParser
from .annotation_db import AnnotationDatabase

__all__ = [
    "VCFParser",
    "AnnotationDatabase"
] 