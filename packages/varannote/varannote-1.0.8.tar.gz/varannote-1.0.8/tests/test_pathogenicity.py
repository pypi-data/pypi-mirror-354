#!/usr/bin/env python3
"""
Test suite for pathogenicity prediction module
"""

import pytest
import random
from unittest.mock import patch, MagicMock
from varannote.core.pathogenicity import PathogenicityPredictor


class TestPathogenicityPredictor:
    """Test suite for PathogenicityPredictor class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.predictor = PathogenicityPredictor()
        self.predictor_cadd = PathogenicityPredictor(model="CADD")
        self.predictor_revel = PathogenicityPredictor(model="REVEL")
        
    def test_init_default_model(self):
        """Test PathogenicityPredictor initialization with default model"""
        predictor = PathogenicityPredictor()
        assert predictor.model == "ensemble"
        
    def test_init_custom_model(self):
        """Test PathogenicityPredictor initialization with custom model"""
        predictor = PathogenicityPredictor(model="CADD")
        assert predictor.model == "CADD"
        
        predictor = PathogenicityPredictor(model="REVEL")
        assert predictor.model == "REVEL"
        
    def test_predict_pathogenicity_basic_variant(self):
        """Test pathogenicity prediction for basic variant"""
        variant = {
            'chr': '1',
            'pos': 12345,
            'ref': 'A',
            'alt': 'T',
            'variant_type': 'SNV'
        }
        
        with patch('random.uniform', return_value=0.5):
            result = self.predictor.predict_pathogenicity(variant)
            
        assert 'pathogenicity_score' in result
        assert 'pathogenicity_class' in result
        assert 'model_used' in result
        assert result['model_used'] == 'ensemble'
        assert 0.0 <= result['pathogenicity_score'] <= 1.0
        
    def test_predict_pathogenicity_snv_variant(self):
        """Test pathogenicity prediction for SNV variant"""
        variant = {
            'variant_type': 'SNV',
            'gene_symbol': 'GENE1',
            'consequence': 'missense_variant'
        }
        
        with patch('random.uniform', return_value=0.3):
            result = self.predictor.predict_pathogenicity(variant)
            
        # Base score 0.3 + missense adjustment 0.1 = 0.4
        assert result['pathogenicity_score'] == 0.4
        assert result['pathogenicity_class'] == 'Likely_benign'
        
    def test_predict_pathogenicity_deletion_variant(self):
        """Test pathogenicity prediction for deletion variant"""
        variant = {
            'variant_type': 'DEL',
            'gene_symbol': 'GENE1',
            'consequence': 'frameshift_variant'
        }
        
        with patch('random.uniform', return_value=0.2):
            result = self.predictor.predict_pathogenicity(variant)
            
        # Base score 0.2 + DEL adjustment 0.2 + frameshift adjustment 0.4 = 0.8
        assert result['pathogenicity_score'] == 0.8
        assert result['pathogenicity_class'] == 'Pathogenic'
        
    def test_predict_pathogenicity_insertion_variant(self):
        """Test pathogenicity prediction for insertion variant"""
        variant = {
            'variant_type': 'INS',
            'gene_symbol': 'GENE1',
            'consequence': 'stop_gained'
        }
        
        with patch('random.uniform', return_value=0.1):
            result = self.predictor.predict_pathogenicity(variant)
            
        # Base score 0.1 + INS adjustment 0.2 + stop_gained adjustment 0.4 = 0.7
        assert result['pathogenicity_score'] == 0.7
        assert result['pathogenicity_class'] == 'Likely_pathogenic'
        
    def test_predict_pathogenicity_brca1_gene(self):
        """Test pathogenicity prediction for BRCA1 gene variant"""
        variant = {
            'variant_type': 'SNV',
            'gene_symbol': 'BRCA1',
            'consequence': 'missense_variant'
        }
        
        with patch('random.uniform', return_value=0.2):
            result = self.predictor.predict_pathogenicity(variant)
            
        # Base score 0.2 + BRCA1 adjustment 0.3 + missense adjustment 0.1 = 0.6
        assert result['pathogenicity_score'] == 0.6
        assert result['pathogenicity_class'] == 'Likely_pathogenic'
        
    def test_predict_pathogenicity_brca2_gene(self):
        """Test pathogenicity prediction for BRCA2 gene variant"""
        variant = {
            'variant_type': 'SNV',
            'gene_symbol': 'BRCA2',
            'consequence': 'synonymous_variant'
        }
        
        with patch('random.uniform', return_value=0.4):
            result = self.predictor.predict_pathogenicity(variant)
            
        # Base score 0.4 + BRCA2 adjustment 0.3 + synonymous adjustment -0.2 = 0.5
        assert result['pathogenicity_score'] == 0.5
        assert result['pathogenicity_class'] == 'Uncertain_significance'
        
    def test_predict_pathogenicity_tp53_gene(self):
        """Test pathogenicity prediction for TP53 gene variant"""
        variant = {
            'variant_type': 'SNV',
            'gene_symbol': 'TP53',
            'consequence': 'stop_gained'
        }
        
        with patch('random.uniform', return_value=0.1):
            result = self.predictor.predict_pathogenicity(variant)
            
        # Base score 0.1 + TP53 adjustment 0.3 + stop_gained adjustment 0.4 = 0.8
        assert result['pathogenicity_score'] == 0.8
        assert result['pathogenicity_class'] == 'Pathogenic'
        
    def test_predict_pathogenicity_frameshift_consequence(self):
        """Test pathogenicity prediction for frameshift consequence"""
        variant = {
            'variant_type': 'SNV',
            'gene_symbol': 'GENE1',
            'consequence': 'frameshift_variant'
        }
        
        with patch('random.uniform', return_value=0.3):
            result = self.predictor.predict_pathogenicity(variant)
            
        # Base score 0.3 + frameshift adjustment 0.4 = 0.7
        assert result['pathogenicity_score'] == 0.7
        assert result['pathogenicity_class'] == 'Likely_pathogenic'
        
    def test_predict_pathogenicity_synonymous_consequence(self):
        """Test pathogenicity prediction for synonymous consequence"""
        variant = {
            'variant_type': 'SNV',
            'gene_symbol': 'GENE1',
            'consequence': 'synonymous_variant'
        }
        
        with patch('random.uniform', return_value=0.5):
            result = self.predictor.predict_pathogenicity(variant)
            
        # Base score 0.5 + synonymous adjustment -0.2 = 0.3
        assert result['pathogenicity_score'] == 0.3
        assert result['pathogenicity_class'] == 'Likely_benign'
        
    def test_predict_pathogenicity_score_normalization_high(self):
        """Test pathogenicity score normalization for high values"""
        variant = {
            'variant_type': 'DEL',
            'gene_symbol': 'BRCA1',
            'consequence': 'frameshift_variant'
        }
        
        with patch('random.uniform', return_value=0.9):
            result = self.predictor.predict_pathogenicity(variant)
            
        # Base score 0.9 + DEL 0.2 + BRCA1 0.3 + frameshift 0.4 = 1.8, normalized to 1.0
        assert result['pathogenicity_score'] == 1.0
        assert result['pathogenicity_class'] == 'Pathogenic'
        
    def test_predict_pathogenicity_score_normalization_low(self):
        """Test pathogenicity score normalization for low values"""
        variant = {
            'variant_type': 'SNV',
            'gene_symbol': 'GENE1',
            'consequence': 'synonymous_variant'
        }
        
        with patch('random.uniform', return_value=0.1):
            result = self.predictor.predict_pathogenicity(variant)
            
        # Base score 0.1 + synonymous adjustment -0.2 = -0.1, normalized to 0.0
        assert result['pathogenicity_score'] == 0.0
        assert result['pathogenicity_class'] == 'Benign'
        
    def test_predict_pathogenicity_classification_pathogenic(self):
        """Test pathogenicity classification for pathogenic variants"""
        variant = {'variant_type': 'SNV'}
        
        with patch('random.uniform', return_value=0.85):
            result = self.predictor.predict_pathogenicity(variant)
            
        assert result['pathogenicity_score'] == 0.85
        assert result['pathogenicity_class'] == 'Pathogenic'
        
    def test_predict_pathogenicity_classification_likely_pathogenic(self):
        """Test pathogenicity classification for likely pathogenic variants"""
        variant = {'variant_type': 'SNV'}
        
        with patch('random.uniform', return_value=0.65):
            result = self.predictor.predict_pathogenicity(variant)
            
        assert result['pathogenicity_score'] == 0.65
        assert result['pathogenicity_class'] == 'Likely_pathogenic'
        
    def test_predict_pathogenicity_classification_uncertain(self):
        """Test pathogenicity classification for uncertain significance variants"""
        variant = {'variant_type': 'SNV'}
        
        with patch('random.uniform', return_value=0.5):
            result = self.predictor.predict_pathogenicity(variant)
            
        assert result['pathogenicity_score'] == 0.5
        assert result['pathogenicity_class'] == 'Uncertain_significance'
        
    def test_predict_pathogenicity_classification_likely_benign(self):
        """Test pathogenicity classification for likely benign variants"""
        variant = {'variant_type': 'SNV'}
        
        with patch('random.uniform', return_value=0.35):
            result = self.predictor.predict_pathogenicity(variant)
            
        assert result['pathogenicity_score'] == 0.35
        assert result['pathogenicity_class'] == 'Likely_benign'
        
    def test_predict_pathogenicity_classification_benign(self):
        """Test pathogenicity classification for benign variants"""
        variant = {'variant_type': 'SNV'}
        
        with patch('random.uniform', return_value=0.15):
            result = self.predictor.predict_pathogenicity(variant)
            
        assert result['pathogenicity_score'] == 0.15
        assert result['pathogenicity_class'] == 'Benign'
        
    def test_predict_pathogenicity_empty_variant(self):
        """Test pathogenicity prediction for empty variant"""
        variant = {}
        
        with patch('random.uniform', return_value=0.5):
            result = self.predictor.predict_pathogenicity(variant)
            
        assert result['pathogenicity_score'] == 0.5
        assert result['pathogenicity_class'] == 'Uncertain_significance'
        assert result['model_used'] == 'ensemble'
        
    def test_predict_pathogenicity_missing_fields(self):
        """Test pathogenicity prediction with missing variant fields"""
        variant = {
            'chr': '1',
            'pos': 12345
            # Missing variant_type, gene_symbol, consequence
        }
        
        with patch('random.uniform', return_value=0.4):
            result = self.predictor.predict_pathogenicity(variant)
            
        assert result['pathogenicity_score'] == 0.4
        assert result['pathogenicity_class'] == 'Likely_benign'
        
    def test_predict_pathogenicity_different_models(self):
        """Test pathogenicity prediction with different models"""
        variant = {'variant_type': 'SNV'}
        
        with patch('random.uniform', return_value=0.5):
            result_ensemble = self.predictor.predict_pathogenicity(variant)
            result_cadd = self.predictor_cadd.predict_pathogenicity(variant)
            result_revel = self.predictor_revel.predict_pathogenicity(variant)
            
        assert result_ensemble['model_used'] == 'ensemble'
        assert result_cadd['model_used'] == 'CADD'
        assert result_revel['model_used'] == 'REVEL'
        
    def test_predict_pathogenicity_score_rounding(self):
        """Test pathogenicity score rounding to 3 decimal places"""
        variant = {'variant_type': 'SNV'}
        
        with patch('random.uniform', return_value=0.123456789):
            result = self.predictor.predict_pathogenicity(variant)
            
        assert result['pathogenicity_score'] == 0.123
        
    def test_predict_pathogenicity_complex_variant(self):
        """Test pathogenicity prediction for complex variant with multiple features"""
        variant = {
            'variant_type': 'DEL',
            'gene_symbol': 'BRCA1',
            'consequence': 'frameshift_variant',
            'chr': '17',
            'pos': 41234567,
            'ref': 'ATCG',
            'alt': 'A'
        }
        
        with patch('random.uniform', return_value=0.2):
            result = self.predictor.predict_pathogenicity(variant)
            
        # Base 0.2 + DEL 0.2 + BRCA1 0.3 + frameshift 0.4 = 1.1, normalized to 1.0
        assert result['pathogenicity_score'] == 1.0
        assert result['pathogenicity_class'] == 'Pathogenic'
        assert result['model_used'] == 'ensemble'
        
    def test_predict_pathogenicity_multiple_consequences(self):
        """Test pathogenicity prediction with multiple consequences"""
        variant = {
            'variant_type': 'SNV',
            'gene_symbol': 'GENE1',
            'consequence': 'missense_variant,synonymous_variant'
        }
        
        with patch('random.uniform', return_value=0.5):
            result = self.predictor.predict_pathogenicity(variant)
            
        # Should match missense first (0.5 + 0.1 = 0.6)
        assert result['pathogenicity_score'] == 0.6
        assert result['pathogenicity_class'] == 'Likely_pathogenic'
        
    def test_predict_pathogenicity_stop_gained_in_consequence(self):
        """Test pathogenicity prediction with stop_gained in consequence string"""
        variant = {
            'variant_type': 'SNV',
            'gene_symbol': 'GENE1',
            'consequence': 'stop_gained&splice_region_variant'
        }
        
        with patch('random.uniform', return_value=0.3):
            result = self.predictor.predict_pathogenicity(variant)
            
        # Base 0.3 + stop_gained 0.4 = 0.7
        assert result['pathogenicity_score'] == 0.7
        assert result['pathogenicity_class'] == 'Likely_pathogenic'
        
    @pytest.mark.parametrize("model", ["ensemble", "CADD", "REVEL", "SIFT", "PolyPhen"])
    def test_predict_pathogenicity_various_models(self, model):
        """Test pathogenicity prediction with various models"""
        predictor = PathogenicityPredictor(model=model)
        variant = {'variant_type': 'SNV'}
        
        with patch('random.uniform', return_value=0.5):
            result = predictor.predict_pathogenicity(variant)
            
        assert result['model_used'] == model
        assert 'pathogenicity_score' in result
        assert 'pathogenicity_class' in result
        
    @pytest.mark.parametrize("variant_type,expected_adjustment", [
        ("SNV", 0.0),
        ("DEL", 0.2),
        ("INS", 0.2),
        ("DUP", 0.0),
        ("CNV", 0.0)
    ])
    def test_predict_pathogenicity_variant_type_adjustments(self, variant_type, expected_adjustment):
        """Test pathogenicity adjustments for different variant types"""
        variant = {'variant_type': variant_type}
        
        with patch('random.uniform', return_value=0.3):
            result = self.predictor.predict_pathogenicity(variant)
            
        expected_score = 0.3 + expected_adjustment
        assert result['pathogenicity_score'] == expected_score
        
    @pytest.mark.parametrize("gene,expected_adjustment", [
        ("BRCA1", 0.3),
        ("BRCA2", 0.3),
        ("TP53", 0.3),
        ("GENE1", 0.0),
        ("", 0.0)
    ])
    def test_predict_pathogenicity_gene_adjustments(self, gene, expected_adjustment):
        """Test pathogenicity adjustments for different genes"""
        variant = {'gene_symbol': gene}
        
        with patch('random.uniform', return_value=0.3):
            result = self.predictor.predict_pathogenicity(variant)
            
        expected_score = 0.3 + expected_adjustment
        assert result['pathogenicity_score'] == expected_score
        
    @pytest.mark.parametrize("consequence,expected_adjustment", [
        ("stop_gained", 0.4),
        ("frameshift_variant", 0.4),
        ("missense_variant", 0.1),
        ("synonymous_variant", -0.2),
        ("intron_variant", 0.0),
        ("", 0.0)
    ])
    def test_predict_pathogenicity_consequence_adjustments(self, consequence, expected_adjustment):
        """Test pathogenicity adjustments for different consequences"""
        variant = {'consequence': consequence}
        
        with patch('random.uniform', return_value=0.5):
            result = self.predictor.predict_pathogenicity(variant)
            
        expected_score = max(0.0, min(1.0, 0.5 + expected_adjustment))
        assert result['pathogenicity_score'] == expected_score 