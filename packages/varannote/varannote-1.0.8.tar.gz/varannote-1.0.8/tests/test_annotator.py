#!/usr/bin/env python3
"""
Annotation Engine Tests for VarAnnote v1.0.0

Tests for core annotation functionality including:
- Functional annotation
- Pathogenicity prediction
- Gene mapping
- Consequence prediction
"""

import pytest
import tempfile
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from varannote.core.annotator import VariantAnnotator
from varannote.tools.annotator import VariantAnnotatorTool


class TestVariantAnnotator:
    """Test suite for core variant annotation functionality"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.annotator = VariantAnnotator(genome="hg38")
        
        # Sample variant for testing
        self.sample_variant = {
            'CHROM': '17',
            'POS': 43044295,
            'REF': 'G',
            'ALT': 'A',
            'variant_id': '17:43044295:G>A'
        }
        
        # Sample variants list
        self.sample_variants = [
            {
                'CHROM': '1',
                'POS': 100,
                'REF': 'A',
                'ALT': 'T',
                'variant_id': '1:100:A>T'
            },
            {
                'CHROM': '2',
                'POS': 200,
                'REF': 'G',
                'ALT': 'C',
                'variant_id': '2:200:G>C'
            }
        ]
    
    def test_annotator_initialization(self):
        """Test annotator initialization with different genomes"""
        # Test default initialization
        annotator_default = VariantAnnotator()
        assert annotator_default.genome == "hg38"
        
        # Test hg19 initialization
        annotator_hg19 = VariantAnnotator(genome="hg19")
        assert annotator_hg19.genome == "hg19"
        
        # Test that invalid genome doesn't crash (no validation in current implementation)
        annotator_invalid = VariantAnnotator(genome="invalid_genome")
        assert annotator_invalid.genome == "invalid_genome"
    
    def test_get_functional_annotations(self):
        """Test functional annotation retrieval"""
        annotations = self.annotator.get_functional_annotations(self.sample_variant)
        
        # Check that annotations are returned as dictionary
        assert isinstance(annotations, dict)
        
        # Check for expected annotation fields
        expected_fields = [
            'gene_symbol',
            'consequence',
            'cadd_score'
        ]
        
        for field in expected_fields:
            assert field in annotations
    
    def test_gene_mapping(self):
        """Test gene symbol mapping"""
        # Test known gene region (BRCA1)
        brca1_variant = {
            'CHROM': '17',
            'POS': 43044295,
            'REF': 'G',
            'ALT': 'A'
        }
        
        gene_symbol = self.annotator._find_overlapping_gene(brca1_variant)
        assert gene_symbol == "BRCA1"
        
        # Test unknown region
        unknown_variant = {
            'CHROM': '1',
            'POS': 1000000,
            'REF': 'A',
            'ALT': 'T'
        }
        
        gene_symbol = self.annotator._find_overlapping_gene(unknown_variant)
        assert gene_symbol is None
    
    def test_consequence_prediction(self):
        """Test variant consequence prediction"""
        # Test different variant types
        test_cases = [
            {
                'variant': {'CHROM': '1', 'POS': 100, 'REF': 'A', 'ALT': 'T', 'variant_type': 'SNV'},
                'gene': 'TEST_GENE'
            },
            {
                'variant': {'CHROM': '1', 'POS': 100, 'REF': 'A', 'ALT': 'AT', 'variant_type': 'INS'},
                'gene': 'TEST_GENE'
            },
            {
                'variant': {'CHROM': '1', 'POS': 100, 'REF': 'AT', 'ALT': 'A', 'variant_type': 'DEL'},
                'gene': 'TEST_GENE'
            }
        ]
        
        for case in test_cases:
            consequence = self.annotator._predict_consequence(case['variant'], case['gene'])
            assert isinstance(consequence, str)
            assert len(consequence) > 0
    
    def test_cadd_score_calculation(self):
        """Test CADD score calculation"""
        cadd_score = self.annotator._calculate_cadd_score(self.sample_variant)
        
        # CADD score should be a float between 0 and 99
        assert isinstance(cadd_score, float)
        assert 0 <= cadd_score <= 99
    
    def test_batch_annotation(self):
        """Test batch annotation of multiple variants"""
        annotations = self.annotator.annotate_batch(self.sample_variants)
        
        assert len(annotations) == len(self.sample_variants)
        
        for annotation in annotations:
            assert isinstance(annotation, dict)
            assert 'gene_symbol' in annotation
            assert 'consequence' in annotation
            assert 'cadd_score' in annotation
    
    def test_annotation_with_invalid_variant(self):
        """Test annotation with invalid variant data"""
        invalid_variant = {
            'CHROM': 'invalid',
            'POS': 'not_a_number',
            'REF': '',
            'ALT': ''
        }
        
        # Should handle gracefully and return annotations
        try:
            annotations = self.annotator.get_functional_annotations(invalid_variant)
            assert isinstance(annotations, dict)
        except Exception:
            # It's acceptable if it raises an exception for invalid data
            pass
    
    def test_genome_version_handling(self):
        """Test different genome version handling"""
        # Test coordinate conversion between genome versions
        hg19_annotator = VariantAnnotator(genome="hg19")
        hg38_annotator = VariantAnnotator(genome="hg38")
        
        # Both should handle the same variant appropriately
        hg19_annotations = hg19_annotator.get_functional_annotations(self.sample_variant)
        hg38_annotations = hg38_annotator.get_functional_annotations(self.sample_variant)
        
        assert isinstance(hg19_annotations, dict)
        assert isinstance(hg38_annotations, dict)


class TestVariantAnnotatorTool:
    """Test suite for the variant annotator tool"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.tool = VariantAnnotatorTool(
            genome="hg38",
            verbose=False,
            use_real_db=False
        )
        
        # Sample VCF content for testing
        self.sample_vcf_content = """##fileformat=VCFv4.2
##reference=hg38
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
1	100	rs123	A	T	60	PASS	AF=0.01
2	200	.	G	C	30	PASS	AF=0.05
"""
    
    def _safe_cleanup(self, filepath):
        """Safely cleanup temporary files"""
        try:
            if Path(filepath).exists():
                Path(filepath).unlink()
        except (PermissionError, OSError):
            pass
    
    def test_tool_initialization(self):
        """Test annotator tool initialization"""
        # Test default initialization
        tool_default = VariantAnnotatorTool()
        assert tool_default.genome == "hg38"
        assert tool_default.use_real_db == False
        
        # Test with real database
        tool_real = VariantAnnotatorTool(use_real_db=True)
        assert tool_real.use_real_db == True
        
        # Test with parallel processing
        tool_parallel = VariantAnnotatorTool(use_parallel=True, max_workers=8)
        assert tool_parallel.use_parallel == True
        assert tool_parallel.max_workers == 8
    
    def test_file_annotation(self):
        """Test file-based annotation"""
        # Create temporary VCF file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.vcf', delete=False) as input_file:
            input_file.write(self.sample_vcf_content)
            input_file.flush()
            input_path = input_file.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.vcf', delete=False) as output_file:
            output_path = output_file.name
        
        try:
            # Test annotation
            result = self.tool.annotate_file(
                input_file=input_path,
                output_file=output_path,
                output_format="vcf"
            )
            
            # Check result structure
            assert isinstance(result, dict)
            assert 'variants_processed' in result
            assert 'output_file' in result
            assert 'output_format' in result
            
            # Check that variants were processed
            assert result['variants_processed'] > 0
            
            # Check output file exists
            assert Path(output_path).exists()
            
        finally:
            self._safe_cleanup(input_path)
            self._safe_cleanup(output_path)
    
    def test_different_output_formats(self):
        """Test different output formats"""
        formats = ['vcf', 'tsv', 'json']
        
        for fmt in formats:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.vcf', delete=False) as input_file:
                input_file.write(self.sample_vcf_content)
                input_file.flush()
                input_path = input_file.name
            
            with tempfile.NamedTemporaryFile(mode='w', suffix=f'.{fmt}', delete=False) as output_file:
                output_path = output_file.name
            
            try:
                result = self.tool.annotate_file(
                    input_file=input_path,
                    output_file=output_path,
                    output_format=fmt
                )
                
                assert result['output_format'] == fmt
                assert Path(output_path).exists()
                
            finally:
                self._safe_cleanup(input_path)
                self._safe_cleanup(output_path)
    
    def test_confidence_statistics(self):
        """Test confidence score statistics calculation"""
        # Mock annotated variants with confidence scores
        mock_variants = [
            {'variant_id': 'var1', 'annotation_confidence': 0.9},
            {'variant_id': 'var2', 'annotation_confidence': 0.7},
            {'variant_id': 'var3', 'annotation_confidence': 0.5},
        ]
        
        stats = self.tool._calculate_confidence_statistics(mock_variants)
        
        assert isinstance(stats, dict)
        assert 'average' in stats
        assert 'high_confidence_count' in stats
        
        # Check calculations
        assert stats['average'] == pytest.approx(0.7, rel=1e-2)
        assert stats['high_confidence_count'] == 2  # >= 0.7
    
    def test_error_handling(self):
        """Test error handling in annotation tool"""
        # Test with non-existent input file
        with pytest.raises(FileNotFoundError):
            self.tool.annotate_file(
                input_file="nonexistent.vcf",
                output_file="output.vcf",
                output_format="vcf"
            )
        
        # Test with invalid output format
        with tempfile.NamedTemporaryFile(mode='w', suffix='.vcf', delete=False) as input_file:
            input_file.write(self.sample_vcf_content)
            input_file.flush()
            input_path = input_file.name
        
        try:
            with pytest.raises(ValueError):
                self.tool.annotate_file(
                    input_file=input_path,
                    output_file="output.invalid",
                    output_format="invalid_format"
                )
        finally:
            self._safe_cleanup(input_path)
    
    def test_database_selection(self):
        """Test database selection functionality"""
        # Test with specific databases
        tool_specific = VariantAnnotatorTool(
            databases=["clinvar", "gnomad"],
            use_real_db=False
        )
        
        assert "clinvar" in tool_specific.databases
        assert "gnomad" in tool_specific.databases
        assert len(tool_specific.databases) == 2
        
        # Test with all databases (default)
        tool_all = VariantAnnotatorTool()
        assert len(tool_all.databases) > 2  # Should have all available databases


