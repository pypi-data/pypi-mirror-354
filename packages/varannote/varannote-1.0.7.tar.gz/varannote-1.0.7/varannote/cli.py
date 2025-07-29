#!/usr/bin/env python3
"""
VarAnnote CLI - Main command line interface
"""

import click
import sys
import json
from pathlib import Path
from . import __version__

@click.group()
@click.version_option(version=__version__)
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--quiet', '-q', is_flag=True, help='Suppress output')
@click.pass_context
def main(ctx, verbose, quiet):
    """
    VarAnnote - Comprehensive Variant Analysis & Annotation Suite
    
    A powerful toolkit for genomic variant annotation and clinical interpretation.
    
    Examples:
        varannote annotate input.vcf --output annotated.vcf
        varannote pathogenicity variants.vcf --model ensemble
        varannote pharmacogenomics patient.vcf --drugs all
        varannote test-databases  # Test real database connections
        varannote manage-cache --clear  # Clear cache
        varannote api-keys --set omim YOUR_API_KEY  # Set API key
    """
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ctx.obj['quiet'] = quiet

@main.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--format', '-f', type=click.Choice(['vcf', 'tsv', 'json']), 
              default='vcf', help='Output format')
@click.option('--databases', '-d', multiple=True, 
              help='Annotation databases to use (clinvar, gnomad, cosmic, omim, pharmgkb, clingen, hgmd, ensembl)')
@click.option('--genome', '-g', type=click.Choice(['hg19', 'hg38']), 
              default='hg38', help='Reference genome version')
@click.option('--real-db', is_flag=True, help='Use real databases instead of mock data')
@click.option('--parallel', is_flag=True, help='Enable parallel processing')
@click.option('--max-workers', type=int, default=4, help='Maximum parallel workers')
@click.option('--confidence-threshold', type=float, default=0.0, 
              help='Minimum confidence score for annotations')
@click.pass_context
def annotate(ctx, input_file, output, format, databases, genome, real_db, parallel, 
             max_workers, confidence_threshold):
    """Annotate variants with comprehensive genomic information."""
    from .tools.annotator import VariantAnnotatorTool
    
    if not output:
        output = Path(input_file).stem + f"_annotated.{format}"
    
    click.echo(f"[*] Annotating variants from {input_file}")
    click.echo(f"[*] Using genome: {genome}")
    click.echo(f"[*] Databases: {', '.join(databases) if databases else 'all available'}")
    
    if real_db:
        click.echo("[*] Using REAL databases (ClinVar, gnomAD, dbSNP, COSMIC, OMIM, PharmGKB, ClinGen, HGMD, Ensembl)")
        if parallel:
            click.echo(f"[*] Parallel processing enabled ({max_workers} workers)")
    else:
        click.echo("[*] Using mock databases (for testing)")
    
    if confidence_threshold > 0:
        click.echo(f"[*] Confidence threshold: {confidence_threshold}")
    
    try:
        annotator = VariantAnnotatorTool(
            genome=genome,
            databases=list(databases) if databases else None,
            verbose=ctx.obj['verbose'],
            use_real_db=real_db,
            use_parallel=parallel,
            max_workers=max_workers
        )
        
        result = annotator.annotate_file(input_file, output, format)
        
        click.echo(f"[+] Annotation complete: {result['variants_processed']} variants processed")
        click.echo(f"[+] Output saved to: {output}")
        
        # Show confidence statistics if using real databases
        if real_db and 'confidence_stats' in result:
            stats = result['confidence_stats']
            click.echo(f"[*] Confidence scores: avg={stats['average']:.3f}, "
                      f"high_confidence={stats['high_confidence_count']}")
        
    except Exception as e:
        click.echo(f"[-] Error: {str(e)}", err=True)
        sys.exit(1)

