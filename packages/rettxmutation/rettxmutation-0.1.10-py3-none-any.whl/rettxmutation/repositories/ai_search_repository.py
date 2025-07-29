"""
AI Search Repository Implementation for Azure AI Search services.

This repository encapsulates Azure AI Search API interactions.
"""

import logging
from typing import Any, List
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import QueryType
from rettxmutation.repositories.interfaces import AISearchRepositoryInterface

logger = logging.getLogger(__name__)


class AISearchRepository(AISearchRepositoryInterface):
    """Repository for Azure AI Search API interactions."""
    
    def __init__(
        self,
        service: str,
        api_key: str,
        index_name: str,
        semantic_configuration: str = None,
    ):
        """Initialize the Azure AI Search client."""
        endpoint = f"https://{service}.search.windows.net"
        self._semantic_config = semantic_configuration
        self._client = SearchClient(
            endpoint=endpoint,
            index_name=index_name,
            credential=AzureKeyCredential(api_key),
        )
        logger.debug("AISearchRepository initialized")

    def search(self, query: str, **kwargs: Any) -> List[Any]:
        """Perform semantic search and return results."""
        params = {
            "search_text": query,
            "query_type": QueryType.SEMANTIC,
        }
        if self._semantic_config:
            params["semantic_configuration_name"] = self._semantic_config
        params.update(kwargs)
        results = self._client.search(**params)
        return [r for r in results]

    def keyword_search(self, query: str, *, search_mode: str = "any", select_fields: List[str] = None, **kwargs: Any) -> List[Any]:
        """Perform keyword search with specified search mode."""
        params = {
            "search_text": query.lower(),
            "query_type": QueryType.SIMPLE,
            "search_fields": ["literal_mutation_tokens"],
            "search_mode": search_mode,
        }
        if self._semantic_config:
            params["semantic_configuration_name"] = self._semantic_config
        if select_fields:
            params["select"] = select_fields
        params.update(kwargs)
        results = self._client.search(**params)
        return [r for r in results]

    def text_search(self, query: str, **kwargs: Any) -> List[Any]:
        """Perform full text search using Lucene syntax."""
        params = {
            "search_text": query,
            "query_type": QueryType.FULL,
            "search_fields": ["literal_mutation_tokens"],
        }
        if self._semantic_config:
            params["semantic_configuration_name"] = self._semantic_config
        params.update(kwargs)
        results = self._client.search(**params)
        return [r for r in results]
