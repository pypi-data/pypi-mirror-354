#!/usr/bin/env python3
"""
PharmGKB Database Integration

Integration with PharmGKB (Pharmacogenomics Knowledgebase) for drug-gene interactions.
Provides comprehensive pharmacogenomic annotations and drug response predictions.
"""

import requests
import json
import time
from typing import Dict, List, Optional, Tuple
from pathlib import Path

class PharmGKBDatabase:
    """
    PharmGKB database integration for pharmacogenomics
    
    Provides access to:
    - Drug-gene interactions
    - Pharmacogenomic variants
    - Drug response predictions
    - Clinical annotations
    - Dosing guidelines
    """
    
    def __init__(self, cache_dir: Optional[str] = None, use_cache: bool = True):
        """
        Initialize PharmGKB database connection
        
        Args:
            cache_dir: Directory for caching results
            use_cache: Whether to use local caching
        """
        self.base_url = "https://api.pharmgkb.org/v1"
        self.cache_dir = Path(cache_dir) if cache_dir else Path.home() / ".varannote" / "cache"
        self.use_cache = use_cache
        
        # Create cache directory
        if self.use_cache:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 0.2  # Conservative rate limiting
        
        # Pharmacogenomic gene-drug mappings (fallback data)
        self.pharmgkb_data = {
            "CYP2D6": {
                "pharmgkb_id": "PA128",
                "drugs": [
                    {"drug": "Codeine", "level": "1A", "effect": "Efficacy", "guideline": "CPIC"},
                    {"drug": "Tramadol", "level": "1A", "effect": "Efficacy", "guideline": "CPIC"},
                    {"drug": "Atomoxetine", "level": "1A", "effect": "Dosing", "guideline": "CPIC"},
                    {"drug": "Paroxetine", "level": "2A", "effect": "Metabolism", "guideline": "FDA"}
                ],
                "function": "Drug metabolism",
                "variants": ["*1", "*2", "*3", "*4", "*5", "*6", "*10", "*17", "*41"]
            },
            "CYP2C19": {
                "pharmgkb_id": "PA124",
                "drugs": [
                    {"drug": "Clopidogrel", "level": "1A", "effect": "Efficacy", "guideline": "CPIC"},
                    {"drug": "Omeprazole", "level": "1A", "effect": "Dosing", "guideline": "CPIC"},
                    {"drug": "Voriconazole", "level": "1A", "effect": "Dosing", "guideline": "CPIC"},
                    {"drug": "Sertraline", "level": "2A", "effect": "Metabolism", "guideline": "CPIC"}
                ],
                "function": "Drug metabolism",
                "variants": ["*1", "*2", "*3", "*17"]
            },
            "SLCO1B1": {
                "pharmgkb_id": "PA134865839",
                "drugs": [
                    {"drug": "Simvastatin", "level": "1A", "effect": "Toxicity", "guideline": "CPIC"},
                    {"drug": "Atorvastatin", "level": "2A", "effect": "Toxicity", "guideline": "CPIC"}
                ],
                "function": "Drug transport",
                "variants": ["*1A", "*1B", "*5", "*15", "*17"]
            },
            "DPYD": {
                "pharmgkb_id": "PA145",
                "drugs": [
                    {"drug": "Fluorouracil", "level": "1A", "effect": "Toxicity", "guideline": "CPIC"},
                    {"drug": "Capecitabine", "level": "1A", "effect": "Toxicity", "guideline": "CPIC"}
                ],
                "function": "Drug metabolism",
                "variants": ["*1", "*2A", "*13"]
            },
            "TPMT": {
                "pharmgkb_id": "PA356",
                "drugs": [
                    {"drug": "Mercaptopurine", "level": "1A", "effect": "Toxicity", "guideline": "CPIC"},
                    {"drug": "Azathioprine", "level": "1A", "effect": "Toxicity", "guideline": "CPIC"},
                    {"drug": "Thioguanine", "level": "1A", "effect": "Toxicity", "guideline": "CPIC"}
                ],
                "function": "Drug metabolism",
                "variants": ["*1", "*2", "*3A", "*3B", "*3C"]
            },
            "UGT1A1": {
                "pharmgkb_id": "PA420",
                "drugs": [
                    {"drug": "Irinotecan", "level": "1A", "effect": "Toxicity", "guideline": "CPIC"},
                    {"drug": "Atazanavir", "level": "2A", "effect": "Toxicity", "guideline": "FDA"}
                ],
                "function": "Drug metabolism",
                "variants": ["*1", "*28", "*6", "*27"]
            }
        }
        
        # Clinical significance levels
        self.evidence_levels = {
            "1A": "High - Preponderance of evidence supports the association",
            "1B": "High - Preponderance of evidence supports the association", 
            "2A": "Moderate - Evidence supports the association",
            "2B": "Moderate - Evidence supports the association",
            "3": "Low - Evidence does not support or refute the association",
            "4": "Negative - Evidence does not support the association"
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
        return self.cache_dir / f"pharmgkb_{safe_gene}.json"
    
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
        Get PharmGKB annotation for a specific gene
        
        Args:
            gene_symbol: Gene symbol (e.g., "CYP2D6", "SLCO1B1")
            
        Returns:
            Dictionary with PharmGKB annotations
        """
        # Check cache first
        cached_result = self._load_from_cache(gene_symbol)
        if cached_result:
            return cached_result
        
        try:
            # Try API query (simplified for now)
            annotations = self._get_pharmgkb_data(gene_symbol)
            
            # Cache the result
            self._save_to_cache(gene_symbol, annotations)
            
            return annotations
            
        except Exception as e:
            print(f"Warning: PharmGKB query failed for {gene_symbol}: {e}")
            
            # Return empty annotation
            return {
                "pharmgkb_id": None,
                "pharmgkb_drugs": None,
                "pharmgkb_guidelines": None,
                "pharmgkb_level": None
            }
    
    def get_variant_annotation(self, chrom: str, pos: int, ref: str, alt: str) -> Dict:
        """
        Get PharmGKB annotation for a variant
        
        Args:
            chrom: Chromosome
            pos: Position
            ref: Reference allele
            alt: Alternative allele
            
        Returns:
            Dictionary with PharmGKB annotations
        """
        # This would need variant-specific mapping
        # For now, return empty annotations
        return {
            "pharmgkb_id": None,
            "pharmgkb_drugs": None,
            "pharmgkb_guidelines": None,
            "pharmgkb_level": None
        }
    
    def _get_pharmgkb_data(self, gene_symbol: str) -> Dict:
        """Get PharmGKB data for gene"""
        
        if gene_symbol in self.pharmgkb_data:
            gene_data = self.pharmgkb_data[gene_symbol]
            drugs = gene_data["drugs"]
            
            # Extract drug names and guidelines
            drug_names = [d["drug"] for d in drugs]
            guidelines = list(set([d["guideline"] for d in drugs]))
            levels = list(set([d["level"] for d in drugs]))
            
            return {
                "pharmgkb_id": gene_data["pharmgkb_id"],
                "pharmgkb_drugs": "; ".join(drug_names),
                "pharmgkb_guidelines": "; ".join(guidelines),
                "pharmgkb_level": "; ".join(levels),
                "pharmgkb_function": gene_data["function"],
                "pharmgkb_variants": len(gene_data["variants"])
            }
        
        return {
            "pharmgkb_id": None,
            "pharmgkb_drugs": None,
            "pharmgkb_guidelines": None,
            "pharmgkb_level": None,
            "pharmgkb_function": None,
            "pharmgkb_variants": None
        }
    
    def get_drug_interactions(self, gene_symbol: str, drug_name: Optional[str] = None) -> List[Dict]:
        """
        Get drug interactions for a specific gene
        
        Args:
            gene_symbol: Gene symbol
            drug_name: Optional specific drug name
            
        Returns:
            List of drug interaction dictionaries
        """
        if gene_symbol not in self.pharmgkb_data:
            return []
        
        gene_data = self.pharmgkb_data[gene_symbol]
        interactions = []
        
        for drug_info in gene_data["drugs"]:
            if drug_name is None or drug_info["drug"].lower() == drug_name.lower():
                interaction = {
                    "gene": gene_symbol,
                    "drug": drug_info["drug"],
                    "effect": drug_info["effect"],
                    "evidence_level": drug_info["level"],
                    "evidence_description": self.evidence_levels.get(drug_info["level"], "Unknown"),
                    "guideline": drug_info["guideline"],
                    "function": gene_data["function"]
                }
                interactions.append(interaction)
        
        return interactions
    
    def batch_annotate(self, variants: List[Dict]) -> List[Dict]:
        """
        Annotate multiple variants with PharmGKB data
        
        Args:
            variants: List of variant dictionaries
            
        Returns:
            List of variants with PharmGKB annotations added
        """
        annotated_variants = []
        
        for i, variant in enumerate(variants):
            print(f"Annotating variant {i+1}/{len(variants)} with PharmGKB...")
            
            try:
                # Get gene symbol from variant
                gene_symbol = variant.get("gene_symbol")
                
                if gene_symbol and gene_symbol in self.pharmgkb_data:
                    pharmgkb_data = self.get_gene_annotation(gene_symbol)
                else:
                    pharmgkb_data = {
                        "pharmgkb_id": None,
                        "pharmgkb_drugs": None,
                        "pharmgkb_guidelines": None,
                        "pharmgkb_level": None,
                        "pharmgkb_function": None,
                        "pharmgkb_variants": None
                    }
                
                # Add PharmGKB annotations to variant
                annotated_variant = {**variant, **pharmgkb_data}
                annotated_variants.append(annotated_variant)
                
            except Exception as e:
                print(f"Warning: Failed to annotate variant {variant.get('variant_id', 'unknown')}: {e}")
                # Add empty annotations
                annotated_variant = {
                    **variant,
                    "pharmgkb_id": None,
                    "pharmgkb_drugs": None,
                    "pharmgkb_guidelines": None,
                    "pharmgkb_level": None,
                    "pharmgkb_function": None,
                    "pharmgkb_variants": None
                }
                annotated_variants.append(annotated_variant)
        
        return annotated_variants
    
    def get_clinical_recommendations(self, gene_symbol: str, genotype: Optional[str] = None) -> List[Dict]:
        """
        Get clinical recommendations for gene/genotype combination
        
        Args:
            gene_symbol: Gene symbol
            genotype: Optional genotype information
            
        Returns:
            List of clinical recommendation dictionaries
        """
        recommendations = []
        
        if gene_symbol in self.pharmgkb_data:
            gene_data = self.pharmgkb_data[gene_symbol]
            
            for drug_info in gene_data["drugs"]:
                if drug_info["guideline"] == "CPIC":  # Focus on CPIC guidelines
                    recommendation = {
                        "gene": gene_symbol,
                        "drug": drug_info["drug"],
                        "recommendation": self._get_recommendation_text(gene_symbol, drug_info["drug"], genotype),
                        "evidence_level": drug_info["level"],
                        "guideline_source": drug_info["guideline"]
                    }
                    recommendations.append(recommendation)
        
        return recommendations
    
    def _get_recommendation_text(self, gene: str, drug: str, genotype: Optional[str] = None) -> str:
        """Generate recommendation text based on gene-drug combination"""
        
        # Simplified recommendation logic
        recommendations = {
            ("CYP2D6", "Codeine"): "Consider alternative analgesic due to variable metabolism",
            ("CYP2C19", "Clopidogrel"): "Consider alternative antiplatelet therapy",
            ("SLCO1B1", "Simvastatin"): "Consider lower dose or alternative statin",
            ("DPYD", "Fluorouracil"): "Consider dose reduction or alternative therapy",
            ("TPMT", "Mercaptopurine"): "Consider dose reduction based on activity",
            ("UGT1A1", "Irinotecan"): "Consider dose reduction to prevent toxicity"
        }
        
        return recommendations.get((gene, drug), f"Consult pharmacogenomic guidelines for {gene}-{drug} interaction")
    
    def get_database_info(self) -> Dict:
        """Get information about PharmGKB database"""
        return {
            "name": "PharmGKB",
            "description": "Pharmacogenomics Knowledgebase - Drug-gene interactions",
            "url": "https://www.pharmgkb.org/",
            "api_url": self.base_url,
            "version": "Current",
            "last_updated": "Monthly",
            "data_types": [
                "Drug-gene interactions",
                "Pharmacogenomic variants",
                "Clinical guidelines",
                "Dosing recommendations",
                "Drug response predictions"
            ],
            "guidelines": ["CPIC", "FDA", "EMA", "DPWG"]
        } 