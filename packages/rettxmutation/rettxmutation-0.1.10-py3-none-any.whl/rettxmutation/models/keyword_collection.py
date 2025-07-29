"""
Keyword Collection Model

Contains keyword-related models and the KeywordCollection class that represents 
a unified collection of keywords detected from various sources with surface-level deduplication.
"""

import logging
from typing import List, Iterator, Optional, Dict, Any, Set, TYPE_CHECKING
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from ..models.gene_models import GeneMutation

logger = logging.getLogger(__name__)

# Import for typed search functionality
try:
    from ..utils.mutation_converter import MutationConverter
    from ..models.search_models import MutationVectorDocument
except ImportError:
    # Handle circular imports gracefully
    MutationConverter = None
    MutationVectorDocument = None


# Keyword model for detected mutations and genetic variants
class Keyword(BaseModel):
    value: str = Field(..., description="The value of the detected keyword")
    type: str = Field(..., description="The type of the keyword (e.g., 'gene_name', 'variant_c', 'variant_p', etc.)")
    source: str = Field(..., description="The source of detection (e.g., 'regex', 'text_analytics', 'ai_search')")
    count: int = Field(1, description="Number of occurrences of the keyword")
    confidence: Optional[float] = Field(None, description="Confidence score of the detected keyword")


# Enriched keyword model with AI search results
class EnrichedKeyword(BaseModel):
    value: str = Field(..., description="The value of the detected keyword")
    type: str = Field(..., description="The type of the keyword (e.g., 'gene_name', 'variant_c', 'variant_p', etc.)")
    source: str = Field(..., description="The source of detection (e.g., 'regex', 'text_analytics', 'ai_search')")
    count: int = Field(1, description="Number of occurrences of the keyword")
    confidence: Optional[float] = Field(None, description="Confidence score of the detected keyword")
    search_result: Optional[dict] = Field(None, description="AI search result containing enriched information about the variant")
    search_score: Optional[float] = Field(None, description="AI search relevance score")


