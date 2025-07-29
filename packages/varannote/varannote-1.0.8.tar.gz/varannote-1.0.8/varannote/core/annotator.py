#!/usr/bin/env python3
"""
Core Variant Annotator - Functional annotation engine
"""

from typing import Dict, List, Optional
import random

class VariantAnnotator:
    """
    Core variant annotation engine
    
    Provides functional annotations for genomic variants including
    gene symbols, consequences, and pathogenicity scores.
    """
    
    def __init__(self, genome: str = "hg38"):
        """
        Initialize variant annotator
        
        Args:
            genome: Reference genome version
        """
        self.genome = genome
        
        # Mock gene database (in real implementation, this would be loaded from files)
        self.gene_regions = {
            "1": [("BRCA1", 43044295, 43125483), ("TP53", 7565097, 7590856)],
            "2": [("BRCA2", 32315086, 32400266), ("MSH2", 47630108, 47710367)],
            "17": [("TP53", 7565097, 7590856), ("BRCA1", 43044295, 43125483)],
            # Add more chromosomes and genes as needed
        }
        
        # Mock consequence types
        self.consequence_types = [
            "missense_variant", "synonymous_variant", "stop_gained", 
            "stop_lost", "frameshift_variant", "inframe_deletion",
            "inframe_insertion", "splice_donor_variant", "splice_acceptor_variant",
            "intron_variant", "5_prime_UTR_variant", "3_prime_UTR_variant",
            "upstream_gene_variant", "downstream_gene_variant", "intergenic_variant"
        ]
    
    def get_functional_annotations(self, variant: Dict) -> Dict:
        """
        Get functional annotations for a variant
        
        Args:
            variant: Variant dictionary with CHROM, POS, REF, ALT
            
        Returns:
            Dictionary with functional annotations
        """
        annotations = {}
        
        # Find overlapping gene
        gene_symbol = self._find_overlapping_gene(variant)
        if gene_symbol:
            annotations['gene_symbol'] = gene_symbol
            
            # Predict consequence type
            consequence = self._predict_consequence(variant, gene_symbol)
            annotations['consequence'] = consequence
            
            # Calculate mock CADD score
            cadd_score = self._calculate_cadd_score(variant)
            annotations['cadd_score'] = cadd_score
            
            # Add transcript information
            annotations['transcript_id'] = f"ENST{random.randint(100000, 999999)}"
            annotations['protein_position'] = random.randint(1, 500)
            
        else:
            annotations['gene_symbol'] = "intergenic"
            annotations['consequence'] = "intergenic_variant"
            annotations['cadd_score'] = random.uniform(0.1, 5.0)
        
        return annotations
    
    def _find_overlapping_gene(self, variant: Dict) -> Optional[str]:
        """Find gene that overlaps with variant position"""
        chrom = variant['CHROM']
        pos = variant['POS']
        
        if chrom in self.gene_regions:
            for gene_name, start, end in self.gene_regions[chrom]:
                if start <= pos <= end:
                    return gene_name
        
        return None
    
    def _predict_consequence(self, variant: Dict, gene_symbol: str) -> str:
        """Predict variant consequence type"""
        
        # Simple mock prediction based on variant type
        variant_type = variant.get('variant_type', 'SNV')
        
        if variant_type == 'SNV':
            # For SNVs, randomly assign consequence with realistic probabilities
            consequences = [
                ("missense_variant", 0.4),
                ("synonymous_variant", 0.3),
                ("stop_gained", 0.05),
                ("splice_donor_variant", 0.02),
                ("splice_acceptor_variant", 0.02),
                ("intron_variant", 0.21)
            ]
        elif variant_type == 'DEL':
            consequences = [
                ("frameshift_variant", 0.4),
                ("inframe_deletion", 0.3),
                ("intron_variant", 0.3)
            ]
        elif variant_type == 'INS':
            consequences = [
                ("frameshift_variant", 0.4),
                ("inframe_insertion", 0.3),
                ("intron_variant", 0.3)
            ]
        else:
            consequences = [("intron_variant", 1.0)]
        
        # Weighted random selection
        rand_val = random.random()
        cumulative = 0
        for consequence, prob in consequences:
            cumulative += prob
            if rand_val <= cumulative:
                return consequence
        
        return consequences[0][0]  # fallback
    
    def _calculate_cadd_score(self, variant: Dict) -> float:
        """Calculate mock CADD pathogenicity score"""
        
        # Mock CADD score calculation
        # Real implementation would use pre-computed CADD scores
        
        base_score = random.uniform(0.1, 30.0)
        
        # Adjust based on variant type
        variant_type = variant.get('variant_type', 'SNV')
        if variant_type in ['DEL', 'INS']:
            base_score += random.uniform(2.0, 10.0)
        
        # Adjust based on chromosome (some chromosomes have higher scores)
        if variant['CHROM'] in ['17', '13', 'X']:
            base_score += random.uniform(1.0, 5.0)
        
        return round(min(base_score, 99.0), 2)
    
    def annotate_batch(self, variants: List[Dict]) -> List[Dict]:
        """
        Annotate a batch of variants
        
        Args:
            variants: List of variant dictionaries
            
        Returns:
            List of annotated variants
        """
        annotated_variants = []
        
        for variant in variants:
            annotations = self.get_functional_annotations(variant)
            annotated_variant = {**variant, **annotations}
            annotated_variants.append(annotated_variant)
        
        return annotated_variants 