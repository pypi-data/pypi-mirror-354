#!/usr/bin/env python3
"""
Variant Annotator Tool - Main annotation interface
"""

import sys
import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional
from tqdm import tqdm

from ..utils.vcf_parser import VCFParser
from ..utils.annotation_db import AnnotationDatabase
from ..utils.real_annotation_db import RealAnnotationDatabase
from ..core.annotator import VariantAnnotator

class VariantAnnotatorTool:
    """
    Enhanced variant annotation tool
    
    Provides comprehensive variant annotation using either mock or real databases
    with advanced features like parallel processing and confidence scoring.
    """
    
    def __init__(self, genome: str = "hg38", databases: Optional[List[str]] = None, 
                 verbose: bool = False, use_real_db: bool = False, cache_dir: Optional[str] = None,
                 use_parallel: bool = False, max_workers: int = 4):
        """
        Initialize enhanced variant annotator tool
        
        Args:
            genome: Reference genome version
            databases: List of databases to use
            verbose: Enable verbose output
            use_real_db: Use real databases instead of mock data
            cache_dir: Cache directory for real database results
            use_parallel: Enable parallel processing
            max_workers: Maximum number of parallel workers
        """
        self.genome = genome
        self.databases = databases or ["clinvar", "gnomad", "dbsnp", "cosmic", "omim", "pharmgkb", "clingen", "hgmd", "ensembl"]
        self.verbose = verbose
        self.use_real_db = use_real_db
        self.cache_dir = cache_dir
        self.use_parallel = use_parallel
        self.max_workers = max_workers
        
        # Initialize components
        self.vcf_parser = VCFParser()
        self.functional_annotator = VariantAnnotator(genome=genome)
        
        # Initialize database (mock or real)
        if use_real_db:
            if verbose:
                print("🔗 Initializing enhanced real database connections...")
            self.annotation_db = RealAnnotationDatabase(
                genome=genome,
                cache_dir=cache_dir,
                use_cache=True
            )
        else:
            if verbose:
                print("🎭 Using mock databases for testing...")
            self.annotation_db = AnnotationDatabase(genome=genome)
    
    def annotate_file(self, input_file: str, output_file: str, output_format: str = "vcf") -> Dict:
        """
        Annotate variants from a VCF file with enhanced features
        
        Args:
            input_file: Input VCF file path
            output_file: Output file path
            output_format: Output format (vcf, tsv, json)
            
        Returns:
            Dictionary with annotation statistics including confidence scores
        """
        if self.verbose:
            print(f"🔧 Initialized Enhanced VariantAnnotator with genome: {self.genome}")
            print(f"⚡ Parallel processing: {'enabled' if self.use_parallel else 'disabled'}")
        
        # Parse VCF file
        if self.verbose:
            print(f"📖 Reading variants from {input_file}")
        
        variants = self.vcf_parser.parse_file(input_file)
        
        if self.verbose:
            print(f"🔍 Found {len(variants)} variants to annotate")
        
        # Annotate variants
        annotated_variants = self._annotate_variants(variants)
        
        # Calculate confidence statistics
        confidence_stats = self._calculate_confidence_statistics(annotated_variants)
        
        # Save results
        self._save_results(annotated_variants, output_file, output_format)
        
        result = {
            'variants_processed': len(annotated_variants),
            'output_file': output_file,
            'output_format': output_format,
            'confidence_stats': confidence_stats
        }
        
        return result
    
    def _annotate_variants(self, variants: List[Dict]) -> List[Dict]:
        """Annotate a list of variants with enhanced processing"""
        
        if self.use_real_db and self.use_parallel and len(variants) > 1:
            # Use enhanced batch annotation with parallel processing
            return self.annotation_db.batch_annotate(
                variants, 
                databases=self.databases,
                max_workers=self.max_workers,
                use_parallel=True
            )
        else:
            # Use sequential processing
            return self._annotate_variants_sequential(variants)
    
    def _annotate_variants_sequential(self, variants: List[Dict]) -> List[Dict]:
        """Sequential variant annotation"""
        
        annotated_variants = []
        
        # Progress bar
        progress_bar = tqdm(
            variants, 
            desc="Annotating variants",
            disable=not self.verbose
        )
        
        for variant in progress_bar:
            try:
                # Get functional annotations
                functional_annotations = self.functional_annotator.get_functional_annotations(variant)
                
                # Get database annotations
                if self.use_real_db:
                    # Use real databases
                    db_annotations = self.annotation_db.get_annotations(variant, "all")
                else:
                    # Use mock databases
                    db_annotations = self.annotation_db.get_annotations(variant, "all")
                
                # Combine all annotations
                annotated_variant = {
                    **variant,
                    **functional_annotations,
                    **db_annotations
                }
                
                annotated_variants.append(annotated_variant)
                
            except Exception as e:
                if self.verbose:
                    print(f"Warning: Failed to annotate variant {variant.get('variant_id', 'unknown')}: {e}")
                
                # Add variant with minimal annotation
                annotated_variant = {
                    **variant,
                    'annotation_error': str(e)
                }
                annotated_variants.append(annotated_variant)
        
        return annotated_variants
    
    def _calculate_confidence_statistics(self, variants: List[Dict]) -> Dict:
        """Calculate confidence score statistics"""
        
        confidence_scores = []
        high_confidence_count = 0
        
        for variant in variants:
            confidence = variant.get('annotation_confidence', 0.0)
            if isinstance(confidence, (int, float)):
                confidence_scores.append(confidence)
                if confidence >= 0.7:  # High confidence threshold
                    high_confidence_count += 1
        
        if not confidence_scores:
            return {
                'average': 0.0,
                'median': 0.0,
                'high_confidence_count': 0,
                'total_variants': len(variants)
            }
        
        return {
            'average': sum(confidence_scores) / len(confidence_scores),
            'median': sorted(confidence_scores)[len(confidence_scores) // 2],
            'high_confidence_count': high_confidence_count,
            'total_variants': len(variants),
            'min_confidence': min(confidence_scores),
            'max_confidence': max(confidence_scores)
        }
    
    def _save_results(self, variants: List[Dict], output_file: str, output_format: str):
        """Save annotated variants to file with enhanced fields"""
        
        output_path = Path(output_file)
        
        if output_format == "vcf":
            self._save_vcf(variants, output_path)
        elif output_format == "tsv":
            self._save_tsv(variants, output_path)
        elif output_format == "json":
            self._save_json(variants, output_path)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
    
    def _save_vcf(self, variants: List[Dict], output_path: Path):
        """Save variants in VCF format with enhanced annotations in INFO field"""
        
        with open(output_path, 'w') as f:
            # Write VCF header
            f.write("##fileformat=VCFv4.2\n")
            f.write(f"##reference={self.genome}\n")
            
            # Add INFO field definitions for annotations
            info_fields = [
                "##INFO=<ID=GENE,Number=1,Type=String,Description=\"Gene symbol\">",
                "##INFO=<ID=CONSEQUENCE,Number=1,Type=String,Description=\"Variant consequence\">",
                "##INFO=<ID=CADD,Number=1,Type=Float,Description=\"CADD pathogenicity score\">",
                "##INFO=<ID=CLINVAR_SIG,Number=1,Type=String,Description=\"ClinVar significance\">",
                "##INFO=<ID=GNOMAD_AF,Number=1,Type=Float,Description=\"gnomAD allele frequency\">",
                "##INFO=<ID=DBSNP_ID,Number=1,Type=String,Description=\"dbSNP identifier\">",
                "##INFO=<ID=COSMIC_ID,Number=1,Type=String,Description=\"COSMIC identifier\">",
                "##INFO=<ID=OMIM_DISEASES,Number=1,Type=String,Description=\"OMIM disease associations\">",
                "##INFO=<ID=PHARMGKB_DRUGS,Number=1,Type=String,Description=\"PharmGKB drug interactions\">",
                "##INFO=<ID=CLINGEN_VALIDITY,Number=1,Type=String,Description=\"ClinGen gene-disease validity\">",
                "##INFO=<ID=CLINGEN_DISEASES,Number=1,Type=String,Description=\"ClinGen disease associations\">",
                "##INFO=<ID=HGMD_ID,Number=1,Type=String,Description=\"HGMD mutation identifier\">",
                "##INFO=<ID=HGMD_PATHOGENICITY,Number=1,Type=String,Description=\"HGMD pathogenicity classification\">",
                "##INFO=<ID=ENSEMBL_CONSEQUENCE,Number=1,Type=String,Description=\"Ensembl VEP consequence\">",
                "##INFO=<ID=ENSEMBL_IMPACT,Number=1,Type=String,Description=\"Ensembl impact prediction\">",
                "##INFO=<ID=CONFIDENCE,Number=1,Type=Float,Description=\"Annotation confidence score\">"
            ]
            
            for info_field in info_fields:
                f.write(f"{info_field}\n")
            
            # Write column header
            f.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
            
            # Write variants
            for variant in variants:
                info_parts = []
                
                # Add annotations to INFO field
                if variant.get('gene_symbol'):
                    info_parts.append(f"GENE={variant['gene_symbol']}")
                if variant.get('consequence'):
                    info_parts.append(f"CONSEQUENCE={variant['consequence']}")
                if variant.get('cadd_score'):
                    info_parts.append(f"CADD={variant['cadd_score']}")
                if variant.get('clinvar_significance'):
                    info_parts.append(f"CLINVAR_SIG={variant['clinvar_significance']}")
                if variant.get('gnomad_af'):
                    info_parts.append(f"GNOMAD_AF={variant['gnomad_af']}")
                if variant.get('dbsnp_id'):
                    info_parts.append(f"DBSNP_ID={variant['dbsnp_id']}")
                if variant.get('cosmic_id'):
                    info_parts.append(f"COSMIC_ID={variant['cosmic_id']}")
                if variant.get('omim_diseases'):
                    # Escape semicolons in OMIM diseases
                    diseases = str(variant['omim_diseases']).replace(';', '%3B')
                    info_parts.append(f"OMIM_DISEASES={diseases}")
                if variant.get('pharmgkb_drugs'):
                    # Escape semicolons in PharmGKB drugs
                    drugs = str(variant['pharmgkb_drugs']).replace(';', '%3B')
                    info_parts.append(f"PHARMGKB_DRUGS={drugs}")
                if variant.get('clingen_validity'):
                    info_parts.append(f"CLINGEN_VALIDITY={variant['clingen_validity']}")
                if variant.get('clingen_diseases'):
                    info_parts.append(f"CLINGEN_DISEASES={variant['clingen_diseases']}")
                if variant.get('hgmd_id'):
                    info_parts.append(f"HGMD_ID={variant['hgmd_id']}")
                if variant.get('hgmd_pathogenicity'):
                    info_parts.append(f"HGMD_PATHOGENICITY={variant['hgmd_pathogenicity']}")
                if variant.get('ensembl_consequence'):
                    info_parts.append(f"ENSEMBL_CONSEQUENCE={variant['ensembl_consequence']}")
                if variant.get('ensembl_impact'):
                    info_parts.append(f"ENSEMBL_IMPACT={variant['ensembl_impact']}")
                if variant.get('annotation_confidence'):
                    info_parts.append(f"CONFIDENCE={variant['annotation_confidence']}")
                
                info_str = ";".join(info_parts) if info_parts else "."
                
                # Write variant line
                f.write(f"{variant['CHROM']}\t{variant['POS']}\t{variant.get('ID', '.')}\t"
                       f"{variant['REF']}\t{variant['ALT']}\t{variant.get('QUAL', '.')}\t"
                       f"{variant.get('FILTER', '.')}\t{info_str}\n")
    
    def _save_tsv(self, variants: List[Dict], output_path: Path):
        """Save variants in TSV format with enhanced columns"""
        
        # Convert to DataFrame
        df = pd.DataFrame(variants)
        
        # Select key columns for TSV output
        key_columns = [
            'CHROM', 'POS', 'REF', 'ALT', 'variant_id',
            'gene_symbol', 'consequence', 'cadd_score',
            'clinvar_significance', 'gnomad_af', 'dbsnp_id', 'cosmic_id',
            'omim_diseases', 'omim_inheritance', 'pharmgkb_drugs', 'pharmgkb_level',
            'clingen_validity', 'clingen_diseases', 'clingen_dosage_hi', 'clingen_evidence',
            'hgmd_id', 'hgmd_pathogenicity', 'hgmd_disease', 'hgmd_evidence',
            'ensembl_consequence', 'ensembl_impact', 'ensembl_transcript', 'ensembl_sift', 'ensembl_polyphen',
            'annotation_confidence'
        ]
        
        # Keep only columns that exist
        available_columns = [col for col in key_columns if col in df.columns]
        df_output = df[available_columns]
        
        # Save to TSV
        df_output.to_csv(output_path, sep='\t', index=False)
    
    def _save_json(self, variants: List[Dict], output_path: Path):
        """Save variants in JSON format"""
        
        with open(output_path, 'w') as f:
            json.dump(variants, f, indent=2, default=str)
    
    def get_annotation_summary(self, variants: List[Dict]) -> Dict:
        """Get enhanced summary statistics for annotations"""
        
        total_variants = len(variants)
        
        # Count annotations
        with_gene = sum(1 for v in variants if v.get('gene_symbol'))
        with_clinvar = sum(1 for v in variants if v.get('clinvar_significance'))
        with_gnomad = sum(1 for v in variants if v.get('gnomad_af'))
        with_dbsnp = sum(1 for v in variants if v.get('dbsnp_id'))
        with_cosmic = sum(1 for v in variants if v.get('cosmic_id'))
        with_omim = sum(1 for v in variants if v.get('omim_diseases'))
        with_pharmgkb = sum(1 for v in variants if v.get('pharmgkb_drugs'))
        
        # Pathogenicity distribution
        pathogenic = sum(1 for v in variants 
                        if v.get('clinvar_significance') in ['Pathogenic', 'Likely_pathogenic'])
        benign = sum(1 for v in variants 
                    if v.get('clinvar_significance') in ['Benign', 'Likely_benign'])
        
        # Confidence statistics
        confidence_stats = self._calculate_confidence_statistics(variants)
        
        return {
            'total_variants': total_variants,
            'functional_annotations': {
                'with_gene_symbol': with_gene,
                'percentage': round(with_gene / total_variants * 100, 1) if total_variants > 0 else 0
            },
            'database_coverage': {
                'clinvar': {'count': with_clinvar, 'percentage': round(with_clinvar / total_variants * 100, 1)},
                'gnomad': {'count': with_gnomad, 'percentage': round(with_gnomad / total_variants * 100, 1)},
                'dbsnp': {'count': with_dbsnp, 'percentage': round(with_dbsnp / total_variants * 100, 1)},
                'cosmic': {'count': with_cosmic, 'percentage': round(with_cosmic / total_variants * 100, 1)},
                'omim': {'count': with_omim, 'percentage': round(with_omim / total_variants * 100, 1)},
                'pharmgkb': {'count': with_pharmgkb, 'percentage': round(with_pharmgkb / total_variants * 100, 1)}
            },
            'clinical_significance': {
                'pathogenic': pathogenic,
                'benign': benign,
                'unknown': total_variants - pathogenic - benign
            },
            'confidence_statistics': confidence_stats
        }

def main():
    """Command line interface for enhanced variant annotator"""
    
    import click
    
    @click.command()
    @click.argument('input_file', type=click.Path(exists=True))
    @click.option('--output', '-o', type=click.Path(), help='Output file path')
    @click.option('--format', '-f', type=click.Choice(['vcf', 'tsv', 'json']), 
                  default='vcf', help='Output format')
    @click.option('--databases', '-d', multiple=True, 
                  help='Annotation databases to use')
    @click.option('--genome', '-g', type=click.Choice(['hg19', 'hg38']), 
                  default='hg38', help='Reference genome version')
    @click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
    @click.option('--use_real_db', '-r', is_flag=True, help='Use real databases instead of mock data')
    @click.option('--cache_dir', '-c', type=click.Path(), help='Cache directory for real database results')
    @click.option('--parallel', is_flag=True, help='Enable parallel processing')
    @click.option('--max_workers', type=int, default=4, help='Maximum parallel workers')
    def cli(input_file, output, format, databases, genome, verbose, use_real_db, cache_dir, parallel, max_workers):
        """Annotate variants with enhanced genomic information."""
        
        if not output:
            output = Path(input_file).stem + f"_annotated.{format}"
        
        try:
            annotator = VariantAnnotatorTool(
                genome=genome,
                databases=list(databases) if databases else None,
                verbose=verbose,
                use_real_db=use_real_db,
                cache_dir=cache_dir,
                use_parallel=parallel,
                max_workers=max_workers
            )
            
            result = annotator.annotate_file(input_file, output, format)
            
            click.echo(f"✅ Enhanced annotation complete!")
            click.echo(f"📊 Variants processed: {result['variants_processed']}")
            click.echo(f"📁 Output saved to: {output}")
            
            # Show confidence statistics
            if 'confidence_stats' in result:
                stats = result['confidence_stats']
                click.echo(f"📈 Confidence: avg={stats['average']:.3f}, high_conf={stats['high_confidence_count']}")
            
        except Exception as e:
            click.echo(f"❌ Error: {str(e)}", err=True)
            sys.exit(1)
    
    cli()

if __name__ == '__main__':
    main() 