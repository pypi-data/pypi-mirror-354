"""
Text Analytics Repository Implementation for Azure Text Analytics services.

This repository encapsulates Azure Text Analytics API interactions.
"""

import logging
from typing import Any
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from rettxmutation.repositories.interfaces import TextAnalyticsRepositoryInterface

logger = logging.getLogger(__name__)


class TextAnalyticsRepository(TextAnalyticsRepositoryInterface):
    """Repository for Azure Text Analytics API interactions."""
    
    def __init__(self, endpoint: str, key: str):
        """Initialize the Azure Text Analytics client."""
        self._client = TextAnalyticsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(key)
        )
        logger.debug("TextAnalyticsRepository initialized")
    
    def analyze_healthcare_entities(self, text: str) -> Any:
        """Analyze healthcare entities in the given text."""
        documents = [text]
        poller = self._client.begin_analyze_healthcare_entities(documents)
        result = poller.result()
        return result
