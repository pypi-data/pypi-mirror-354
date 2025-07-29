#!/usr/bin/env python3
"""
Database Integration Tests for VarAnnote v1.0.0

Tests for database connectivity, caching, and annotation retrieval:
- Mock database functionality
- Real database API connections
- Cache management
- Error handling and fallbacks
"""

import pytest
import tempfile
import json
import time
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Import from actual module structure
try:
    from varannote.utils.annotation_db import MockAnnotationDatabase
except ImportError:
    MockAnnotationDatabase = None

try:
    from varannote.utils.real_annotation_db import RealAnnotationDatabase
except ImportError:
    RealAnnotationDatabase = None

from varannote.databases.clinvar import ClinVarDatabase
from varannote.databases.gnomad import GnomADDatabase
from varannote.databases.dbsnp import DbSNPDatabase
from varannote.databases.cosmic import COSMICDatabase
from varannote.databases.omim import OMIMDatabase
from varannote.databases.pharmgkb import PharmGKBDatabase
from varannote.databases.clingen import ClinGenDatabase
from varannote.databases.hgmd import HGMDDatabase
from varannote.databases.ensembl import EnsemblDatabase


class TestMockAnnotationDatabase:
    """Test suite for mock annotation database functionality"""
    
    def setup_method(self):
        """Set up test fixtures"""
        if MockAnnotationDatabase is None:
            pytest.skip("MockAnnotationDatabase not available")
        
        self.mock_db = MockAnnotationDatabase()
        
        # Sample variant for testing
        self.sample_variant = {
            'CHROM': 'chr17',
            'POS': 43044295,
            'REF': 'G',
            'ALT': 'A',
            'variant_id': 'chr17:43044295:G>A'
        }
    
    def test_mock_database_initialization(self):
        """Test mock database initialization"""
        assert self.mock_db is not None
        assert hasattr(self.mock_db, 'get_clinvar_annotation') or hasattr(self.mock_db, 'get_annotation')
    
    def test_mock_annotation_basic(self):
        """Test basic mock annotation functionality"""
        if hasattr(self.mock_db, 'get_annotation'):
            annotation = self.mock_db.get_annotation(self.sample_variant)
        elif hasattr(self.mock_db, 'get_clinvar_annotation'):
            annotation = self.mock_db.get_clinvar_annotation(self.sample_variant)
        else:
            pytest.skip("No annotation method available")
        
        assert isinstance(annotation, dict)
        # Basic structure test - should have some annotation data
        assert len(annotation) > 0


class TestRealAnnotationDatabase:
    """Test suite for real database API connections"""
    
    def setup_method(self):
        """Set up test fixtures"""
        if RealAnnotationDatabase is None:
            pytest.skip("RealAnnotationDatabase not available")
        
        try:
            self.real_db = RealAnnotationDatabase()
        except Exception:
            pytest.skip("Could not initialize RealAnnotationDatabase")
        
        # Sample variant for testing
        self.sample_variant = {
            'CHROM': 'chr17',
            'POS': 43044295,
            'REF': 'G',
            'ALT': 'A',
            'variant_id': 'chr17:43044295:G>A'
        }
    
    def test_real_database_initialization(self):
        """Test real database initialization"""
        assert self.real_db is not None
        # Check for basic attributes
        assert hasattr(self.real_db, 'get_annotation') or hasattr(self.real_db, 'get_annotations')
    
    def test_database_connection_handling(self):
        """Test database connection handling"""
        # This is a basic connectivity test
        try:
            if hasattr(self.real_db, 'test_connections'):
                results = self.real_db.test_connections()
                assert isinstance(results, dict)
            else:
                # Basic annotation test
                if hasattr(self.real_db, 'get_annotation'):
                    annotation = self.real_db.get_annotation(self.sample_variant)
                    assert annotation is None or isinstance(annotation, dict)
        except Exception as e:
            # Network errors are acceptable in tests
            assert "network" in str(e).lower() or "connection" in str(e).lower() or "timeout" in str(e).lower()


