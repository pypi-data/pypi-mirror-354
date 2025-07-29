#!/usr/bin/env python3
"""
Real Annotation Database Tests for VarAnnote v1.0.0

Comprehensive tests for the real annotation database system:
- SmartCache functionality
- APIKeyManager
- RealAnnotationDatabase integration
- Batch processing
- Confidence scoring
"""

import pytest
import tempfile
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock

from varannote.utils.real_annotation_db import (
    SmartCache, 
    APIKeyManager, 
    RealAnnotationDatabase
)


class TestSmartCache:
    """Comprehensive test suite for SmartCache"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.cache_dir = Path(self.temp_dir)
        self.cache = SmartCache(self.cache_dir, default_ttl=3600)  # 1 hour
    
    def teardown_method(self):
        """Clean up test fixtures"""
        import shutil
        try:
            shutil.rmtree(self.temp_dir)
        except (PermissionError, OSError):
            pass
    
    def test_smart_cache_initialization(self):
        """Test SmartCache initialization"""
        assert self.cache.cache_dir == self.cache_dir
        assert self.cache.default_ttl == 3600
        assert self.cache_dir.exists()
        
        # Check database TTL settings
        assert self.cache.database_ttl["clinvar"] == 86400
        assert self.cache.database_ttl["gnomad"] == 604800
        assert self.cache.database_ttl["ensembl"] == 2592000
    
    def test_cache_path_generation(self):
        """Test cache path generation"""
        path = self.cache.get_cache_path("clinvar", "chr17:43044295:G>A")
        
        assert path.parent == self.cache_dir
        assert "clinvar_chr17_43044295_G_A.json" in str(path)
    
    def test_cache_set_and_get(self):
        """Test cache set and get operations"""
        test_data = {
            "clinvar_significance": "Pathogenic",
            "clinvar_id": "VCV000012345"
        }
        
        # Set cache
        self.cache.set("clinvar", "chr17:43044295:G>A", test_data)
        
        # Get cache
        retrieved_data = self.cache.get("clinvar", "chr17:43044295:G>A")
        
        assert retrieved_data == test_data
    
    def test_cache_get_nonexistent(self):
        """Test getting non-existent cache entry"""
        result = self.cache.get("clinvar", "nonexistent_key")
        assert result is None
    
    def test_cache_ttl_expiration(self):
        """Test cache TTL expiration"""
        # Create cache with very short TTL
        short_cache = SmartCache(self.cache_dir, default_ttl=1)
        short_cache.database_ttl["test_db"] = 1  # 1 second TTL
        
        test_data = {"test": "data"}
        
        # Set cache
        short_cache.set("test_db", "test_key", test_data)
        
        # Should be available immediately
        assert short_cache.get("test_db", "test_key") == test_data
        
        # Wait for expiration
        time.sleep(2)
        
        # Should be expired
        assert short_cache.get("test_db", "test_key") is None
    
    def test_cache_clear_expired(self):
        """Test clearing expired cache entries"""
        # Create cache with very short TTL
        short_cache = SmartCache(self.cache_dir, default_ttl=1)
        short_cache.database_ttl["test_db"] = 1
        
        # Add some cache entries
        short_cache.set("test_db", "key1", {"data": "1"})
        short_cache.set("test_db", "key2", {"data": "2"})
        
        # Wait for expiration
        time.sleep(2)
        
        # Clear expired entries
        cleared_count = short_cache.clear_expired()
        
        assert cleared_count >= 2
    
    def test_cache_corrupted_file_handling(self):
        """Test handling of corrupted cache files"""
        # Create a corrupted cache file
        corrupted_file = self.cache_dir / "corrupted_cache.json"
        with open(corrupted_file, 'w') as f:
            f.write("invalid json content")
        
        # clear_expired should handle corrupted files gracefully
        cleared_count = self.cache.clear_expired()
        assert cleared_count >= 1
        assert not corrupted_file.exists()


class TestAPIKeyManager:
    """Test suite for APIKeyManager"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = Path(self.temp_dir) / "api_keys.json"
        self.api_manager = APIKeyManager(self.config_file)
    
    def teardown_method(self):
        """Clean up test fixtures"""
        import shutil
        try:
            shutil.rmtree(self.temp_dir)
        except (PermissionError, OSError):
            pass
    
    def test_api_key_manager_initialization(self):
        """Test APIKeyManager initialization"""
        assert self.api_manager.config_file == self.config_file
        assert isinstance(self.api_manager.api_keys, dict)
    
    def test_api_key_manager_initialization_default(self):
        """Test APIKeyManager initialization with default config"""
        manager = APIKeyManager()
        expected_path = Path.home() / ".varannote" / "api_keys.json"
        assert manager.config_file == expected_path
    
    def test_set_and_get_api_key(self):
        """Test setting and getting API keys"""
        # Set API key
        self.api_manager.set_key("cosmic", "test_cosmic_key")
        
        # Get API key
        retrieved_key = self.api_manager.get_key("cosmic")
        assert retrieved_key == "test_cosmic_key"
    
    def test_get_nonexistent_api_key(self):
        """Test getting non-existent API key"""
        result = self.api_manager.get_key("nonexistent_db")
        assert result is None
    
    def test_api_key_persistence(self):
        """Test API key persistence to file"""
        # Set API key
        self.api_manager.set_key("hgmd", "test_hgmd_key")
        
        # Create new manager instance
        new_manager = APIKeyManager(self.config_file)
        
        # Should load the saved key
        assert new_manager.get_key("hgmd") == "test_hgmd_key"
    
    def test_load_existing_api_keys(self):
        """Test loading existing API keys from file"""
        # Create config file with existing keys
        existing_keys = {
            "cosmic": "cosmic_key_123",
            "hgmd": "hgmd_key_456"
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(existing_keys, f)
        
        # Create manager
        manager = APIKeyManager(self.config_file)
        
        assert manager.get_key("cosmic") == "cosmic_key_123"
        assert manager.get_key("hgmd") == "hgmd_key_456"
    
    def test_corrupted_config_file_handling(self):
        """Test handling of corrupted config file"""
        # Create corrupted config file
        with open(self.config_file, 'w') as f:
            f.write("invalid json")
        
        # Should handle gracefully
        manager = APIKeyManager(self.config_file)
        assert manager.api_keys == {}


class TestRealAnnotationDatabase:
    """Comprehensive test suite for RealAnnotationDatabase"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        
        # Sample variant for testing
        self.sample_variant = {
            'CHROM': 'chr17',
            'POS': 43044295,
            'REF': 'G',
            'ALT': 'A',
            'variant_id': 'chr17:43044295:G>A'
        }
    
    def teardown_method(self):
        """Clean up test fixtures"""
        import shutil
        try:
            shutil.rmtree(self.temp_dir)
        except (PermissionError, OSError):
            pass
    
    def test_real_annotation_db_initialization(self):
        """Test RealAnnotationDatabase initialization"""
        db = RealAnnotationDatabase(
            genome="hg38",
            cache_dir=self.temp_dir,
            use_cache=True
        )
        
        assert db.genome == "hg38"
        assert db.use_cache is True
        assert db.cache_dir == Path(self.temp_dir)
        assert isinstance(db.smart_cache, SmartCache)
        assert isinstance(db.api_key_manager, APIKeyManager)
    
    def test_real_annotation_db_initialization_custom(self):
        """Test RealAnnotationDatabase initialization with custom parameters"""
        api_keys = {"cosmic": "test_key"}
        priorities = {"clinvar": 1, "gnomad": 2}
        
        db = RealAnnotationDatabase(
            genome="hg19",
            cache_dir=self.temp_dir,
            use_cache=False,
            api_keys=api_keys,
            database_priorities=priorities
        )
        
        assert db.genome == "hg19"
        assert db.use_cache is False
        assert db.database_priorities == priorities
        assert db.api_key_manager.get_key("cosmic") == "test_key"
    
    def test_database_initialization(self):
        """Test database instances initialization"""
        db = RealAnnotationDatabase(cache_dir=self.temp_dir)
        
        # Check that all database instances are created
        assert hasattr(db, 'clinvar_db')
        assert hasattr(db, 'gnomad_db')
        assert hasattr(db, 'dbsnp_db')
        assert hasattr(db, 'cosmic_db')
        assert hasattr(db, 'omim_db')
        assert hasattr(db, 'pharmgkb_db')
        assert hasattr(db, 'clingen_db')
        assert hasattr(db, 'hgmd_db')
        assert hasattr(db, 'ensembl_db')
    
    @patch('varannote.utils.real_annotation_db.ClinVarDatabase')
    def test_get_annotations_single_database(self, mock_clinvar):
        """Test getting annotations from single database"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.get_variant_annotation.return_value = {
            "clinvar_significance": "Pathogenic"
        }
        mock_clinvar.return_value = mock_instance
        
        db = RealAnnotationDatabase(cache_dir=self.temp_dir)
        db.clinvar_db = mock_instance
        
        result = db.get_annotations(self.sample_variant, "clinvar")
        
        assert "clinvar_significance" in result
        assert result["clinvar_significance"] == "Pathogenic"
    
    @patch('varannote.utils.real_annotation_db.ClinVarDatabase')
    @patch('varannote.utils.real_annotation_db.GnomADDatabase')
    def test_get_annotations_all_databases(self, mock_gnomad, mock_clinvar):
        """Test getting annotations from all databases"""
        # Setup mocks
        mock_clinvar_instance = Mock()
        mock_clinvar_instance.get_variant_annotation.return_value = {
            "clinvar_significance": "Pathogenic"
        }
        mock_clinvar.return_value = mock_clinvar_instance
        
        mock_gnomad_instance = Mock()
        mock_gnomad_instance.get_variant_annotation.return_value = {
            "gnomad_af": 0.001
        }
        mock_gnomad.return_value = mock_gnomad_instance
        
        db = RealAnnotationDatabase(cache_dir=self.temp_dir)
        db.clinvar_db = mock_clinvar_instance
        db.gnomad_db = mock_gnomad_instance
        
        result = db.get_annotations(self.sample_variant, "all")
        
        assert "clinvar_significance" in result
        assert "gnomad_af" in result
        assert "annotation_confidence" in result
    
    def test_get_available_databases(self):
        """Test getting available databases"""
        db = RealAnnotationDatabase(cache_dir=self.temp_dir)
        databases = db.get_available_databases()
        
        expected_databases = [
            "clinvar", "gnomad", "dbsnp", "cosmic", "omim", 
            "pharmgkb", "clingen", "hgmd", "ensembl"
        ]
        
        for expected_db in expected_databases:
            assert expected_db in databases
    
    def test_get_database_info(self):
        """Test getting database info"""
        db = RealAnnotationDatabase(cache_dir=self.temp_dir)
        
        with patch.object(db.clinvar_db, 'get_database_info') as mock_info:
            mock_info.return_value = {
                "name": "ClinVar",
                "description": "Clinical significance database"
            }
            
            info = db.get_database_info("clinvar")
            assert info["name"] == "ClinVar"
    
    def test_get_all_database_info(self):
        """Test getting all database info"""
        db = RealAnnotationDatabase(cache_dir=self.temp_dir)
        
        # Mock all database info methods
        for db_name in db.get_available_databases():
            db_instance = getattr(db, f"{db_name}_db")
            with patch.object(db_instance, 'get_database_info') as mock_info:
                mock_info.return_value = {"name": db_name.upper()}
        
        all_info = db.get_all_database_info()
        assert isinstance(all_info, dict)
        assert len(all_info) > 0
    
    def test_calculate_confidence_score(self):
        """Test confidence score calculation"""
        db = RealAnnotationDatabase(cache_dir=self.temp_dir)
        
        # Test with high-confidence annotations
        high_conf_annotations = {
            "clinvar_significance": "Pathogenic",
            "gnomad_af": 0.001,
            "dbsnp_id": "rs123456",
            "gene": "BRCA1"
        }
        
        score = db._calculate_confidence_score(high_conf_annotations)
        assert 0.0 <= score <= 1.0
        assert score > 0.5  # Should be high confidence
        
        # Test with low-confidence annotations
        low_conf_annotations = {
            "clinvar_significance": None,
            "gnomad_af": None
        }
        
        score = db._calculate_confidence_score(low_conf_annotations)
        assert 0.0 <= score <= 1.0
        assert score < 0.5  # Should be low confidence
    
    def test_batch_annotate_sequential(self):
        """Test batch annotation in sequential mode"""
        db = RealAnnotationDatabase(cache_dir=self.temp_dir, use_cache=False)
        
        variants = [
            self.sample_variant,
            {
                'CHROM': 'chr13',
                'POS': 32906729,
                'REF': 'C',
                'ALT': 'T',
                'variant_id': 'chr13:32906729:C>T'
            }
        ]
        
        with patch.object(db, 'get_annotations') as mock_get:
            mock_get.return_value = {"clinvar_significance": "Pathogenic"}
            
            results = db.batch_annotate(
                variants, 
                databases=["clinvar"], 
                use_parallel=False
            )
            
            assert len(results) == 2
            assert all("clinvar_significance" in result for result in results)
    
    def test_batch_annotate_parallel(self):
        """Test batch annotation in parallel mode"""
        db = RealAnnotationDatabase(cache_dir=self.temp_dir, use_cache=False)
        
        variants = [self.sample_variant] * 3  # 3 identical variants
        
        with patch.object(db, '_annotate_single_variant') as mock_annotate:
            mock_annotate.return_value = {
                **self.sample_variant,
                "clinvar_significance": "Pathogenic"
            }
            
            results = db.batch_annotate(
                variants,
                databases=["clinvar"],
                use_parallel=True,
                max_workers=2
            )
            
            assert len(results) == 3
            assert mock_annotate.call_count == 3
    
    def test_cache_operations(self):
        """Test cache operations"""
        db = RealAnnotationDatabase(cache_dir=self.temp_dir, use_cache=True)
        
        # Test cache stats
        stats = db.get_cache_stats()
        assert isinstance(stats, dict)
        assert "total_files" in stats
        assert "total_size_mb" in stats
        
        # Test cache clearing
        cleared_count = db.clear_cache()
        assert isinstance(cleared_count, int)
        assert cleared_count >= 0
    
    def test_test_connections(self):
        """Test database connection testing"""
        db = RealAnnotationDatabase(cache_dir=self.temp_dir)
        
        # Mock all database test methods
        for db_name in ["clinvar", "gnomad"]:  # Test subset for speed
            db_instance = getattr(db, f"{db_name}_db")
            with patch.object(db_instance, 'get_variant_annotation') as mock_test:
                mock_test.return_value = {"test": "success"}
        
        results = db.test_connections()
        assert isinstance(results, dict)
    
    def test_gene_symbol_retrieval(self):
        """Test gene symbol retrieval"""
        db = RealAnnotationDatabase(cache_dir=self.temp_dir)
        
        with patch.object(db.ensembl_db, 'get_variant_annotation') as mock_ensembl:
            mock_ensembl.return_value = {"gene": "BRCA1"}
            
            gene = db._get_gene_symbol("17", 43044295)
            assert gene == "BRCA1"
    
    def test_error_handling_in_annotations(self):
        """Test error handling during annotation"""
        db = RealAnnotationDatabase(cache_dir=self.temp_dir)
        
        with patch.object(db.clinvar_db, 'get_variant_annotation') as mock_clinvar:
            mock_clinvar.side_effect = Exception("API Error")
            
            # Should handle errors gracefully
            result = db.get_annotations(self.sample_variant, "clinvar")
            assert isinstance(result, dict)
            # Should still return some result even with errors


