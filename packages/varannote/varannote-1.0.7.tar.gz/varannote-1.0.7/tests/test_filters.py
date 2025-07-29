#!/usr/bin/env python3
"""
Test suite for Advanced Filtering System

Tests variant filtering functionality including quality filters, clinical filters,
gene filters, and custom filter expressions.
"""

import pytest
from typing import Dict, List, Any

from varannote.utils.filters import (
    VariantFilter, FilterRule, FilterSet, FilterOperator, ClinicalSignificance,
    get_variant_filter, apply_quality_filter, apply_clinical_filter, apply_predefined_filter
)


class TestFilterOperator:
    """Test FilterOperator enum"""
    
    def test_filter_operator_values(self):
        """Test filter operator enum values"""
        assert FilterOperator.EQUALS.value == "=="
        assert FilterOperator.GREATER_THAN.value == ">"
        assert FilterOperator.CONTAINS.value == "contains"
        assert FilterOperator.IN.value == "in"
        assert FilterOperator.IS_NULL.value == "is_null"


class TestFilterRule:
    """Test FilterRule dataclass"""
    
    def test_filter_rule_creation(self):
        """Test filter rule creation"""
        rule = FilterRule(
            field="quality_score",
            operator=FilterOperator.GREATER_THAN,
            value=0.8,
            description="High quality variants"
        )
        
        assert rule.field == "quality_score"
        assert rule.operator == FilterOperator.GREATER_THAN
        assert rule.value == 0.8
        assert rule.description == "High quality variants"
    
    def test_filter_rule_string_operator(self):
        """Test filter rule with string operator"""
        rule = FilterRule(
            field="clinical_significance",
            operator="==",
            value="Pathogenic"
        )
        
        # Should convert string to enum
        assert rule.operator == FilterOperator.EQUALS


class TestFilterSet:
    """Test FilterSet dataclass"""
    
    def test_filter_set_creation(self):
        """Test filter set creation"""
        rules = [
            FilterRule("quality_score", FilterOperator.GREATER_THAN, 0.8),
            FilterRule("population_frequency", FilterOperator.LESS_THAN, 0.01)
        ]
        
        filter_set = FilterSet(
            name="test_filter",
            rules=rules,
            logic="AND",
            description="Test filter set",
            enabled=True
        )
        
        assert filter_set.name == "test_filter"
        assert len(filter_set.rules) == 2
        assert filter_set.logic == "AND"
        assert filter_set.enabled is True
    
    def test_filter_set_defaults(self):
        """Test filter set default values"""
        filter_set = FilterSet(
            name="test",
            rules=[]
        )
        
        assert filter_set.logic == "AND"
        assert filter_set.description is None
        assert filter_set.enabled is True


