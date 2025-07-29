#!/usr/bin/env python3
"""
Real Annotation Database - Integration with actual bioinformatics databases

This module provides real-time access to major bioinformatics databases
including ClinVar, gnomAD, dbSNP, COSMIC, OMIM, PharmGKB, ClinGen, HGMD, and Ensembl.

Enhanced with:
- Batch processing capabilities
- Smart caching with TTL
- API key management
- Custom database priorities
- Annotation confidence scores
"""

import time
import json
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

from ..databases.clinvar import ClinVarDatabase
from ..databases.gnomad import GnomADDatabase
from ..databases.dbsnp import DbSNPDatabase
from ..databases.cosmic import COSMICDatabase
from ..databases.omim import OMIMDatabase
from ..databases.pharmgkb import PharmGKBDatabase
from ..databases.clingen import ClinGenDatabase
from ..databases.hgmd import HGMDDatabase
from ..databases.ensembl import EnsemblDatabase

class SmartCache:
    """
    Smart caching system with TTL (Time To Live) support
    """
    
    def __init__(self, cache_dir: Path, default_ttl: int = 86400):  # 24 hours default
        """
        Initialize smart cache
        
        Args:
            cache_dir: Cache directory
            default_ttl: Default TTL in seconds
        """
        self.cache_dir = cache_dir
        self.default_ttl = default_ttl
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # TTL settings for different databases
        self.database_ttl = {
            "clinvar": 86400,    # 24 hours
            "gnomad": 604800,    # 7 days (stable population data)
            "dbsnp": 604800,     # 7 days
            "cosmic": 86400,     # 24 hours
            "omim": 604800,      # 7 days (disease associations stable)
            "pharmgkb": 604800,  # 7 days (guidelines stable)
            "clingen": 604800,   # 7 days (gene-disease validity stable)
            "hgmd": 86400,       # 24 hours (mutation database updates)
            "ensembl": 2592000   # 30 days (genome annotation stable)
        }
    
    def get_cache_path(self, database: str, key: str) -> Path:
        """Get cache file path"""
        safe_key = key.replace(":", "_").replace(">", "_").replace("/", "_")
        return self.cache_dir / f"{database}_{safe_key}.json"
    
    def get(self, database: str, key: str) -> Optional[Dict]:
        """Get cached data if not expired"""
        cache_path = self.get_cache_path(database, key)
        
        if not cache_path.exists():
            return None
        
        try:
            with open(cache_path, 'r') as f:
                cached_data = json.load(f)
            
            # Check TTL
            cached_time = datetime.fromisoformat(cached_data.get("cached_at", "1970-01-01"))
            ttl = self.database_ttl.get(database, self.default_ttl)
            
            if datetime.now() - cached_time > timedelta(seconds=ttl):
                # Cache expired
                cache_path.unlink(missing_ok=True)
                return None
            
            return cached_data.get("data")
            
        except Exception:
            return None
    
    def set(self, database: str, key: str, data: Dict):
        """Cache data with timestamp"""
        cache_path = self.get_cache_path(database, key)
        
        cached_data = {
            "data": data,
            "cached_at": datetime.now().isoformat(),
            "database": database,
            "key": key
        }
        
        try:
            with open(cache_path, 'w') as f:
                json.dump(cached_data, f, indent=2)
        except Exception:
            pass
    
    def clear_expired(self):
        """Clear all expired cache entries"""
        cleared_count = 0
        
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, 'r') as f:
                    cached_data = json.load(f)
                
                cached_time = datetime.fromisoformat(cached_data.get("cached_at", "1970-01-01"))
                database = cached_data.get("database", "unknown")
                ttl = self.database_ttl.get(database, self.default_ttl)
                
                if datetime.now() - cached_time > timedelta(seconds=ttl):
                    cache_file.unlink()
                    cleared_count += 1
                    
            except Exception:
                # Remove corrupted cache files
                cache_file.unlink(missing_ok=True)
                cleared_count += 1
        
        return cleared_count