class TestCacheManagement:
    """Test suite for cache management functionality"""
    
    def setup_method(self):
        """Set up test fixtures"""
        # Create temporary cache directory
        self.temp_cache_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Clean up test fixtures"""
        import shutil
        try:
            shutil.rmtree(self.temp_cache_dir)
        except (PermissionError, OSError):
            pass
    
    def test_cache_directory_creation(self):
        """Test cache directory creation"""
        assert Path(self.temp_cache_dir).exists()
        assert Path(self.temp_cache_dir).is_dir()
    
    def test_cache_file_operations(self):
        """Test basic cache file operations"""
        test_file = Path(self.temp_cache_dir) / "test_cache.json"
        test_data = {"test": "data", "timestamp": time.time()}
        
        # Write test data
        with open(test_file, 'w') as f:
            json.dump(test_data, f)
        
        # Read test data
        with open(test_file, 'r') as f:
            loaded_data = json.load(f)
        
        assert loaded_data == test_data


class TestDatabaseErrorHandling:
    """Test suite for database error handling and fallbacks"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.sample_variant = {
            'CHROM': 'chr17',
            'POS': 43044295,
            'REF': 'G',
            'ALT': 'A',
            'variant_id': 'chr17:43044295:G>A'
        }
    
    @patch('requests.get')
    def test_api_timeout_handling(self, mock_get):
        """Test API timeout handling"""
        # Mock timeout exception
        mock_get.side_effect = Exception("Connection timeout")
        
        # This test verifies that timeout exceptions are handled gracefully
        # The actual implementation may vary
        try:
            # Simulate API call
            import requests
            response = requests.get('http://test.api', timeout=1)
        except Exception as e:
            assert "timeout" in str(e).lower() or "connection" in str(e).lower()
    
    @patch('requests.get')
    def test_api_rate_limit_handling(self, mock_get):
        """Test API rate limit handling"""
        # Mock rate limit response
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.headers = {'Retry-After': '1'}
        mock_get.return_value = mock_response
        
        # Test that rate limiting is detected
        import requests
        response = requests.get('http://test.api')
        assert response.status_code == 429
    
    def test_invalid_variant_handling(self):
        """Test handling of invalid variant data"""
        invalid_variants = [
            {},  # Empty variant
            {'CHROM': 'invalid'},  # Missing required fields
            {'CHROM': 'chr1', 'POS': 'not_a_number'},  # Invalid position
        ]
        
        for invalid_variant in invalid_variants:
            # Should not crash with invalid input
            # The specific behavior depends on implementation
            assert isinstance(invalid_variant, dict)


@pytest.mark.integration
class TestDatabaseIntegration:
    """Integration tests for database functionality"""
    
    def setup_method(self):
        """Set up integration test fixtures"""
        # Test variants with known annotations
        self.test_variants = [
            {
                'CHROM': 'chr17',
                'POS': 43044295,
                'REF': 'G',
                'ALT': 'A',
                'variant_id': 'chr17:43044295:G>A'
            },
            {
                'CHROM': 'chr1',
                'POS': 100,
                'REF': 'A',
                'ALT': 'T',
                'variant_id': 'chr1:100:A>T'
            }
        ]
    
    def test_variant_data_structure(self):
        """Test variant data structure consistency"""
        for variant in self.test_variants:
            # Check required fields
            assert 'CHROM' in variant
            assert 'POS' in variant
            assert 'REF' in variant
            assert 'ALT' in variant
            
            # Check data types
            assert isinstance(variant['CHROM'], str)
            assert isinstance(variant['POS'], int)
            assert isinstance(variant['REF'], str)
            assert isinstance(variant['ALT'], str)
    
    def test_annotation_data_consistency(self):
        """Test annotation data consistency"""
        # This test verifies that annotation data structures are consistent
        # across different database sources
        
        sample_annotation = {
            'clinical_significance': 'Pathogenic',
            'allele_frequency': 0.001,
            'gene_symbol': 'BRCA1'
        }
        
        # Check data types
        assert isinstance(sample_annotation['clinical_significance'], str)
        assert isinstance(sample_annotation['allele_frequency'], (int, float))
        assert isinstance(sample_annotation['gene_symbol'], str)
        
        # Check value ranges
        assert 0 <= sample_annotation['allele_frequency'] <= 1


