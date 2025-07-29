"""
VarAnnote Real Databases Package

Integration with real bioinformatics databases including:
- ClinVar (NCBI)
- gnomAD (Broad Institute)
- dbSNP (NCBI)
- COSMIC (Sanger Institute)
- OMIM (Johns Hopkins)
- PharmGKB (Stanford)
- ClinGen (Clinical Genome Resource)
- HGMD (Human Gene Mutation Database)
- Ensembl (European Bioinformatics Institute)
"""

from .clinvar import ClinVarDatabase
from .gnomad import GnomADDatabase
from .dbsnp import DbSNPDatabase
from .cosmic import COSMICDatabase
from .omim import OMIMDatabase
from .pharmgkb import PharmGKBDatabase
from .clingen import ClinGenDatabase
from .hgmd import HGMDDatabase
from .ensembl import EnsemblDatabase

__all__ = [
    "ClinVarDatabase",
    "GnomADDatabase", 
    "DbSNPDatabase",
    "COSMICDatabase",
    "OMIMDatabase",
    "PharmGKBDatabase",
    "ClinGenDatabase",
    "HGMDDatabase",
    "EnsemblDatabase"
] 