class TestVariantFilter:
    """Test VariantFilter class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.filter_obj = VariantFilter()
        
        # Sample variants for testing
        self.sample_variants = [
            {
                "variant_id": "var1",
                "quality_score": 0.9,
                "population_frequency": 0.001,
                "clinical_significance": "Pathogenic",
                "gene_symbol": "BRCA1",
                "consequence": "missense_variant",
                "review_status": "reviewed_by_expert_panel"
            },
            {
                "variant_id": "var2",
                "quality_score": 0.5,
                "population_frequency": 0.05,
                "clinical_significance": "Benign",
                "gene_symbol": "TP53",
                "consequence": "synonymous_variant",
                "review_status": "no_assertion"
            },
            {
                "variant_id": "var3",
                "quality_score": 0.8,
                "population_frequency": 0.02,
                "clinical_significance": "Uncertain_significance",
                "gene_symbol": "BRCA2",
                "consequence": "frameshift_variant",
                "review_status": "reviewed_by_expert_panel"
            },
            {
                "variant_id": "var4",
                "quality_score": None,
                "population_frequency": None,
                "clinical_significance": None,
                "gene_symbol": None,
                "consequence": "intergenic_variant",
                "review_status": None
            }
        ]
    
    def test_variant_filter_initialization(self):
        """Test variant filter initialization"""
        assert isinstance(self.filter_obj.operators, dict)
        assert isinstance(self.filter_obj.predefined_filters, dict)
        assert len(self.filter_obj.predefined_filters) > 0
    
    def test_apply_empty_filter(self):
        """Test applying empty filter set"""
        empty_filter = FilterSet(name="empty", rules=[])
        result = self.filter_obj.apply_filter(self.sample_variants, empty_filter)
        
        assert len(result) == len(self.sample_variants)
        assert result == self.sample_variants
    
    def test_apply_disabled_filter(self):
        """Test applying disabled filter set"""
        disabled_filter = FilterSet(
            name="disabled",
            rules=[FilterRule("quality_score", FilterOperator.GREATER_THAN, 0.9)],
            enabled=False
        )
        result = self.filter_obj.apply_filter(self.sample_variants, disabled_filter)
        
        assert len(result) == len(self.sample_variants)
        assert result == self.sample_variants
    
    def test_apply_quality_score_filter(self):
        """Test quality score filtering"""
        quality_filter = FilterSet(
            name="quality",
            rules=[FilterRule("quality_score", FilterOperator.GREATER_EQUAL, 0.8)]
        )
        
        result = self.filter_obj.apply_filter(self.sample_variants, quality_filter)
        
        # Should include var1 (0.9) and var3 (0.8), exclude var2 (0.5) and var4 (None)
        assert len(result) == 2
        variant_ids = [v["variant_id"] for v in result]
        assert "var1" in variant_ids
        assert "var3" in variant_ids
    
    def test_apply_population_frequency_filter(self):
        """Test population frequency filtering"""
        freq_filter = FilterSet(
            name="frequency",
            rules=[FilterRule("population_frequency", FilterOperator.LESS_EQUAL, 0.01)]
        )
        
        result = self.filter_obj.apply_filter(self.sample_variants, freq_filter)
        
        # Should include var1 (0.001), exclude var2 (0.05), var3 (0.02), var4 (None)
        assert len(result) == 1
        assert result[0]["variant_id"] == "var1"
    
    def test_apply_clinical_significance_filter(self):
        """Test clinical significance filtering"""
        clinical_filter = FilterSet(
            name="clinical",
            rules=[FilterRule("clinical_significance", FilterOperator.IN, 
                            ["Pathogenic", "Likely_pathogenic"])]
        )
        
        result = self.filter_obj.apply_filter(self.sample_variants, clinical_filter)
        
        # Should include var1 (Pathogenic), exclude others
        assert len(result) == 1
        assert result[0]["variant_id"] == "var1"
    
    def test_apply_multiple_rules_and_logic(self):
        """Test multiple rules with AND logic"""
        multi_filter = FilterSet(
            name="multi_and",
            rules=[
                FilterRule("quality_score", FilterOperator.GREATER_EQUAL, 0.8),
                FilterRule("clinical_significance", FilterOperator.NOT_EQUALS, "Benign")
            ],
            logic="AND"
        )
        
        result = self.filter_obj.apply_filter(self.sample_variants, multi_filter)
        
        # Should include var1 and var3 (both have quality >= 0.8 and not Benign)
        assert len(result) == 2
        variant_ids = [v["variant_id"] for v in result]
        assert "var1" in variant_ids
        assert "var3" in variant_ids
    
    def test_apply_multiple_rules_or_logic(self):
        """Test multiple rules with OR logic"""
        multi_filter = FilterSet(
            name="multi_or",
            rules=[
                FilterRule("quality_score", FilterOperator.GREATER_THAN, 0.85),
                FilterRule("clinical_significance", FilterOperator.EQUALS, "Benign")
            ],
            logic="OR"
        )
        
        result = self.filter_obj.apply_filter(self.sample_variants, multi_filter)
        
        # Should include var1 (quality > 0.85) and var2 (Benign)
        assert len(result) == 2
        variant_ids = [v["variant_id"] for v in result]
        assert "var1" in variant_ids
        assert "var2" in variant_ids
    
    def test_apply_multiple_filter_sets_and(self):
        """Test applying multiple filter sets with AND logic"""
        filter1 = FilterSet(
            name="filter1",
            rules=[FilterRule("quality_score", FilterOperator.GREATER_EQUAL, 0.8)]
        )
        filter2 = FilterSet(
            name="filter2",
            rules=[FilterRule("population_frequency", FilterOperator.LESS_THAN, 0.1)]
        )
        
        result = self.filter_obj.apply_multiple_filters(
            self.sample_variants, [filter1, filter2], "AND"
        )
        
        # Should include variants that pass both filters
        assert len(result) == 2  # var1 and var3
        variant_ids = [v["variant_id"] for v in result]
        assert "var1" in variant_ids
        assert "var3" in variant_ids
    
    def test_apply_multiple_filter_sets_or(self):
        """Test applying multiple filter sets with OR logic"""
        filter1 = FilterSet(
            name="filter1",
            rules=[FilterRule("quality_score", FilterOperator.GREATER_THAN, 0.85)]
        )
        filter2 = FilterSet(
            name="filter2",
            rules=[FilterRule("clinical_significance", FilterOperator.EQUALS, "Benign")]
        )
        
        result = self.filter_obj.apply_multiple_filters(
            self.sample_variants, [filter1, filter2], "OR"
        )
        
        # Should include variants that pass either filter
        assert len(result) == 2  # var1 and var2
        variant_ids = [v["variant_id"] for v in result]
        assert "var1" in variant_ids
        assert "var2" in variant_ids
    
    def test_contains_operator(self):
        """Test contains operator"""
        contains_filter = FilterSet(
            name="contains",
            rules=[FilterRule("consequence", FilterOperator.CONTAINS, "variant")]
        )
        
        result = self.filter_obj.apply_filter(self.sample_variants, contains_filter)
        
        # Should include variants with "variant" in consequence
        assert len(result) == 4  # All have "variant" in consequence
    
    def test_not_contains_operator(self):
        """Test not contains operator"""
        not_contains_filter = FilterSet(
            name="not_contains",
            rules=[FilterRule("consequence", FilterOperator.NOT_CONTAINS, "intergenic")]
        )
        
        result = self.filter_obj.apply_filter(self.sample_variants, not_contains_filter)
        
        # Should exclude var4 (intergenic_variant)
        assert len(result) == 3
        variant_ids = [v["variant_id"] for v in result]
        assert "var4" not in variant_ids
    
    def test_is_null_operator(self):
        """Test is null operator"""
        null_filter = FilterSet(
            name="null",
            rules=[FilterRule("quality_score", FilterOperator.IS_NULL, None)]
        )
        
        result = self.filter_obj.apply_filter(self.sample_variants, null_filter)
        
        # Should include var4 (quality_score is None)
        assert len(result) == 1
        assert result[0]["variant_id"] == "var4"
    
    def test_is_not_null_operator(self):
        """Test is not null operator"""
        not_null_filter = FilterSet(
            name="not_null",
            rules=[FilterRule("gene_symbol", FilterOperator.IS_NOT_NULL, None)]
        )
        
        result = self.filter_obj.apply_filter(self.sample_variants, not_null_filter)
        
        # Should exclude var4 (gene_symbol is None)
        assert len(result) == 3
        variant_ids = [v["variant_id"] for v in result]
        assert "var4" not in variant_ids
    
    def test_create_quality_filter(self):
        """Test creating quality filter"""
        quality_filter = self.filter_obj.create_quality_filter(
            min_quality=0.7,
            max_population_freq=0.05,
            include_uncertain=False
        )
        
        assert quality_filter.name == "quality_filter"
        assert len(quality_filter.rules) == 3  # quality, frequency, clinical significance
        assert quality_filter.logic == "AND"
    
    def test_create_clinical_filter(self):
        """Test creating clinical filter"""
        clinical_filter = self.filter_obj.create_clinical_filter(
            significance_levels=["Pathogenic", "Likely_pathogenic"],
            exclude_benign=True,
            require_review=True
        )
        
        assert clinical_filter.name == "clinical_filter"
        assert len(clinical_filter.rules) == 3
        assert clinical_filter.logic == "AND"
    
    def test_create_gene_filter(self):
        """Test creating gene filter"""
        gene_filter = self.filter_obj.create_gene_filter(
            gene_list=["BRCA1", "BRCA2", "TP53"],
            exclude_intergenic=True
        )
        
        assert gene_filter.name == "gene_filter"
        assert len(gene_filter.rules) == 2  # gene list and exclude intergenic
        assert gene_filter.logic == "AND"
    
    def test_create_consequence_filter(self):
        """Test creating consequence filter"""
        consequence_filter = self.filter_obj.create_consequence_filter(
            consequence_types=["missense_variant", "frameshift_variant"],
            severity_threshold="moderate"
        )
        
        assert consequence_filter.name == "consequence_filter"
        assert len(consequence_filter.rules) == 2
        assert consequence_filter.logic == "AND"
    
    def test_get_predefined_filter(self):
        """Test getting predefined filter"""
        high_conf_filter = self.filter_obj.get_predefined_filter("high_confidence")
        
        assert high_conf_filter is not None
        assert high_conf_filter.name == "high_confidence"
        assert len(high_conf_filter.rules) > 0
        
        # Test non-existent filter
        non_existent = self.filter_obj.get_predefined_filter("non_existent")
        assert non_existent is None
    
    def test_list_predefined_filters(self):
        """Test listing predefined filters"""
        filter_names = self.filter_obj.list_predefined_filters()
        
        assert isinstance(filter_names, list)
        assert len(filter_names) > 0
        assert "high_confidence" in filter_names
        assert "rare_variants" in filter_names
        assert "coding_variants" in filter_names
    
    def test_get_filter_statistics(self):
        """Test getting filter statistics"""
        quality_filter = FilterSet(
            name="test_stats",
            rules=[FilterRule("quality_score", FilterOperator.GREATER_EQUAL, 0.8)]
        )
        
        stats = self.filter_obj.get_filter_statistics(self.sample_variants, quality_filter)
        
        assert isinstance(stats, dict)
        assert "filter_name" in stats
        assert "total_variants" in stats
        assert "filtered_variants" in stats
        assert "filtered_percentage" in stats
        assert "removed_variants" in stats
        assert "removed_percentage" in stats
        
        assert stats["total_variants"] == 4
        assert stats["filtered_variants"] == 2  # var1 and var3
        assert stats["filtered_percentage"] == 50.0
    
    def test_nested_field_access(self):
        """Test nested field access in variants"""
        nested_variant = {
            "variant_id": "nested_test",
            "annotations": {
                "clinical": {
                    "significance": "Pathogenic"
                }
            }
        }
        
        nested_filter = FilterSet(
            name="nested",
            rules=[FilterRule("annotations.clinical.significance", 
                            FilterOperator.EQUALS, "Pathogenic")]
        )
        
        result = self.filter_obj.apply_filter([nested_variant], nested_filter)
        assert len(result) == 1
    
    def test_error_handling_in_evaluation(self):
        """Test error handling during filter evaluation"""
        # Create filter with invalid field
        invalid_filter = FilterSet(
            name="invalid",
            rules=[FilterRule("non_existent_field", FilterOperator.GREATER_THAN, 0.5)]
        )
        
        # Should not crash, should exclude all variants (stricter filtering)
        result = self.filter_obj.apply_filter(self.sample_variants, invalid_filter)
        assert len(result) == 0


class TestCustomFilterExpressions:
    """Test custom filter expression parsing"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.filter_obj = VariantFilter()
    
    def test_parse_simple_comparison(self):
        """Test parsing simple comparison expressions"""
        expression = "quality_score > 0.8"
        custom_filter = self.filter_obj.create_custom_filter(expression)
        
        assert custom_filter.name == "custom_filter"
        assert len(custom_filter.rules) == 1
        assert custom_filter.rules[0].field == "quality_score"
        assert custom_filter.rules[0].operator == FilterOperator.GREATER_THAN
        assert custom_filter.rules[0].value == 0.8
    
    def test_parse_contains_expression(self):
        """Test parsing contains expressions"""
        expression = "consequence contains missense"
        custom_filter = self.filter_obj.create_custom_filter(expression)
        
        assert len(custom_filter.rules) == 1
        assert custom_filter.rules[0].field == "consequence"
        assert custom_filter.rules[0].operator == FilterOperator.CONTAINS
        assert custom_filter.rules[0].value == "missense"
    
    def test_parse_in_expression(self):
        """Test parsing 'in' expressions"""
        expression = "gene_symbol in [BRCA1, BRCA2, TP53]"
        custom_filter = self.filter_obj.create_custom_filter(expression)
        
        assert len(custom_filter.rules) == 1
        assert custom_filter.rules[0].field == "gene_symbol"
        assert custom_filter.rules[0].operator == FilterOperator.IN
        assert "BRCA1" in custom_filter.rules[0].value
        assert "BRCA2" in custom_filter.rules[0].value
        assert "TP53" in custom_filter.rules[0].value