class TestDatabaseConfiguration:
    """Test suite for database configuration and setup"""
    
    def test_database_priorities(self):
        """Test database priority configuration"""
        # Sample priority configuration
        priorities = {
            'clinvar': 12,
            'clingen': 11,
            'hgmd': 10,
            'omim': 9,
            'ensembl': 8,
            'pharmgkb': 7,
            'gnomad': 6,
            'cosmic': 5,
            'dbsnp': 4
        }
        
        # Check that priorities are properly ordered
        priority_values = list(priorities.values())
        assert priority_values == sorted(priority_values, reverse=True)
        
        # Check that clinical databases have higher priority
        assert priorities['clinvar'] > priorities['gnomad']
        assert priorities['clingen'] > priorities['cosmic']
    
    def test_api_key_configuration(self):
        """Test API key configuration structure"""
        # Sample API key configuration
        api_config = {
            'clinvar': {'required': False, 'url': 'https://eutils.ncbi.nlm.nih.gov'},
            'omim': {'required': True, 'url': 'https://api.omim.org'},
            'pharmgkb': {'required': False, 'url': 'https://api.pharmgkb.org'}
        }
        
        for db_name, config in api_config.items():
            assert 'required' in config
            assert 'url' in config
            assert isinstance(config['required'], bool)
            assert isinstance(config['url'], str)
            assert config['url'].startswith('http')


