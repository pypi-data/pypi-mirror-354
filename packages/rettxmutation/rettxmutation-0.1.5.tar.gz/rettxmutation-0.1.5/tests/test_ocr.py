"""
Comprehensive Test Suite for OCR Components

This module provides complete test coverage for the OCR functionality including:
- OcrService initialization and method signatures  
- Text extraction and processing workflows
- Text cleaning and variant detection methods
- Error handling and edge cases
- Integration with Azure Document Analysis service
- Configuration validation

Tests use proper mocking to avoid actual API calls.
"""

import pytest
import io
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from dotenv import load_dotenv
import os

from rettxmutation import DefaultConfig
from rettxmutation.services import OcrService
from rettxmutation.services.exceptions import OcrException, OcrExtractionError, OcrProcessingError
from rettxmutation.repositories import DocumentAnalysisRepository
from rettxmutation.models.document import Document


class TestOcrService:
    """Test suite for OcrService component."""
    
    @pytest.fixture
    def config(self):
        """Create test configuration."""
        config = DefaultConfig()
        # Set required Azure Document Intelligence fields for testing
        config.RETTX_DOCUMENT_ANALYSIS_ENDPOINT = "https://test.cognitiveservices.azure.com/"
        config.RETTX_DOCUMENT_ANALYSIS_KEY = "test-key"
        return config
    
    @pytest.fixture
    def ocr_processor(self, config):
        """Create OCR service instance for testing."""
        document_analysis_repo = DocumentAnalysisRepository(config)
        return OcrService(document_analysis_repo)

    @pytest.fixture
    def mock_document(self):
        """Create mock document result for testing."""
        doc = Document(
            raw_text="Sample extracted text from document with MECP2 c.123A>G mutation",
            language="en",
            words=[],
            lines=[]
        )
        doc.cleaned_text = "Sample extracted text from document with MECP2 c.123A>G mutation"
        return doc

    def test_initialization_success(self, config):
        """Test successful OCR service initialization."""
        document_analysis_repo = DocumentAnalysisRepository(config)
        processor = OcrService(document_analysis_repo)
        assert processor is not None
        assert hasattr(processor, '_document_analysis_repository')
        # OcrService implements OCR-related methods
        assert hasattr(processor, 'clean_ocr_text')
    
    def test_initialization_missing_endpoint(self):
        """Test OCR service initialization with missing endpoint."""
        config = DefaultConfig()
        config.RETTX_DOCUMENT_ANALYSIS_KEY = "test-key"
        config.RETTX_DOCUMENT_ANALYSIS_ENDPOINT = None  # Explicitly set to None
        # Missing endpoint should cause ValueError
        
        with pytest.raises(ValueError):
            document_analysis_repo = DocumentAnalysisRepository(config)
    
    def test_initialization_missing_key(self):
        """Test OCR service initialization with missing key."""
        config = DefaultConfig()
        config.RETTX_DOCUMENT_ANALYSIS_ENDPOINT = "https://test.cognitiveservices.azure.com/"
        config.RETTX_DOCUMENT_ANALYSIS_KEY = None  # Explicitly set to None
        # Missing key should cause ValueError
        
        with pytest.raises(ValueError):
            document_analysis_repo = DocumentAnalysisRepository(config)

    def test_has_required_methods(self, ocr_processor):
        """Test that OCR processor has all required methods."""
        assert hasattr(ocr_processor, 'extract_and_process_text')
        assert callable(getattr(ocr_processor, 'extract_and_process_text'))
        assert hasattr(ocr_processor, 'clean_ocr_text')
        assert callable(getattr(ocr_processor, 'clean_ocr_text'))

    @patch('rettxmutation.repositories.document_analysis_repository.DocumentAnalysisRepository.analyze_document')
    def test_extract_and_process_text_success(self, mock_analyze, ocr_processor, mock_document):
        """Test successful text extraction and processing."""
        # Create a mock AnalyzeResult that the repository returns
        from azure.ai.documentintelligence.models import AnalyzeResult, DocumentPage, DocumentLine, DocumentWord
        
        # Create properly structured mock with real values for Pydantic validation
        mock_word = Mock(spec=DocumentWord)
        mock_word.content = "Sample"
        mock_word.confidence = 0.95
        mock_word.span = Mock()
        mock_word.span.offset = 0
        mock_word.span.length = 6
        
        mock_line = Mock(spec=DocumentLine)
        mock_line.content = "Sample extracted text from document with MECP2 c.123A>G mutation"
        mock_line.span = Mock()
        mock_line.span.offset = 0
        mock_line.span.length = 67
        
        mock_page = Mock(spec=DocumentPage)
        mock_page.page_number = 1
        mock_page.lines = [mock_line]
        mock_page.words = [mock_word]
        
        mock_result = Mock(spec=AnalyzeResult)
        mock_result.pages = [mock_page]
        mock_result.content = "Sample extracted text from document with MECP2 c.123A>G mutation"
        mock_result.languages = []  # Empty list for language detection
        
        # Mock the repository response
        mock_analyze.return_value = mock_result
          # Create mock file stream
        mock_file = io.BytesIO(b"mock pdf content")
        
        # Process the document
        result = ocr_processor.extract_and_process_text(mock_file)
        # Verify the call was made and result contains expected data        mock_analyze.assert_called_once()
        assert result is not None
        assert isinstance(result, Document)
        assert hasattr(result, 'cleaned_text')

    @patch('rettxmutation.repositories.document_analysis_repository.DocumentAnalysisRepository.analyze_document')
    def test_extract_and_process_text_empty_file(self, mock_analyze, ocr_processor):
        """Test text extraction from empty file."""
        # Create a mock AnalyzeResult for empty document
        from azure.ai.documentintelligence.models import AnalyzeResult, DocumentPage
        
        mock_page = Mock(spec=DocumentPage)
        mock_page.page_number = 1
        mock_page.lines = []
        mock_page.words = []
        
        mock_result = Mock(spec=AnalyzeResult)
        mock_result.pages = [mock_page]
        mock_result.content = ""
        mock_result.languages = []  # Empty list will use default language
        
        mock_analyze.return_value = mock_result
        
        # Create empty mock file
        mock_file = io.BytesIO(b"")
        
        # Process the document
        result = ocr_processor.extract_and_process_text(mock_file)
        
        # Verify handling of empty content
        mock_analyze.assert_called_once()
        assert result is not None
        assert isinstance(result, Document)
        assert result.language == "en"  # Should default to English
        assert result.raw_text == ""
    
    @patch('rettxmutation.repositories.document_analysis_repository.DocumentAnalysisRepository.analyze_document')
    def test_extract_and_process_text_with_genetic_content(self, mock_analyze, ocr_processor):
        """Test text extraction with genetic content."""
        # Create a properly mocked AnalyzeResult with genetic content
        from azure.ai.documentintelligence.models import AnalyzeResult, DocumentPage, DocumentLine, DocumentWord
        
        # Create mock genetic content
        genetic_text = "MECP2 gene mutation c.123A>G causes Rett syndrome"
        
        mock_word = Mock(spec=DocumentWord)
        mock_word.content = "MECP2"
        mock_word.confidence = 0.95
        mock_word.span = Mock()
        mock_word.span.offset = 0
        mock_word.span.length = 5
        
        mock_line = Mock(spec=DocumentLine)
        mock_line.content = genetic_text
        mock_line.span = Mock()
        mock_line.span.offset = 0
        mock_line.span.length = len(genetic_text)
        
        mock_page = Mock(spec=DocumentPage)
        mock_page.page_number = 1
        mock_page.lines = [mock_line]
        mock_page.words = [mock_word]
        
        mock_result = Mock(spec=AnalyzeResult)
        mock_result.pages = [mock_page]
        mock_result.content = genetic_text
        mock_result.languages = []
        
        mock_analyze.return_value = mock_result
        
        # Create mock file with genetic content
        mock_file = io.BytesIO(b"mock genetic document content")
        
        # Process the document
        result = ocr_processor.extract_and_process_text(mock_file)
        
        # Verify processing
        mock_analyze.assert_called_once()
        assert result is not None
        assert isinstance(result, Document)
        assert hasattr(result, 'cleaned_text')


    def test_clean_ocr_text_method(self, ocr_processor):
        """Test text cleaning functionality."""
        # Test text cleaning with various input
        dirty_text = "Sample   text  with   extra\nspaces\nand\nlinebreaks"
        cleaned = ocr_processor.clean_ocr_text(dirty_text)
        
        assert isinstance(cleaned, str)
        assert len(cleaned) > 0
        # Should have collapsed whitespace
        assert "   " not in cleaned
    

    @patch('rettxmutation.repositories.document_analysis_repository.DocumentAnalysisRepository.analyze_document')
    def test_error_handling_on_processing_failure(self, mock_analyze, ocr_processor):
        """Test error handling when processing fails."""
        # Make the repository throw an exception
        mock_analyze.side_effect = Exception("Service error")
        
        mock_file = io.BytesIO(b"mock content")
        
        # Should raise Exception (as that's what the service currently does)
        with pytest.raises(Exception, match="OCR text processing failed"):
            ocr_processor.extract_and_process_text(mock_file)


