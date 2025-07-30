"""
Service Layer Exceptions

Custom exceptions for the services layer of RettXMutation library.
"""


class ServiceException(Exception):
    """Base exception for service-related errors."""
    pass


class OcrException(ServiceException):
    """Base exception for OCR-related errors."""
    pass


class OcrExtractionError(OcrException):
    """Raised when OCR text extraction fails."""
    pass


class OcrProcessingError(OcrException):
    """Raised when OCR text processing (cleaning, variant detection) fails."""
    pass


class OcrConfidenceError(OcrException):
    """Raised when OCR confidence validation fails."""
    pass
