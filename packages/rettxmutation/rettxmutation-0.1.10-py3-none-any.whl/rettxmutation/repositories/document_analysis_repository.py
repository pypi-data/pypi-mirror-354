"""
Document Analysis Repository

Repository implementation for Azure Document Intelligence operations.
This handles the infrastructure concerns of interacting with Azure Document Analysis.
"""

import logging
from typing import BinaryIO, Optional, List
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.ai.documentintelligence.models import DocumentAnalysisFeature, AnalyzeResult

from rettxmutation.config import RettxConfig, validate_config_fields
from rettxmutation.repositories.interfaces import DocumentAnalysisRepositoryInterface

logger = logging.getLogger(__name__)


class DocumentAnalysisRepository(DocumentAnalysisRepositoryInterface):
    """
    Repository for Azure Document Analysis operations.
    
    This class handles the infrastructure concerns of interacting with 
    Azure Document Intelligence / Form Recognizer API.
    """
    
    def __init__(self, config: RettxConfig):
        """
        Initialize the Document Analysis repository with configuration.
        
        Args:
            config: Configuration object implementing RettxConfig protocol
            
        Raises:
            ValueError: If required configuration fields are missing or invalid
        """
        # Validate required configuration fields for this repository
        required_fields = [
            'RETTX_DOCUMENT_ANALYSIS_ENDPOINT',
            'RETTX_DOCUMENT_ANALYSIS_KEY'
        ]
        validate_config_fields(config, required_fields, 'DocumentAnalysisRepository')
        
        # Store config for internal use
        self._config = config
        
        # Initialize the Document Analysis client with validated configuration
        try:
            self._client = DocumentAnalysisClient(
                endpoint=config.RETTX_DOCUMENT_ANALYSIS_ENDPOINT,
                credential=AzureKeyCredential(config.RETTX_DOCUMENT_ANALYSIS_KEY)
            )
            logger.debug("DocumentAnalysisRepository initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize DocumentAnalysisClient: {e}")
            raise ValueError(f"DocumentAnalysisRepository initialization failed: {e}") from e

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
        try:
            logger.debug("Analyzing document with Azure Document Analysis")
            
            # Use default features if none provided
            if features is None:
                features = [DocumentAnalysisFeature.LANGUAGES]
            
            poller = self._client.begin_analyze_document(
                "prebuilt-read",
                document=file_stream,
                features=features
            )
            result: AnalyzeResult = poller.result()

            if not result:
                error_msg = "No valid document found by Azure Document Analysis"
                logger.error(error_msg)
                raise Exception(error_msg)

            logger.debug(f"Document analysis completed: {len(result.pages)} pages processed")
            return result

        except Exception as e:
            error_msg = f"Error analyzing document: {e}"
            logger.error(error_msg)
            raise Exception(error_msg) from e