@main.command()
@click.option('--test-variant', is_flag=True, help='Test with a specific variant')
@click.option('--cache-dir', type=click.Path(), help='Cache directory for results')
@click.option('--show-priorities', is_flag=True, help='Show database priorities')
def test_databases(test_variant, cache_dir, show_priorities):
    """Test connections to real bioinformatics databases."""
    from .utils.real_annotation_db import RealAnnotationDatabase
    
    click.echo("🔍 Testing Enhanced Database Connections")
    click.echo("=" * 50)
    
    try:
        # Initialize real database
        real_db = RealAnnotationDatabase(cache_dir=cache_dir)
        
        # Test connections
        results = real_db.test_connections()
        
        # Display results
        click.echo("\n📊 Connection Test Results:")
        
        # Sort by priority
        sorted_results = sorted(results.items(), 
                              key=lambda x: x[1].get('priority', 0), 
                              reverse=True)
        
        for db_name, result in sorted_results:
            priority = result.get('priority', 0)
            click.echo(f"\n🗄️  {db_name.upper()} (Priority: {priority}):")
            click.echo(f"   Status: {result['status']}")
            click.echo(f"   Data received: {result['data_received']}")
            if result['fields']:
                click.echo(f"   Fields: {', '.join(result['fields'][:5])}{'...' if len(result['fields']) > 5 else ''}")
        
        # Show cache statistics
        cache_stats = real_db.get_cache_stats()
        if cache_stats['cache_enabled']:
            click.echo("\n💾 Cache Statistics:")
            for db_name, stats in cache_stats['databases'].items():
                if stats['cached_entries'] > 0:
                    size_mb = stats['total_size_bytes'] / (1024 * 1024)
                    ttl_hours = stats['ttl_seconds'] / 3600
                    click.echo(f"   {db_name}: {stats['cached_entries']} entries, "
                              f"{size_mb:.1f}MB, TTL: {ttl_hours:.1f}h")
        
        # Test with specific variant if requested
        if test_variant:
            click.echo("\n🧬 Testing with specific variant...")
            test_var = {
                "CHROM": "17",
                "POS": 43044295,
                "REF": "G",
                "ALT": "A",
                "variant_id": "17:43044295:G>A"
            }
            
            click.echo(f"Variant: {test_var['variant_id']}")
            
            # Test comprehensive annotation
            annotations = real_db.get_annotations(test_var, "all")
            
            # Show key results
            key_fields = ["clinvar_significance", "gnomad_af", "omim_diseases", 
                         "pharmgkb_drugs", "cosmic_id", "dbsnp_id", "annotation_confidence"]
            
            click.echo("\n📋 Annotation Results:")
            for field in key_fields:
                if field in annotations and annotations[field] is not None:
                    value = annotations[field]
                    if isinstance(value, float):
                        click.echo(f"   {field}: {value:.6f}")
                    else:
                        # Truncate long values
                        str_value = str(value)
                        if len(str_value) > 50:
                            str_value = str_value[:47] + "..."
                        click.echo(f"   {field}: {str_value}")
        
        # Show database information
        if show_priorities:
            click.echo("\n📚 Database Information:")
            db_info = real_db.get_all_database_info()
            for db_name, info in db_info.items():
                priority = real_db.database_priorities.get(db_name, 0)
                click.echo(f"\n🗄️  {info['name']} (Priority: {priority}):")
                click.echo(f"   Description: {info['description']}")
                click.echo(f"   URL: {info['url']}")
                click.echo(f"   Version: {info.get('version', 'N/A')}")
                if info.get('requires_api_key'):
                    api_key_status = "✅ Set" if real_db.api_key_manager.get_key(db_name) else "❌ Not set"
                    click.echo(f"   API Key: {api_key_status}")
        
    except Exception as e:
        click.echo(f"❌ Error testing databases: {str(e)}", err=True)
        sys.exit(1)

@main.command()
@click.option('--set', 'set_key', nargs=2, metavar='DATABASE API_KEY', 
              help='Set API key for database')
