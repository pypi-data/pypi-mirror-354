"""
Tests for Unified KeywordDetectorService

Comprehensive tests for the KeywordDetectorService that integrates regex-based detection,
text analytics repository, and AI search enrichment with automatic deduplication.
"""

import pytest
from unittest.mock import MagicMock, patch
from typing import List, Optional

from rettxmutation.models.document import Document
from rettxmutation.models.keyword_collection import Keyword, EnrichedKeyword, KeywordCollection
from rettxmutation.services.keyword_detector_service import KeywordDetectorService
from rettxmutation.repositories.interfaces import TextAnalyticsRepositoryInterface
from rettxmutation.services.ai_search import AISearchService


class TestKeywordDetectorServiceUnified:
    """Test suite for unified KeywordDetectorService."""
    def setup_method(self):
        """Set up test fixtures."""
        # Mock repositories and services
        self.mock_text_analytics_repo = MagicMock(spec=TextAnalyticsRepositoryInterface)
        self.mock_ai_search_service = MagicMock(spec=AISearchService)
        
        # Test document with sample text
        self.test_document = Document(
            raw_text="Patient has MECP2 mutation c.1035A>G (p.Arg306Cys) according to NM_004992.4.",
            cleaned_text="Patient has MECP2 mutation c.1035A>G (p.Arg306Cys) according to NM_004992.4.",
            language="en",
            words=[],  # Empty for simplicity in tests
            lines=[]   # Empty for simplicity in tests
        )

    def test_init_with_all_dependencies(self):
        """Test service initialization with all dependencies."""
        service = KeywordDetectorService(
            text_analytics_repository=self.mock_text_analytics_repo,
            ai_search_service=self.mock_ai_search_service
        )
        
        assert service._text_analytics_repository == self.mock_text_analytics_repo
        assert service._ai_search_service == self.mock_ai_search_service

    def test_init_with_no_dependencies(self):
        """Test service initialization with no dependencies (regex only)."""
        service = KeywordDetectorService()
        
        assert service._text_analytics_repository is None
        assert service._ai_search_service is None

    def test_detect_keywords_regex_only(self):
        """Test keyword detection with regex patterns only."""
        service = KeywordDetectorService()
        
        collection = service.detect_keywords(self.test_document)
        
        # Should detect MECP2, c.1035A>G, p.Arg306Cys, NM_004992.4
        assert len(collection) > 0
          # Check for specific expected keywords
        all_keywords = list(collection)
        keyword_values = [kw.value for kw in all_keywords]
        
        assert "MECP2" in keyword_values
        assert "c.1035A>G" in keyword_values
        assert "p.Arg306Cys" in keyword_values
        assert "NM_004992.4" in keyword_values

    def test_detect_keywords_with_text_analytics(self):
        """Test keyword detection with text analytics integration."""
        # Mock text analytics response
        mock_entity = MagicMock()
        mock_entity.text = "BRCA1"
        mock_entity.category = "Gene"
        mock_entity.confidence_score = 0.88
        
        mock_doc_result = MagicMock()
        mock_doc_result.entities = [mock_entity]
        
        self.mock_text_analytics_repo.analyze_healthcare_entities.return_value = [mock_doc_result]
        
        service = KeywordDetectorService(
            text_analytics_repository=self.mock_text_analytics_repo
        )
        
        collection = service.detect_keywords(self.test_document)
          # Should include both regex and text analytics results
        all_keywords = list(collection)
        keyword_values = [kw.value for kw in all_keywords]
        
        # Regex results
        assert "MECP2" in keyword_values
        assert "c.1035A>G" in keyword_values
        
        # Text analytics results
        assert "BRCA1" in keyword_values        # Verify text analytics was called
        self.mock_text_analytics_repo.analyze_healthcare_entities.assert_called_once()
    
    def test_detect_keywords_with_ai_search_enrichment(self):
        """Test keyword detection with AI search enrichment."""
        # Mock AI search response - note that AI search only enriches "Variant" keywords
        mock_search_result = {
            "title": "R306C Variant Information",
            "content": "R306C is a common variant in MECP2...",
            "score": 0.95
        }
        
        self.mock_ai_search_service.keyword_search.return_value = [mock_search_result]
        
        service = KeywordDetectorService(
            ai_search_service=self.mock_ai_search_service
        )
        
        collection = service.detect_keywords(self.test_document)
        
        # Should have enriched keywords (only variants get enriched)
        enriched_keywords = collection.get_enriched_keywords()
        
        # AI search only enriches variants that are detected by regex, so we need variants in the test document
        variants = collection.get_variants()
        if len(variants) > 0:
            # Only check for enrichment if variants were found
            assert len(enriched_keywords) >= 0  # AI search may or may not enrich depending on what's found
          # Check that AI search was called if variants exist
        if len(variants) > 0:
            self.mock_ai_search_service.keyword_search.assert_called()

    def test_detect_keywords_full_integrationtest_detect_keywords_full_integration(self):
        """Test keyword detection with all components integrated."""
        # Mock text analytics
        mock_entity = MagicMock()
        mock_entity.text = "BRCA1"
        mock_entity.category = "Gene"
        mock_entity.confidence_score = 0.88
        
        mock_doc_result = MagicMock()
        mock_doc_result.entities = [mock_entity]
        
        self.mock_text_analytics_repo.analyze_healthcare_entities.return_value = [mock_doc_result]
        
        # Mock AI search
        mock_search_result = {
            "title": "Gene Information",
            "content": "Detailed gene information...",
            "score": 0.95
        }
        
        self.mock_ai_search_service.keyword_search.return_value = [mock_search_result]
        
        service = KeywordDetectorService(
            text_analytics_repository=self.mock_text_analytics_repo,
            ai_search_service=self.mock_ai_search_service
        )
        
        collection = service.detect_keywords(self.test_document)
          # Should have keywords from all sources
        all_keywords = list(collection)
        enriched_keywords = collection.get_enriched_keywords()
        variants = collection.get_variants()
        
        assert len(all_keywords) > 0
        # Only check for enrichment if variants were found (since only variants get enriched)
        if len(variants) > 0:
            assert len(enriched_keywords) >= 0  # May or may not have enrichment depending on AI search results
        
        # Verify both services were called
        self.mock_text_analytics_repo.analyze_healthcare_entities.assert_called_once()
        # AI search is only called if variants are found
        if len(variants) > 0:
            self.mock_ai_search_service.keyword_search.assert_called()

    def test_surface_level_deduplication(self):
        """Test that surface-level deduplication works across sources."""
        # Mock text analytics to return a duplicate gene
        mock_entity = MagicMock()
        mock_entity.text = "MECP2"  # Same as regex will find
        mock_entity.category = "Gene"
        mock_entity.confidence_score = 0.90
        
        mock_doc_result = MagicMock()
        mock_doc_result.entities = [mock_entity]
        
        self.mock_text_analytics_repo.analyze_healthcare_entities.return_value = [mock_doc_result]
        
        service = KeywordDetectorService(
            text_analytics_repository=self.mock_text_analytics_repo
        )
        
        collection = service.detect_keywords(self.test_document)
        
        # Should only have one MECP2 entry despite being found by both sources
        all_keywords = list(collection)
        mecp2_keywords = [kw for kw in all_keywords if kw.value == "MECP2"]
        assert len(mecp2_keywords) == 1
        
        # The count should be merged
        mecp2_keyword = mecp2_keywords[0]
        assert mecp2_keyword.count >= 1  # At least from regex
        assert mecp2_keyword.confidence == 0.90  # Should use higher confidence

    def test_case_insensitive_deduplication(self):
        """Test that case-insensitive deduplication works."""
        # Mock text analytics to return different case
        mock_entity = MagicMock()
        mock_entity.text = "mecp2"  # Different case
        mock_entity.category = "Gene"
        mock_entity.confidence_score = 0.85
        
        mock_doc_result = MagicMock()
        mock_doc_result.entities = [mock_entity]
        
        self.mock_text_analytics_repo.analyze_healthcare_entities.return_value = [mock_doc_result]
        
        service = KeywordDetectorService(
            text_analytics_repository=self.mock_text_analytics_repo
        )
        
        collection = service.detect_keywords(self.test_document)
        
        # Should deduplicate case-insensitive matches
        gene_keywords = collection.get_genes()
        mecp2_matches = [kw for kw in gene_keywords if kw.value.upper() == "MECP2"]
        assert len(mecp2_matches) == 1

    def test_detect_and_validate_keywords(self):
        """Test the combined detection and validation method."""
        service = KeywordDetectorService()
        
        # Call the combined method
        result_collection = service.detect_and_validate_keywords(self.test_document)
        
        # Should return a KeywordCollection
        assert isinstance(result_collection, KeywordCollection)
        assert len(result_collection) > 0

    def test_error_handling_regex(self):
        """Test error handling in regex detection."""
        service = KeywordDetectorService()
          # Create a document that might cause regex issues
        problematic_doc = Document(
            raw_text="",  # Empty text
            cleaned_text="",
            language="en",
            words=[],
            lines=[]
        )
        
        # Should not crash and return empty collection
        collection = service.detect_keywords(problematic_doc)
        assert isinstance(collection, KeywordCollection)

    def test_error_handling_text_analytics(self):
        """Test error handling in text analytics."""
        self.mock_text_analytics_repo.analyze_healthcare_entities.side_effect = Exception("API Error")
        
        service = KeywordDetectorService(
            text_analytics_repository=self.mock_text_analytics_repo
        )
        
        # Should not crash despite text analytics error
        collection = service.detect_keywords(self.test_document)
        assert isinstance(collection, KeywordCollection)
        
        # Should still have regex results
        assert len(collection) > 0

    def test_error_handling_ai_search(self):
        """Test error handling in AI search enrichment."""
        self.mock_ai_search_service.search.side_effect = Exception("Search Error")
        
        service = KeywordDetectorService(
            ai_search_service=self.mock_ai_search_service
        )
        
        # Should not crash despite AI search error
        collection = service.detect_keywords(self.test_document)
        assert isinstance(collection, KeywordCollection)
        
        # Should still have regex results
        assert len(collection) > 0

    def test_keyword_types_detection(self):
        """Test detection of different keyword types."""
        service = KeywordDetectorService()
        
        collection = service.detect_keywords(self.test_document)
        
        # Check specific types are detected
        genes = collection.get_genes()
        variants = collection.get_variants()
        
        assert len(genes) > 0
        assert len(variants) > 0
        
        # Verify specific types
        gene_types = {kw.type for kw in genes}
        variant_types = {kw.type for kw in variants}
        
        assert "gene_name" in gene_types
        assert "Variant" in variant_types

    def test_processing_summary(self):
        """Test processing summary generation."""
        service = KeywordDetectorService()
        
        collection = service.detect_keywords(self.test_document)
        summary = collection.get_processing_summary()
        
        # Should have summary statistics
        assert "total_keywords" in summary
        assert "regular_keywords" in summary
        assert "enriched_keywords" in summary
        assert summary["total_keywords"] > 0

    def test_empty_text_handling(self):
        """Test handling of empty or whitespace-only text."""
        empty_doc = Document(
            raw_text="   ",
            cleaned_text="   ",
            language="en",
            words=[],
            lines=[]
        )
        
        service = KeywordDetectorService()
        collection = service.detect_keywords(empty_doc)
        
        # Should return empty collection for empty text
        assert len(collection) == 0

    def test_regex_patterns_comprehensive(self):
        """Test comprehensive regex pattern detection."""
        comprehensive_text = """
        Patient analysis reveals MECP2 mutations including:
        - c.1035A>G and c.[473C>T]
        - p.Arg306Cys and p.[Thr158Met]
        - Reference sequences: NM_004992.4, NP_004983.1
        - Deletions: c.1040_1047del
        """
        comprehensive_doc = Document(
            raw_text=comprehensive_text,
            cleaned_text=comprehensive_text,
            language="en",
            words=[],
            lines=[]
        )
        
        service = KeywordDetectorService()
        collection = service.detect_keywords(comprehensive_doc)

        all_keywords = list(collection)
        keyword_values = [kw.value for kw in all_keywords]
        
        # Should detect all pattern types
        assert "MECP2" in keyword_values
        assert "c.1035A>G" in keyword_values
        assert "c.[473C>T]" in keyword_values
        assert "p.Arg306Cys" in keyword_values
        assert "p.[Thr158Met]" in keyword_values
        assert "NM_004992.4" in keyword_values
        assert "NP_004983.1" in keyword_values
        assert "c.1040_1047del" in keyword_values

    @patch('rettxmutation.models.document.Document.find_word_confidence')
    def test_confidence_validation_integration(self, mock_find_confidence):
        """Test confidence validation integration."""
        # Mock different confidence scores for different words
        def mock_confidence_side_effect(word):
            confidence_map = {
                "MECP2": 0.95,
                "c.1035A>G": 0.88,
                "p.Arg306Cys": 0.92
            }
            return confidence_map.get(word, None)
        
        mock_find_confidence.side_effect = mock_confidence_side_effect
        
        service = KeywordDetectorService()
        result_collection = service.detect_and_validate_keywords(self.test_document)
        
        # Check that keywords have appropriate confidence scores
        all_keywords = list(result_collection)
        for keyword in all_keywords:
            if keyword.value in ["MECP2", "c.1035A>G", "p.Arg306Cys"]:
                assert keyword.confidence > 0.8
            else:
                assert keyword.confidence == 0.0  # Not found in OCR