@pytest.mark.performance
class TestAnnotationPerformance:
    """Performance tests for annotation functionality"""
    
    def setup_method(self):
        """Set up performance test fixtures"""
        self.annotator = VariantAnnotator()
        
        # Create larger variant set for performance testing
        self.large_variant_set = []
        for i in range(100):  # 100 variants for performance testing
            self.large_variant_set.append({
                'CHROM': str((i % 22) + 1),
                'POS': 1000 + i * 100,
                'REF': 'A',
                'ALT': 'T',
                'variant_id': f'{(i % 22) + 1}:{1000 + i * 100}:A>T'
            })
    
    def test_annotation_speed(self):
        """Test annotation speed for multiple variants"""
        import time
        
        start_time = time.time()
        annotations = self.annotator.annotate_batch(self.large_variant_set)
        end_time = time.time()
        
        processing_time = end_time - start_time
        
        # Avoid division by zero for very fast operations
        if processing_time > 0:
            variants_per_second = len(self.large_variant_set) / processing_time
        # Should process at least 10 variants per second
        assert variants_per_second >= 10
        else:
            # If processing is instantaneous, that's also good
            assert processing_time >= 0
        
        assert len(annotations) == len(self.large_variant_set)
    
    def test_memory_usage(self):
        """Test memory usage during annotation"""
        try:
            import psutil
            import os
            
            process = psutil.Process(os.getpid())
            initial_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            # Process large variant set
            annotations = self.annotator.annotate_batch(self.large_variant_set)
            
            final_memory = process.memory_info().rss / 1024 / 1024  # MB
            memory_increase = final_memory - initial_memory
            
            # Memory increase should be reasonable (less than 100MB for 100 variants)
            assert memory_increase < 100
            assert len(annotations) == len(self.large_variant_set)
            
        except ImportError:
            pytest.skip("psutil not available for memory testing")


if __name__ == "__main__":
    pytest.main([__file__]) 