class TestRealAnnotationDatabaseIntegration:
    """Integration tests for RealAnnotationDatabase"""
    
    def test_full_annotation_workflow(self):
        """Test complete annotation workflow"""
        temp_dir = tempfile.mkdtemp()
        
        try:
            db = RealAnnotationDatabase(cache_dir=temp_dir, use_cache=True)
            
            variant = {
                'CHROM': 'chr17',
                'POS': 43044295,
                'REF': 'G',
                'ALT': 'A',
                'variant_id': 'chr17:43044295:G>A'
            }
            
            # Mock database responses
            with patch.object(db.clinvar_db, 'get_variant_annotation') as mock_clinvar:
                with patch.object(db.gnomad_db, 'get_variant_annotation') as mock_gnomad:
                    mock_clinvar.return_value = {"clinvar_significance": "Pathogenic"}
                    mock_gnomad.return_value = {"gnomad_af": 0.001}
                    
                    # Test single annotation
                    result = db.get_annotations(variant, "all")
                    
                    assert "clinvar_significance" in result
                    assert "gnomad_af" in result
                    assert "annotation_confidence" in result
                    
                    # Test batch annotation
                    batch_results = db.batch_annotate([variant, variant])
                    assert len(batch_results) == 2
                    
        finally:
            import shutil
            try:
                shutil.rmtree(temp_dir)
            except (PermissionError, OSError):
                pass


if __name__ == "__main__":
    pytest.main([__file__]) 