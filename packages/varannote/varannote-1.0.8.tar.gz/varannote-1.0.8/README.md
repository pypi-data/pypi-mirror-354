# VarAnnote - Comprehensive Variant Analysis & Annotation Suite

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15615370.svg)](https://doi.org/10.5281/zenodo.15615370)

🧬 A powerful toolkit for genomic variant annotation and clinical interpretation.

## Features

- **Comprehensive Annotation**: ClinVar, gnomAD, COSMIC, dbSNP integration
- **Functional Prediction**: Gene symbols, consequences, pathogenicity scores
- **Multiple Output Formats**: VCF, TSV, JSON
- **Command Line Interface**: Easy-to-use CLI with progress bars
- **Modular Design**: Each tool can be used independently
- **Academic Ready**: Designed for research and publication

## Installation

### From Source (Development)

```bash
git clone https://github.com/yourusername/varannote.git
cd VarAnnote
pip install -e .
```

### From PyPI (Coming Soon)

```bash
pip install varannote
```

## Installation

### Option 1: Install from PyPI (Recommended)

```bash
pip install varannote
```

### Option 2: Install from Source

```bash
git clone https://github.com/AtaUmutOZSOY/VarAnnote.git
cd VarAnnote
pip install -e .
```

### Windows PATH Configuration

VarAnnote automatically configures PATH on Windows during installation. If you encounter any issues:

1. **Restart your terminal** after installation - this is usually enough
2. **Alternative: Use python -m** (always works):
   ```bash
   python -m varannote --help
   python -m varannote annotate input.vcf --output output.vcf
   ```
3. **Manual setup** (if needed):
   ```bash
   python -m varannote setup-path
   ```

### Verify Installation

```bash
# Test installation
varannote --version
# or
python -m varannote --version

# Test with help
varannote --help
```

## Quick Start

### Basic Variant Annotation

```bash
# Annotate variants with default databases
varannote annotate test_variants.vcf --output annotated.vcf

# Use specific databases
varannote annotate input.vcf -d clinvar -d gnomad --output result.vcf

# Output in different formats
varannote annotate input.vcf --format tsv --output result.tsv
varannote annotate input.vcf --format json --output result.json
```

### Pathogenicity Prediction

```bash
# Predict pathogenicity using ensemble model
varannote pathogenicity variants.vcf --model ensemble

# Use specific model with custom threshold
varannote pathogenicity variants.vcf --model cadd --threshold 0.7
```

### Available Commands

```bash
varannote --help                    # Show all commands
varannote annotate --help           # Annotation help
varannote pathogenicity --help      # Pathogenicity prediction help
varannote pharmacogenomics --help   # Pharmacogenomics analysis help
varannote population-freq --help    # Population frequency help
varannote compound-het --help       # Compound heterozygote detection help
varannote segregation --help        # Family segregation analysis help
```

## Command Reference

### Main Commands

| Command | Description |
|---------|-------------|
| `annotate` | Comprehensive variant annotation |
| `pathogenicity` | Pathogenicity prediction |
| `pharmacogenomics` | Drug-gene interaction analysis |
| `population-freq` | Population frequency calculation |
| `compound-het` | Compound heterozygote detection |
| `segregation` | Family segregation analysis |

### Common Options

| Option | Description |
|--------|-------------|
| `--output, -o` | Output file path |
| `--format, -f` | Output format (vcf, tsv, json) |
| `--genome, -g` | Reference genome (hg19, hg38) |
| `--verbose, -v` | Enable verbose output |

## Input/Output Formats

### Input
- **VCF files** (.vcf, .vcf.gz)
- **Standard VCF format** with CHROM, POS, REF, ALT fields

### Output
- **VCF**: Annotated VCF with INFO fields
- **TSV**: Tab-separated values for analysis
- **JSON**: Structured data for programmatic use

## Annotation Databases

| Database | Description | Fields Added |
|----------|-------------|--------------|
| **ClinVar** | Clinical significance | `clinvar_significance`, `clinvar_id` |
| **gnomAD** | Population frequencies | `gnomad_af`, `gnomad_ac`, `gnomad_an` |
| **COSMIC** | Cancer mutations | `cosmic_id`, `cosmic_count` |
| **dbSNP** | Variant identifiers | `dbsnp_id` |

## Examples

### Example 1: Basic Annotation

```bash
varannote annotate test_variants.vcf --output annotated.vcf --verbose
```

Output:
```
🧬 Annotating variants from test_variants.vcf
📊 Using genome: hg38
🗄️  Databases: clinvar, gnomad, dbsnp
🔧 Initialized VariantAnnotator with genome: hg38
📖 Reading variants from test_variants.vcf
🔍 Found 5 variants to annotate
Annotating variants  [####################################]  100%
✅ Annotation complete: 5 variants processed
📁 Output saved to: annotated.vcf
```

### Example 2: TSV Output for Analysis

```bash
varannote annotate test_variants.vcf --format tsv --output results.tsv
```

### Example 3: Pathogenicity Analysis

```bash
varannote pathogenicity test_variants.vcf --model ensemble --threshold 0.6
```

## Development

### Project Structure

```
VarAnnote/
├── setup.py                    # Package configuration
├── requirements.txt            # Dependencies
├── README.md                   # This file
├── test_variants.vcf          # Test data
└── varannote/
    ├── __init__.py            # Main package
    ├── cli.py                 # Command line interface
    ├── core/                  # Core functionality
    │   ├── annotator.py       # Variant annotation engine
    │   └── pathogenicity.py   # Pathogenicity prediction
    ├── tools/                 # Individual tools
    │   ├── annotator.py       # Annotation tool
    │   └── ...                # Other tools
    └── utils/                 # Utilities
        ├── vcf_parser.py      # VCF file parser
        └── annotation_db.py   # Database interface
```

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run with coverage
pytest --cov=varannote tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Citation

If you use VarAnnote in your research, please cite:

### APA Format:
```
Özsoy, A. U. (2025). VarAnnote: Comprehensive Variant Analysis & Annotation Suite (Version 1.0.0) [Computer software]. https://doi.org/10.5281/zenodo.15615370
```

### BibTeX:
```bibtex
@software{ozsoy2025varannote,
  author = {Özsoy, Ata Umut},
  title = {VarAnnote: Comprehensive Variant Analysis \& Annotation Suite},
  url = {https://github.com/AtaUmutOZSOY/VarAnnote},
  doi = {10.5281/zenodo.15615370},
  version = {1.0.0},
  year = {2025}
}
```

### IEEE Format:
```
A. U. Özsoy, "VarAnnote: Comprehensive Variant Analysis & Annotation Suite," Version 1.0.0, 2025, doi: 10.5281/zenodo.15615370. [Online]. Available: https://github.com/AtaUmutOZSOY/VarAnnote
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

- **Author**: Ata Umut ÖZSOY
- **Email**: ataumut7@gmail.com
- **GitHub**: https://github.com/AtaUmutOZSOY/VarAnnote

## Acknowledgments

- BioPython community for sequence analysis tools
- gnomAD consortium for population frequency data
- ClinVar team for clinical variant curation
- COSMIC database for cancer mutation data 