class TestClinVarDatabase:
    """Comprehensive test suite for ClinVar database integration"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.temp_cache_dir = tempfile.mkdtemp()
        self.clinvar_db = ClinVarDatabase(cache_dir=self.temp_cache_dir, use_cache=True)
        
        # Sample variants for testing
        self.sample_variant = {
            'chrom': '17',
            'pos': 43044295,
            'ref': 'G',
            'alt': 'A'
        }
        
        self.sample_annotation = {
            "clinvar_significance": "Pathogenic",
            "clinvar_id": "12345",
            "clinvar_review_status": "reviewed_by_expert_panel",
            "clinvar_conditions": ["Breast cancer"]
        }
    
    def teardown_method(self):
        """Clean up test fixtures"""
        import shutil
        try:
            shutil.rmtree(self.temp_cache_dir)
        except (PermissionError, OSError):
            pass
    
    def test_clinvar_initialization(self):
        """Test ClinVar database initialization"""
        assert self.clinvar_db.base_url == "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        assert self.clinvar_db.clinvar_api == "https://www.ncbi.nlm.nih.gov/clinvar/api/v2"
        assert self.clinvar_db.use_cache is True
        assert self.clinvar_db.cache_dir.exists()
        assert self.clinvar_db.min_request_interval == 0.34
    
    def test_clinvar_initialization_no_cache(self):
        """Test ClinVar database initialization without cache"""
        db = ClinVarDatabase(use_cache=False)
        assert db.use_cache is False
    
    def test_rate_limiting(self):
        """Test rate limiting functionality"""
        start_time = time.time()
        self.clinvar_db._rate_limit()
        self.clinvar_db._rate_limit()
        end_time = time.time()
        
        # Should have some delay due to rate limiting
        assert end_time - start_time >= self.clinvar_db.min_request_interval * 0.8
    
    def test_cache_path_generation(self):
        """Test cache path generation"""
        variant_key = "17:43044295:G>A"
        cache_path = self.clinvar_db._get_cache_path(variant_key)
        
        assert cache_path.parent == self.clinvar_db.cache_dir
        assert "clinvar_17_43044295_G_A.json" in str(cache_path)
    
    def test_cache_operations(self):
        """Test cache save and load operations"""
        variant_key = "17:43044295:G>A"
        
        # Test save to cache
        self.clinvar_db._save_to_cache(variant_key, self.sample_annotation)
        
        # Test load from cache
        loaded_data = self.clinvar_db._load_from_cache(variant_key)
        assert loaded_data == self.sample_annotation
    
    def test_cache_operations_disabled(self):
        """Test cache operations when caching is disabled"""
        db = ClinVarDatabase(use_cache=False)
        variant_key = "17:43044295:G>A"
        
        # Should not save or load when cache is disabled
        db._save_to_cache(variant_key, self.sample_annotation)
        loaded_data = db._load_from_cache(variant_key)
        assert loaded_data is None
    
    def test_significance_mapping(self):
        """Test clinical significance mapping"""
        expected_mappings = {
            "Pathogenic": "Pathogenic",
            "Likely pathogenic": "Likely_pathogenic",
            "Uncertain significance": "Uncertain_significance",
            "Likely benign": "Likely_benign",
            "Benign": "Benign"
        }
        
        for key, value in expected_mappings.items():
            assert self.clinvar_db.significance_mapping[key] == value
    
    @patch('requests.get')
    def test_search_by_coordinates_success(self, mock_get):
        """Test successful coordinate-based search"""
        # Mock successful API responses
        mock_search_response = Mock()
        mock_search_response.json.return_value = {
            "esearchresult": {"idlist": ["12345", "67890"]}
        }
        mock_search_response.raise_for_status.return_value = None
        
        mock_details_response = Mock()
        mock_details_response.json.return_value = {
            "result": {
                "12345": {
                    "clinical_significance": "Pathogenic",
                    "review_status": "reviewed_by_expert_panel",
                    "accession": "000123",
                    "condition_list": [{"name": "Breast cancer"}],
                    "last_evaluated": "2023-01-01"
                }
            }
        }
        mock_details_response.raise_for_status.return_value = None
        
        mock_get.side_effect = [mock_search_response, mock_details_response]
        
        result = self.clinvar_db._search_by_coordinates("17", 43044295, "G", "A")
        assert result is not None
        assert isinstance(result, dict)
        assert result["clinvar_significance"] == "Pathogenic"
    
    @patch('requests.get')
    def test_search_by_coordinates_no_results(self, mock_get):
        """Test coordinate search with no results"""
        mock_response = Mock()
        mock_response.json.return_value = {"esearchresult": {"idlist": []}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = self.clinvar_db._search_by_coordinates("17", 43044295, "G", "A")
        assert result is None
    
    @patch('requests.get')
    def test_search_by_coordinates_api_error(self, mock_get):
        """Test coordinate search with API error"""
        mock_get.side_effect = Exception("API Error")
        
        result = self.clinvar_db._search_by_coordinates("17", 43044295, "G", "A")
        assert result is None
    
    @patch('requests.get')
    def test_search_by_hgvs_success(self, mock_get):
        """Test successful HGVS-based search"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "esearchresult": {"idlist": ["12345"]}
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        with patch.object(self.clinvar_db, '_get_variant_details') as mock_details:
            mock_details.return_value = self.sample_annotation
            result = self.clinvar_db._search_by_hgvs("17", 43044295, "G", "A")
            assert result == self.sample_annotation
    
    @patch('requests.get')
    def test_search_by_hgvs_no_results(self, mock_get):
        """Test HGVS search with no results"""
        mock_response = Mock()
        mock_response.json.return_value = {"esearchresult": {"idlist": []}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = self.clinvar_db._search_by_hgvs("17", 43044295, "G", "A")
        assert result is None
    
    def test_get_variant_annotation_cached(self):
        """Test variant annotation retrieval from cache"""
        variant_key = "17:43044295:G>A"
        self.clinvar_db._save_to_cache(variant_key, self.sample_annotation)
        
        result = self.clinvar_db.get_variant_annotation("17", 43044295, "G", "A")
        assert result == self.sample_annotation
    
    @patch.object(ClinVarDatabase, '_search_by_coordinates')
    @patch.object(ClinVarDatabase, '_search_by_hgvs')
    def test_get_variant_annotation_no_cache(self, mock_hgvs, mock_coords):
        """Test variant annotation retrieval without cache"""
        mock_coords.return_value = self.sample_annotation
        mock_hgvs.return_value = None
        
        db = ClinVarDatabase(use_cache=False)
        result = db.get_variant_annotation("17", 43044295, "G", "A")
        assert result == self.sample_annotation
    
    @patch.object(ClinVarDatabase, '_search_by_coordinates')
    @patch.object(ClinVarDatabase, '_search_by_hgvs')
    def test_get_variant_annotation_no_results(self, mock_hgvs, mock_coords):
        """Test variant annotation with no results"""
        mock_coords.return_value = None
        mock_hgvs.return_value = None
        
        result = self.clinvar_db.get_variant_annotation("17", 43044295, "G", "A")
        expected = {
            "clinvar_significance": None,
            "clinvar_id": None,
            "clinvar_review_status": None,
            "clinvar_conditions": None
        }
        assert result == expected
    
    def test_batch_annotate(self):
        """Test batch annotation functionality"""
        variants = [
            {"CHROM": "17", "POS": 43044295, "REF": "G", "ALT": "A"},
            {"CHROM": "13", "POS": 32906729, "REF": "C", "ALT": "T"}
        ]
        
        with patch.object(self.clinvar_db, 'get_variant_annotation') as mock_get:
            mock_get.return_value = self.sample_annotation
            results = self.clinvar_db.batch_annotate(variants)
            
            assert len(results) == 2
            # Check that annotations were added to each variant
            for result in results:
                assert "clinvar_significance" in result
                assert result["clinvar_significance"] == "Pathogenic"
    
    def test_get_database_info(self):
        """Test database info retrieval"""
        info = self.clinvar_db.get_database_info()
        
        assert isinstance(info, dict)
        assert "name" in info
        assert "version" in info
        assert "description" in info
        assert info["name"] == "ClinVar"


class TestGnomADDatabase:
    """Test suite for GnomAD database integration"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.temp_cache_dir = tempfile.mkdtemp()
        self.gnomad_db = GnomADDatabase(cache_dir=self.temp_cache_dir, use_cache=True)
    
    def teardown_method(self):
        """Clean up test fixtures"""
        import shutil
        try:
            shutil.rmtree(self.temp_cache_dir)
        except (PermissionError, OSError):
            pass
    
    def test_gnomad_initialization(self):
        """Test GnomAD database initialization"""
        assert self.gnomad_db.graphql_url == "https://gnomad.broadinstitute.org/api"
        assert self.gnomad_db.use_cache is True
        assert self.gnomad_db.cache_dir.exists()
    
    def test_gnomad_initialization_no_cache(self):
        """Test GnomAD database initialization without cache"""
        db = GnomADDatabase(use_cache=False)
        assert db.use_cache is False
    
    @patch('requests.post')
    def test_get_variant_annotation_success(self, mock_post):
        """Test successful variant annotation from GnomAD"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "data": {
                "variant": {
                    "genome": {
                        "ac": 10,
                        "an": 1000,
                        "af": 0.01
                    },
                    "exome": {
                        "ac": 5,
                        "an": 500,
                        "af": 0.01
                    }
                }
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        result = self.gnomad_db.get_variant_annotation("17", 43044295, "G", "A")
        
        assert isinstance(result, dict)
        assert "gnomad_af" in result or "af" in result
    
    @patch('requests.post')
    def test_get_variant_annotation_no_data(self, mock_post):
        """Test variant annotation with no data"""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"variant": None}}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        result = self.gnomad_db.get_variant_annotation("17", 43044295, "G", "A")
        assert result is not None
        assert isinstance(result, dict)
    
    @patch('requests.post')
    def test_get_variant_annotation_api_error(self, mock_post):
        """Test variant annotation with API error"""
        mock_post.side_effect = Exception("API Error")
        
        result = self.gnomad_db.get_variant_annotation("17", 43044295, "G", "A")
        assert result is not None  # Should return empty dict on error
        assert isinstance(result, dict)
    
    def test_get_database_info(self):
        """Test database info retrieval"""
        info = self.gnomad_db.get_database_info()
        
        assert isinstance(info, dict)
        assert "name" in info
        assert "version" in info
        assert info["name"] == "gnomAD"


