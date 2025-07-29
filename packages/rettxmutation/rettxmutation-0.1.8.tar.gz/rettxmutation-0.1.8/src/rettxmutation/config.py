"""
Unified Configuration for the RettX Mutation Library.

This module provides a single, unified configuration protocol that all services
can use. Each service validates only the configuration fields it needs.
"""

import logging
from typing import Protocol, Optional

logger = logging.getLogger(__name__)


class RettxConfig(Protocol):
    """
    Unified configuration protocol for the entire RettX Mutation Library.
    
    All fields are optional except for truly cross-cutting concerns.
    Each service validates only the fields it actually needs.
    """
    
    # Cross-cutting configuration (minimal mandatory fields)
    LOG_LEVEL: Optional[str] = "INFO"
    ENVIRONMENT: Optional[str] = "development"
    
    # Document Analysis Service (Azure Form Recognizer)
    RETTX_DOCUMENT_ANALYSIS_ENDPOINT: Optional[str] = None
    RETTX_DOCUMENT_ANALYSIS_KEY: Optional[str] = None
    
    # Azure OpenAI Configuration
    RETTX_OPENAI_KEY: Optional[str] = None
    RETTX_OPENAI_MODEL_VERSION: Optional[str] = None
    RETTX_OPENAI_ENDPOINT: Optional[str] = None
    RETTX_OPENAI_MODEL_NAME: Optional[str] = None
    RETTX_EMBEDDING_DEPLOYMENT: Optional[str] = None
    
    # Azure Cognitive Services (Text Analytics)
    RETTX_COGNITIVE_SERVICES_ENDPOINT: Optional[str] = None
    RETTX_COGNITIVE_SERVICES_KEY: Optional[str] = None
    
    # Azure AI Search (optional)
    RETTX_AI_SEARCH_SERVICE: Optional[str] = None
    RETTX_AI_SEARCH_API_KEY: Optional[str] = None
    RETTX_AI_SEARCH_INDEX_NAME: Optional[str] = None
    RETTX_AI_SEARCH_SEMANTIC_CONFIGURATION: Optional[str] = None


class DefaultConfig:
    """
    Default configuration implementation that loads from environment variables.
    
    This is a convenience implementation for development and testing.
    Production users should implement their own RettxConfig following their
    organization's security and operational requirements (Key Vault, etc.).
    """
    
    def __init__(self, env_file_path: Optional[str] = None):
        """
        Initialize configuration from environment variables.
        
        Args:
            env_file_path: Optional path to .env file. If None, searches for .env
                          in current directory and examples/ directory.
        """
        import os
        from pathlib import Path
        
        # Load environment variables from .env file if available
        try:
            from dotenv import load_dotenv
            
            if env_file_path:
                load_dotenv(env_file_path)
                logger.debug(f"Loaded environment variables from {env_file_path}")
            else:
                # Try to find .env file in common locations
                current_dir = Path.cwd()
                env_locations = [
                    current_dir / ".env",
                    current_dir / "examples" / ".env",
                    Path(__file__).parent.parent.parent / "examples" / ".env"
                ]
                
                for env_path in env_locations:
                    if env_path.exists():
                        load_dotenv(env_path)
                        logger.debug(f"Loaded environment variables from {env_path}")
                        break
                else:
                    logger.debug("No .env file found in standard locations")
                    
        except ImportError:
            logger.warning("python-dotenv not available, skipping .env file loading")
        
        # Cross-cutting configuration
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
        self.ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
          # Document Analysis Service  
        self.RETTX_DOCUMENT_ANALYSIS_ENDPOINT = os.getenv('RETTX_DOCUMENT_ANALYSIS_ENDPOINT')
        self.RETTX_DOCUMENT_ANALYSIS_KEY = os.getenv('RETTX_DOCUMENT_ANALYSIS_KEY')

        # Azure OpenAI Configuration
        self.RETTX_OPENAI_KEY = os.getenv('RETTX_OPENAI_KEY')
        self.RETTX_OPENAI_MODEL_VERSION = os.getenv('RETTX_OPENAI_MODEL_VERSION', '2024-02-01')
        self.RETTX_OPENAI_ENDPOINT = os.getenv('RETTX_OPENAI_ENDPOINT')
        self.RETTX_OPENAI_MODEL_NAME = os.getenv('RETTX_OPENAI_MODEL_NAME')
        self.RETTX_EMBEDDING_DEPLOYMENT = os.getenv('RETTX_EMBEDDING_DEPLOYMENT')
        
        # Azure Cognitive Services
        self.RETTX_COGNITIVE_SERVICES_ENDPOINT = os.getenv('RETTX_COGNITIVE_SERVICES_ENDPOINT')
        self.RETTX_COGNITIVE_SERVICES_KEY = os.getenv('RETTX_COGNITIVE_SERVICES_KEY')
        
        # Azure AI Search
        self.RETTX_AI_SEARCH_SERVICE = os.getenv('RETTX_AI_SEARCH_SERVICE')
        self.RETTX_AI_SEARCH_API_KEY = os.getenv('RETTX_AI_SEARCH_API_KEY')
        self.RETTX_AI_SEARCH_INDEX_NAME = os.getenv('RETTX_AI_SEARCH_INDEX_NAME')
        self.RETTX_AI_SEARCH_SEMANTIC_CONFIGURATION = os.getenv(
            'RETTX_AI_SEARCH_SEMANTIC_CONFIGURATION'
        )
        
        logger.debug("DefaultConfig initialized from environment variables")


def validate_config_fields(config: RettxConfig, required_fields: list[str], service_name: str) -> None:
    """
    Utility function to validate that required configuration fields are present.

    Args:
        config: Configuration object to validate
        required_fields: List of field names that must be present and non-empty
        service_name: Name of the service requesting validation (for error messages)

    Raises:
        ValueError: If any required fields are missing or empty
    """
    missing_fields = []
    empty_fields = []
    
    for field in required_fields:
        if not hasattr(config, field):
            missing_fields.append(field)
        else:
            value = getattr(config, field)
            if value is None or (isinstance(value, str) and not value.strip()):
                empty_fields.append(field)
    
    error_messages = []
    if missing_fields:
        error_messages.append(f"missing fields: {', '.join(missing_fields)}")
    if empty_fields:
        error_messages.append(f"empty fields: {', '.join(empty_fields)}")
    
    if error_messages:
        error_msg = "; ".join(error_messages)
        full_error = f"{service_name} configuration validation failed - {error_msg}"
        logger.error(full_error)
        raise ValueError(full_error)
    
    logger.debug(f"{service_name} configuration validation successful")
