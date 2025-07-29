"""
Unified Keyword Detector Service

Service responsible for detecting gene-related keywords and variant patterns
using multiple methods: regex, text analytics, and AI search enrichment.
Follows the 3-layer architecture with automatic deduplication.
"""

import re
import logging
from typing import List, Optional
from collections import Counter

from rettxmutation.models.document import Document
from rettxmutation.models.keyword_collection import Keyword, EnrichedKeyword, KeywordCollection
from rettxmutation.repositories.interfaces import TextAnalyticsRepositoryInterface
from rettxmutation.services.ai_search import AISearchService

logger = logging.getLogger(__name__)


class KeywordDetectorService:
    """
    Unified service for detecting keywords from multiple sources with automatic deduplication.
    
    This service orchestrates keyword detection through:
    1. Regex-based pattern matching
    2. Text analytics via repository
    3. AI search enrichment via service
    
    All results are unified in a KeywordCollection with surface-level deduplication.
    """

    def __init__(self, 
                 text_analytics_repository: Optional[TextAnalyticsRepositoryInterface] = None,
                 ai_search_service: Optional[AISearchService] = None):
        """Initialize the unified keyword detector service."""
        self._text_analytics_repository = text_analytics_repository
        self._ai_search_service = ai_search_service
        logger.debug("KeywordDetectorService initialized with unified detection capabilities")

    def detect_keywords(self, document: Document) -> KeywordCollection:
        """
        Detect keywords from all sources and return a unified collection.
        
        Args:
            document: Document to analyze for keywords
            
        Returns:
            KeywordCollection: Unified collection with automatic deduplication
        """
        try:
            logger.debug("Starting unified keyword detection")
            collection = KeywordCollection()

            # 1. Regex-based detection
            regex_keywords = self._detect_regex_keywords(document.cleaned_text)
            for keyword in regex_keywords:
                collection.add(keyword)
            logger.debug(f"Added {len(regex_keywords)} regex keywords to collection")

            # 2. Text analytics detection (via repository)
            if self._text_analytics_repository:
                analytics_keywords = self._detect_text_analytics_keywords(document.cleaned_text)
                for keyword in analytics_keywords:
                    collection.add(keyword)
                logger.debug(f"Added text analytics keywords to collection")

            # 3. AI search enrichment (via service)
            if self._ai_search_service and len(collection) > 0:
                enriched_keywords = self._enrich_with_ai_search(collection)
                for enriched_keyword in enriched_keywords:
                    collection.add_enriched(enriched_keyword)
                logger.debug(f"Added AI search enriched keywords to collection")

            logger.debug(f"Keyword detection completed. Total unique keywords: {len(collection)}")
            return collection

        except Exception as e:
            logger.error(f"Unified keyword detection failed: {e}")
            return KeywordCollection()  # Return empty collection on error

    def detect_and_validate_keywords(self, document: Document) -> KeywordCollection:
        """
        Detect keywords using unified approach and validate their OCR confidence scores.
        
        Args:
            document: Document to process for keyword detection and validation
              Returns:
            KeywordCollection: Unified collection with validated confidence scores
        """
        try:
            # Detect keywords using unified approach
            keyword_collection = self.detect_keywords(document)
            
            # Extract all keywords for validation
            all_keywords = list(keyword_collection)
            
            # Validate OCR confidence for detected keywords
            self._validate_keyword_confidence(document, all_keywords)
            
            logger.debug(f"Unified keyword detection and validation completed for document")
            return keyword_collection

        except Exception as e:
            logger.error(f"Unified keyword detection and validation failed: {e}")
            return KeywordCollection()  # Return empty collection on error

    def _detect_regex_keywords(self, text: str) -> List[Keyword]:
        """
        Detect gene-related keywords and variant patterns using regex.
        
        Args:
            text: Cleaned text to analyze for keywords
            
        Returns:
            List[Keyword]: List of detected keywords with their types and counts
        """
        try:
            detected_keywords = []

            # Detect various types of keywords using existing patterns
            detected_keywords.extend(self._detect_gene_names(text))
            detected_keywords.extend(self._detect_c_variants(text))
            detected_keywords.extend(self._detect_p_variants(text))
            detected_keywords.extend(self._detect_reference_sequences(text))

            logger.debug(f"Regex detection found {len(detected_keywords)} keywords")
            return detected_keywords

        except Exception as e:
            logger.warning(f"Regex keyword detection failed: {e}")
            return []

    def _detect_text_analytics_keywords(self, text: str) -> List[Keyword]:
        """
        Detect keywords using Azure Text Analytics for Health.
        
        Args:
            text: Text to analyze
            
        Returns:
            List[Keyword]: Keywords detected by text analytics
        """
        try:
            if not self._text_analytics_repository:
                logger.debug("Text analytics repository not available, skipping")
                return []

            # Call repository to analyze healthcare entities
            analytics_result = self._text_analytics_repository.analyze_healthcare_entities(text)
            
            # Convert analytics results to Keywords
            keywords = self._convert_analytics_to_keywords(analytics_result)
            
            logger.debug(f"Text analytics detection found {len(keywords)} keywords")
            return keywords

        except Exception as e:
            logger.warning(f"Text analytics keyword detection failed: {e}")
            return []

    def _enrich_with_ai_search(self, collection: KeywordCollection) -> List[EnrichedKeyword]:
        """
        Enrich variant keywords with AI keyword search results.
        
        Args:
            collection: Current keyword collection
            
        Returns:
            List[EnrichedKeyword]: Variant keywords enriched with keyword search context
        """
        try:
            if not self._ai_search_service:
                logger.debug("AI search service not available, skipping enrichment")
                return []

            enriched_keywords = []
            
            # Get only "Variant" keywords for AI search enrichment
            variant_keywords = [kw for kw in collection.keywords_index.values() if kw.type == "Variant"]
            
            for keyword in variant_keywords:
                # Perform keyword search for each variant
                search_results = self._ai_search_service.keyword_search(keyword.value)
                
                if search_results:
                    # Take the first/best result
                    best_result = search_results[0] if search_results else None
                    enriched = EnrichedKeyword(
                        value=keyword.value,
                        type=keyword.type,
                        source="ai_search",
                        count=keyword.count,
                        confidence=keyword.confidence,
                        search_result=best_result
                    )
                    enriched_keywords.append(enriched)
            
            logger.debug(f"AI search enrichment processed {len(variant_keywords)} variants, found {len(enriched_keywords)} enriched keywords")
            return enriched_keywords

        except Exception as e:
            logger.warning(f"AI search enrichment failed: {e}")
            return []

    def _convert_analytics_to_keywords(self, analytics_result) -> List[Keyword]:
        """
        Convert Azure Text Analytics results to Keyword objects.
        
        Args:
            analytics_result: Results from text analytics
            
        Returns:
            List[Keyword]: Converted keywords
        """
        keywords = []
        
        try:            # Process the analytics results
            # Note: This is a simplified conversion - adjust based on actual analytics result structure
            for doc_result in analytics_result:
                if hasattr(doc_result, 'entities'):
                    for entity in doc_result.entities:
                        # Map categories to our keyword types
                        keyword_type = None
                        if entity.category == "Gene":
                            keyword_type = "gene_name"
                        elif entity.category == "Variant":
                            keyword_type = "Variant"
                        elif entity.category in ["Medication", "Drug", "Treatment"]:
                            keyword_type = "treatment"
                        
                        # Only store relevant keywords 
                        if keyword_type:
                            keyword = Keyword(
                                value=entity.text,
                                type=keyword_type,
                                source="text_analytics",
                                count=1,  # Analytics doesn't provide count
                                confidence=entity.confidence_score if hasattr(entity, 'confidence_score') else None
                            )
                            keywords.append(keyword)
            
        except Exception as e:
            logger.warning(f"Failed to convert analytics results to keywords: {e}")
        
        return keywords

    def _detect_gene_names(self, text: str) -> List[Keyword]:
        """
        Detect gene name mentions (currently focuses on MECP2).
        
        Args:
            text: Text to analyze
            
        Returns:
            List[Keyword]: List of gene name keywords
        """
        keywords = []
          # Detect "MECP2" (case-insensitive)
        mecp2_mentions = re.findall(r"\bMECP2\b", text, flags=re.IGNORECASE)
        mecp2_count = len(mecp2_mentions)
        if mecp2_count > 0:
            keywords.append(Keyword(value="MECP2", type="gene_name", source="regex", count=mecp2_count))
            
        return keywords

    def _detect_c_variants(self, text: str) -> List[Keyword]:
        """
        Detect c. variant notations (e.g., "c.1035A>G" or "c.[473C>T]").
        
        Args:
            text: Text to analyze
            
        Returns:
            List[Keyword]: List of c. variant keywords
        """
        keywords = []
          # Detect c. variants: e.g., "c.1035A>G" or "c.[473C>T]"
        variants_c = re.findall(r"(c\.\[?\d+[ACGTacgt>]+\]?)", text)
        variants_c_counter = Counter(variants_c)
        keywords.extend(
            [Keyword(value=variant, type="Variant", source="regex", count=count) 
             for variant, count in variants_c_counter.items()]
        )

        # Detect c. variants with deletion: e.g., "c.1040_1047del"
        variants_c_del = re.findall(r"(c\.\d+_\d+del)", text)
        variants_c_del_counter = Counter(variants_c_del)
        keywords.extend(
            [Keyword(value=variant, type="Variant", source="regex", count=count) 
             for variant, count in variants_c_del_counter.items()]
        )
        
        return keywords

    def _detect_p_variants(self, text: str) -> List[Keyword]:
        """
        Detect p. variant notations (e.g., "p.Arg306Cys" or "p.[Thr158Met]").
        
        Args:
            text: Text to analyze
            
        Returns:
            List[Keyword]: List of p. variant keywords
        """
        keywords = []
          # Detect p. variants: e.g., "p.Arg306Cys" or "p.[Thr158Met]"
        variants_p = re.findall(r"(p\.\[?[A-Za-z]{1,3}\d+[A-Za-z]{1,3}\]?)", text)
        variants_p_counter = Counter(variants_p)
        keywords.extend(
            [Keyword(value=variant, type="Variant", source="regex", count=count) 
             for variant, count in variants_p_counter.items()]
        )
        
        return keywords

    def _detect_reference_sequences(self, text: str) -> List[Keyword]:
        """
        Detect reference sequence identifiers (e.g., "NM_004992.4" or "NP_004983.1").
        
        Args:
            text: Text to analyze
            
        Returns:
            List[Keyword]: List of reference sequence keywords
        """
        keywords = []
          # Detect reference sequences like NM_####.# or NP_####.#
        refs = re.findall(r"(NM_\d+\.\d+|NP_\d+\.\d+)", text)
        refs_counter = Counter(refs)
        keywords.extend(
            [Keyword(value=ref, type="reference_sequence", source="regex", count=count) 
             for ref, count in refs_counter.items()]
        )

        # Detect reference sequences without version like NM_#### or NP_####
        refs_no_version = re.findall(r"(NM_\d+|NP_\d+)", text)
        refs_no_version_counter = Counter(refs_no_version)
        keywords.extend(
            [Keyword(value=ref, type="reference_sequence", source="regex", count=count) 
             for ref, count in refs_no_version_counter.items()]
        )
        
        return keywords

    def _validate_keyword_confidence(self, document: Document, keywords: List[Keyword]) -> None:
        """
        Validate OCR confidence scores for detected keywords.
        Updates the confidence scores in the keyword objects.

        Args:
            document: Document with OCR results
            keywords: List of keywords to validate
        """
        try:
            logger.debug("Validating OCR confidence for detected keywords")

            for keyword in keywords:
                confidence_value = document.find_word_confidence(keyword.value)
                if confidence_value is not None:
                    logger.debug(f"Found {keyword} with confidence {confidence_value}")
                    keyword.confidence = confidence_value
                else:
                    logger.warning(f"{keyword} was not found in OCR results")
                    keyword.confidence = 0.0

            logger.debug(f"Keyword confidence validation completed")

        except Exception as e:
            # Don't fail the entire process for confidence validation issues
            logger.error(f"Confidence validation failed: {e}")
            # Set all confidences to 0.0 as fallback
            for keyword in keywords:
                keyword.confidence = 0.0