@click.option('--list', 'list_keys', is_flag=True, help='List configured API keys')
@click.option('--remove', metavar='DATABASE', help='Remove API key for database')
@click.option('--test', metavar='DATABASE', help='Test API key for database')
def api_keys(set_key, list_keys, remove, test):
    """Manage API keys for databases."""
    from .utils.real_annotation_db import APIKeyManager
    
    api_manager = APIKeyManager()
    
    if set_key:
        database, api_key = set_key
        api_manager.set_key(database, api_key)
        click.echo(f"✅ API key set for {database}")
        
    elif list_keys:
        click.echo("🔑 Configured API Keys:")
        for db, key in api_manager.api_keys.items():
            masked_key = key[:8] + "..." + key[-4:] if len(key) > 12 else "***"
            click.echo(f"   {db}: {masked_key}")
        
        if not api_manager.api_keys:
            click.echo("   No API keys configured")
            
    elif remove:
        if remove in api_manager.api_keys:
            del api_manager.api_keys[remove]
            api_manager._save_api_keys()
            click.echo(f"✅ API key removed for {remove}")
        else:
            click.echo(f"❌ No API key found for {remove}")
            
    elif test:
        api_key = api_manager.get_key(test)
        if api_key:
            click.echo(f"🔍 Testing API key for {test}...")
            # Here you would test the actual API connection
            click.echo(f"✅ API key appears to be configured for {test}")
        else:
            click.echo(f"❌ No API key configured for {test}")
            
    else:
        click.echo("Use --help to see available options")

@main.command()
@click.option('--clear', is_flag=True, help='Clear expired cache entries')
@click.option('--clear-all', is_flag=True, help='Clear all cache entries')
@click.option('--clear-db', metavar='DATABASE', help='Clear cache for specific database')
@click.option('--stats', is_flag=True, help='Show cache statistics')
@click.option('--cache-dir', type=click.Path(), help='Cache directory')
def manage_cache(clear, clear_all, clear_db, stats, cache_dir):
    """Manage annotation cache."""
    from .utils.real_annotation_db import RealAnnotationDatabase
    
    real_db = RealAnnotationDatabase(cache_dir=cache_dir)
    
    if clear:
        cleared = real_db.clear_cache()
        click.echo(f"🧹 Cleared {cleared} expired cache entries")
        
    elif clear_all:
        cleared = 0
        for db_name in real_db.get_available_databases():
            cleared += real_db.clear_cache(db_name)
        click.echo(f"🧹 Cleared {cleared} cache entries")
        
    elif clear_db:
        cleared = real_db.clear_cache(clear_db)
        click.echo(f"🧹 Cleared {cleared} cache entries for {clear_db}")
        
    elif stats:
        cache_stats = real_db.get_cache_stats()
        
        if not cache_stats['cache_enabled']:
            click.echo("❌ Cache is disabled")
            return
            
        click.echo("💾 Cache Statistics:")
        click.echo(f"   Cache directory: {real_db.cache_dir}")
        
        total_entries = 0
        total_size = 0
        
        for db_name, stats in cache_stats['databases'].items():
            entries = stats['cached_entries']
            size_bytes = stats['total_size_bytes']
            ttl_hours = stats['ttl_seconds'] / 3600
            
            total_entries += entries
            total_size += size_bytes
            
            if entries > 0:
                size_mb = size_bytes / (1024 * 1024)
                click.echo(f"   {db_name}: {entries} entries, {size_mb:.1f}MB, TTL: {ttl_hours:.1f}h")
        
        total_size_mb = total_size / (1024 * 1024)
        click.echo(f"\n   Total: {total_entries} entries, {total_size_mb:.1f}MB")
        
    else:
        click.echo("Use --help to see available options")

@main.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--model', '-m', type=click.Choice(['cadd', 'revel', 'ensemble']), 
              default='ensemble', help='Pathogenicity prediction model')
@click.option('--threshold', '-t', type=float, default=0.5, 
              help='Pathogenicity threshold (0-1)')
@click.pass_context
def pathogenicity(ctx, input_file, output, model, threshold):
    """Predict variant pathogenicity using machine learning models."""
    from .tools.pathogenicity import PathogenicityTool
    
    if not output:
        output = Path(input_file).stem + "_pathogenicity.tsv"
    
    click.echo(f"🔬 Predicting pathogenicity for variants in {input_file}")
    click.echo(f"🤖 Using model: {model}")
    click.echo(f"📊 Threshold: {threshold}")
    
    try:
        predictor = PathogenicityTool(
            model=model,
            threshold=threshold,
            verbose=ctx.obj['verbose']
        )
        
        result = predictor.predict_file(input_file, output)
        
        click.echo(f"✅ Prediction complete: {result['variants_analyzed']} variants analyzed")
        click.echo(f"⚠️  Pathogenic variants: {result['pathogenic_count']}")
        click.echo(f"📁 Output saved to: {output}")
        
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)