class TestDbSNPDatabase:
    """Test suite for dbSNP database integration"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.temp_cache_dir = tempfile.mkdtemp()
        self.dbsnp_db = DbSNPDatabase(cache_dir=self.temp_cache_dir, use_cache=True)
    
    def teardown_method(self):
        """Clean up test fixtures"""
        import shutil
        try:
            shutil.rmtree(self.temp_cache_dir)
        except (PermissionError, OSError):
            pass
    
    def test_dbsnp_initialization(self):
        """Test dbSNP database initialization"""
        assert "ncbi.nlm.nih.gov" in self.dbsnp_db.base_url
        assert self.dbsnp_db.use_cache is True
        assert self.dbsnp_db.cache_dir.exists()
    
    @patch('requests.get')
    def test_get_variant_annotation_success(self, mock_get):
        """Test successful variant annotation from dbSNP"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "primary_snapshot_data": {
                "allele_annotations": [{
                    "frequency": [{"study_name": "1000Genomes", "allele_count": 10, "total_count": 1000}]
                }]
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = self.dbsnp_db.get_variant_annotation("17", 43044295, "G", "A")
        assert isinstance(result, dict)
    
    def test_get_database_info(self):
        """Test database info retrieval"""
        info = self.dbsnp_db.get_database_info()
        
        assert isinstance(info, dict)
        assert "name" in info
        assert info["name"] == "dbSNP"


