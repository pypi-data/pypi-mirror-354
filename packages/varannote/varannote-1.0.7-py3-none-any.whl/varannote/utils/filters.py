#!/usr/bin/env python3
"""
Advanced Filtering System for VarAnnote v1.0.0

Provides comprehensive variant filtering capabilities including:
- Quality score filtering
- Population frequency thresholds
- Clinical significance filters
- Gene-based filtering
- Consequence type filtering
- Custom filter expressions
"""

import re
import operator
from typing import Dict, List, Any, Optional, Union, Callable
from dataclasses import dataclass
from enum import Enum
import logging

from .logger import get_logger


class FilterOperator(Enum):
    """Filter operators"""
    EQUALS = "=="
    NOT_EQUALS = "!="
    GREATER_THAN = ">"
    GREATER_EQUAL = ">="
    LESS_THAN = "<"
    LESS_EQUAL = "<="
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
    IN = "in"
    NOT_IN = "not_in"
    REGEX = "regex"
    IS_NULL = "is_null"
    IS_NOT_NULL = "is_not_null"


class ClinicalSignificance(Enum):
    """Clinical significance categories"""
    PATHOGENIC = "Pathogenic"
    LIKELY_PATHOGENIC = "Likely_pathogenic"
    UNCERTAIN_SIGNIFICANCE = "Uncertain_significance"
    LIKELY_BENIGN = "Likely_benign"
    BENIGN = "Benign"
    CONFLICTING = "Conflicting"
    NOT_PROVIDED = "Not_provided"


@dataclass
class FilterRule:
    """Individual filter rule"""
    field: str
    operator: FilterOperator
    value: Any
    description: Optional[str] = None
    
    def __post_init__(self):
        if isinstance(self.operator, str):
            self.operator = FilterOperator(self.operator)


@dataclass
class FilterSet:
    """Collection of filter rules with logic"""
    name: str
    rules: List[FilterRule]
    logic: str = "AND"  # AND, OR
    description: Optional[str] = None
    enabled: bool = True


