import logging
from typing import List, Any

from rettxmutation.config import RettxConfig, validate_config_fields
from rettxmutation.repositories import AISearchRepositoryInterface, AISearchRepository

logger = logging.getLogger(__name__)


class AISearchService:
    """Service for performing AI search using Azure AI Search via repository pattern."""

    def __init__(self, config: RettxConfig, repository: AISearchRepositoryInterface = None):
        """Initialize the search service with configuration and optional repository."""
        required_fields = [
            "RETTX_AI_SEARCH_SERVICE",
            "RETTX_AI_SEARCH_API_KEY",
            "RETTX_AI_SEARCH_INDEX_NAME",
        ]
        validate_config_fields(config, required_fields, "AISearchService")

        # Use provided repository or create default one
        if repository is None:
            semantic_config = getattr(config, "RETTX_AI_SEARCH_SEMANTIC_CONFIGURATION", None)
            self._repository = AISearchRepository(
                service=config.RETTX_AI_SEARCH_SERVICE,
                api_key=config.RETTX_AI_SEARCH_API_KEY,
                index_name=config.RETTX_AI_SEARCH_INDEX_NAME,
                semantic_configuration=semantic_config,
            )
        else:
            self._repository = repository
        
        logger.debug("AISearchService initialized with repository")

    def search(self, query: str, **kwargs: Any) -> List[Any]:
        """Perform an AI semantic search and return results as a list."""
        logger.debug("Executing AI semantic search")
        try:
            return self._repository.search(query, **kwargs)
        except Exception as e:
            logger.error(f"AI semantic search failed: {e}")
            raise

    def keyword_search(
        self, query: str, *, search_mode: str = "any", select_fields: List[str] = None, **kwargs: Any
    ) -> List[Any]:
        """Perform keyword search using the simple query syntax."""
        logger.debug("Executing keyword search")
        try:
            return self._repository.keyword_search(
                query,
                search_mode=search_mode,
                select_fields=select_fields,
                **kwargs
            )
        except Exception as e:
            logger.error(f"Keyword search failed: {e}")
            raise

    def text_search(self, query: str, **kwargs: Any) -> List[Any]:
        """Perform full text search using the Lucene syntax."""
        logger.debug("Executing text search")
        try:
            return self._repository.text_search(query, **kwargs)
        except Exception as e:
            logger.error(f"Text search failed: {e}")
            raise

    # === Strongly Typed Search Methods ===
    
    def search_mutations(self, query: str = "", **filters) -> List[Any]:
        """
        Search and return GeneMutation objects directly.
        
        Args:
            query: Search query string
            **filters: Additional filter parameters
            
        Returns:
            List of GeneMutation objects
        """
        from ..models.search_models import MutationVectorDocument
        from ..utils.mutation_converter import MutationConverter
        
        logger.debug("Executing typed mutation search")
        try:
            # Get search results as MutationVectorDocument objects
            documents = self.keyword_search(query, **filters)
            vector_docs = []
            
            for doc in documents:
                if isinstance(doc, dict):
                    vector_docs.append(MutationVectorDocument(**doc))
                else:
                    vector_docs.append(doc)
            
            # Convert to GeneMutation objects
            return MutationConverter.documents_to_gene_mutations(vector_docs)
        except Exception as e:
            logger.error(f"Typed mutation search failed: {e}")
            raise

    def search_by_gene(self, gene_id: str) -> List[Any]:
        """Search mutations by gene ID."""
        logger.debug(f"Searching mutations for gene: {gene_id}")
        return self.search_mutations("", gene_id=gene_id)

    def search_by_coordinates(self, assembly: str, start: int, end: int) -> List[Any]:
        """Search mutations by genomic coordinates."""
        logger.debug(f"Searching mutations in {assembly} coordinates: {start}-{end}")
        assembly_lower = assembly.lower()
        filters = {
            f"{assembly_lower}_start__gte": start,
            f"{assembly_lower}_end__lte": end
        }
        return self.search_mutations("", **filters)

    def search_by_variant_type(self, variant_type: str) -> List[Any]:
        """Search mutations by variant type."""
        logger.debug(f"Searching mutations by variant type: {variant_type}")
        return self.search_mutations("", variant_type=variant_type)

    def search_by_transcript(self, transcript_id: str) -> List[Any]:
        """Search mutations by transcript ID."""
        logger.debug(f"Searching mutations for transcript: {transcript_id}")
        filters = {
            "$filter": f"primary_transcript eq '{transcript_id}' or secondary_transcript eq '{transcript_id}'"
        }
        return self.search_mutations("", **filters)