class APIKeyManager:
    """
    Centralized API key management
    """
    
    def __init__(self, config_file: Optional[Path] = None):
        """
        Initialize API key manager
        
        Args:
            config_file: Optional config file path
        """
        self.config_file = config_file or Path.home() / ".varannote" / "api_keys.json"
        self.api_keys = self._load_api_keys()
    
    def _load_api_keys(self) -> Dict[str, str]:
        """Load API keys from config file"""
        if not self.config_file.exists():
            return {}
        
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except Exception:
            return {}
    
    def get_key(self, database: str) -> Optional[str]:
        """Get API key for database"""
        return self.api_keys.get(database)
    
    def set_key(self, database: str, api_key: str):
        """Set API key for database"""
        self.api_keys[database] = api_key
        self._save_api_keys()
    
    def _save_api_keys(self):
        """Save API keys to config file"""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.api_keys, f, indent=2)
        except Exception:
            pass

class RealAnnotationDatabase:
    """
    Enhanced real annotation database integrating multiple sources
    
    Provides unified access to:
    - ClinVar (clinical significance)
    - gnomAD (population frequencies)
    - dbSNP (variant identifiers)
    - COSMIC (cancer mutations)
    - OMIM (disease-gene associations)
    - PharmGKB (pharmacogenomics)
    - ClinGen (gene-disease validity)
    - HGMD (disease-causing mutations)
    - Ensembl (gene annotation & VEP)
    
    Enhanced features:
    - Batch processing
    - Smart caching with TTL
    - API key management
    - Custom database priorities
    - Annotation confidence scores
    """
    
    def __init__(self, genome: str = "hg38", cache_dir: Optional[str] = None, 
                 use_cache: bool = True, api_keys: Optional[Dict[str, str]] = None,
                 database_priorities: Optional[Dict[str, int]] = None):
        """
        Initialize enhanced real annotation database
        
        Args:
            genome: Reference genome version
            cache_dir: Directory for caching results
            use_cache: Whether to use local caching
            api_keys: Dictionary of API keys for databases
            database_priorities: Custom priority scores for databases
        """
        self.genome = genome
        self.cache_dir = Path(cache_dir) if cache_dir else Path.home() / ".varannote" / "cache"
        self.use_cache = use_cache
        
        # Initialize smart cache
        self.smart_cache = SmartCache(self.cache_dir) if use_cache else None
        
        # Initialize API key manager
        self.api_key_manager = APIKeyManager()
        if api_keys:
            for db, key in api_keys.items():
                self.api_key_manager.set_key(db, key)
        
        # Database priorities (higher = more important)
        self.database_priorities = database_priorities or {
            "clinvar": 12,    # Highest priority for clinical data
            "clingen": 11,    # Gene-disease validity
            "hgmd": 10,       # Disease-causing mutations
            "omim": 9,        # Disease associations
            "ensembl": 8,     # Gene annotation and VEP
            "pharmgkb": 7,    # Pharmacogenomics
            "gnomad": 6,      # Population frequencies
            "cosmic": 5,      # Cancer data
            "dbsnp": 4        # Variant IDs
        }
        
        # Initialize database connections
        self._init_databases()
        
        # Thread lock for thread-safe operations
        self._lock = threading.Lock()
    
    def _init_databases(self):
        """Initialize all database connections"""
        
        # Get API keys
        omim_key = self.api_key_manager.get_key("omim")
        cosmic_key = self.api_key_manager.get_key("cosmic")
        hgmd_key = self.api_key_manager.get_key("hgmd")
        
        # Initialize databases
        self.clinvar = ClinVarDatabase(cache_dir=self.cache_dir, use_cache=self.use_cache)
        self.gnomad = GnomADDatabase(cache_dir=self.cache_dir, use_cache=self.use_cache)
        self.dbsnp = DbSNPDatabase(cache_dir=self.cache_dir, use_cache=self.use_cache)
        self.cosmic = COSMICDatabase(cache_dir=self.cache_dir, use_cache=self.use_cache, 
                                   api_key=cosmic_key)
        self.omim = OMIMDatabase(api_key=omim_key, cache_dir=self.cache_dir, use_cache=self.use_cache)
        self.pharmgkb = PharmGKBDatabase(cache_dir=self.cache_dir, use_cache=self.use_cache)
        self.clingen = ClinGenDatabase(cache_dir=self.cache_dir, use_cache=self.use_cache)
        self.hgmd = HGMDDatabase(api_key=hgmd_key, cache_dir=self.cache_dir, use_cache=self.use_cache)
        self.ensembl = EnsemblDatabase(cache_dir=self.cache_dir, use_cache=self.use_cache)
        
        # Available databases
        self.databases = {
            "clinvar": self.clinvar,
            "gnomad": self.gnomad,
            "dbsnp": self.dbsnp,
            "cosmic": self.cosmic,
            "omim": self.omim,
            "pharmgkb": self.pharmgkb,
            "clingen": self.clingen,
            "hgmd": self.hgmd,
            "ensembl": self.ensembl
        }
    
    def get_annotations(self, variant: Dict, database: str = "all", 
                       use_cache: bool = True) -> Dict:
        """
        Get annotations for a variant from specified database(s)
        
        Args:
            variant: Variant dictionary with CHROM, POS, REF, ALT
            database: Database name or "all"
            use_cache: Whether to use smart caching
            
        Returns:
            Dictionary with annotations from requested database(s)
        """
        annotations = {}
        
        chrom = str(variant["CHROM"])
        pos = int(variant["POS"])
        ref = variant["REF"]
        alt = variant["ALT"]
        variant_key = f"{chrom}:{pos}:{ref}>{alt}"
        
        if database == "all":
            # Get annotations from all databases in priority order
            sorted_dbs = sorted(self.databases.items(), 
                              key=lambda x: self.database_priorities.get(x[0], 0), 
                              reverse=True)
            
            for db_name, db_instance in sorted_dbs:
                try:
                    db_annotations = self._get_database_annotations(
                        db_name, db_instance, chrom, pos, ref, alt, variant_key, use_cache
                    )
                    annotations.update(db_annotations)
                except Exception as e:
                    print(f"Warning: Failed to get {db_name} annotations: {e}")
        
        elif database in self.databases:
            # Get annotations from specific database
            try:
                db_instance = self.databases[database]
                annotations = self._get_database_annotations(
                    database, db_instance, chrom, pos, ref, alt, variant_key, use_cache
                )
            except Exception as e:
                print(f"Warning: Failed to get {database} annotations: {e}")
        
        else:
            raise ValueError(f"Unknown database: {database}")
        
        # Add confidence scores
        annotations["annotation_confidence"] = self._calculate_confidence_score(annotations)
        
        return annotations
    
    def _get_database_annotations(self, db_name: str, db_instance, chrom: str, pos: int, 
                                ref: str, alt: str, variant_key: str, use_cache: bool) -> Dict:
        """Get annotations from a specific database with smart caching"""
        
        # Check smart cache first
        if use_cache and self.smart_cache:
            cached_result = self.smart_cache.get(db_name, variant_key)
            if cached_result:
                return cached_result
        
        # Get fresh annotations
        if db_name in ["omim", "pharmgkb", "clingen"]:
            # These databases need gene symbol
            gene_symbol = self._get_gene_symbol(chrom, pos)
            if gene_symbol and hasattr(db_instance, 'get_gene_annotation'):
                annotations = db_instance.get_gene_annotation(gene_symbol)
            else:
                annotations = db_instance.get_variant_annotation(chrom, pos, ref, alt)
        else:
            annotations = db_instance.get_variant_annotation(chrom, pos, ref, alt)
        
        # Cache the result
        if use_cache and self.smart_cache:
            self.smart_cache.set(db_name, variant_key, annotations)
        
        return annotations
    
    def _get_gene_symbol(self, chrom: str, pos: int) -> Optional[str]:
        """Get gene symbol for genomic coordinates (simplified)"""
        # This is a simplified implementation
        # In practice, would use proper gene annotation
        
        gene_regions = {
            "17": {
                (43044295, 43125483): "BRCA1",
                (7565097, 7590856): "TP53"
            },
            "13": {
                (32315086, 32400266): "BRCA2"
            }
        }
        
        if chrom in gene_regions:
            for (start, end), gene in gene_regions[chrom].items():
                if start <= pos <= end:
                    return gene
        
        return None
    
    def batch_annotate(self, variants: List[Dict], databases: Optional[List[str]] = None,
                      max_workers: int = 4, use_parallel: bool = True) -> List[Dict]:
        """
        Annotate multiple variants with enhanced batch processing
        
        Args:
            variants: List of variant dictionaries
            databases: List of databases to use (default: all)
            max_workers: Maximum number of parallel workers
            use_parallel: Whether to use parallel processing
            
        Returns:
            List of variants with annotations added
        """
        if databases is None:
            databases = list(self.databases.keys())
        
        print(f"🔗 Starting enhanced batch annotation for {len(variants)} variants...")
        print(f"📊 Using databases: {', '.join(databases)}")
        print(f"⚡ Parallel processing: {'enabled' if use_parallel else 'disabled'}")
        
        if use_parallel and len(variants) > 1:
            return self._batch_annotate_parallel(variants, databases, max_workers)
        else:
            return self._batch_annotate_sequential(variants, databases)
    
    def _batch_annotate_parallel(self, variants: List[Dict], databases: List[str], 
                               max_workers: int) -> List[Dict]:
        """Parallel batch annotation"""
        
        annotated_variants = [None] * len(variants)  # Pre-allocate list
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all annotation tasks
            future_to_index = {}
            
            for i, variant in enumerate(variants):
                future = executor.submit(self._annotate_single_variant, variant, databases)
                future_to_index[future] = i
            
            # Collect results as they complete
            completed = 0
            for future in as_completed(future_to_index):
                index = future_to_index[future]
                completed += 1
                
                try:
                    annotated_variant = future.result()
                    annotated_variants[index] = annotated_variant
                    
                    if completed % 10 == 0 or completed == len(variants):
                        print(f"  ✅ Completed {completed}/{len(variants)} variants")
                        
                except Exception as e:
                    print(f"  ❌ Error annotating variant {index}: {e}")
                    # Add original variant with error annotation
                    annotated_variants[index] = {
                        **variants[index],
                        "annotation_error": str(e)
                    }
        
        print(f"🎉 Parallel batch annotation complete!")
        return annotated_variants
    
    def _batch_annotate_sequential(self, variants: List[Dict], databases: List[str]) -> List[Dict]:
        """Sequential batch annotation"""
        
        annotated_variants = []
        
        for i, variant in enumerate(variants):
            print(f"\n🧬 Annotating variant {i+1}/{len(variants)}: {variant.get('variant_id', 'unknown')}")
            
            try:
                annotated_variant = self._annotate_single_variant(variant, databases)
                annotated_variants.append(annotated_variant)
                
            except Exception as e:
                print(f"    ❌ Error: {e}")
                annotated_variants.append({
                    **variant,
                    "annotation_error": str(e)
                })
        
        print(f"\n🎉 Sequential batch annotation complete!")
        return annotated_variants
    
    def _annotate_single_variant(self, variant: Dict, databases: List[str]) -> Dict:
        """Annotate a single variant with specified databases"""
        
        # Start with the original variant
        annotated_variant = variant.copy()
        
        # Annotate with each requested database
        for db_name in databases:
            if db_name in self.databases:
                try:
                    db_annotations = self.get_annotations(variant, db_name)
                    annotated_variant.update(db_annotations)
                    
                except Exception as e:
                    print(f"    ⚠️  {db_name}: Error - {e}")
        
        return annotated_variant
    
    def _calculate_confidence_score(self, annotations: Dict) -> float:
        """
        Calculate annotation confidence score based on data availability and quality
        
        Args:
            annotations: Dictionary of annotations
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        score = 0.0
        max_score = 0.0
        
        # Database-specific scoring with updated weights
        scoring_weights = {
            "clinvar_significance": 0.25,      # Clinical significance
            "clingen_validity": 0.20,          # Gene-disease validity
            "hgmd_pathogenicity": 0.15,        # Disease-causing mutations
            "omim_diseases": 0.10,             # Disease associations
            "ensembl_consequence": 0.10,       # Variant consequences
            "pharmgkb_drugs": 0.08,            # Pharmacogenomics
            "gnomad_af": 0.07,                 # Population frequencies
            "cosmic_id": 0.03,                 # Cancer mutations
            "dbsnp_id": 0.02                   # Variant IDs
        }
        
        for field, weight in scoring_weights.items():
            max_score += weight
            
            if field in annotations and annotations[field] is not None:
                # Add weight for having data
                score += weight
                
                # Bonus for high-quality data
                if field == "clinvar_significance" and annotations[field] in ["Pathogenic", "Benign"]:
                    score += weight * 0.5  # 50% bonus for definitive clinical significance
                elif field == "clingen_validity" and annotations[field] in ["Definitive", "Strong"]:
                    score += weight * 0.4  # 40% bonus for strong gene-disease evidence
                elif field == "hgmd_pathogenicity" and "Disease-causing" in str(annotations[field]):
                    score += weight * 0.4  # 40% bonus for disease-causing mutations
                elif field == "ensembl_consequence" and annotations[field] in ["stop_gained", "frameshift_variant"]:
                    score += weight * 0.3  # 30% bonus for high-impact consequences
                elif field == "gnomad_af" and isinstance(annotations[field], (int, float)):
                    score += weight * 0.2  # 20% bonus for population frequency data
        
        return round(score / max_score, 3) if max_score > 0 else 0.0
    
    def get_available_databases(self) -> List[str]:
        """Get list of available databases"""
        return list(self.databases.keys())
    
    def get_database_info(self, database: str) -> Dict:
        """Get information about a specific database"""
        if database in self.databases:
            return self.databases[database].get_database_info()
        else:
            raise ValueError(f"Unknown database: {database}")
    
    def get_all_database_info(self) -> Dict:
        """Get information about all databases"""
        info = {}
        for db_name, db_instance in self.databases.items():
            info[db_name] = db_instance.get_database_info()
        return info
    
    def test_connections(self) -> Dict:
        """
        Test connections to all databases
        
        Returns:
            Dictionary with connection status for each database
        """
        print("🔍 Testing enhanced database connections...")
        
        # Test variant (common SNP)
        test_variant = {
            "CHROM": "17",
            "POS": 43044295,
            "REF": "G", 
            "ALT": "A"
        }
        
        results = {}
        
        for db_name, db_instance in self.databases.items():
            try:
                print(f"  Testing {db_name}...")
                
                if db_name in ["omim", "pharmgkb", "clingen"]:
                    # Test gene-based databases
                    annotations = db_instance.get_gene_annotation("BRCA1")
                else:
                    # Test variant-based databases
                    annotations = db_instance.get_variant_annotation(
                        test_variant["CHROM"],
                        test_variant["POS"],
                        test_variant["REF"],
                        test_variant["ALT"]
                    )
                
                # Check if we got meaningful data
                has_data = any(v is not None for v in annotations.values())
                
                results[db_name] = {
                    "status": "✅ Connected" if has_data else "⚠️ Connected (no data)",
                    "data_received": has_data,
                    "fields": list(annotations.keys()),
                    "priority": self.database_priorities.get(db_name, 0)
                }
                
            except Exception as e:
                results[db_name] = {
                    "status": f"❌ Failed: {str(e)}",
                    "data_received": False,
                    "fields": [],
                    "priority": self.database_priorities.get(db_name, 0)
                }
        
        return results
    
    def clear_cache(self, database: Optional[str] = None) -> int:
        """
        Clear cache entries
        
        Args:
            database: Specific database to clear (None for all)
            
        Returns:
            Number of cache entries cleared
        """
        if not self.smart_cache:
            return 0
        
        if database is None:
            return self.smart_cache.clear_expired()
        else:
            # Clear specific database cache
            cleared = 0
            pattern = f"{database}_*.json"
            
            for cache_file in self.cache_dir.glob(pattern):
                try:
                    cache_file.unlink()
                    cleared += 1
                except Exception:
                    pass
            
            return cleared
    
    def get_cache_stats(self) -> Dict:
        """Get cache statistics"""
        if not self.smart_cache:
            return {"cache_enabled": False}
        
        stats = {"cache_enabled": True, "databases": {}}
        
        for db_name in self.databases.keys():
            pattern = f"{db_name}_*.json"
            cache_files = list(self.cache_dir.glob(pattern))
            
            total_size = sum(f.stat().st_size for f in cache_files if f.exists())
            
            stats["databases"][db_name] = {
                "cached_entries": len(cache_files),
                "total_size_bytes": total_size,
                "ttl_seconds": self.smart_cache.database_ttl.get(db_name, self.smart_cache.default_ttl)
            }
        
        return stats 