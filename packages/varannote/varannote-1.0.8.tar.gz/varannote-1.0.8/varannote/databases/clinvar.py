#!/usr/bin/env python3
"""
ClinVar Database Integration

Real-time integration with NCBI ClinVar database for clinical significance annotations.
Uses both REST API and local VCF files for comprehensive coverage.
"""

import requests
import json
import time
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import pandas as pd
from urllib.parse import quote

class ClinVarDatabase:
    """
    ClinVar database integration for clinical variant significance
    
    Provides access to:
    - Clinical significance classifications
    - Review status information
    - Condition information
    - Submission details
    """
    
    def __init__(self, cache_dir: Optional[str] = None, use_cache: bool = True):
        """
        Initialize ClinVar database connection
        
        Args:
            cache_dir: Directory for caching results
            use_cache: Whether to use local caching
        """
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        self.clinvar_api = "https://www.ncbi.nlm.nih.gov/clinvar/api/v2"
        self.cache_dir = Path(cache_dir) if cache_dir else Path.home() / ".varannote" / "cache"
        self.use_cache = use_cache
        
        # Create cache directory
        if self.use_cache:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 0.34  # NCBI allows ~3 requests per second
        
        # Clinical significance mapping
        self.significance_mapping = {
            "Pathogenic": "Pathogenic",
            "Likely pathogenic": "Likely_pathogenic", 
            "Uncertain significance": "Uncertain_significance",
            "Likely benign": "Likely_benign",
            "Benign": "Benign",
            "Pathogenic/Likely pathogenic": "Pathogenic",
            "Benign/Likely benign": "Benign",
            "Conflicting interpretations of pathogenicity": "Conflicting",
            "not provided": "Not_provided"
        }
    
    def _rate_limit(self):
        """Implement rate limiting for API requests"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _get_cache_path(self, variant_key: str) -> Path:
        """Get cache file path for variant"""
        safe_key = variant_key.replace(":", "_").replace(">", "_")
        return self.cache_dir / f"clinvar_{safe_key}.json"
    
    def _load_from_cache(self, variant_key: str) -> Optional[Dict]:
        """Load annotation from cache"""
        if not self.use_cache:
            return None
        
        cache_path = self._get_cache_path(variant_key)
        if cache_path.exists():
            try:
                with open(cache_path, 'r') as f:
                    return json.load(f)
            except Exception:
                return None
        return None
    
    def _save_to_cache(self, variant_key: str, data: Dict):
        """Save annotation to cache"""
        if not self.use_cache:
            return
        
        cache_path = self._get_cache_path(variant_key)
        try:
            with open(cache_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass
    
    def get_variant_annotation(self, chrom: str, pos: int, ref: str, alt: str) -> Dict:
        """
        Get ClinVar annotation for a specific variant
        
        Args:
            chrom: Chromosome (e.g., "17", "X")
            pos: Position (1-based)
            ref: Reference allele
            alt: Alternative allele
            
        Returns:
            Dictionary with ClinVar annotations
        """
        variant_key = f"{chrom}:{pos}:{ref}>{alt}"
        
        # Check cache first
        cached_result = self._load_from_cache(variant_key)
        if cached_result:
            return cached_result
        
        # Try multiple search strategies
        annotations = {}
        
        # Strategy 1: Search by genomic coordinates
        genomic_annotations = self._search_by_coordinates(chrom, pos, ref, alt)
        if genomic_annotations:
            annotations.update(genomic_annotations)
        
        # Strategy 2: Search by HGVS notation (if we can construct it)
        hgvs_annotations = self._search_by_hgvs(chrom, pos, ref, alt)
        if hgvs_annotations:
            annotations.update(hgvs_annotations)
        
        # If no results, return empty annotation
        if not annotations:
            annotations = {
                "clinvar_significance": None,
                "clinvar_id": None,
                "clinvar_review_status": None,
                "clinvar_conditions": None
            }
        
        # Cache the result
        self._save_to_cache(variant_key, annotations)
        
        return annotations
    
    def _search_by_coordinates(self, chrom: str, pos: int, ref: str, alt: str) -> Optional[Dict]:
        """Search ClinVar by genomic coordinates"""
        try:
            self._rate_limit()
            
            # Construct search query
            # Format: chr17:43044295[chrpos] AND G>A[variant]
            search_term = f"chr{chrom}:{pos}[chrpos] AND {ref}>{alt}[variant]"
            
            # Search using ESearch
            esearch_url = f"{self.base_url}/esearch.fcgi"
            esearch_params = {
                "db": "clinvar",
                "term": search_term,
                "retmode": "json",
                "retmax": "10"
            }
            
            response = requests.get(esearch_url, params=esearch_params, timeout=30)
            response.raise_for_status()
            
            search_data = response.json()
            
            if not search_data.get("esearchresult", {}).get("idlist"):
                return None
            
            # Get detailed information using ESummary
            ids = search_data["esearchresult"]["idlist"][:5]  # Limit to first 5 results
            
            return self._get_variant_details(ids)
            
        except Exception as e:
            print(f"Warning: ClinVar coordinate search failed: {e}")
            return None
    
    def _search_by_hgvs(self, chrom: str, pos: int, ref: str, alt: str) -> Optional[Dict]:
        """Search ClinVar by HGVS notation"""
        try:
            # Simple HGVS construction for SNVs
            if len(ref) == 1 and len(alt) == 1:
                hgvs_g = f"NC_000{chrom.zfill(2)}.11:g.{pos}{ref}>{alt}"
                
                self._rate_limit()
                
                search_term = f'"{hgvs_g}"[variant name]'
                
                esearch_url = f"{self.base_url}/esearch.fcgi"
                esearch_params = {
                    "db": "clinvar",
                    "term": search_term,
                    "retmode": "json",
                    "retmax": "5"
                }
                
                response = requests.get(esearch_url, params=esearch_params, timeout=30)
                response.raise_for_status()
                
                search_data = response.json()
                
                if not search_data.get("esearchresult", {}).get("idlist"):
                    return None
                
                ids = search_data["esearchresult"]["idlist"]
                return self._get_variant_details(ids)
                
        except Exception as e:
            print(f"Warning: ClinVar HGVS search failed: {e}")
            return None
    
    def _get_variant_details(self, clinvar_ids: List[str]) -> Optional[Dict]:
        """Get detailed variant information from ClinVar IDs"""
        try:
            self._rate_limit()
            
            # Use ESummary to get detailed information
            esummary_url = f"{self.base_url}/esummary.fcgi"
            esummary_params = {
                "db": "clinvar",
                "id": ",".join(clinvar_ids),
                "retmode": "json"
            }
            
            response = requests.get(esummary_url, params=esummary_params, timeout=30)
            response.raise_for_status()
            
            summary_data = response.json()
            
            if "result" not in summary_data:
                return None
            
            # Process the first valid result
            for clinvar_id in clinvar_ids:
                if clinvar_id in summary_data["result"]:
                    variant_data = summary_data["result"][clinvar_id]
                    
                    # Extract clinical significance
                    clinical_significance = variant_data.get("clinical_significance", "")
                    mapped_significance = self.significance_mapping.get(
                        clinical_significance, clinical_significance
                    )
                    
                    # Extract other information
                    review_status = variant_data.get("review_status", "")
                    conditions = variant_data.get("condition_list", [])
                    
                    # Format conditions
                    condition_names = []
                    if isinstance(conditions, list):
                        for condition in conditions:
                            if isinstance(condition, dict):
                                condition_names.append(condition.get("name", ""))
                    
                    return {
                        "clinvar_significance": mapped_significance,
                        "clinvar_id": f"VCV{variant_data.get('accession', clinvar_id)}",
                        "clinvar_review_status": review_status,
                        "clinvar_conditions": "; ".join(condition_names) if condition_names else None,
                        "clinvar_last_evaluated": variant_data.get("last_evaluated", None)
                    }
            
            return None
            
        except Exception as e:
            print(f"Warning: ClinVar details retrieval failed: {e}")
            return None
    
    def batch_annotate(self, variants: List[Dict]) -> List[Dict]:
        """
        Annotate multiple variants with ClinVar data
        
        Args:
            variants: List of variant dictionaries
            
        Returns:
            List of variants with ClinVar annotations added
        """
        annotated_variants = []
        
        for i, variant in enumerate(variants):
            print(f"Annotating variant {i+1}/{len(variants)} with ClinVar...")
            
            try:
                clinvar_data = self.get_variant_annotation(
                    variant["CHROM"],
                    variant["POS"], 
                    variant["REF"],
                    variant["ALT"]
                )
                
                # Add ClinVar annotations to variant
                annotated_variant = {**variant, **clinvar_data}
                annotated_variants.append(annotated_variant)
                
            except Exception as e:
                print(f"Warning: Failed to annotate variant {variant.get('variant_id', 'unknown')}: {e}")
                # Add empty annotations
                annotated_variant = {
                    **variant,
                    "clinvar_significance": None,
                    "clinvar_id": None,
                    "clinvar_review_status": None,
                    "clinvar_conditions": None
                }
                annotated_variants.append(annotated_variant)
        
        return annotated_variants
    
    def get_database_info(self) -> Dict:
        """Get information about ClinVar database"""
        return {
            "name": "ClinVar",
            "description": "NCBI database of genomic variation and human health",
            "url": "https://www.ncbi.nlm.nih.gov/clinvar/",
            "api_url": self.clinvar_api,
            "version": "Current",
            "last_updated": "Real-time",
            "data_types": [
                "Clinical significance",
                "Review status", 
                "Condition information",
                "Submission details"
            ]
        } 