"""
Unified Service Factory for the RettX Mutation Library.

This module provides centralized service creation and management following Azure best practices
for connection pooling, resource management, and dependency injection.

Each service validates only the configuration it needs, enabling flexible deployment
in both development and production environments.
"""

import logging
from typing import Optional
from rettxmutation.config import RettxConfig
from rettxmutation.services.embedding_service import EmbeddingService
from rettxmutation.services.mutation_validator import MutationValidator
from rettxmutation.services.mutation_tokenizator import MutationTokenizator
from rettxmutation.services.ai_search import AISearchService
from rettxmutation.services.ocr_service import OcrService
from rettxmutation.services.keyword_detector_service import KeywordDetectorService
from rettxmutation.services.variant_validator_service import VariantValidatorService
from rettxmutation.repositories import DocumentAnalysisRepository, TextAnalyticsRepository
from rettxmutation.openai_agent import ValidationAgent, MutationExtractionAgent, SummarizationAgent

logger = logging.getLogger(__name__)


class RettxServices:
    """
    Central service factory for the RettX Mutation Library.
    
    Provides lazy initialization and connection pooling for Azure services.
    Follows Azure best practices for resource management and dependency injection.
    
    Each service validates only the configuration fields it needs, enabling
    flexible deployment scenarios and fail-fast validation.
    """
    
    def __init__(self, config: RettxConfig):
        """
        Initialize the service factory with unified configuration.
        
        Args:
            config: Configuration object implementing RettxConfig protocol
            
        Note:
            Services are initialized lazily when first accessed.
            Each service validates its own required configuration fields.
        """
        self._config = config
          # Lazy-initialized repositories
        self._text_analytics_repository: Optional[TextAnalyticsRepository] = None
          # Lazy-initialized services
        self._embedding_service: Optional[EmbeddingService] = None
        self._variant_validator_service: Optional[VariantValidatorService] = None
        self._mutation_validator: Optional[MutationValidator] = None
        self._mutation_tokenizator: Optional[MutationTokenizator] = None
        self._ocr_service: Optional[OcrService] = None
        self._keyword_detector_service: Optional[KeywordDetectorService] = None
        self._semantic_search_service: Optional[AISearchService] = None
        # Lazy-initialized agents
        self._validation_agent: Optional[ValidationAgent] = None
        self._extraction_agent: Optional[MutationExtractionAgent] = None
        self._summarization_agent: Optional[SummarizationAgent] = None
        
        logger.debug("RettxServices factory initialized with unified configuration")
    
    @property
    def embedding_service(self) -> EmbeddingService:
        """
        Get or create the embedding service.
        
        Returns:
            EmbeddingService: Configured embedding service for Azure OpenAI integration
            
        Raises:
            ValueError: If required configuration fields are missing
        """
        if self._embedding_service is None:
            logger.debug("Initializing EmbeddingService")
            self._embedding_service = EmbeddingService(self._config)
        return self._embedding_service
    
    @embedding_service.setter
    def embedding_service(self, service: EmbeddingService):
        """Set the embedding service (for testing purposes)."""
        self._embedding_service = service
    
    @embedding_service.deleter
    def embedding_service(self):
        """Delete the embedding service (for testing purposes)."""
        self._embedding_service = None
    
    @property
    def text_analytics_repository(self) -> TextAnalyticsRepository:
        """
        Get or create the text analytics repository.
        
        Returns:
            TextAnalyticsRepository: Repository for Azure Text Analytics API interactions
            
        Raises:
            ValueError: If required configuration fields are missing
        """
        if self._text_analytics_repository is None:
            logger.debug("Initializing TextAnalyticsRepository")
            self._text_analytics_repository = TextAnalyticsRepository(
                endpoint=self._config.RETTX_COGNITIVE_SERVICES_ENDPOINT,
                key=self._config.RETTX_COGNITIVE_SERVICES_KEY
            )
        return self._text_analytics_repository

    @text_analytics_repository.setter
    def text_analytics_repository(self, repository: TextAnalyticsRepository):
        """Set the text analytics repository (for testing purposes)."""
        self._text_analytics_repository = repository
    
    @text_analytics_repository.deleter
    def text_analytics_repository(self):
        """Delete the text analytics repository (for testing purposes)."""
        self._text_analytics_repository = None
    
    @property
    def variant_validator_service(self) -> VariantValidatorService:
        """
        Get or create the variant validator service.
        
        Returns:
            VariantValidatorService: Service for validating and processing variants
        """
        if self._variant_validator_service is None:
            logger.debug("Initializing VariantValidatorService")
            from rettxmutation.repositories import VariantValidatorRepository
            repository = VariantValidatorRepository()
            self._variant_validator_service = VariantValidatorService(repository)
        return self._variant_validator_service
    
    @property
    def mutation_validator(self) -> MutationValidator:
        """
        Get or create the mutation validator service.
        
        Returns:
            MutationValidator: Service for validating raw mutations
        """
        if self._mutation_validator is None:
            logger.debug("Initializing MutationValidator")
            self._mutation_validator = MutationValidator(
                config=self._config,
                variant_validator_service=self.variant_validator_service
            )
        return self._mutation_validator
    
    @mutation_validator.setter
    def mutation_validator(self, validator: MutationValidator):
        """Set the mutation validator (for testing purposes)."""
        self._mutation_validator = validator
    
    @mutation_validator.deleter
    def mutation_validator(self):
        """Delete the mutation validator (for testing purposes)."""
        self._mutation_validator = None

    @property
    def mutation_tokenizator(self) -> MutationTokenizator:
        """
        Get or create the mutation tokenizator service.
        
        Returns:
            MutationTokenizator: Service for tokenizing mutation strings
        """
        if self._mutation_tokenizator is None:
            logger.debug("Initializing MutationTokenizator")
            self._mutation_tokenizator = MutationTokenizator()
        return self._mutation_tokenizator

    @property
    def ocr_service(self) -> OcrService:
        """
        Get or create the OCR service.
        
        Returns:
            OcrService: Configured service for document analysis and text processing
            
        Raises:
            ValueError: If required configuration fields are missing
        """
        if self._ocr_service is None:
            logger.debug("Initializing OcrService with DocumentAnalysisRepository")
            # Create the repository first
            document_analysis_repo = DocumentAnalysisRepository(self._config)
            # Create the service with the repository
            self._ocr_service = OcrService(document_analysis_repo)

        return self._ocr_service

    @property
    def ai_search_service(self) -> AISearchService:
        """Get or create the AI search service."""
        if self._semantic_search_service is None:
            logger.debug("Initializing AISearchService")
            self._semantic_search_service = AISearchService(self._config)
        return self._semantic_search_service

    @ai_search_service.setter
    def semantic_search_service(self, service: AISearchService):
        """Set the AI search service (for testing purposes)."""
        self._semantic_search_service = service

    @ai_search_service.deleter
    def ai_search_service(self):
        """Delete the AI search service (for testing purposes)."""
        self._semantic_search_service = None    
    @ocr_service.setter
    def ocr_service(self, service: OcrService):
        """Set the OCR service (for testing purposes)."""
        self._ocr_service = service
    
    @ocr_service.deleter
    def ocr_service(self):
        """Delete the OCR service (for testing purposes)."""
        self._ocr_service = None
    
    @property
    def validation_agent(self) -> ValidationAgent:
        """
        Get or create the validation agent.
        
        Returns:
            ValidationAgent: Agent for document validation using Azure OpenAI
            
        Raises:
            ValueError: If required configuration fields are missing
        """
        if self._validation_agent is None:
            logger.debug("Initializing ValidationAgent")
            self._validation_agent = ValidationAgent(
                api_key=self._config.RETTX_OPENAI_KEY,
                api_version=self._config.RETTX_OPENAI_MODEL_VERSION,
                azure_endpoint=self._config.RETTX_OPENAI_ENDPOINT,
                model_name=self._config.RETTX_OPENAI_MODEL_NAME
            )
        
        return self._validation_agent
    
    @validation_agent.setter
    def validation_agent(self, agent: ValidationAgent):
        """Set the validation agent (for testing purposes)."""
        self._validation_agent = agent
    
    @validation_agent.deleter
    def validation_agent(self):
        """Delete the validation agent (for testing purposes)."""
        self._validation_agent = None
    
    @property
    def extraction_agent(self) -> MutationExtractionAgent:
        """
        Get or create the mutation extraction agent.
        
        Returns:
            MutationExtractionAgent: Agent for extracting mutations using Azure OpenAI
            
        Raises:
            ValueError: If required configuration fields are missing
        """
        if self._extraction_agent is None:
            logger.debug("Initializing MutationExtractionAgent")
            self._extraction_agent = MutationExtractionAgent(
                api_key=self._config.RETTX_OPENAI_KEY,
                api_version=self._config.RETTX_OPENAI_MODEL_VERSION,
                azure_endpoint=self._config.RETTX_OPENAI_ENDPOINT,
                model_name=self._config.RETTX_OPENAI_MODEL_NAME
            )
        
        return self._extraction_agent

    @extraction_agent.setter
    def extraction_agent(self, agent: MutationExtractionAgent):
        """Set the extraction agent (for testing purposes)."""
        self._extraction_agent = agent
    
    @extraction_agent.deleter
    def extraction_agent(self):
        """Delete the extraction agent (for testing purposes)."""
        self._extraction_agent = None

    @property
    def summarization_agent(self) -> SummarizationAgent:
        """
        Get or create the summarization agent.
        
        Returns:
            SummarizationAgent: Agent for summarizing reports using Azure OpenAI
            
        Raises:
            ValueError: If required configuration fields are missing
        """
        if self._summarization_agent is None:
            logger.debug("Initializing SummarizationAgent")
            self._summarization_agent = SummarizationAgent(
                api_key=self._config.RETTX_OPENAI_KEY,
                api_version=self._config.RETTX_OPENAI_MODEL_VERSION,
                azure_endpoint=self._config.RETTX_OPENAI_ENDPOINT,
                model_name=self._config.RETTX_OPENAI_MODEL_NAME
            )
        
        return self._summarization_agent
    
    @summarization_agent.setter
    def summarization_agent(self, agent: SummarizationAgent):
        """Set the summarization agent (for testing purposes)."""
        self._summarization_agent = agent
    
    @summarization_agent.deleter
    def summarization_agent(self):
        """Delete the summarization agent (for testing purposes)."""
        self._summarization_agent = None

    @property
    def keyword_detector_service(self) -> KeywordDetectorService:
        """
        Get or create the keyword detector service.
        
        Returns:
            KeywordDetectorService: Service for MECP2-specific keyword detection
        """
        if self._keyword_detector_service is None:
            logger.debug("Initializing KeywordDetectorService with unified detection capabilities")
            
            # Get optional dependencies - gracefully handle missing config
            text_analytics_repo = None
            ai_search_svc = None
            
            try:
                text_analytics_repo = self.text_analytics_repository
            except (ValueError, AttributeError) as e:
                logger.debug(f"Text analytics repository not available: {e}")
            
            try:
                ai_search_svc = self.semantic_search_service
            except (ValueError, AttributeError) as e:
                logger.debug(f"AI search service not available: {e}")
            
            # Create with available dependencies
            self._keyword_detector_service = KeywordDetectorService(
                text_analytics_repository=text_analytics_repo,
                ai_search_service=ai_search_svc            )
        return self._keyword_detector_service
    
    @keyword_detector_service.setter
    def keyword_detector_service(self, service: KeywordDetectorService):
        """Set the keyword detector service (for testing purposes)."""
        self._keyword_detector_service = service
    
    @keyword_detector_service.deleter
    def keyword_detector_service(self):
        """Delete the keyword detector service (for testing purposes)."""
        self._keyword_detector_service = None
    
    def close(self):
        """
        Clean up all initialized services and their resources.
        
        This method should be called when the service factory is no longer needed
        to ensure proper cleanup of Azure connections and other resources.
        """
        logger.debug("Cleaning up RettxServices resources")
        
        if self._variant_validator_service:
            self._variant_validator_service.close()
        
        if self._mutation_validator:
            self._mutation_validator.close()
        
        # Other services don't currently have cleanup methods, but this provides
        # a central place to add cleanup logic as services evolve
        
        logger.debug("RettxServices cleanup completed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with automatic cleanup."""
        self.close()


# Convenience function for creating services with default configuration
def create_services(config: Optional[RettxConfig] = None) -> RettxServices:
    """
    Create a RettxServices factory with optional configuration.
    
    Args:
        config: Optional configuration object. If None, uses DefaultConfig.
        
    Returns:
        RettxServices: Configured service factory
        
    Example:
        # Using default environment-based configuration
        services = create_services()
        
        # Using custom configuration
        custom_config = MyKeyVaultConfig()
        services = create_services(custom_config)
        
        # Using as context manager for automatic cleanup
        with create_services() as services:
            embeddings = services.embedding_service.create_embeddings(mutations)
    """
    if config is None:
        from rettxmutation.config import DefaultConfig
        config = DefaultConfig()
    
    return RettxServices(config)