@main.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--drugs', '-d', type=str, help='Comma-separated drug list or "all"')
@click.option('--population', '-p', type=click.Choice(['EUR', 'AFR', 'AMR', 'EAS', 'SAS']), 
              help='Population for frequency analysis')
@click.option('--guidelines', '-g', type=click.Choice(['CPIC', 'FDA', 'EMA', 'DPWG']),
              help='Pharmacogenomic guidelines to use')
@click.pass_context
def pharmacogenomics(ctx, input_file, output, drugs, population, guidelines):
    """Analyze pharmacogenomic variants and drug interactions."""
    from .tools.pharmacogenomics import PharmacogenomicsTool
    
    if not output:
        output = Path(input_file).stem + "_pharmacogenomics.tsv"
    
    click.echo(f"💊 Analyzing pharmacogenomic variants in {input_file}")
    click.echo(f"🧬 Population: {population or 'mixed'}")
    if guidelines:
        click.echo(f"📋 Guidelines: {guidelines}")
    
    try:
        analyzer = PharmacogenomicsTool(
            population=population,
            guidelines=guidelines,
            verbose=ctx.obj['verbose']
        )
        
        drug_list = drugs.split(',') if drugs and drugs != 'all' else None
        result = analyzer.analyze_file(input_file, output, drug_list)
        
        click.echo(f"✅ Analysis complete: {result['variants_analyzed']} variants analyzed")
        click.echo(f"💊 Drug interactions found: {result['interactions_found']}")
        click.echo(f"📁 Output saved to: {output}")
        
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)

@main.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--populations', '-p', multiple=True, 
              help='Population databases (gnomad, 1000g, topmed)')
@click.pass_context
def population_freq(ctx, input_file, output, populations):
    """Calculate population frequencies for variants."""
    from .tools.population_freq import PopulationFreqTool
    
    if not output:
        output = Path(input_file).stem + "_population_freq.tsv"
    
    click.echo(f"🌍 Calculating population frequencies for {input_file}")
    
    try:
        calculator = PopulationFreqTool(
            populations=list(populations) if populations else None,
            verbose=ctx.obj['verbose']
        )
        
        result = calculator.calculate_file(input_file, output)
        
        click.echo(f"✅ Calculation complete: {result['variants_processed']} variants processed")
        click.echo(f"📁 Output saved to: {output}")
        
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)

@main.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--min-quality', '-q', type=int, default=20, help='Minimum variant quality')
@click.pass_context
def compound_het(ctx, input_file, output, min_quality):
    """Detect compound heterozygous variants."""
    from .tools.compound_het import CompoundHetTool
    
    if not output:
        output = Path(input_file).stem + "_compound_het.tsv"
    
    click.echo(f"🧬 Detecting compound heterozygous variants in {input_file}")
    
    try:
        detector = CompoundHetTool(
            min_quality=min_quality,
            verbose=ctx.obj['verbose']
        )
        
        result = detector.detect_file(input_file, output)
        
        click.echo(f"✅ Detection complete: {result['compound_het_pairs']} pairs found")
        click.echo(f"📁 Output saved to: {output}")
        
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)

@main.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--pedigree', '-p', type=click.Path(exists=True), 
              help='Pedigree file (PED format)')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.pass_context
def segregation(ctx, input_file, pedigree, output):
    """Analyze variant segregation in families."""
    from .tools.segregation import SegregationTool
    
    if not pedigree:
        click.echo("❌ Error: Pedigree file is required for segregation analysis", err=True)
        sys.exit(1)
    
    if not output:
        output = Path(input_file).stem + "_segregation.tsv"
    
    click.echo(f"👨‍👩‍👧‍👦 Analyzing variant segregation in {input_file}")
    click.echo(f"📋 Using pedigree: {pedigree}")
    
    try:
        analyzer = SegregationTool(
            pedigree_file=pedigree,
            verbose=ctx.obj['verbose']
        )
        
        result = analyzer.analyze_file(input_file, output)
        
        click.echo(f"✅ Analysis complete: {result['variants_analyzed']} variants analyzed")
        click.echo(f"📁 Output saved to: {output}")
        
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    main() 