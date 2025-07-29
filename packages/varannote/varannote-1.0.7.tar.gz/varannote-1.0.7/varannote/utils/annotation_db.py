#!/usr/bin/env python3
"""
Annotation Database - Mock database for variant annotations
"""

from typing import Dict, List, Optional
import random

class AnnotationDatabase:
    """
    Mock annotation database for testing
    
    In a real implementation, this would connect to actual databases
    like ClinVar, gnomAD, COSMIC, etc.
    """
    
    def __init__(self, genome: str = "hg38"):
        """
        Initialize annotation database
        
        Args:
            genome: Reference genome version
        """
        self.genome = genome
        
        # Mock database contents
        self.clinvar_data = {
            "17:43044295:G>A": {"clinvar_significance": "Pathogenic", "clinvar_id": "VCV000001"},
            "17:7577121:C>T": {"clinvar_significance": "Likely_pathogenic", "clinvar_id": "VCV000002"},
            "13:32315086:T>C": {"clinvar_significance": "Benign", "clinvar_id": "VCV000003"},
        }
        
        self.gnomad_data = {
            "17:43044295:G>A": {"gnomad_af": 0.0001, "gnomad_ac": 12, "gnomad_an": 120000},
            "17:7577121:C>T": {"gnomad_af": 0.0005, "gnomad_ac": 60, "gnomad_an": 120000},
            "13:32315086:T>C": {"gnomad_af": 0.15, "gnomad_ac": 18000, "gnomad_an": 120000},
        }
        
        self.cosmic_data = {
            "17:7577121:C>T": {"cosmic_id": "COSM12345", "cosmic_count": 45},
            "13:32315086:T>C": {"cosmic_id": "COSM67890", "cosmic_count": 12},
        }
        
        self.dbsnp_data = {
            "17:43044295:G>A": {"dbsnp_id": "rs80357713"},
            "17:7577121:C>T": {"dbsnp_id": "rs28934576"},
            "13:32315086:T>C": {"dbsnp_id": "rs144848"},
        }
    
    def get_annotations(self, variant: Dict, database: str = "all") -> Dict:
        """
        Get annotations for a variant from specified database(s)
        
        Args:
            variant: Variant dictionary
            database: Database name or "all"
            
        Returns:
            Dictionary with annotations
        """
        annotations = {}
        variant_key = self._get_variant_key(variant)
        
        if database == "all" or database == "clinvar":
            clinvar_annotations = self._get_clinvar_annotations(variant_key)
            annotations.update(clinvar_annotations)
        
        if database == "all" or database == "gnomad":
            gnomad_annotations = self._get_gnomad_annotations(variant_key)
            annotations.update(gnomad_annotations)
        
        if database == "all" or database == "cosmic":
            cosmic_annotations = self._get_cosmic_annotations(variant_key)
            annotations.update(cosmic_annotations)
        
        if database == "all" or database == "dbsnp":
            dbsnp_annotations = self._get_dbsnp_annotations(variant_key)
            annotations.update(dbsnp_annotations)
        
        return annotations
    
    def _get_variant_key(self, variant: Dict) -> str:
        """Generate variant key for database lookup"""
        return f"{variant['CHROM']}:{variant['POS']}:{variant['REF']}>{variant['ALT']}"
    
    def _get_clinvar_annotations(self, variant_key: str) -> Dict:
        """Get ClinVar annotations"""
        if variant_key in self.clinvar_data:
            return self.clinvar_data[variant_key]
        else:
            # Return mock data for unknown variants
            significances = ["Uncertain_significance", "Benign", "Likely_benign", "Pathogenic", "Likely_pathogenic"]
            return {
                "clinvar_significance": random.choice(significances),
                "clinvar_id": f"VCV{random.randint(100000, 999999)}"
            }
    
    def _get_gnomad_annotations(self, variant_key: str) -> Dict:
        """Get gnomAD population frequency annotations"""
        if variant_key in self.gnomad_data:
            return self.gnomad_data[variant_key]
        else:
            # Generate mock frequency data
            af = random.uniform(0.0001, 0.5)
            an = 120000
            ac = int(af * an)
            return {
                "gnomad_af": round(af, 6),
                "gnomad_ac": ac,
                "gnomad_an": an
            }
    
    def _get_cosmic_annotations(self, variant_key: str) -> Dict:
        """Get COSMIC cancer mutation annotations"""
        if variant_key in self.cosmic_data:
            return self.cosmic_data[variant_key]
        else:
            # 30% chance of being in COSMIC
            if random.random() < 0.3:
                return {
                    "cosmic_id": f"COSM{random.randint(10000, 999999)}",
                    "cosmic_count": random.randint(1, 100)
                }
            return {}
    
    def _get_dbsnp_annotations(self, variant_key: str) -> Dict:
        """Get dbSNP annotations"""
        if variant_key in self.dbsnp_data:
            return self.dbsnp_data[variant_key]
        else:
            # 70% chance of having dbSNP ID
            if random.random() < 0.7:
                return {"dbsnp_id": f"rs{random.randint(1000, 999999999)}"}
            return {}
    
    def get_available_databases(self) -> List[str]:
        """Get list of available databases"""
        return ["clinvar", "gnomad", "cosmic", "dbsnp"]
    
    def get_database_info(self, database: str) -> Dict:
        """Get information about a specific database"""
        database_info = {
            "clinvar": {
                "name": "ClinVar",
                "description": "Clinical significance of variants",
                "version": "2024-01",
                "url": "https://www.ncbi.nlm.nih.gov/clinvar/"
            },
            "gnomad": {
                "name": "gnomAD",
                "description": "Population allele frequencies",
                "version": "v3.1.2",
                "url": "https://gnomad.broadinstitute.org/"
            },
            "cosmic": {
                "name": "COSMIC",
                "description": "Catalogue of Somatic Mutations in Cancer",
                "version": "v97",
                "url": "https://cancer.sanger.ac.uk/"
            },
            "dbsnp": {
                "name": "dbSNP",
                "description": "Single Nucleotide Polymorphism Database",
                "version": "b155",
                "url": "https://www.ncbi.nlm.nih.gov/snp/"
            }
        }
        
        return database_info.get(database, {}) 