#!/usr/bin/env python3
"""
dbSNP Database Integration

Integration with NCBI dbSNP database for variant identifiers and basic information.
"""

import requests
import json
import time
from typing import Dict, List, Optional
from pathlib import Path

class DbSNPDatabase:
    """
    dbSNP database integration for variant identifiers
    
    Provides access to:
    - rsID identifiers
    - Variant validation status
    - Allele frequencies (when available)
    - Clinical significance flags
    """
    
    def __init__(self, cache_dir: Optional[str] = None, use_cache: bool = True):
        """
        Initialize dbSNP database connection
        
        Args:
            cache_dir: Directory for caching results
            use_cache: Whether to use local caching
        """
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        self.cache_dir = Path(cache_dir) if cache_dir else Path.home() / ".varannote" / "cache"
        self.use_cache = use_cache
        
        # Create cache directory
        if self.use_cache:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 0.34  # NCBI allows ~3 requests per second
    
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
        return self.cache_dir / f"dbsnp_{safe_key}.json"
    
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
        Get dbSNP annotation for a specific variant
        
        Args:
            chrom: Chromosome (e.g., "17", "X")
            pos: Position (1-based)
            ref: Reference allele
            alt: Alternative allele
            
        Returns:
            Dictionary with dbSNP annotations
        """
        variant_key = f"{chrom}:{pos}:{ref}>{alt}"
        
        # Check cache first
        cached_result = self._load_from_cache(variant_key)
        if cached_result:
            return cached_result
        
        try:
            # Search dbSNP by coordinates
            annotations = self._search_by_coordinates(chrom, pos, ref, alt)
            
            # Cache the result
            self._save_to_cache(variant_key, annotations)
            
            return annotations
            
        except Exception as e:
            print(f"Warning: dbSNP query failed for {variant_key}: {e}")
            
            # Return empty annotation
            return {
                "dbsnp_id": None,
                "dbsnp_validated": None,
                "dbsnp_maf": None
            }
    
    def _search_by_coordinates(self, chrom: str, pos: int, ref: str, alt: str) -> Dict:
        """Search dbSNP by genomic coordinates"""
        
        self._rate_limit()
        
        # Construct search term
        search_term = f"chr{chrom}:{pos}[chrpos]"
        
        # Search using ESearch
        esearch_url = f"{self.base_url}/esearch.fcgi"
        esearch_params = {
            "db": "snp",
            "term": search_term,
            "retmode": "json",
            "retmax": "10"
        }
        
        response = requests.get(esearch_url, params=esearch_params, timeout=30)
        response.raise_for_status()
        
        search_data = response.json()
        
        if not search_data.get("esearchresult", {}).get("idlist"):
            return {
                "dbsnp_id": None,
                "dbsnp_validated": None,
                "dbsnp_maf": None
            }
        
        # Get detailed information using ESummary
        ids = search_data["esearchresult"]["idlist"][:5]
        
        return self._get_snp_details(ids, ref, alt)
    
    def _get_snp_details(self, snp_ids: List[str], ref: str, alt: str) -> Dict:
        """Get detailed SNP information from dbSNP IDs"""
        
        self._rate_limit()
        
        # Use ESummary to get detailed information
        esummary_url = f"{self.base_url}/esummary.fcgi"
        esummary_params = {
            "db": "snp",
            "id": ",".join(snp_ids),
            "retmode": "json"
        }
        
        response = requests.get(esummary_url, params=esummary_params, timeout=30)
        response.raise_for_status()
        
        summary_data = response.json()
        
        if "result" not in summary_data:
            return {
                "dbsnp_id": None,
                "dbsnp_validated": None,
                "dbsnp_maf": None
            }
        
        # Process results to find matching alleles
        for snp_id in snp_ids:
            if snp_id in summary_data["result"]:
                snp_data = summary_data["result"][snp_id]
                
                # Check if alleles match
                if self._alleles_match(snp_data, ref, alt):
                    return {
                        "dbsnp_id": f"rs{snp_data.get('rsid', snp_id)}",
                        "dbsnp_validated": snp_data.get("validation", "").lower() == "true",
                        "dbsnp_maf": self._extract_maf(snp_data)
                    }
        
        # If no exact match found, return the first result
        if snp_ids and snp_ids[0] in summary_data["result"]:
            snp_data = summary_data["result"][snp_ids[0]]
            return {
                "dbsnp_id": f"rs{snp_data.get('rsid', snp_ids[0])}",
                "dbsnp_validated": snp_data.get("validation", "").lower() == "true",
                "dbsnp_maf": self._extract_maf(snp_data)
            }
        
        return {
            "dbsnp_id": None,
            "dbsnp_validated": None,
            "dbsnp_maf": None
        }
    
    def _alleles_match(self, snp_data: Dict, ref: str, alt: str) -> bool:
        """Check if SNP alleles match the query variant"""
        # Simple allele matching - could be improved
        alleles = snp_data.get("alleles", "")
        return ref in alleles and alt in alleles
    
    def _extract_maf(self, snp_data: Dict) -> Optional[float]:
        """Extract minor allele frequency from SNP data"""
        # This is simplified - real implementation would parse frequency data
        maf_str = snp_data.get("maf", "")
        if maf_str:
            try:
                return float(maf_str)
            except ValueError:
                return None
        return None
    
    def batch_annotate(self, variants: List[Dict]) -> List[Dict]:
        """
        Annotate multiple variants with dbSNP data
        
        Args:
            variants: List of variant dictionaries
            
        Returns:
            List of variants with dbSNP annotations added
        """
        annotated_variants = []
        
        for i, variant in enumerate(variants):
            print(f"Annotating variant {i+1}/{len(variants)} with dbSNP...")
            
            try:
                dbsnp_data = self.get_variant_annotation(
                    variant["CHROM"],
                    variant["POS"],
                    variant["REF"],
                    variant["ALT"]
                )
                
                # Add dbSNP annotations to variant
                annotated_variant = {**variant, **dbsnp_data}
                annotated_variants.append(annotated_variant)
                
            except Exception as e:
                print(f"Warning: Failed to annotate variant {variant.get('variant_id', 'unknown')}: {e}")
                # Add empty annotations
                annotated_variant = {
                    **variant,
                    "dbsnp_id": None,
                    "dbsnp_validated": None,
                    "dbsnp_maf": None
                }
                annotated_variants.append(annotated_variant)
        
        return annotated_variants
    
    def get_database_info(self) -> Dict:
        """Get information about dbSNP database"""
        return {
            "name": "dbSNP",
            "description": "NCBI database of single nucleotide polymorphisms",
            "url": "https://www.ncbi.nlm.nih.gov/snp/",
            "api_url": self.base_url,
            "version": "Build 155",
            "last_updated": "2023-05-09",
            "data_types": [
                "rsID identifiers",
                "Validation status",
                "Minor allele frequencies",
                "Population data"
            ]
        } 