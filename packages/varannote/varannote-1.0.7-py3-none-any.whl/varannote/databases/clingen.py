#!/usr/bin/env python3
"""
ClinGen Database Integration

Integration with ClinGen (Clinical Genome Resource) for gene-disease validity
and dosage sensitivity information. Provides evidence-based gene-disease associations.
"""

import requests
import json
import time
from typing import Dict, List, Optional, Tuple
from pathlib import Path

class ClinGenDatabase:
    """
    ClinGen database integration for gene-disease validity
    
    Provides access to:
    - Gene-disease validity classifications
    - Dosage sensitivity information
    - Haploinsufficiency scores
    - Triplosensitivity scores
    - Evidence levels and classifications
    """
    
    def __init__(self, cache_dir: Optional[str] = None, use_cache: bool = True):
        """
        Initialize ClinGen database connection
        
        Args:
            cache_dir: Directory for caching results
            use_cache: Whether to use local caching
        """
        self.base_url = "https://search.clinicalgenome.org/kb"
        self.api_url = "https://search.clinicalgenome.org/kb/api"
        self.cache_dir = Path(cache_dir) if cache_dir else Path.home() / ".varannote" / "cache"
        self.use_cache = use_cache
        
        # Create cache directory
        if self.use_cache:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 0.5  # Conservative rate limiting
        
        # Gene-disease validity data (fallback)
        self.clingen_data = {
            "BRCA1": {
                "clingen_gene_id": "HGNC:1100",
                "validity_classifications": [
                    {
                        "disease": "Hereditary breast and ovarian cancer syndrome",
                        "classification": "Definitive",
                        "moi": "Autosomal dominant",
                        "evidence_level": "Strong"
                    }
                ],
                "dosage_sensitivity": {
                    "haploinsufficiency": "Sufficient evidence",
                    "triplosensitivity": "No evidence",
                    "hi_score": 3,
                    "ts_score": 0
                }
            },
            "BRCA2": {
                "clingen_gene_id": "HGNC:1101",
                "validity_classifications": [
                    {
                        "disease": "Hereditary breast and ovarian cancer syndrome",
                        "classification": "Definitive", 
                        "moi": "Autosomal dominant",
                        "evidence_level": "Strong"
                    }
                ],
                "dosage_sensitivity": {
                    "haploinsufficiency": "Sufficient evidence",
                    "triplosensitivity": "No evidence",
                    "hi_score": 3,
                    "ts_score": 0
                }
            },
            "TP53": {
                "clingen_gene_id": "HGNC:11998",
                "validity_classifications": [
                    {
                        "disease": "Li-Fraumeni syndrome",
                        "classification": "Definitive",
                        "moi": "Autosomal dominant", 
                        "evidence_level": "Strong"
                    }
                ],
                "dosage_sensitivity": {
                    "haploinsufficiency": "Sufficient evidence",
                    "triplosensitivity": "No evidence",
                    "hi_score": 3,
                    "ts_score": 0
                }
            },
            "CFTR": {
                "clingen_gene_id": "HGNC:1884",
                "validity_classifications": [
                    {
                        "disease": "Cystic fibrosis",
                        "classification": "Definitive",
                        "moi": "Autosomal recessive",
                        "evidence_level": "Strong"
                    }
                ],
                "dosage_sensitivity": {
                    "haploinsufficiency": "Little evidence",
                    "triplosensitivity": "No evidence",
                    "hi_score": 1,
                    "ts_score": 0
                }
            },
            "APOE": {
                "clingen_gene_id": "HGNC:613",
                "validity_classifications": [
                    {
                        "disease": "Alzheimer disease",
                        "classification": "Moderate",
                        "moi": "Complex",
                        "evidence_level": "Moderate"
                    }
                ],
                "dosage_sensitivity": {
                    "haploinsufficiency": "No evidence",
                    "triplosensitivity": "No evidence", 
                    "hi_score": 0,
                    "ts_score": 0
                }
            }
        }
        
        # Classification levels
        self.classification_levels = {
            "Definitive": "Definitive evidence for gene-disease association",
            "Strong": "Strong evidence for gene-disease association",
            "Moderate": "Moderate evidence for gene-disease association",
            "Limited": "Limited evidence for gene-disease association",
            "No Known Disease Relationship": "No evidence for gene-disease association",
            "Disputed": "Disputed evidence for gene-disease association"
        }
    
    def _rate_limit(self):
        """Implement rate limiting for API requests"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _get_cache_path(self, gene_symbol: str) -> Path:
        """Get cache file path for gene"""
        safe_gene = gene_symbol.replace("/", "_").replace("\\", "_")
        return self.cache_dir / f"clingen_{safe_gene}.json"
    
    def _load_from_cache(self, gene_symbol: str) -> Optional[Dict]:
        """Load annotation from cache"""
        if not self.use_cache:
            return None
        
        cache_path = self._get_cache_path(gene_symbol)
        if cache_path.exists():
            try:
                with open(cache_path, 'r') as f:
                    return json.load(f)
            except Exception:
                return None
        return None
    
    def _save_to_cache(self, gene_symbol: str, data: Dict):
        """Save annotation to cache"""
        if not self.use_cache:
            return
        
        cache_path = self._get_cache_path(gene_symbol)
        try:
            with open(cache_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass
    
    def get_gene_annotation(self, gene_symbol: str) -> Dict:
        """
        Get ClinGen annotation for a specific gene
        
        Args:
            gene_symbol: Gene symbol (e.g., "BRCA1", "TP53")
            
        Returns:
            Dictionary with ClinGen annotations
        """
        # Check cache first
        cached_result = self._load_from_cache(gene_symbol)
        if cached_result:
            return cached_result
        
        try:
            # Use fallback data for now (API integration can be added later)
            annotations = self._get_clingen_data(gene_symbol)
            
            # Cache the result
            self._save_to_cache(gene_symbol, annotations)
            
            return annotations
            
        except Exception as e:
            print(f"Warning: ClinGen query failed for {gene_symbol}: {e}")
            
            # Return empty annotation
            return {
                "clingen_gene_id": None,
                "clingen_validity": None,
                "clingen_dosage_hi": None,
                "clingen_dosage_ts": None,
                "clingen_evidence": None
            }
    
    def get_variant_annotation(self, chrom: str, pos: int, ref: str, alt: str) -> Dict:
        """
        Get ClinGen annotation for a variant based on its gene location
        
        Args:
            chrom: Chromosome
            pos: Position
            ref: Reference allele
            alt: Alternative allele
            
        Returns:
            Dictionary with ClinGen annotations
        """
        # This would need gene mapping - for now return empty
        # In real implementation, would map coordinates to genes first
        return {
            "clingen_gene_id": None,
            "clingen_validity": None,
            "clingen_dosage_hi": None,
            "clingen_dosage_ts": None,
            "clingen_evidence": None
        }
    
    def _get_clingen_data(self, gene_symbol: str) -> Dict:
        """Get ClinGen data for gene"""
        
        if gene_symbol in self.clingen_data:
            gene_data = self.clingen_data[gene_symbol]
            validity_classifications = gene_data["validity_classifications"]
            dosage_sensitivity = gene_data["dosage_sensitivity"]
            
            # Extract validity information
            diseases = [v["disease"] for v in validity_classifications]
            classifications = [v["classification"] for v in validity_classifications]
            evidence_levels = [v["evidence_level"] for v in validity_classifications]
            
            return {
                "clingen_gene_id": gene_data["clingen_gene_id"],
                "clingen_validity": "; ".join(classifications),
                "clingen_diseases": "; ".join(diseases),
                "clingen_dosage_hi": dosage_sensitivity["haploinsufficiency"],
                "clingen_dosage_ts": dosage_sensitivity["triplosensitivity"],
                "clingen_evidence": "; ".join(evidence_levels),
                "clingen_hi_score": dosage_sensitivity["hi_score"],
                "clingen_ts_score": dosage_sensitivity["ts_score"]
            }
        
        return {
            "clingen_gene_id": None,
            "clingen_validity": None,
            "clingen_diseases": None,
            "clingen_dosage_hi": None,
            "clingen_dosage_ts": None,
            "clingen_evidence": None,
            "clingen_hi_score": None,
            "clingen_ts_score": None
        }
    
    def get_dosage_sensitivity(self, gene_symbol: str) -> Dict:
        """
        Get dosage sensitivity information for a gene
        
        Args:
            gene_symbol: Gene symbol
            
        Returns:
            Dictionary with dosage sensitivity information
        """
        if gene_symbol in self.clingen_data:
            dosage_data = self.clingen_data[gene_symbol]["dosage_sensitivity"]
            
            return {
                "gene": gene_symbol,
                "haploinsufficiency": dosage_data["haploinsufficiency"],
                "triplosensitivity": dosage_data["triplosensitivity"],
                "hi_score": dosage_data["hi_score"],
                "ts_score": dosage_data["ts_score"],
                "interpretation": self._interpret_dosage_scores(
                    dosage_data["hi_score"], 
                    dosage_data["ts_score"]
                )
            }
        
        return {
            "gene": gene_symbol,
            "haploinsufficiency": "Unknown",
            "triplosensitivity": "Unknown",
            "hi_score": None,
            "ts_score": None,
            "interpretation": "No dosage sensitivity data available"
        }
    
    def _interpret_dosage_scores(self, hi_score: int, ts_score: int) -> str:
        """Interpret dosage sensitivity scores"""
        
        hi_interpretation = {
            3: "Sufficient evidence for haploinsufficiency",
            2: "Some evidence for haploinsufficiency", 
            1: "Little evidence for haploinsufficiency",
            0: "No evidence for haploinsufficiency"
        }
        
        ts_interpretation = {
            3: "Sufficient evidence for triplosensitivity",
            2: "Some evidence for triplosensitivity",
            1: "Little evidence for triplosensitivity", 
            0: "No evidence for triplosensitivity"
        }
        
        hi_text = hi_interpretation.get(hi_score, "Unknown haploinsufficiency")
        ts_text = ts_interpretation.get(ts_score, "Unknown triplosensitivity")
        
        return f"{hi_text}; {ts_text}"
    
    def batch_annotate(self, variants: List[Dict]) -> List[Dict]:
        """
        Annotate multiple variants with ClinGen data
        
        Args:
            variants: List of variant dictionaries
            
        Returns:
            List of variants with ClinGen annotations added
        """
        annotated_variants = []
        
        for i, variant in enumerate(variants):
            print(f"Annotating variant {i+1}/{len(variants)} with ClinGen...")
            
            try:
                # Get gene symbol from variant
                gene_symbol = variant.get("gene_symbol")
                
                if gene_symbol and gene_symbol != "intergenic":
                    clingen_data = self.get_gene_annotation(gene_symbol)
                else:
                    clingen_data = {
                        "clingen_gene_id": None,
                        "clingen_validity": None,
                        "clingen_diseases": None,
                        "clingen_dosage_hi": None,
                        "clingen_dosage_ts": None,
                        "clingen_evidence": None,
                        "clingen_hi_score": None,
                        "clingen_ts_score": None
                    }
                
                # Add ClinGen annotations to variant
                annotated_variant = {**variant, **clingen_data}
                annotated_variants.append(annotated_variant)
                
            except Exception as e:
                print(f"Warning: Failed to annotate variant {variant.get('variant_id', 'unknown')}: {e}")
                # Add empty annotations
                annotated_variant = {
                    **variant,
                    "clingen_gene_id": None,
                    "clingen_validity": None,
                    "clingen_diseases": None,
                    "clingen_dosage_hi": None,
                    "clingen_dosage_ts": None,
                    "clingen_evidence": None,
                    "clingen_hi_score": None,
                    "clingen_ts_score": None
                }
                annotated_variants.append(annotated_variant)
        
        return annotated_variants
    
    def get_database_info(self) -> Dict:
        """Get information about ClinGen database"""
        return {
            "name": "ClinGen",
            "description": "Clinical Genome Resource - Gene-disease validity and dosage sensitivity",
            "url": "https://clinicalgenome.org/",
            "api_url": self.api_url,
            "version": "Current",
            "last_updated": "Monthly",
            "data_types": [
                "Gene-disease validity",
                "Dosage sensitivity",
                "Haploinsufficiency scores",
                "Triplosensitivity scores",
                "Evidence classifications"
            ],
            "requires_api_key": False
        } 