class KeywordCollection(BaseModel):
    """
    A collection of keywords with automatic surface-level deduplication.
    
    This class unifies keywords from multiple sources and automatically
    deduplicates based on exact text match (case-insensitive):
    - Regex-based detection
    - Text analytics (Azure Health)  
    - AI search enrichment
    """
      # Internal storage - using private fields
    keywords_index: Dict[str, Keyword] = Field(default_factory=dict, description="Internal keyword storage with deduplication index")
    enriched_keywords_index: Dict[str, EnrichedKeyword] = Field(default_factory=dict, description="Internal enriched keyword storage")
    
    # Metadata
    confidence_threshold: float = Field(0.5, description="Confidence threshold used for filtering")
    processing_stats: Dict[str, Any] = Field(default_factory=dict, description="Statistics about the processing")

    def __iter__(self) -> Iterator[Keyword]:
        """Allow iteration over all keywords."""
        for keyword in self.keywords_index.values():
            yield keyword

    def __len__(self) -> int:
        """Return total count of unique keywords."""
        return len(self.keywords_index)

    def __getitem__(self, index: int) -> Keyword:
        """Allow indexing into the collection."""
        keywords_list = list(self.keywords_index.values())
        return keywords_list[index]

    def add(self, keyword: Keyword) -> bool:
        """
        Add a keyword to the collection with automatic deduplication.
        
        Args:
            keyword: Keyword to add
            
        Returns:
            bool: True if keyword was added, False if it was a duplicate (ignored)
        """
        # Use case-insensitive text + type as deduplication key
        key = f"{keyword.value.lower()}:{keyword.type}"
        
        if key in self.keywords_index:
            # Merge with existing - combine counts and use higher confidence
            existing = self.keywords_index[key]
            existing.count += keyword.count
            if keyword.confidence and (not existing.confidence or keyword.confidence > existing.confidence):
                existing.confidence = keyword.confidence
            return False  # Was duplicate
        else:
            # Add new keyword
            self.keywords_index[key] = keyword
            return True  # Was new

    def add_enriched(self, enriched_keyword: EnrichedKeyword) -> bool:
        """
        Add an enriched keyword to the collection with automatic deduplication.
        
        Args:
            enriched_keyword: EnrichedKeyword to add
            
        Returns:
            bool: True if keyword was added, False if it was a duplicate (ignored)
        """
        key = f"{enriched_keyword.value.lower()}:{enriched_keyword.type}"
        
        if key in self.enriched_keywords_index:
            # Merge with existing
            existing = self.enriched_keywords_index[key]
            existing.count += enriched_keyword.count
            if enriched_keyword.confidence and (not existing.confidence or enriched_keyword.confidence > existing.confidence):
                existing.confidence = enriched_keyword.confidence            # Keep the search result from the new one if it exists
            if enriched_keyword.search_result:
                existing.search_result = enriched_keyword.search_result
            return False  # Was duplicate
        else:
            # Add new enriched keyword
            self.enriched_keywords_index[key] = enriched_keyword
            return True  # Was new

    def get_enriched_keywords(self) -> List[EnrichedKeyword]:
        """Get only keywords that have been enriched with AI search results."""
        return [kw for kw in self.enriched_keywords_index.values() if kw.search_result is not None]

    def get_keywords_by_type(self, keyword_type: str) -> List[Keyword]:
        """Get all keywords of a specific type."""
        return [kw for kw in self.keywords_index.values() if kw.type == keyword_type]

    def get_variants(self) -> List[Keyword]:
        """Get all variant-related keywords."""
        variant_types = ["Variant", "variant", "variant_c", "variant_p", "c_variant", "p_variant"]
        return [kw for kw in self.keywords_index.values() if kw.type in variant_types]

    def get_genes(self) -> List[Keyword]:
        """Get all gene-related keywords."""
        return [kw for kw in self.keywords_index.values() if kw.type == "gene_name"]

    def get_high_confidence_keywords(self, threshold: Optional[float] = None) -> List[Keyword]:
        """Get keywords above the confidence threshold."""
        threshold = threshold or self.confidence_threshold
        return [kw for kw in self.keywords_index.values() 
                if kw.confidence is not None and kw.confidence >= threshold]

    def get_processing_summary(self) -> Dict[str, Any]:
        """Get a summary of the processing results."""
        return {
            "total_keywords": len(self.keywords_index),
            "regular_keywords": len(self.keywords_index),
            "enriched_keywords": len(self.enriched_keywords_index),
            "keywords_with_search_results": len(self.get_enriched_keywords()),
            "unique_variants": len(self.get_variants()),
            "unique_genes": len(self.get_genes()),
            "high_confidence_keywords": len(self.get_high_confidence_keywords()),
            "confidence_threshold": self.confidence_threshold,
            "processing_stats": self.processing_stats
        }
    
    # === Strongly Typed Search Result Methods ===
    
    def get_gene_mutations(self) -> List["GeneMutation"]:
        """
        Get all enriched keywords as GeneMutation objects.
        
        Returns:
            List of GeneMutation objects converted from search results
        """
        if not MutationConverter or not MutationVectorDocument:
            logger.warning("Search models not available. Cannot convert to GeneMutation objects.")
            return []
            
        mutations = []
        for enriched_kw in self.get_enriched_keywords():
            if enriched_kw.search_result:
                try:
                    doc = MutationVectorDocument(**enriched_kw.search_result)
                    mutation = MutationConverter.document_to_gene_mutation(doc)
                    mutations.append(mutation)
                except Exception as e:
                    logger.warning(f"Failed to convert search result to GeneMutation: {e}")
                    continue
        return mutations
    def get_enriched_mutations_by_gene(self, gene_id: str) -> List["GeneMutation"]:
        """Get mutations filtered by gene ID."""
        return [mutation for mutation in self.get_gene_mutations() 
                if mutation.primary_transcript and mutation.primary_transcript.gene_id == gene_id]

    def get_unique_mutations_by_hgvs(self) -> Dict[str, "GeneMutation"]:
        """Get unique mutations keyed by HGVS notation."""
        unique_mutations = {}
        for mutation in self.get_gene_mutations():
            # Use primary HGVS as key, or fallback to other identifiers
            key = None
            if mutation.primary_transcript and mutation.primary_transcript.hgvs_transcript_variant:
                key = mutation.primary_transcript.hgvs_transcript_variant
            elif mutation.genomic_coordinates:
                for assembly, coord in mutation.genomic_coordinates.items():
                    if coord.hgvs:
                        key = coord.hgvs
                        break
            
            if not key:
                # Use a combination of fields as key since gene_id is not directly available
                gene_id = mutation.primary_transcript.gene_id if mutation.primary_transcript else "Unknown"
                key = f"{gene_id}_{mutation.variant_type}_{hash(str(mutation))}"
            
            unique_mutations[key] = mutation
        return unique_mutations

    def get_mutations_by_coordinates(self, assembly: str, start: int, end: int) -> List["GeneMutation"]:
        """Get mutations within specified genomic coordinate range."""
        mutations = []
        for mutation in self.get_gene_mutations():
            if mutation.genomic_coordinates and assembly in mutation.genomic_coordinates:
                coord = mutation.genomic_coordinates[assembly]
                if (coord.start is not None and coord.end is not None and
                    coord.start >= start and coord.end <= end):
                    mutations.append(mutation)
        return mutations

    def get_mutations_by_variant_type(self, variant_type: str) -> List["GeneMutation"]:
        """Get mutations filtered by variant type."""
        return [mutation for mutation in self.get_gene_mutations() 
                if mutation.variant_type == variant_type]

    def get_mutation_summary(self) -> Dict[str, Any]:
        """Get a summary of typed mutation data."""
        mutations = self.get_gene_mutations()
        gene_counts = {}
        variant_type_counts = {}
        
        for mutation in mutations:
            # Count by gene
            gene_id = mutation.primary_transcript.gene_id if mutation.primary_transcript else None
            if gene_id:
                gene_counts[gene_id] = gene_counts.get(gene_id, 0) + 1
            
            # Count by variant type
            if mutation.variant_type:
                variant_type_counts[mutation.variant_type] = variant_type_counts.get(mutation.variant_type, 0) + 1
        
        return {
            "total_mutations": len(mutations),
            "unique_genes": len(gene_counts),
            "gene_distribution": gene_counts,
            "variant_type_distribution": variant_type_counts,
            "mutations_with_coordinates": len([m for m in mutations if m.genomic_coordinates]),
            "mutations_with_transcripts": len([m for m in mutations if m.primary_transcript])
        }
