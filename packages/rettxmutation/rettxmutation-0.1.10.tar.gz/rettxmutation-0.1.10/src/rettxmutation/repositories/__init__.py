"""Repository layer for external service clients."""

# Repository Interfaces
from .interfaces import (
    AISearchRepositoryInterface,
    TextAnalyticsRepositoryInterface,
    DocumentAnalysisRepositoryInterface,
    OpenAIRepositoryInterface,
    VariantValidatorRepositoryInterface,
)

# Repository Implementations
from .document_analysis_repository import DocumentAnalysisRepository
from .text_analytics_repository import TextAnalyticsRepository
from .openai_repository import OpenAIRepository
from .ai_search_repository import AISearchRepository
from .variant_validator_repository import (
    VariantValidatorRepository,
    VariantValidatorError,
    VariantValidatorNormalizationError,
)

__all__ = [
    # Interfaces
    "AISearchRepositoryInterface",
    "TextAnalyticsRepositoryInterface", 
    "DocumentAnalysisRepositoryInterface",
    "OpenAIRepositoryInterface",
    "VariantValidatorRepositoryInterface",
    # Implementations
    "DocumentAnalysisRepository",
    "TextAnalyticsRepository",
    "OpenAIRepository",
    "AISearchRepository",
    "VariantValidatorRepository",
    "VariantValidatorError",
    "VariantValidatorNormalizationError",
]
