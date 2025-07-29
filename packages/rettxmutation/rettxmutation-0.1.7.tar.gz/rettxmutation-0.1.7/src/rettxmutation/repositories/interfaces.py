"""
Repository interfaces for the RettX Mutation Library.

These interfaces define contracts for external service interactions,
enabling better testability and flexibility in implementation.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, BinaryIO, Optional, Iterable
from azure.ai.documentintelligence.models import AnalyzeResult, DocumentAnalysisFeature


class AISearchRepositoryInterface(ABC):
    """Interface for AI Search repository operations."""
    
    @abstractmethod
    def search(self, query: str, **kwargs: Any) -> List[Any]:
        """Perform semantic search and return results."""
        pass
    
    @abstractmethod
    def keyword_search(self, query: str, *, search_mode: str = "any", **kwargs: Any) -> List[Any]:
        """Perform keyword search with specified search mode."""
        pass
    
    @abstractmethod
    def text_search(self, query: str, **kwargs: Any) -> List[Any]:
        """Perform full text search using Lucene syntax."""
        pass


class TextAnalyticsRepositoryInterface(ABC):
    """Interface for Text Analytics repository operations."""
    
    @abstractmethod
    def analyze_healthcare_entities(self, text: str) -> Any:
        """Analyze healthcare entities in the given text."""
        pass


class DocumentAnalysisRepositoryInterface(ABC):
    """Interface for Document Analysis repository operations."""
    
    @abstractmethod
    def analyze_document(
        self,
        file_stream: BinaryIO,
        features: Optional[List[DocumentAnalysisFeature]] = None,
    ) -> AnalyzeResult:
        """
        Analyze a document using Azure Document Analysis.
        
        Args:
            file_stream: Binary stream of the document
            features: Optional list of analysis features to enable
            
        Returns:
            AnalyzeResult: The analysis result from Azure Document Analysis
            
        Raises:
            Exception: If document analysis fails
        """
        pass


class OpenAIRepositoryInterface(ABC):
    """Interface for OpenAI repository operations."""
    
    @abstractmethod
    def create_embedding(self, deployment: str, text: str) -> Iterable[float]:
        """Create embedding for a single text."""
        pass
    
    @abstractmethod
    def create_embeddings(self, deployment: str, texts: List[str]) -> List[List[float]]:
        """Create embeddings for multiple texts."""
        pass


class VariantValidatorRepositoryInterface(ABC):
    """Interface for VariantValidator repository operations."""
    
    @abstractmethod
    def normalize_mutation(
        self,
        target_assembly: str,
        variant_description: str,
        select_transcripts: str,
    ) -> Dict[str, Any]:
        """Normalize a mutation using VariantValidator API."""
        pass
    
    @abstractmethod
    def resolve_transcripts(self, transcript_id: str) -> Dict[str, Any]:
        """Resolve transcript information using VariantValidator tools API."""
        pass
    
    @abstractmethod
    def format_variant(
        self,
        genomic_hgvs: str,
        select_transcripts: str,
        genome_build: str,
        transcript_model: str = "refseq",
        use_hgvs: bool = False,
    ) -> Dict[str, Any]:
        """Format variant using VariantValidator formatter API."""
        pass
    
    @abstractmethod
    def close(self):
        """Clean up repository resources."""
        pass