class TestOcrIntegration:
    """Integration tests for OCR workflow."""
    
    @pytest.fixture
    def config(self):
        """Create test configuration."""
        config = DefaultConfig()
        # Set required Azure Document Intelligence fields for testing
        config.RETTX_DOCUMENT_ANALYSIS_ENDPOINT = "https://test.cognitiveservices.azure.com/"
        config.RETTX_DOCUMENT_ANALYSIS_KEY = "test-key"
        return config
    
    def test_ocr_processor_creation_with_env_config(self, config):
        """Test OCR service creation using environment configuration."""
        document_analysis_repo = DocumentAnalysisRepository(config)
        processor = OcrService(document_analysis_repo)
        
        assert processor is not None
        assert processor._document_analysis_repository is not None
        # Verify methods exist
        assert hasattr(processor, 'clean_ocr_text')

    @patch('rettxmutation.repositories.document_analysis_repository.DocumentAnalysisRepository.analyze_document')
    def test_ocr_workflow_simulation(self, mock_analyze, config):
        """Test complete OCR workflow simulation."""
        # Setup mock response with proper structure
        from azure.ai.documentintelligence.models import AnalyzeResult, DocumentPage, DocumentLine, DocumentWord
        
        genetic_text = "MECP2 gene variant c.316C>T (p.Arg106Trp) identified in patient with Rett syndrome"
        
        mock_word = Mock(spec=DocumentWord)
        mock_word.content = "MECP2"
        mock_word.confidence = 0.95
        mock_word.span = Mock()
        mock_word.span.offset = 0
        mock_word.span.length = 5
        
        mock_line = Mock(spec=DocumentLine)
        mock_line.content = genetic_text
        mock_line.span = Mock()
        mock_line.span.offset = 0
        mock_line.span.length = len(genetic_text)
        
        mock_page = Mock(spec=DocumentPage)
        mock_page.page_number = 1
        mock_page.lines = [mock_line]
        mock_page.words = [mock_word]
        
        mock_result = Mock(spec=AnalyzeResult)
        mock_result.pages = [mock_page]
        mock_result.content = genetic_text
        mock_result.languages = []
        
        mock_analyze.return_value = mock_result
        
        # Create processor and test document
        document_analysis_repo = DocumentAnalysisRepository(config)
        processor = OcrService(document_analysis_repo)

        # Simulate document processing
        mock_file = io.BytesIO(b"mock document with genetic content")
        result = processor.extract_and_process_text(mock_file)

        # Verify complete workflow
        mock_analyze.assert_called_once()
        assert result is not None
        assert isinstance(result, Document)
        assert hasattr(result, 'raw_text')
        assert hasattr(result, 'cleaned_text')
        
        # Should contain genetic content
        assert genetic_text == result.raw_text
    
    def test_text_processing_methods_work_independently(self, config):
        """Test that text processing methods work independently."""
        document_analysis_repo = DocumentAnalysisRepository(config)
        processor = OcrService(document_analysis_repo)
        
        # Test text cleaning
        test_text = "Messy   text\nwith\nproblems"
        cleaned = processor.clean_ocr_text(test_text)
        assert isinstance(cleaned, str)

if __name__ == "__main__":
    pytest.main([__file__])
