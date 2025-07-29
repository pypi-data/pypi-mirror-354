"""
OpenAI Repository Implementation for Azure OpenAI services.

This repository encapsulates Azure OpenAI API interactions for embedding generation.
"""

import logging
from typing import List, Iterable
from openai import AzureOpenAI
from rettxmutation.repositories.interfaces import OpenAIRepositoryInterface

logger = logging.getLogger(__name__)


class OpenAIRepository(OpenAIRepositoryInterface):
    """Repository for Azure OpenAI API interactions."""
    
    def __init__(self, api_key: str, api_version: str, azure_endpoint: str):
        """Initialize the Azure OpenAI client."""
        self._client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=azure_endpoint
        )
        logger.debug("OpenAIRepository initialized")
    
    def create_embedding(self, deployment: str, text: str) -> Iterable[float]:
        """Create embedding for a single text."""
        response = self._client.embeddings.create(
            model=deployment,
            input=text,
            encoding_format="float"
        )
        return response.data[0].embedding
    
    def create_embeddings(self, deployment: str, texts: List[str]) -> List[List[float]]:
        """Create embeddings for multiple texts."""
        response = self._client.embeddings.create(
            model=deployment,
            input=texts,
            encoding_format="float"
        )
        return [data.embedding for data in response.data]
