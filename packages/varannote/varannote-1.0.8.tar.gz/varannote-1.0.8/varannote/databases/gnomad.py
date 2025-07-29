#!/usr/bin/env python3
"""
gnomAD Database Integration

Real-time integration with gnomAD (Genome Aggregation Database) for population frequency data.
Provides comprehensive allele frequency information across diverse populations.
"""

import requests
import json
import time
from typing import Dict, List, Optional, Tuple
from pathlib import Path

class GnomADDatabase:
    """
    gnomAD database integration for population allele frequencies
    
    Provides access to:
    - Global allele frequencies
    - Population-specific frequencies (AFR, AMR, EAS, EUR, SAS)
    - Allele counts and numbers
    - Quality metrics
    """
    
    def __init__(self, cache_dir: Optional[str] = None, use_cache: bool = True, version: str = "v4.1"):
        """
        Initialize gnomAD database connection
        
        Args:
            cache_dir: Directory for caching results
            use_cache: Whether to use local caching
            version: gnomAD version (v4.1, v3.1.2, v2.1.1)
        """
        self.graphql_url = "https://gnomad.broadinstitute.org/api"
        self.version = version
        self.cache_dir = Path(cache_dir) if cache_dir else Path.home() / ".varannote" / "cache"
        self.use_cache = use_cache
        
        # Create cache directory
        if self.use_cache:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Rate limiting - gnomAD allows 10 queries per minute
        self.last_request_time = 0
        self.min_request_interval = 6.0  # 6 seconds between requests (10 per minute)
        
        # Population codes
        self.populations = {
            "afr": "African/African American",
            "amr": "Latino/Admixed American", 
            "eas": "East Asian",
            "eur": "European (non-Finnish)",
            "sas": "South Asian",
            "fin": "Finnish",
            "asj": "Ashkenazi Jewish",
            "oth": "Other"
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
        return self.cache_dir / f"gnomad_{safe_key}.json"
    
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
        Get gnomAD annotation for a specific variant
        
        Args:
            chrom: Chromosome (e.g., "17", "X")
            pos: Position (1-based)
            ref: Reference allele
            alt: Alternative allele
            
        Returns:
            Dictionary with gnomAD annotations
        """
        variant_key = f"{chrom}:{pos}:{ref}>{alt}"
        
        # Check cache first
        cached_result = self._load_from_cache(variant_key)
        if cached_result:
            return cached_result
        
        try:
            # Query gnomAD GraphQL API
            annotations = self._query_gnomad_api(chrom, pos, ref, alt)
            
            # Cache the result
            self._save_to_cache(variant_key, annotations)
            
            return annotations
            
        except Exception as e:
            print(f"Warning: gnomAD query failed for {variant_key}: {e}")
            
            # Return empty annotation
            return {
                "gnomad_af": None,
                "gnomad_ac": None,
                "gnomad_an": None,
                "gnomad_af_afr": None,
                "gnomad_af_amr": None,
                "gnomad_af_eas": None,
                "gnomad_af_eur": None,
                "gnomad_af_sas": None,
                "gnomad_filter": None
            }
    
    def _query_gnomad_api(self, chrom: str, pos: int, ref: str, alt: str) -> Dict:
        """Query gnomAD GraphQL API for variant information"""
        
        self._rate_limit()
        
        # Construct GraphQL query
        query = """
        query VariantQuery($chrom: String!, $pos: Int!, $ref: String!, $alt: String!) {
          variant(chrom: $chrom, pos: $pos, ref: $ref, alt: $alt, dataset: gnomad_r4) {
            variant_id
            genome {
              ac
              an
              af
              filters
              populations {
                id
                ac
                an
                af
              }
            }
            exome {
              ac
              an
              af
              filters
              populations {
                id
                ac
                an
                af
              }
            }
          }
        }
        """
        
        variables = {
            "chrom": str(chrom),
            "pos": int(pos),
            "ref": ref,
            "alt": alt
        }
        
        payload = {
            "query": query,
            "variables": variables
        }
        
        response = requests.post(
            self.graphql_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        response.raise_for_status()
        data = response.json()
        
        if "errors" in data:
            raise Exception(f"GraphQL errors: {data['errors']}")
        
        return self._parse_gnomad_response(data)
    
    def _parse_gnomad_response(self, response_data: Dict) -> Dict:
        """Parse gnomAD GraphQL response into annotation dictionary"""
        
        annotations = {
            "gnomad_af": None,
            "gnomad_ac": None,
            "gnomad_an": None,
            "gnomad_af_afr": None,
            "gnomad_af_amr": None,
            "gnomad_af_eas": None,
            "gnomad_af_eur": None,
            "gnomad_af_sas": None,
            "gnomad_filter": None
        }
        
        variant_data = response_data.get("data", {}).get("variant")
        if not variant_data:
            return annotations
        
        # Prefer genome data, fall back to exome
        freq_data = variant_data.get("genome") or variant_data.get("exome")
        if not freq_data:
            return annotations
        
        # Global frequencies
        annotations["gnomad_af"] = freq_data.get("af")
        annotations["gnomad_ac"] = freq_data.get("ac")
        annotations["gnomad_an"] = freq_data.get("an")
        
        # Filters
        filters = freq_data.get("filters", [])
        if filters:
            annotations["gnomad_filter"] = ";".join(filters)
        else:
            annotations["gnomad_filter"] = "PASS"
        
        # Population-specific frequencies
        populations = freq_data.get("populations", [])
        for pop_data in populations:
            pop_id = pop_data.get("id", "").lower()
            pop_af = pop_data.get("af")
            
            if pop_id in ["afr", "amr", "eas", "eur", "sas"]:
                annotations[f"gnomad_af_{pop_id}"] = pop_af
        
        return annotations
    
    def batch_annotate(self, variants: List[Dict]) -> List[Dict]:
        """
        Annotate multiple variants with gnomAD data
        
        Args:
            variants: List of variant dictionaries
            
        Returns:
            List of variants with gnomAD annotations added
        """
        annotated_variants = []
        
        for i, variant in enumerate(variants):
            print(f"Annotating variant {i+1}/{len(variants)} with gnomAD...")
            
            try:
                gnomad_data = self.get_variant_annotation(
                    variant["CHROM"],
                    variant["POS"],
                    variant["REF"], 
                    variant["ALT"]
                )
                
                # Add gnomAD annotations to variant
                annotated_variant = {**variant, **gnomad_data}
                annotated_variants.append(annotated_variant)
                
            except Exception as e:
                print(f"Warning: Failed to annotate variant {variant.get('variant_id', 'unknown')}: {e}")
                # Add empty annotations
                annotated_variant = {
                    **variant,
                    "gnomad_af": None,
                    "gnomad_ac": None,
                    "gnomad_an": None,
                    "gnomad_af_afr": None,
                    "gnomad_af_amr": None,
                    "gnomad_af_eas": None,
                    "gnomad_af_eur": None,
                    "gnomad_af_sas": None,
                    "gnomad_filter": None
                }
                annotated_variants.append(annotated_variant)
        
        return annotated_variants
    
    def get_population_frequencies(self, chrom: str, pos: int, ref: str, alt: str) -> Dict:
        """
        Get detailed population frequency breakdown
        
        Returns:
            Dictionary with population-specific frequency data
        """
        annotation = self.get_variant_annotation(chrom, pos, ref, alt)
        
        population_freqs = {}
        for pop_code, pop_name in self.populations.items():
            freq_key = f"gnomad_af_{pop_code}"
            if freq_key in annotation and annotation[freq_key] is not None:
                population_freqs[pop_name] = annotation[freq_key]
        
        return population_freqs
    
    def get_database_info(self) -> Dict:
        """Get information about gnomAD database"""
        return {
            "name": "gnomAD",
            "description": "Genome Aggregation Database - Population allele frequencies",
            "url": "https://gnomad.broadinstitute.org/",
            "api_url": self.graphql_url,
            "version": self.version,
            "last_updated": "2020-10-29",
            "populations": list(self.populations.values()),
            "data_types": [
                "Global allele frequencies",
                "Population-specific frequencies",
                "Allele counts",
                "Quality filters"
            ]
        } 