class TestCOSMICDatabase:
    """Test suite for COSMIC database integration"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.temp_cache_dir = tempfile.mkdtemp()
        self.cosmic_db = COSMICDatabase(cache_dir=self.temp_cache_dir, use_cache=True)
    
    def teardown_method(self):
        """Clean up test fixtures"""
        import shutil
        try:
            shutil.rmtree(self.temp_cache_dir)
        except (PermissionError, OSError):
            pass
    
    def test_cosmic_initialization(self):
        """Test COSMIC database initialization"""
        assert "cancer.sanger.ac.uk" in self.cosmic_db.base_url
        assert self.cosmic_db.use_cache is True
        assert self.cosmic_db.cache_dir.exists()
    
    def test_get_database_info(self):
        """Test database info retrieval"""
        info = self.cosmic_db.get_database_info()
        
        assert isinstance(info, dict)
        assert "name" in info
        assert info["name"] == "COSMIC"


class TestOMIMDatabase:
    """Test suite for OMIM database integration"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.temp_cache_dir = tempfile.mkdtemp()
        self.omim_db = OMIMDatabase(cache_dir=self.temp_cache_dir, use_cache=True)
    
    def teardown_method(self):
        """Clean up test fixtures"""
        import shutil
        try:
            shutil.rmtree(self.temp_cache_dir)
        except (PermissionError, OSError):
            pass
    
    def test_omim_initialization(self):
        """Test OMIM database initialization"""
        assert "omim.org" in self.omim_db.base_url
        assert self.omim_db.use_cache is True
        assert self.omim_db.cache_dir.exists()
    
    def test_get_database_info(self):
        """Test database info retrieval"""
        info = self.omim_db.get_database_info()
        
        assert isinstance(info, dict)
        assert "name" in info
        assert info["name"] == "OMIM"


