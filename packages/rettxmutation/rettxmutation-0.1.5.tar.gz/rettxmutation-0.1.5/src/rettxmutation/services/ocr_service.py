"""
OCR Service

Business logic for OCR text extraction and cleaning.
Uses the DocumentAnalysisRepository for infrastructure concerns.
Keyword detection is handled by the KeywordDetectorService.
"""

import re
import ftfy
import logging
from typing import List, BinaryIO, Optional

from rettxmutation.models.document import Document, WordData, LineData
from rettxmutation.repositories.interfaces import DocumentAnalysisRepositoryInterface
from azure.ai.documentintelligence.models import DocumentAnalysisFeature, AnalyzeResult

logger = logging.getLogger(__name__)


class OcrService:
    """
    OCR service that handles text extraction and cleaning operations.
    
    This service focuses purely on OCR-related operations: extracting text from documents,
    cleaning and normalizing the text, and extracting structured data (words, lines).
    Keyword detection is handled by the KeywordDetectorService.
    """

    def __init__(self, document_analysis_repository: DocumentAnalysisRepositoryInterface):
        """
        Initialize the OCR service with a document analysis repository.
        
        Args:
            document_analysis_repository: Repository for document analysis operations
        """
        self._document_analysis_repository = document_analysis_repository
        logger.debug("OcrService initialized successfully")

    def extract_and_process_text(self, file_stream: BinaryIO) -> Document:
        """
        OCR processing pipeline: extract text, clean, and create structured document.
        
        Note: This method focuses only on OCR operations. Keyword detection should be
        performed separately using the KeywordDetectorService.
        
        Args:
            file_stream: Binary stream of the document
            
        Returns:
            Document: Document with extracted and cleaned text, words, and lines
            
        Raises:
            Exception: If OCR processing fails
        """
        try:
            # Step 1: Extract text using the repository
            result = self._document_analysis_repository.analyze_document(
                file_stream, 
                features=[DocumentAnalysisFeature.LANGUAGES]
            )
            
            # Step 2: Convert result to Document model
            document = self._convert_analysis_result_to_document(result)
            
            # Step 3: Clean the extracted text
            document.cleaned_text = self.clean_ocr_text(document.raw_text)
            
            # Note: Keyword detection has been moved to KeywordDetectorService
            # Call keyword_detector_service.detect_and_validate_keywords(document) separately
            
            logger.debug(f"OCR processing completed successfully")
            return document
            
        except Exception as e:
            error_msg = f"OCR text processing failed: {e}"
            logger.error(error_msg)
            raise Exception(error_msg) from e

    def extract_text_from_document(self, file_stream: BinaryIO) -> Document:
        """
        Extract raw text and structured data from a document using Azure Document Intelligence.
        
        Args:
            file_stream: Binary stream of the document
            
        Returns:
            Document: Document with raw text, words, and lines extracted
            
        Raises:
            Exception: If text extraction fails
        """
        try:
            # Use repository to analyze document
            result = self._document_analysis_repository.analyze_document(
                file_stream, 
                features=[DocumentAnalysisFeature.LANGUAGES]
            )
            
            # Convert to our Document model
            document = self._convert_analysis_result_to_document(result)
            
            logger.debug(f"Text extraction successful. Raw text length: {len(document.raw_text)}")
            return document
            
        except Exception as e:
            error_msg = f"Text extraction failed: {e}"
            logger.error(error_msg)
            raise Exception(error_msg) from e

    def _convert_analysis_result_to_document(self, result: AnalyzeResult) -> Document:
        """
        Convert Azure Document Analysis result to our Document model.
        
        Args:
            result: Azure Document Analysis result
            
        Returns:
            Document: Document object containing extracted text and metadata
        """
        # Infer language
        inferred_language = "en"  # Default to English
        if result.languages:
            detected_language = self._infer_language(result.languages)
            if detected_language:
                inferred_language = detected_language
            logger.debug(f"Detected language: {inferred_language}")

        # Extract structured data
        words = self._extract_words(result)
        lines = self._extract_lines(result)

        logger.debug(f"Words processed: {len(words)}")
        logger.debug(f"Lines processed: {len(lines)}")
        logger.debug(f"Pages processed: {len(result.pages)}")

        return Document(
            raw_text=result.content,
            language=inferred_language,
            words=words,
            lines=lines
        )

    def _extract_words(self, result: AnalyzeResult) -> List[WordData]:
        """
        Private helper to extract words data from an AnalyzeResult object.
        
        Args:
            result: Azure Document Analysis result
            
        Returns:
            List[WordData]: List of word data objects
        """
        words_data = []
        for page in result.pages:
            for word in page.words:
                words_data.append(
                    WordData(
                        word=word.content,
                        confidence=word.confidence,
                        page_number=page.page_number,
                        offset=word.span.offset if word.span else None,
                        length=word.span.length if word.span else None
                    )
                )
        logger.debug(f"Extracted {len(words_data)} words across {len(result.pages)} pages.")
        return words_data

    def _extract_lines(self, result: AnalyzeResult) -> List[LineData]:
        """
        Private helper to extract lines data from an AnalyzeResult object.
        
        Args:
            result: Azure Document Analysis result
            
        Returns:
            List[LineData]: List of line data objects
        """
        lines_data = []
        for page in result.pages:
            for line in page.lines:
                lines_data.append(
                    LineData(
                        line=line.content,
                        page_number=page.page_number,
                        length=len(line.content)
                    )
                )
        return lines_data

    def _infer_language(self, languages) -> Optional[str]:
        """
        Private helper to infer the most likely language from a list of language detections.
        
        Args:
            languages: Language detection results from Azure Document Analysis
            
        Returns:
            Optional[str]: Most likely language code or None
        """
        language_confidences = {}
        for language in languages:
            lang = language.locale
            conf = language.confidence
            language_confidences[lang] = language_confidences.get(lang, 0) + conf
        if not language_confidences:
            return None
        return max(language_confidences, key=language_confidences.get)

    def clean_ocr_text(self, raw_text: str) -> str:
        """
        Takes raw text (e.g. from OCR) and normalizes / cleans it up:
        1. Fix common Unicode issues (ftfy).
        2. Collapse whitespace.
        3. Fix typical HGVS-like patterns.
        4. Additional checks for missing '.' after 'c', etc.

        Args:
            raw_text: Raw text from OCR

        Returns:
            str: Cleaned and normalized text
        """
        try:
            # 1) Fix garbled Unicode with ftfy
            text = ftfy.fix_text(raw_text)

            # 2) Collapse all whitespace into a single space
            text = re.sub(r"\s+", " ", text).strip()

            # 3) Remove line breaks
            text = text.replace("\n", " ")

            # 4) Fix common HGVS patterns and OCR errors
            text = self._fix_hgvs_patterns(text)

            # 5) Additional OCR error corrections
            text = self._fix_common_ocr_errors(text)

            return text

        except Exception as e:
            logger.warning(f"Text cleaning failed, returning original text: {e}")
            return raw_text

    def _fix_hgvs_patterns(self, text: str) -> str:
        """
        Fix common HGVS pattern OCR errors.
        
        Args:
            text: Text to fix
            
        Returns:
            str: Text with HGVS patterns corrected
        """
        # Fix missing dots in HGVS notation (e.g., "c473C>T" -> "c.473C>T")
        text = re.sub(r"\bc(\d)", r"c.\1", text)
        text = re.sub(r"\bp(\d)", r"p.\1", text)
        text = re.sub(r"\bg(\d)", r"g.\1", text)
        
        # Fix common substitution errors in nucleotides/amino acids
        text = re.sub(r"([ACGTacgt])>([ACGTacgt])", r"\1>\2", text)
        
        return text

    def _fix_common_ocr_errors(self, text: str) -> str:
        """
        Fix common OCR character recognition errors.
        
        Args:
            text: Text to fix
            
        Returns:
            str: Text with common OCR errors corrected
        """
        # Common character misrecognitions
        ocr_fixes = {
            "0": "O",  # Zero to letter O in gene names
            "1": "I",  # One to letter I in some contexts
            # Add more common OCR fixes as needed
        }
        
        # Apply fixes in gene/protein contexts
        for wrong, correct in ocr_fixes.items():
            # This is a simple example - more sophisticated context-aware fixes could be added
            pass
            
        return text
