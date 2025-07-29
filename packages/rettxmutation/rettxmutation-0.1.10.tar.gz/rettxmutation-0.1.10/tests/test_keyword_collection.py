"""
Tests for KeywordCollection model with surface-level deduplication.

Tests the new KeywordCollection architecture that unifies keywords from
multiple sources with automatic deduplication.
"""

import pytest
from rettxmutation.models.keyword_collection import KeywordCollection, Keyword, EnrichedKeyword


class TestKeywordCollection:
    """Test KeywordCollection functionality."""

    def test_empty_collection(self):
        """Test empty collection initialization."""
        collection = KeywordCollection()
        assert len(collection) == 0
        assert list(collection) == []

    def test_add_single_keyword(self):
        """Test adding a single keyword."""
        collection = KeywordCollection()
        keyword = Keyword(value="MECP2", type="gene_name", source="test", count=1)
        
        result = collection.add(keyword)
        assert result is True  # Should return True for new keyword
        assert len(collection) == 1
        assert list(collection)[0].value == "MECP2"

    def test_surface_level_deduplication(self):
        """Test that exact duplicates are deduplicated."""
        collection = KeywordCollection()
        
        # Add first keyword
        keyword1 = Keyword(value="MECP2", type="gene_name", source="test", count=1, confidence=0.8)
        result1 = collection.add(keyword1)
        assert result1 is True
        
        # Add duplicate (same value and type)
        keyword2 = Keyword(value="MECP2", type="gene_name", source="test", count=2, confidence=0.9)
        result2 = collection.add(keyword2)
        assert result2 is False  # Should return False for duplicate
        
        # Should have only one keyword with merged count and higher confidence
        assert len(collection) == 1
        merged_keyword = list(collection)[0]
        assert merged_keyword.value == "MECP2"
        assert merged_keyword.count == 3  # 1 + 2
        assert merged_keyword.confidence == 0.9  # Higher confidence

    def test_case_insensitive_deduplication(self):
        """Test that deduplication is case-insensitive."""
        collection = KeywordCollection()
        
        keyword1 = Keyword(value="MECP2", type="gene_name", source="test", count=1)
        keyword2 = Keyword(value="mecp2", type="gene_name", source="test", count=1)
        
        collection.add(keyword1)
        result = collection.add(keyword2)
        
        assert result is False  # Should be treated as duplicate
        assert len(collection) == 1
        assert list(collection)[0].count == 2

    def test_different_types_not_deduplicated(self):
        """Test that same value with different types are not deduplicated."""
        collection = KeywordCollection()
        
        keyword1 = Keyword(value="C306", type="Variant", source="test", count=1)
        keyword2 = Keyword(value="C306", type="gene_name", source="test", count=1)
        
        collection.add(keyword1)
        result = collection.add(keyword2)
        
        assert result is True  # Should not be duplicate due to different type
        assert len(collection) == 2

    def test_add_enriched_keyword(self):
        """Test adding enriched keywords."""
        collection = KeywordCollection()
        
        enriched = EnrichedKeyword(
            value="R306C", 
            type="Variant", 
            source="ai_search",
            count=1,
            search_result={"title": "Test Result", "content": "Test content"}
        )
        
        result = collection.add_enriched(enriched)
        assert result is True
        assert len(collection.get_enriched_keywords()) == 1

    def test_enriched_keyword_deduplication(self):
        """Test that enriched keywords also deduplicate."""
        collection = KeywordCollection()
        
        enriched1 = EnrichedKeyword(value="R306C", type="Variant", source="ai_search", count=1,
                                  search_result={"title": "Result 1"})
        enriched2 = EnrichedKeyword(value="R306C", type="Variant", source="ai_search", count=2,
                                  search_result={"title": "Result 2"})
        
        collection.add_enriched(enriched1)
        result = collection.add_enriched(enriched2)
        
        assert result is False  # Should be duplicate
        assert len(collection.get_enriched_keywords()) == 1
        
        # Should use the second search result (latest)
        enriched = collection.get_enriched_keywords()[0]
        assert enriched.search_result["title"] == "Result 2"
        assert enriched.count == 3  # Merged count

    def test_iteration_protocol(self):
        """Test that collection can be iterated."""
        collection = KeywordCollection()
        
        keywords = [
            Keyword(value="MECP2", type="gene_name", source="test", count=1),
            Keyword(value="R306C", type="Variant", source="test", count=1)
        ]
        
        for keyword in keywords:
            collection.add(keyword)
        
        # Test iteration
        iterated_values = [kw.value for kw in collection]
        assert "MECP2" in iterated_values
        assert "R306C" in iterated_values
        assert len(iterated_values) == 2

    def test_indexing_protocol(self):
        """Test that collection supports indexing."""
        collection = KeywordCollection()
        
        keyword = Keyword(value="MECP2", type="gene_name", source="test", count=1)
        collection.add(keyword)
        
        # Test indexing
        first_keyword = collection[0]
        assert first_keyword.value == "MECP2"

    def test_get_keywords_by_type(self):
        """Test filtering keywords by type."""
        collection = KeywordCollection()
        
        collection.add(Keyword(value="MECP2", type="gene_name", source="test", count=1))
        collection.add(Keyword(value="R306C", type="Variant", source="test", count=1))
        collection.add(Keyword(value="c.916C>T", type="Variant", source="test", count=1))
        
        gene_keywords = collection.get_keywords_by_type("gene_name")
        assert len(gene_keywords) == 1
        assert gene_keywords[0].value == "MECP2"

    def test_get_variants(self):
        """Test getting variant-related keywords."""
        collection = KeywordCollection()
        
        collection.add(Keyword(value="MECP2", type="gene_name", source="test", count=1))
        collection.add(Keyword(value="R306C", type="Variant", source="test", count=1))
        collection.add(Keyword(value="c.916C>T", type="Variant", source="test", count=1))
        
        variants = collection.get_variants()
        assert len(variants) == 2
        variant_values = [kw.value for kw in variants]
        assert "R306C" in variant_values
        assert "c.916C>T" in variant_values

    def test_get_genes(self):
        """Test getting gene-related keywords."""
        collection = KeywordCollection()
        
        collection.add(Keyword(value="MECP2", type="gene_name", source="test", count=1))
        collection.add(Keyword(value="FOXG1", type="gene_name", source="test", count=1))
        collection.add(Keyword(value="R306C", type="Variant", source="test", count=1))
        
        genes = collection.get_genes()
        assert len(genes) == 2
        gene_values = [kw.value for kw in genes]
        assert "MECP2" in gene_values
        assert "FOXG1" in gene_values

    def test_get_high_confidence_keywords(self):
        """Test filtering by confidence threshold."""
        collection = KeywordCollection()
        
        collection.add(Keyword(value="High", type="test", source="test", count=1, confidence=0.9))
        collection.add(Keyword(value="Low", type="test", source="test", count=1, confidence=0.3))
        collection.add(Keyword(value="Medium", type="test", source="test", count=1, confidence=0.6))
        
        # Test with default threshold (0.5)
        high_conf = collection.get_high_confidence_keywords()
        assert len(high_conf) == 2
        values = [kw.value for kw in high_conf]
        assert "High" in values
        assert "Medium" in values
        
        # Test with custom threshold
        very_high_conf = collection.get_high_confidence_keywords(threshold=0.8)
        assert len(very_high_conf) == 1
        assert very_high_conf[0].value == "High"

    def test_get_processing_summary(self):
        """Test processing summary statistics."""
        collection = KeywordCollection()
        
        # Add various types of keywords
        collection.add(Keyword(value="MECP2", type="gene_name", source="test", count=1))
        collection.add(Keyword(value="R306C", type="Variant", source="test", count=1))
        collection.add_enriched(EnrichedKeyword(
            value="c.916C>T", type="Variant", source="ai_search", count=1,
            search_result={"title": "Test"}
        ))
        
        summary = collection.get_processing_summary()
        
        assert summary["total_keywords"] == 2  # Only regular keywords count
        assert summary["regular_keywords"] == 2
        assert summary["enriched_keywords"] == 1
        assert summary["keywords_with_search_results"] == 1
        assert summary["unique_variants"] == 1  # Only regular variants count here
        assert summary["unique_genes"] == 1

    def test_pydantic_serialization(self):
        """Test that the collection can be serialized using Pydantic methods."""
        collection = KeywordCollection()
        
        collection.add(Keyword(value="MECP2", type="gene_name", source="test", count=1))
        collection.add(Keyword(value="R306C", type="Variant", source="test", count=1))
        
        # Test model_dump
        data = collection.model_dump()
        assert "keywords_index" in data
        assert "enriched_keywords_index" in data
        assert len(data["keywords_index"]) == 2
        
        # Test model_dump_json
        json_str = collection.model_dump_json()
        assert "keywords_index" in json_str
        assert "MECP2" in json_str
        assert "R306C" in json_str
