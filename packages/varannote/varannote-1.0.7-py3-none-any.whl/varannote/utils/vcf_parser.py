#!/usr/bin/env python3
"""
VCF Parser - Utility for parsing VCF files
"""

import re
import gzip
from typing import Dict, List, Iterator, Optional, Union
from pathlib import Path

class VCFParser:
    """
    VCF file parser for genomic variants
    
    Supports both compressed (.vcf.gz) and uncompressed (.vcf) files.
    Provides methods to parse variants and extract relevant information.
    """
    
    def __init__(self):
        """Initialize VCF parser"""
        self.header_lines = []
        self.column_headers = []
        self.info_fields = {}
        self.format_fields = {}
    
    def parse_file(self, vcf_file: str) -> List[Dict]:
        """
        Parse a VCF file and return list of variant dictionaries
        
        Args:
            vcf_file: Path to VCF file (.vcf or .vcf.gz)
            
        Returns:
            List of variant dictionaries
        """
        variants = []
        
        # Determine if file is compressed
        is_compressed = str(vcf_file).endswith('.gz')
        
        # Open file with appropriate method
        open_func = gzip.open if is_compressed else open
        mode = 'rt' if is_compressed else 'r'
        
        with open_func(vcf_file, mode) as f:
            for line in f:
                line = line.strip()
                
                if not line:
                    continue
                
                if line.startswith('##'):
                    # Header line
                    self.header_lines.append(line)
                    self._parse_header_line(line)
                    
                elif line.startswith('#CHROM'):
                    # Column header line
                    self.column_headers = line.split('\t')
                    
                elif not line.startswith('#'):
                    # Variant line
                    variant = self._parse_variant_line(line)
                    if variant:
                        variants.append(variant)
        
        return variants
    
    def parse_variants_iterator(self, vcf_file: str) -> Iterator[Dict]:
        """
        Parse VCF file and yield variants one by one (memory efficient)
        
        Args:
            vcf_file: Path to VCF file
            
        Yields:
            Variant dictionaries
        """
        is_compressed = str(vcf_file).endswith('.gz')
        open_func = gzip.open if is_compressed else open
        mode = 'rt' if is_compressed else 'r'
        
        with open_func(vcf_file, mode) as f:
            for line in f:
                line = line.strip()
                
                if not line:
                    continue
                
                if line.startswith('##'):
                    self.header_lines.append(line)
                    self._parse_header_line(line)
                    
                elif line.startswith('#CHROM'):
                    self.column_headers = line.split('\t')
                    
                elif not line.startswith('#'):
                    variant = self._parse_variant_line(line)
                    if variant:
                        yield variant
    
    def _parse_header_line(self, line: str):
        """Parse VCF header lines to extract field definitions"""
        
        # Parse INFO field definitions
        if line.startswith('##INFO='):
            info_match = re.match(r'##INFO=<ID=([^,]+),.*Description="([^"]*)"', line)
            if info_match:
                field_id, description = info_match.groups()
                self.info_fields[field_id] = description
        
        # Parse FORMAT field definitions
        elif line.startswith('##FORMAT='):
            format_match = re.match(r'##FORMAT=<ID=([^,]+),.*Description="([^"]*)"', line)
            if format_match:
                field_id, description = format_match.groups()
                self.format_fields[field_id] = description
    
    def _parse_variant_line(self, line: str) -> Optional[Dict]:
        """
        Parse a single variant line from VCF
        
        Args:
            line: VCF variant line
            
        Returns:
            Variant dictionary or None if parsing fails
        """
        try:
            fields = line.split('\t')
            
            if len(fields) < 8:
                return None
            
            # Basic variant information
            variant = {
                'CHROM': fields[0],
                'POS': int(fields[1]),
                'ID': fields[2] if fields[2] != '.' else None,
                'REF': fields[3],
                'ALT': fields[4],
                'QUAL': self._parse_numeric_field(fields[5]),
                'FILTER': fields[6] if fields[6] != '.' else None,
                'INFO': fields[7]
            }
            
            # Parse INFO field
            info_dict = self._parse_info_field(fields[7])
            variant.update(info_dict)
            
            # Add sample information if present
            if len(fields) > 8 and len(self.column_headers) > 8:
                variant['FORMAT'] = fields[8]
                
                # Parse sample genotypes
                for i, sample_name in enumerate(self.column_headers[9:], 9):
                    if i < len(fields):
                        sample_data = self._parse_sample_field(fields[8], fields[i])
                        variant[f'SAMPLE_{sample_name}'] = sample_data
            
            # Add derived fields
            variant['variant_id'] = f"{variant['CHROM']}:{variant['POS']}:{variant['REF']}>{variant['ALT']}"
            variant['variant_type'] = self._determine_variant_type(variant['REF'], variant['ALT'])
            
            return variant
            
        except Exception as e:
            # Skip malformed lines
            return None
    
    def _parse_info_field(self, info_str: str) -> Dict:
        """Parse VCF INFO field into dictionary"""
        info_dict = {}
        
        if info_str == '.':
            return info_dict
        
        for item in info_str.split(';'):
            if '=' in item:
                key, value = item.split('=', 1)
                # Try to convert to appropriate type
                info_dict[key] = self._parse_info_value(value)
            else:
                # Flag field (present = True)
                info_dict[item] = True
        
        return info_dict
    
    def _parse_sample_field(self, format_str: str, sample_str: str) -> Dict:
        """Parse sample genotype field"""
        sample_dict = {}
        
        if format_str == '.' or sample_str == '.':
            return sample_dict
        
        format_fields = format_str.split(':')
        sample_values = sample_str.split(':')
        
        for i, field_name in enumerate(format_fields):
            if i < len(sample_values):
                sample_dict[field_name] = self._parse_sample_value(sample_values[i])
        
        return sample_dict
    
    def _parse_info_value(self, value: str) -> Union[str, int, float, List]:
        """Parse INFO field value to appropriate type"""
        if ',' in value:
            # Multiple values
            return [self._parse_single_value(v) for v in value.split(',')]
        else:
            return self._parse_single_value(value)
    
    def _parse_sample_value(self, value: str) -> Union[str, int, float]:
        """Parse sample field value to appropriate type"""
        return self._parse_single_value(value)
    
    def _parse_single_value(self, value: str) -> Union[str, int, float]:
        """Parse a single value to appropriate type"""
        if value == '.':
            return None
        
        # Try integer
        try:
            return int(value)
        except ValueError:
            pass
        
        # Try float
        try:
            return float(value)
        except ValueError:
            pass
        
        # Return as string
        return value
    
    def _parse_numeric_field(self, value: str) -> Optional[Union[int, float]]:
        """Parse numeric field (QUAL, etc.)"""
        if value == '.':
            return None
        
        try:
            if '.' in value:
                return float(value)
            else:
                return int(value)
        except ValueError:
            return None
    
    def _determine_variant_type(self, ref: str, alt: str) -> str:
        """Determine variant type based on REF and ALT alleles"""
        
        if len(ref) == 1 and len(alt) == 1:
            return 'SNV'  # Single nucleotide variant
        elif len(ref) > len(alt):
            return 'DEL'  # Deletion
        elif len(ref) < len(alt):
            return 'INS'  # Insertion
        else:
            return 'COMPLEX'  # Complex variant
    
    def get_variant_key(self, variant: Dict) -> str:
        """Generate unique key for variant"""
        return f"{variant['CHROM']}:{variant['POS']}:{variant['REF']}>{variant['ALT']}"
    
    def filter_variants(self, variants: List[Dict], 
                       filters: Dict) -> List[Dict]:
        """
        Filter variants based on criteria
        
        Args:
            variants: List of variant dictionaries
            filters: Dictionary of filter criteria
            
        Returns:
            Filtered list of variants
        """
        filtered_variants = []
        
        for variant in variants:
            include_variant = True
            
            # Quality filter
            if 'min_qual' in filters and variant.get('QUAL'):
                if variant['QUAL'] < filters['min_qual']:
                    include_variant = False
            
            # Chromosome filter
            if 'chromosomes' in filters:
                if variant['CHROM'] not in filters['chromosomes']:
                    include_variant = False
            
            # Variant type filter
            if 'variant_types' in filters:
                if variant.get('variant_type') not in filters['variant_types']:
                    include_variant = False
            
            # Custom filter function
            if 'custom_filter' in filters:
                if not filters['custom_filter'](variant):
                    include_variant = False
            
            if include_variant:
                filtered_variants.append(variant)
        
        return filtered_variants 