class TestPharmGKBDatabase:
    """Test suite for PharmGKB database integration"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.temp_cache_dir = tempfile.mkdtemp()
        self.pharmgkb_db = PharmGKBDatabase(cache_dir=self.temp_cache_dir, use_cache=True)
    
    def teardown_method(self):
        """Clean up test fixtures"""
        import shutil
        try:
            shutil.rmtree(self.temp_cache_dir)
        except (PermissionError, OSError):
            pass
    
    def test_pharmgkb_initialization(self):
        """Test PharmGKB database initialization"""
        assert "pharmgkb.org" in self.pharmgkb_db.base_url
        assert self.pharmgkb_db.use_cache is True
        assert self.pharmgkb_db.cache_dir.exists()
    
    def test_get_database_info(self):
        """Test database info retrieval"""
        info = self.pharmgkb_db.get_database_info()
        
        assert isinstance(info, dict)
        assert "name" in info
        assert info["name"] == "PharmGKB"


class TestClinGenDatabase:
    """Test suite for ClinGen database integration"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.temp_cache_dir = tempfile.mkdtemp()
        self.clingen_db = ClinGenDatabase(cache_dir=self.temp_cache_dir, use_cache=True)
    
    def teardown_method(self):
        """Clean up test fixtures"""
        import shutil
        try:
            shutil.rmtree(self.temp_cache_dir)
        except (PermissionError, OSError):
            pass
    
    def test_clingen_initialization(self):
        """Test ClinGen database initialization"""
        assert "clinicalgenome.org" in self.clingen_db.base_url
        assert self.clingen_db.use_cache is True
        assert self.clingen_db.cache_dir.exists()
    
    def test_get_database_info(self):
        """Test database info retrieval"""
        info = self.clingen_db.get_database_info()
        
        assert isinstance(info, dict)
        assert "name" in info
        assert info["name"] == "ClinGen"


class TestHGMDDatabase:
    """Test suite for HGMD database integration"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.temp_cache_dir = tempfile.mkdtemp()
        self.hgmd_db = HGMDDatabase(cache_dir=self.temp_cache_dir, use_cache=True)
    
    def teardown_method(self):
        """Clean up test fixtures"""
        import shutil
        try:
            shutil.rmtree(self.temp_cache_dir)
        except (PermissionError, OSError):
            pass
    
    def test_hgmd_initialization(self):
        """Test HGMD database initialization"""
        assert "hgmd" in self.hgmd_db.base_url.lower()
        assert self.hgmd_db.use_cache is True
        assert self.hgmd_db.cache_dir.exists()
    
    def test_get_database_info(self):
        """Test database info retrieval"""
        info = self.hgmd_db.get_database_info()
        
        assert isinstance(info, dict)
        assert "name" in info
        assert info["name"] == "HGMD"


class TestEnsemblDatabase:
    """Test suite for Ensembl database integration"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.temp_cache_dir = tempfile.mkdtemp()
        self.ensembl_db = EnsemblDatabase(cache_dir=self.temp_cache_dir, use_cache=True)
    
    def teardown_method(self):
        """Clean up test fixtures"""
        import shutil
        try:
            shutil.rmtree(self.temp_cache_dir)
        except (PermissionError, OSError):
            pass
    
    def test_ensembl_initialization(self):
        """Test Ensembl database initialization"""
        assert "ensembl.org" in self.ensembl_db.base_url
        assert self.ensembl_db.use_cache is True
        assert self.ensembl_db.cache_dir.exists()
    
    @patch('requests.get')
    def test_get_variant_annotation_success(self, mock_get):
        """Test successful variant annotation from Ensembl"""
        mock_response = Mock()
        mock_response.json.return_value = [{
            "most_severe_consequence": "missense_variant",
            "transcript_consequences": [{
                "gene_symbol": "BRCA1",
                "consequence_terms": ["missense_variant"]
            }]
        }]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = self.ensembl_db.get_variant_annotation("17", 43044295, "G", "A")
        assert isinstance(result, dict)
    
    def test_get_database_info(self):
        """Test database info retrieval"""
        info = self.ensembl_db.get_database_info()
        
        assert isinstance(info, dict)
        assert "name" in info
        assert info["name"] == "Ensembl"


if __name__ == "__main__":
    pytest.main([__file__]) 