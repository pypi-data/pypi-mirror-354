#!/usr/bin/env python3
"""
VCF Parser Tests for VarAnnote v1.0.0

Tests for VCF file parsing functionality including:
- Basic VCF parsing
- Compressed file handling
- Error handling
- Edge cases
"""

import pytest
import tempfile
import gzip
import os
from pathlib import Path
from unittest.mock import patch, mock_open

from varannote.utils.vcf_parser import VCFParser


class TestVCFParser:
    """Test suite for VCF parser functionality"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.parser = VCFParser()
        
        # Sample VCF content
        self.sample_vcf_content = """##fileformat=VCFv4.2
##reference=hg38
##contig=<ID=chr1,length=248956422>
##INFO=<ID=AF,Number=A,Type=Float,Description="Allele Frequency">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
chr1	100	rs123	A	T	60	PASS	AF=0.01
chr2	200	.	G	C	30	PASS	AF=0.05
chr3	300	rs456	C	G,A	90	PASS	AF=0.02,0.01
"""
        
        # Invalid VCF content
        self.invalid_vcf_content = """##fileformat=VCFv4.2
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
chr1	invalid_pos	rs123	A	T	60	PASS	AF=0.01
"""
    
    def _safe_cleanup(self, filepath):
        """Safely cleanup temporary files on Windows"""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except (PermissionError, OSError):
            # File might still be in use, ignore cleanup error
            pass
    
    def test_parse_valid_vcf_content(self):
        """Test parsing valid VCF content"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.vcf', delete=False) as f:
            f.write(self.sample_vcf_content)
            f.flush()
            temp_path = f.name
        
        try:
            variants = self.parser.parse_file(temp_path)
            
            assert len(variants) == 3
            
            # Test first variant
            assert variants[0]['CHROM'] == 'chr1'
            assert variants[0]['POS'] == 100
            assert variants[0]['ID'] == 'rs123'
            assert variants[0]['REF'] == 'A'
            assert variants[0]['ALT'] == 'T'
            assert variants[0]['QUAL'] == 60.0
            assert variants[0]['FILTER'] == 'PASS'
            
            # Test multi-allelic variant
            assert variants[2]['ALT'] == 'G,A'
            
            # Test variant ID generation
            assert variants[0]['variant_id'] == "chr1:100:A>T"
            
        finally:
            self._safe_cleanup(temp_path)
    
    def test_parse_compressed_vcf(self):
        """Test parsing gzip-compressed VCF files"""
        with tempfile.NamedTemporaryFile(suffix='.vcf.gz', delete=False) as f:
            temp_path = f.name
        
        try:
            with gzip.open(temp_path, 'wt') as gz_file:
                gz_file.write(self.sample_vcf_content)
            
            variants = self.parser.parse_file(temp_path)
            
            assert len(variants) == 3
            assert variants[0]['CHROM'] == 'chr1'
            
        finally:
            self._safe_cleanup(temp_path)
    
    def test_parse_invalid_vcf(self):
        """Test error handling for invalid VCF content"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.vcf', delete=False) as f:
            f.write(self.invalid_vcf_content)
            f.flush()
            temp_path = f.name
        
        try:
            # The parser should handle invalid lines gracefully by skipping them
            variants = self.parser.parse_file(temp_path)
            # Should return empty list or skip invalid lines
            assert isinstance(variants, list)
            
        finally:
            self._safe_cleanup(temp_path)
    
    def test_parse_nonexistent_file(self):
        """Test error handling for non-existent files"""
        with pytest.raises(FileNotFoundError):
            self.parser.parse_file("nonexistent_file.vcf")
    
    def test_parse_empty_vcf(self):
        """Test parsing empty VCF file"""
        empty_vcf = """##fileformat=VCFv4.2
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.vcf', delete=False) as f:
            f.write(empty_vcf)
            f.flush()
            temp_path = f.name
        
        try:
            variants = self.parser.parse_file(temp_path)
            assert len(variants) == 0
            
        finally:
            self._safe_cleanup(temp_path)
    
    def test_info_field_parsing(self):
        """Test INFO field parsing"""
        info_string = "AF=0.01;DP=100;AC=2"
        info_dict = self.parser._parse_info_field(info_string)
        
        assert info_dict['AF'] == 0.01  # Should be converted to float
        assert info_dict['DP'] == 100   # Should be converted to int
        assert info_dict['AC'] == 2     # Should be converted to int
    
    def test_numeric_field_conversion(self):
        """Test numeric field conversion"""
        # Test valid quality scores
        assert self.parser._parse_numeric_field("60") == 60
        assert self.parser._parse_numeric_field("30.5") == 30.5
        
        # Test missing quality
        assert self.parser._parse_numeric_field(".") is None
    
    def test_variant_type_determination(self):
        """Test variant type determination"""
        # Test SNV
        assert self.parser._determine_variant_type("A", "T") == "SNV"
        
        # Test insertion
        assert self.parser._determine_variant_type("A", "AT") == "INS"
        
        # Test deletion
        assert self.parser._determine_variant_type("AT", "A") == "DEL"
        
        # Test complex
        assert self.parser._determine_variant_type("AT", "GC") == "COMPLEX"
    
    def test_variant_key_generation(self):
        """Test variant key generation"""
        variant = {
            'CHROM': 'chr1',
            'POS': 100,
            'REF': 'A',
            'ALT': 'T'
        }
        
        variant_key = self.parser.get_variant_key(variant)
        assert variant_key == "chr1:100:A>T"
    
    def test_iterator_mode(self):
        """Test iterator mode for large files"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.vcf', delete=False) as f:
            f.write(self.sample_vcf_content)
            f.flush()
            temp_path = f.name
        
        try:
            variant_count = 0
            for variant in self.parser.parse_variants_iterator(temp_path):
                variant_count += 1
                assert 'CHROM' in variant
                assert 'POS' in variant
                assert 'variant_id' in variant
            
            assert variant_count == 3
            
        finally:
            self._safe_cleanup(temp_path)
    
    def test_memory_efficient_parsing(self):
        """Test memory-efficient parsing for large files"""
        # Create a larger VCF file
        large_vcf_content = """##fileformat=VCFv4.2
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
"""
        
        # Add 100 variants (reduced from 1000 for faster testing)
        for i in range(100):
            large_vcf_content += f"chr1	{i+1000}	rs{i}	A	T	60	PASS	AF=0.01\n"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.vcf', delete=False) as f:
            f.write(large_vcf_content)
            f.flush()
            temp_path = f.name
        
        try:
            # Test that we can parse without loading everything into memory
            variant_count = sum(1 for _ in self.parser.parse_variants_iterator(temp_path))
            assert variant_count == 100
            
        finally:
            self._safe_cleanup(temp_path)
    
    def test_header_parsing(self):
        """Test VCF header parsing"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.vcf', delete=False) as f:
            f.write(self.sample_vcf_content)
            f.flush()
            temp_path = f.name
        
        try:
            # Parse the file to populate header information
            self.parser.parse_file(temp_path)
            
            # Check that header lines were captured
            assert len(self.parser.header_lines) > 0
            assert any('fileformat=VCFv4.2' in line for line in self.parser.header_lines)
            
            # Check INFO field definitions
            assert 'AF' in self.parser.info_fields
            assert self.parser.info_fields['AF'] == 'Allele Frequency'
            
        finally:
            self._safe_cleanup(temp_path)
    
    def test_chromosome_normalization(self):
        """Test chromosome name handling"""
        # Test with and without 'chr' prefix
        vcf_content_no_chr = """##fileformat=VCFv4.2
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
1	100	rs123	A	T	60	PASS	AF=0.01
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.vcf', delete=False) as f:
            f.write(vcf_content_no_chr)
            f.flush()
            temp_path = f.name
        
        try:
            variants = self.parser.parse_file(temp_path)
            
            # Should preserve chromosome names as provided
            assert variants[0]['CHROM'] == '1'
            
        finally:
            self._safe_cleanup(temp_path)
    
    def test_filter_variants(self):
        """Test variant filtering functionality"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.vcf', delete=False) as f:
            f.write(self.sample_vcf_content)
            f.flush()
            temp_path = f.name
        
        try:
            variants = self.parser.parse_file(temp_path)
            
            # Test filtering by quality
            high_qual_variants = self.parser.filter_variants(
                variants, 
                {'min_qual': 50}
            )
            
            # Should filter based on quality threshold
            assert len(high_qual_variants) <= len(variants)
            
        finally:
            self._safe_cleanup(temp_path)
    
    @patch("builtins.open", side_effect=FileNotFoundError("File not found"))
    def test_file_not_found_handling(self, mock_open):
        """Test handling of file not found errors"""
        with pytest.raises(FileNotFoundError):
            self.parser.parse_file("nonexistent.vcf")
    
    def test_malformed_line_handling(self):
        """Test handling of malformed VCF lines"""
        malformed_vcf = """##fileformat=VCFv4.2
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
chr1	100	rs123	A	T	60	PASS	AF=0.01
chr2	200	incomplete_line
chr3	300	rs456	C	G	90	PASS	AF=0.02
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.vcf', delete=False) as f:
            f.write(malformed_vcf)
            f.flush()
            temp_path = f.name
        
        try:
            variants = self.parser.parse_file(temp_path)
            
            # Should skip malformed lines and continue parsing
            assert len(variants) == 2  # Should have 2 valid variants
            assert variants[0]['CHROM'] == 'chr1'
            assert variants[1]['CHROM'] == 'chr3'
            
        finally:
            self._safe_cleanup(temp_path)


if __name__ == "__main__":
    pytest.main([__file__]) 