class VariantFilter:
    """
    Advanced variant filtering system
    
    Features:
    - Multiple filter criteria
    - Logical combinations (AND/OR)
    - Custom filter expressions
    - Predefined filter sets
    - Performance optimization
    """
    
    def __init__(self):
        """Initialize variant filter"""
        self.logger = get_logger("variant_filter")
        
        # Operator mapping
        self.operators = {
            FilterOperator.EQUALS: operator.eq,
            FilterOperator.NOT_EQUALS: operator.ne,
            FilterOperator.GREATER_THAN: operator.gt,
            FilterOperator.GREATER_EQUAL: operator.ge,
            FilterOperator.LESS_THAN: operator.lt,
            FilterOperator.LESS_EQUAL: operator.le,
            FilterOperator.CONTAINS: self._contains,
            FilterOperator.NOT_CONTAINS: self._not_contains,
            FilterOperator.IN: self._in,
            FilterOperator.NOT_IN: self._not_in,
            FilterOperator.REGEX: self._regex_match,
            FilterOperator.IS_NULL: self._is_null,
            FilterOperator.IS_NOT_NULL: self._is_not_null
        }
        
        # Predefined filter sets
        self.predefined_filters = self._create_predefined_filters()
        
        self.logger.info("Variant filter initialized")
    
    def apply_filter(self, variants: List[Dict[str, Any]], 
                    filter_set: FilterSet) -> List[Dict[str, Any]]:
        """
        Apply filter set to variants
        
        Args:
            variants: List of variant dictionaries
            filter_set: Filter set to apply
            
        Returns:
            Filtered list of variants
        """
        if not filter_set.enabled or not filter_set.rules:
            return variants
        
        filtered_variants = []
        
        for variant in variants:
            if self._evaluate_filter_set(variant, filter_set):
                filtered_variants.append(variant)
        
        self.logger.info(f"Filtered {len(variants)} variants to {len(filtered_variants)} "
                        f"using filter set '{filter_set.name}'")
        
        return filtered_variants
    
    def apply_multiple_filters(self, variants: List[Dict[str, Any]], 
                             filter_sets: List[FilterSet],
                             combine_logic: str = "AND") -> List[Dict[str, Any]]:
        """
        Apply multiple filter sets
        
        Args:
            variants: List of variant dictionaries
            filter_sets: List of filter sets to apply
            combine_logic: How to combine filter sets (AND/OR)
            
        Returns:
            Filtered list of variants
        """
        if not filter_sets:
            return variants
        
        # Filter enabled filter sets
        enabled_filters = [f for f in filter_sets if f.enabled]
        if not enabled_filters:
            return variants
        
        filtered_variants = []
        
        for variant in variants:
            if combine_logic.upper() == "AND":
                # All filter sets must pass
                if all(self._evaluate_filter_set(variant, fs) for fs in enabled_filters):
                    filtered_variants.append(variant)
            else:  # OR
                # At least one filter set must pass
                if any(self._evaluate_filter_set(variant, fs) for fs in enabled_filters):
                    filtered_variants.append(variant)
        
        self.logger.info(f"Applied {len(enabled_filters)} filter sets with {combine_logic} logic: "
                        f"{len(variants)} -> {len(filtered_variants)} variants")
        
        return filtered_variants
    
    def create_quality_filter(self, min_quality: float = 0.0,
                            max_population_freq: float = 1.0,
                            include_uncertain: bool = True) -> FilterSet:
        """Create quality-based filter set"""
        rules = []
        
        # Quality score filter
        if min_quality > 0:
            rules.append(FilterRule(
                field="quality_score",
                operator=FilterOperator.GREATER_EQUAL,
                value=min_quality,
                description=f"Quality score >= {min_quality}"
            ))
        
        # Population frequency filter
        if max_population_freq < 1.0:
            rules.append(FilterRule(
                field="population_frequency",
                operator=FilterOperator.LESS_EQUAL,
                value=max_population_freq,
                description=f"Population frequency <= {max_population_freq}"
            ))
        
        # Clinical significance filter
        if not include_uncertain:
            rules.append(FilterRule(
                field="clinical_significance",
                operator=FilterOperator.NOT_IN,
                value=["Uncertain_significance", "Conflicting", "Not_provided"],
                description="Exclude uncertain clinical significance"
            ))
        
        return FilterSet(
            name="quality_filter",
            rules=rules,
            logic="AND",
            description="Quality-based variant filtering"
        )
    
    def create_clinical_filter(self, 
                             significance_levels: List[str] = None,
                             exclude_benign: bool = False,
                             require_review: bool = False) -> FilterSet:
        """Create clinical significance filter set"""
        rules = []
        
        if significance_levels:
            rules.append(FilterRule(
                field="clinical_significance",
                operator=FilterOperator.IN,
                value=significance_levels,
                description=f"Clinical significance in {significance_levels}"
            ))
        
        if exclude_benign:
            rules.append(FilterRule(
                field="clinical_significance",
                operator=FilterOperator.NOT_IN,
                value=["Benign", "Likely_benign"],
                description="Exclude benign variants"
            ))
        
        if require_review:
            rules.append(FilterRule(
                field="review_status",
                operator=FilterOperator.NOT_EQUALS,
                value="no_assertion",
                description="Require reviewed variants"
            ))
        
        return FilterSet(
            name="clinical_filter",
            rules=rules,
            logic="AND",
            description="Clinical significance filtering"
        )
    
    def create_gene_filter(self, 
                          gene_list: List[str] = None,
                          gene_types: List[str] = None,
                          exclude_intergenic: bool = True) -> FilterSet:
        """Create gene-based filter set"""
        rules = []
        
        if gene_list:
            rules.append(FilterRule(
                field="gene_symbol",
                operator=FilterOperator.IN,
                value=gene_list,
                description=f"Genes in {gene_list}"
            ))
        
        if gene_types:
            rules.append(FilterRule(
                field="gene_type",
                operator=FilterOperator.IN,
                value=gene_types,
                description=f"Gene types in {gene_types}"
            ))
        
        if exclude_intergenic:
            rules.append(FilterRule(
                field="consequence",
                operator=FilterOperator.NOT_CONTAINS,
                value="intergenic",
                description="Exclude intergenic variants"
            ))
        
        return FilterSet(
            name="gene_filter",
            rules=rules,
            logic="AND",
            description="Gene-based filtering"
        )
    
    def create_consequence_filter(self, 
                                consequence_types: List[str] = None,
                                severity_threshold: str = "moderate") -> FilterSet:
        """Create consequence-based filter set"""
        rules = []
        
        # Severity mapping
        severity_map = {
            "high": ["stop_gained", "frameshift_variant", "start_lost", "stop_lost"],
            "moderate": ["missense_variant", "inframe_deletion", "inframe_insertion"],
            "low": ["synonymous_variant", "stop_retained_variant"],
            "modifier": ["intron_variant", "upstream_variant", "downstream_variant"]
        }
        
        if consequence_types:
            rules.append(FilterRule(
                field="consequence",
                operator=FilterOperator.IN,
                value=consequence_types,
                description=f"Consequences in {consequence_types}"
            ))
        
        if severity_threshold in severity_map:
            # Include consequences at or above threshold
            allowed_consequences = []
            severity_order = ["high", "moderate", "low", "modifier"]
            threshold_index = severity_order.index(severity_threshold)
            
            for i in range(threshold_index + 1):
                allowed_consequences.extend(severity_map[severity_order[i]])
            
            rules.append(FilterRule(
                field="consequence",
                operator=FilterOperator.IN,
                value=allowed_consequences,
                description=f"Consequence severity >= {severity_threshold}"
            ))
        
        return FilterSet(
            name="consequence_filter",
            rules=rules,
            logic="AND",
            description="Consequence-based filtering"
        )
    
    def create_custom_filter(self, expression: str) -> FilterSet:
        """
        Create custom filter from expression
        
        Args:
            expression: Filter expression (e.g., "quality_score > 0.8 AND population_frequency < 0.01")
            
        Returns:
            FilterSet object
        """
        # Parse expression into rules
        rules = self._parse_filter_expression(expression)
        
        return FilterSet(
            name="custom_filter",
            rules=rules,
            logic="AND",
            description=f"Custom filter: {expression}"
        )
    
    def get_predefined_filter(self, name: str) -> Optional[FilterSet]:
        """Get predefined filter set by name"""
        return self.predefined_filters.get(name)
    
    def list_predefined_filters(self) -> List[str]:
        """List available predefined filter names"""
        return list(self.predefined_filters.keys())
    
    def get_filter_statistics(self, variants: List[Dict[str, Any]], 
                            filter_set: FilterSet) -> Dict[str, Any]:
        """Get statistics about filter application"""
        total_variants = len(variants)
        filtered_variants = self.apply_filter(variants, filter_set)
        filtered_count = len(filtered_variants)
        
        return {
            "filter_name": filter_set.name,
            "total_variants": total_variants,
            "filtered_variants": filtered_count,
            "filtered_percentage": (filtered_count / total_variants * 100) if total_variants > 0 else 0,
            "removed_variants": total_variants - filtered_count,
            "removed_percentage": ((total_variants - filtered_count) / total_variants * 100) if total_variants > 0 else 0
        }
    
    def _evaluate_filter_set(self, variant: Dict[str, Any], filter_set: FilterSet) -> bool:
        """Evaluate filter set against variant"""
        if not filter_set.rules:
            return True
        
        results = []
        for rule in filter_set.rules:
            result = self._evaluate_rule(variant, rule)
            results.append(result)
        
        # Apply logic
        if filter_set.logic.upper() == "AND":
            return all(results)
        else:  # OR
            return any(results)
    
    def _evaluate_rule(self, variant: Dict[str, Any], rule: FilterRule) -> bool:
        """Evaluate single filter rule"""
        try:
            # Get field value
            field_value = self._get_field_value(variant, rule.field)
            
            # Handle None values for comparison operators
            if field_value is None and rule.operator in [
                FilterOperator.GREATER_THAN, FilterOperator.GREATER_EQUAL,
                FilterOperator.LESS_THAN, FilterOperator.LESS_EQUAL
            ]:
                return False  # None values fail numeric comparisons
            
            # Apply operator
            operator_func = self.operators.get(rule.operator)
            if not operator_func:
                self.logger.warning(f"Unknown operator: {rule.operator}")
                return True
            
            return operator_func(field_value, rule.value)
            
        except Exception as e:
            self.logger.warning(f"Error evaluating rule {rule.field} {rule.operator} {rule.value}: {e}")
            return False  # Default to exclude variant on error for stricter filtering
    
    def _get_field_value(self, variant: Dict[str, Any], field: str) -> Any:
        """Get field value from variant, supporting nested fields"""
        if '.' in field:
            # Nested field access
            parts = field.split('.')
            value = variant
            for part in parts:
                if isinstance(value, dict) and part in value:
                    value = value[part]
                else:
                    return None
            return value
        else:
            return variant.get(field)
    
    def _contains(self, field_value: Any, filter_value: Any) -> bool:
        """Contains operator"""
        if field_value is None:
            return False
        return str(filter_value).lower() in str(field_value).lower()
    
    def _not_contains(self, field_value: Any, filter_value: Any) -> bool:
        """Not contains operator"""
        return not self._contains(field_value, filter_value)
    
    def _in(self, field_value: Any, filter_value: List[Any]) -> bool:
        """In operator"""
        if field_value is None:
            return False
        return field_value in filter_value
    
    def _not_in(self, field_value: Any, filter_value: List[Any]) -> bool:
        """Not in operator"""
        return not self._in(field_value, filter_value)
    
    def _regex_match(self, field_value: Any, filter_value: str) -> bool:
        """Regex match operator"""
        if field_value is None:
            return False
        try:
            return bool(re.search(filter_value, str(field_value)))
        except re.error as e:
            self.logger.warning(f"Invalid regex pattern '{filter_value}': {e}")
            return False
    
    def _is_null(self, field_value: Any, filter_value: Any) -> bool:
        """Is null operator"""
        return field_value is None or field_value == ""
    
    def _is_not_null(self, field_value: Any, filter_value: Any) -> bool:
        """Is not null operator"""
        return not self._is_null(field_value, filter_value)
    
    def _parse_filter_expression(self, expression: str) -> List[FilterRule]:
        """Parse filter expression into rules (simplified implementation)"""
        # This is a simplified parser - in production, you'd want a more robust one
        rules = []
        
        # Split by AND/OR (simplified)
        parts = re.split(r'\s+(AND|OR)\s+', expression, flags=re.IGNORECASE)
        
        for part in parts:
            if part.upper() in ['AND', 'OR']:
                continue
            
            # Parse individual condition
            rule = self._parse_condition(part.strip())
            if rule:
                rules.append(rule)
        
        return rules
    
    def _parse_condition(self, condition: str) -> Optional[FilterRule]:
        """Parse individual condition into FilterRule"""
        # Match patterns like "field operator value"
        patterns = [
            (r'(\w+)\s*(>=|<=|>|<|==|!=)\s*([^\s]+)', 'comparison'),
            (r'(\w+)\s+contains\s+(.+)', 'contains'),
            (r'(\w+)\s+in\s+\[([^\]]+)\]', 'in')
        ]
        
        for pattern, op_type in patterns:
            match = re.match(pattern, condition, re.IGNORECASE)
            if match:
                field = match.group(1)
                
                if op_type == 'comparison':
                    operator_str = match.group(2)
                    value_str = match.group(3)
                    
                    # Convert value
                    try:
                        value = float(value_str)
                    except ValueError:
                        value = value_str.strip('"\'')
                    
                    return FilterRule(
                        field=field,
                        operator=FilterOperator(operator_str),
                        value=value
                    )
                
                elif op_type == 'contains':
                    value = match.group(2).strip('"\'')
                    return FilterRule(
                        field=field,
                        operator=FilterOperator.CONTAINS,
                        value=value
                    )
                
                elif op_type == 'in':
                    values_str = match.group(2)
                    values = [v.strip().strip('"\'') for v in values_str.split(',')]
                    return FilterRule(
                        field=field,
                        operator=FilterOperator.IN,
                        value=values
                    )
        
        return None
    
    def _create_predefined_filters(self) -> Dict[str, FilterSet]:
        """Create predefined filter sets"""
        filters = {}
        
        # High confidence filter
        filters["high_confidence"] = FilterSet(
            name="high_confidence",
            rules=[
                FilterRule("quality_score", FilterOperator.GREATER_EQUAL, 0.8),
                FilterRule("clinical_significance", FilterOperator.IN, 
                          ["Pathogenic", "Likely_pathogenic"]),
                FilterRule("review_status", FilterOperator.NOT_EQUALS, "no_assertion")
            ],
            description="High confidence pathogenic variants"
        )
        
        # Rare variants filter
        filters["rare_variants"] = FilterSet(
            name="rare_variants",
            rules=[
                FilterRule("population_frequency", FilterOperator.LESS_EQUAL, 0.01),
                FilterRule("clinical_significance", FilterOperator.NOT_IN, 
                          ["Benign", "Likely_benign"])
            ],
            description="Rare variants (MAF <= 1%)"
        )
        
        # Coding variants filter
        filters["coding_variants"] = FilterSet(
            name="coding_variants",
            rules=[
                FilterRule("consequence", FilterOperator.IN, 
                          ["missense_variant", "stop_gained", "frameshift_variant", 
                           "start_lost", "stop_lost", "inframe_deletion", "inframe_insertion"]),
                FilterRule("gene_symbol", FilterOperator.IS_NOT_NULL, None)
            ],
            description="Protein-coding variants"
        )
        
        # Pharmacogenomics filter
        filters["pharmacogenomics"] = FilterSet(
            name="pharmacogenomics",
            rules=[
                FilterRule("drug_interactions", FilterOperator.IS_NOT_NULL, None),
                FilterRule("pharmgkb_level", FilterOperator.IN, ["1A", "1B", "2A", "2B"])
            ],
            description="Pharmacogenomically relevant variants"
        )
        
        return filters


