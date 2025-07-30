import logging
from typing import Optional, List
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


# Word data model, extracted from a document by OCR tool
class WordData(BaseModel):
    word: str = Field(..., description="The word extracted from the document")
    confidence: float = Field(..., description="Confidence score of the extracted word")
    page_number: int = Field(..., description="Page number where the word was found")
    offset: int = Field(None, description="Offset of the word in the page")
    length: int = Field(None, description="Length of the word")

# Line data model, extracted from a document by OCR tool
class LineData(BaseModel):
    line: str = Field(..., description="The line extracted from the document")
    page_number: int = Field(..., description="Page number where the line was found")
    length: int = Field(None, description="Length of the line")


# Document model
class Document(BaseModel):
    raw_text: str = Field(..., description="The extracted text from the document")
    cleaned_text: Optional[str] = Field("", description="The cleaned version of the extracted text")
    summary: Optional[str] = Field("", description="Summary of the document content")
    language: str = Field(..., description="Language of the extracted text")
    words: List[WordData] = Field(..., description="List of extracted words with confidence scores")
    lines: List[LineData] = Field(..., description="List of extracted lines")

    def find_word_confidence(self, word_to_find: str) -> Optional[float]:
        """
        Finds a word in the word data and returns its confidence value.

        :param word_to_find: The word to search for in the words data.
        :return: The confidence score of the word if found, else None.
        """
        for word_data in self.words:
            if word_to_find in word_data.word:
                return word_data.confidence
        return None

    def dump_all_content(self) -> dict:
        """
        Dump the document content into a dictionary for serialization.
        """
        return {
            "cleaned_text": self.cleaned_text,
            "language": self.language
        }

    def dump_plain_text(self) -> str:
        """
        Generates a plain text output from cleaned_text.
        """
        return self.cleaned_text.strip()
