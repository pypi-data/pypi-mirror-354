"""
VarAnnote Core Package

Core functionality for variant annotation and analysis.
"""

from .annotator import VariantAnnotator
from .pathogenicity import PathogenicityPredictor

__all__ = [
    "VariantAnnotator",
    "PathogenicityPredictor"
] 