class TestGlobalFilterFunctions:
    """Test global filter functions"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.sample_variants = [
            {
                "variant_id": "var1",
                "quality_score": 0.9,
                "population_frequency": 0.001,
                "clinical_significance": "Pathogenic"
            },
            {
                "variant_id": "var2",
                "quality_score": 0.5,
                "population_frequency": 0.05,
                "clinical_significance": "Benign"
            }
        ]
    
    def test_get_variant_filter(self):
        """Test get_variant_filter function"""
        filter_obj = get_variant_filter()
        
        assert isinstance(filter_obj, VariantFilter)
        
        # Should return same instance on subsequent calls
        filter_obj2 = get_variant_filter()
        assert filter_obj is filter_obj2
    
    def test_apply_quality_filter_function(self):
        """Test apply_quality_filter function"""
        result = apply_quality_filter(
            self.sample_variants,
            min_quality=0.8,
            max_population_freq=0.01
        )
        
        # Should include var1 (quality 0.9, freq 0.001)
        assert len(result) == 1
        assert result[0]["variant_id"] == "var1"
    
    def test_apply_clinical_filter_function(self):
        """Test apply_clinical_filter function"""
        result = apply_clinical_filter(
            self.sample_variants,
            significance_levels=["Pathogenic", "Likely_pathogenic"]
        )
        
        # Should include var1 (Pathogenic)
        assert len(result) == 1
        assert result[0]["variant_id"] == "var1"
    
    def test_apply_predefined_filter_function(self):
        """Test apply_predefined_filter function"""
        # This will use the high_confidence predefined filter
        # We need to add required fields to our test variants
        enhanced_variants = [
            {
                "variant_id": "var1",
                "quality_score": 0.9,
                "clinical_significance": "Pathogenic",
                "review_status": "reviewed_by_expert_panel"
            },
            {
                "variant_id": "var2",
                "quality_score": 0.5,
                "clinical_significance": "Benign",
                "review_status": "no_assertion"
            }
        ]
        
        result = apply_predefined_filter(enhanced_variants, "high_confidence")
        
        # Should include var1 (meets high confidence criteria)
        assert len(result) == 1
        assert result[0]["variant_id"] == "var1"
    
    def test_apply_predefined_filter_invalid_name(self):
        """Test apply_predefined_filter with invalid filter name"""
        with pytest.raises(ValueError, match="Unknown predefined filter"):
            apply_predefined_filter(self.sample_variants, "non_existent_filter")


class TestFilterEdgeCases:
    """Test edge cases and error conditions"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.filter_obj = VariantFilter()
    
    def test_empty_variant_list(self):
        """Test filtering empty variant list"""
        empty_variants = []
        quality_filter = FilterSet(
            name="test",
            rules=[FilterRule("quality_score", FilterOperator.GREATER_THAN, 0.5)]
        )
        
        result = self.filter_obj.apply_filter(empty_variants, quality_filter)
        assert len(result) == 0
    
    def test_filter_with_none_values(self):
        """Test filtering variants with None values"""
        variants_with_none = [
            {"variant_id": "var1", "quality_score": None, "gene_symbol": None},
            {"variant_id": "var2", "quality_score": 0.8, "gene_symbol": "BRCA1"}
        ]
        
        # Test greater than with None value
        gt_filter = FilterSet(
            name="gt_test",
            rules=[FilterRule("quality_score", FilterOperator.GREATER_THAN, 0.5)]
        )
        
        result = self.filter_obj.apply_filter(variants_with_none, gt_filter)
        assert len(result) == 1  # Only var2 should pass
        assert result[0]["variant_id"] == "var2"
    
    def test_regex_filter_with_invalid_pattern(self):
        """Test regex filter with invalid pattern"""
        variants = [{"variant_id": "var1", "consequence": "missense_variant"}]
        
        # Invalid regex pattern
        regex_filter = FilterSet(
            name="regex_test",
            rules=[FilterRule("consequence", FilterOperator.REGEX, "[invalid")]
        )
        
        # Should not crash, should exclude variant (stricter filtering on error)
        result = self.filter_obj.apply_filter(variants, regex_filter)
        assert len(result) == 0
    
    def test_filter_statistics_empty_variants(self):
        """Test filter statistics with empty variant list"""
        empty_variants = []
        test_filter = FilterSet(
            name="test",
            rules=[FilterRule("quality_score", FilterOperator.GREATER_THAN, 0.5)]
        )
        
        stats = self.filter_obj.get_filter_statistics(empty_variants, test_filter)
        
        assert stats["total_variants"] == 0
        assert stats["filtered_variants"] == 0
        assert stats["filtered_percentage"] == 0
        assert stats["removed_percentage"] == 0


if __name__ == "__main__":
    pytest.main([__file__]) 