# Global filter instance
_variant_filter: Optional[VariantFilter] = None


def get_variant_filter() -> VariantFilter:
    """Get global variant filter instance"""
    global _variant_filter
    if _variant_filter is None:
        _variant_filter = VariantFilter()
    return _variant_filter


def apply_quality_filter(variants: List[Dict[str, Any]], 
                        min_quality: float = 0.0,
                        max_population_freq: float = 1.0) -> List[Dict[str, Any]]:
    """Apply quality filter to variants"""
    filter_obj = get_variant_filter()
    quality_filter = filter_obj.create_quality_filter(min_quality, max_population_freq)
    return filter_obj.apply_filter(variants, quality_filter)


def apply_clinical_filter(variants: List[Dict[str, Any]], 
                         significance_levels: List[str] = None) -> List[Dict[str, Any]]:
    """Apply clinical significance filter to variants"""
    filter_obj = get_variant_filter()
    clinical_filter = filter_obj.create_clinical_filter(significance_levels)
    return filter_obj.apply_filter(variants, clinical_filter)


def apply_predefined_filter(variants: List[Dict[str, Any]], 
                          filter_name: str) -> List[Dict[str, Any]]:
    """Apply predefined filter to variants"""
    filter_obj = get_variant_filter()
    predefined_filter = filter_obj.get_predefined_filter(filter_name)
    if predefined_filter:
        return filter_obj.apply_filter(variants, predefined_filter)
    else:
        raise ValueError(f"Unknown predefined filter: {filter_name}") 