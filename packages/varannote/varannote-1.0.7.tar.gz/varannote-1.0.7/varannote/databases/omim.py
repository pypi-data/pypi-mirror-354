#!/usr/bin/env python3
"""
OMIM Database Integration

Integration with OMIM (Online Mendelian Inheritance in Man) for disease-gene associations.
Provides comprehensive information about genetic disorders and phenotypes.
"""

import requests
import json
import time
from typing import Dict, List, Optional, Tuple
from pathlib import Path

class OMIMDatabase:
    """
    OMIM database integration for disease-gene associations
    
    Provides access to:
    - Disease-gene associations
    - Phenotype information
    - Inheritance patterns
    - Clinical features
    - Gene function descriptions
    """
    
    def __init__(self, api_key: Optional[str] = None, cache_dir: Optional[str] = None, use_cache: bool = True):
        """
        Initialize OMIM database connection
        
        Args:
            api_key: OMIM API key (required for full access)
            cache_dir: Directory for caching results
            use_cache: Whether to use local caching
        """
        self.base_url = "https://api.omim.org/api"
        self.api_key = api_key
        self.cache_dir = Path(cache_dir) if cache_dir else Path.home() / ".varannote" / "cache"
        self.use_cache = use_cache
        
        # Create cache directory
        if self.use_cache:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 0.5  # Conservative rate limiting
        
        # Gene-disease mappings (fallback data)
        self.gene_disease_map = {
            "BRCA1": {
                "omim_gene_id": "113705",
                "diseases": [
                    {"omim_id": "604370", "name": "Breast-ovarian cancer, familial 1", "inheritance": "AD"},
                    {"omim_id": "612555", "name": "Fanconi anemia, complementation group S", "inheritance": "AR"}
                ]
            },
            "BRCA2": {
                "omim_gene_id": "600185", 
                "diseases": [
                    {"omim_id": "612001", "name": "Breast-ovarian cancer, familial 2", "inheritance": "AD"},
                    {"omim_id": "605724", "name": "Fanconi anemia, complementation group D1", "inheritance": "AR"}
                ]
            },
            "TP53": {
                "omim_gene_id": "191170",
                "diseases": [
                    {"omim_id": "151623", "name": "Li-Fraumeni syndrome 1", "inheritance": "AD"},
                    {"omim_id": "609265", "name": "Colorectal cancer, hereditary nonpolyposis, type 1", "inheritance": "AD"}
                ]
            },
            "CFTR": {
                "omim_gene_id": "602421",
                "diseases": [
                    {"omim_id": "219700", "name": "Cystic fibrosis", "inheritance": "AR"},
                    {"omim_id": "277180", "name": "Congenital bilateral absence of vas deferens", "inheritance": "AR"}
                ]
            },
            "APOE": {
                "omim_gene_id": "107741",
                "diseases": [
                    {"omim_id": "104300", "name": "Alzheimer disease, late-onset", "inheritance": "Complex"},
                    {"omim_id": "143890", "name": "Hyperlipoproteinemia, type III", "inheritance": "AR"}
                ]
            }
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
        return self.cache_dir / f"omim_{safe_gene}.json"
    
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
        Get OMIM annotation for a specific gene
        
        Args:
            gene_symbol: Gene symbol (e.g., "BRCA1", "TP53")
            
        Returns:
            Dictionary with OMIM annotations
        """
        # Check cache first
        cached_result = self._load_from_cache(gene_symbol)
        if cached_result:
            return cached_result
        
        try:
            # Try API if key is available
            if self.api_key:
                annotations = self._query_omim_api(gene_symbol)
            else:
                # Use fallback data
                annotations = self._get_fallback_data(gene_symbol)
            
            # Cache the result
            self._save_to_cache(gene_symbol, annotations)
            
            return annotations
            
        except Exception as e:
            print(f"Warning: OMIM query failed for {gene_symbol}: {e}")
            
            # Return empty annotation
            return {
                "omim_gene_id": None,
                "omim_diseases": None,
                "omim_inheritance": None,
                "omim_phenotypes": None
            }
    
    def get_variant_annotation(self, chrom: str, pos: int, ref: str, alt: str) -> Dict:
        """
        Get OMIM annotation for a variant based on its gene location
        
        Args:
            chrom: Chromosome
            pos: Position
            ref: Reference allele
            alt: Alternative allele
            
        Returns:
            Dictionary with OMIM annotations
        """
        # This would need gene mapping - for now return empty
        # In real implementation, would map coordinates to genes first
        return {
            "omim_gene_id": None,
            "omim_diseases": None,
            "omim_inheritance": None,
            "omim_phenotypes": None
        }
    
    def _query_omim_api(self, gene_symbol: str) -> Dict:
        """Query OMIM API for gene information"""
        
        self._rate_limit()
        
        # Search for gene
        search_url = f"{self.base_url}/geneMap/search"
        search_params = {
            "search": gene_symbol,
            "format": "json",
            "apiKey": self.api_key
        }
        
        response = requests.get(search_url, params=search_params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get("omim", {}).get("searchResponse", {}).get("geneMapList"):
            return self._get_fallback_data(gene_symbol)
        
        # Process the first result
        gene_map = data["omim"]["searchResponse"]["geneMapList"][0]["geneMap"]
        
        # Get detailed information
        gene_id = gene_map.get("mimNumber")
        if gene_id:
            return self._get_gene_details(gene_id, gene_symbol)
        
        return self._get_fallback_data(gene_symbol)
    
    def _get_gene_details(self, gene_id: str, gene_symbol: str) -> Dict:
        """Get detailed gene information from OMIM"""
        
        self._rate_limit()
        
        entry_url = f"{self.base_url}/entry"
        entry_params = {
            "mimNumber": gene_id,
            "include": "geneMap,phenotypeMap,clinicalSynopsis",
            "format": "json",
            "apiKey": self.api_key
        }
        
        response = requests.get(entry_url, params=entry_params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get("omim", {}).get("entryList"):
            return self._get_fallback_data(gene_symbol)
        
        entry = data["omim"]["entryList"][0]["entry"]
        
        # Extract disease associations
        diseases = []
        phenotype_map = entry.get("phenotypeMapList", [])
        
        for phenotype in phenotype_map:
            pheno_data = phenotype.get("phenotypeMap", {})
            diseases.append({
                "omim_id": pheno_data.get("mimNumber"),
                "name": pheno_data.get("phenotype", "").split(",")[0],  # Remove inheritance info
                "inheritance": self._extract_inheritance(pheno_data.get("phenotype", "")),
                "mapping_key": pheno_data.get("phenotypeMappingKey")
            })
        
        return {
            "omim_gene_id": gene_id,
            "omim_diseases": "; ".join([d["name"] for d in diseases if d["name"]]),
            "omim_inheritance": "; ".join(list(set([d["inheritance"] for d in diseases if d["inheritance"]]))),
            "omim_phenotypes": len(diseases)
        }
    
    def _extract_inheritance(self, phenotype_text: str) -> str:
        """Extract inheritance pattern from phenotype text"""
        if "autosomal dominant" in phenotype_text.lower():
            return "AD"
        elif "autosomal recessive" in phenotype_text.lower():
            return "AR"
        elif "x-linked" in phenotype_text.lower():
            return "XL"
        elif "mitochondrial" in phenotype_text.lower():
            return "MT"
        else:
            return "Unknown"
    
    def _get_fallback_data(self, gene_symbol: str) -> Dict:
        """Get fallback data for known genes"""
        
        if gene_symbol in self.gene_disease_map:
            gene_data = self.gene_disease_map[gene_symbol]
            diseases = gene_data["diseases"]
            
            return {
                "omim_gene_id": gene_data["omim_gene_id"],
                "omim_diseases": "; ".join([d["name"] for d in diseases]),
                "omim_inheritance": "; ".join(list(set([d["inheritance"] for d in diseases]))),
                "omim_phenotypes": len(diseases)
            }
        
        return {
            "omim_gene_id": None,
            "omim_diseases": None,
            "omim_inheritance": None,
            "omim_phenotypes": None
        }
    
    def batch_annotate(self, variants: List[Dict]) -> List[Dict]:
        """
        Annotate multiple variants with OMIM data
        
        Args:
            variants: List of variant dictionaries
            
        Returns:
            List of variants with OMIM annotations added
        """
        annotated_variants = []
        
        for i, variant in enumerate(variants):
            print(f"Annotating variant {i+1}/{len(variants)} with OMIM...")
            
            try:
                # Get gene symbol from variant
                gene_symbol = variant.get("gene_symbol")
                
                if gene_symbol and gene_symbol != "intergenic":
                    omim_data = self.get_gene_annotation(gene_symbol)
                else:
                    omim_data = {
                        "omim_gene_id": None,
                        "omim_diseases": None,
                        "omim_inheritance": None,
                        "omim_phenotypes": None
                    }
                
                # Add OMIM annotations to variant
                annotated_variant = {**variant, **omim_data}
                annotated_variants.append(annotated_variant)
                
            except Exception as e:
                print(f"Warning: Failed to annotate variant {variant.get('variant_id', 'unknown')}: {e}")
                # Add empty annotations
                annotated_variant = {
                    **variant,
                    "omim_gene_id": None,
                    "omim_diseases": None,
                    "omim_inheritance": None,
                    "omim_phenotypes": None
                }
                annotated_variants.append(annotated_variant)
        
        return annotated_variants
    
    def get_database_info(self) -> Dict:
        """Get information about OMIM database"""
        return {
            "name": "OMIM",
            "description": "Online Mendelian Inheritance in Man - Disease-gene associations",
            "url": "https://www.omim.org/",
            "api_url": self.base_url,
            "version": "Current",
            "last_updated": "Daily",
            "data_types": [
                "Disease-gene associations",
                "Inheritance patterns",
                "Phenotype descriptions",
                "Clinical features",
                "Gene function"
            ],
            "requires_api_key": True
        } 