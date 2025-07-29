import pytest
from pydantic import ValidationError
from rettxmutation.models.document import Document, WordData, LineData
from rettxmutation.models.keyword_collection import Keyword


# Tests for the Document model
def test_document_initialization():
    # Test successful initialization
    word_data = [
        WordData(word="test", confidence=0.9, page_number=1),
        WordData(word="example", confidence=0.8, page_number=1)
    ]
    line_data = [
        LineData(line="Line 1", page_number=1, length=5),
        LineData(line="Line 123", page_number=1, length=8)
    ]
    doc = Document(
        raw_text="Sample text",
        cleaned_text="Clean text",
        summary="Summary",
        language="en",
        words=word_data,
        lines=line_data,
    )
    assert doc.raw_text == "Sample text"
    assert doc.cleaned_text == "Clean text"
    assert doc.language == "en"
    assert len(doc.words) == 2
    assert len(doc.lines) == 2
    assert doc.words[0].word == "test"
    assert doc.words[1].word == "example"
    assert doc.lines[0].line == "Line 1"
    assert doc.lines[0].length == 5
    assert doc.lines[1].line == "Line 123"
    assert doc.lines[1].length == 8


def test_document_invalid_data():
    # Test validation errors
    with pytest.raises(ValidationError):
        Document(raw_text="Sample", language="en", words="invalid_type")


def test_find_word_confidence():
    word_data = [
        WordData(word="test", confidence=0.9, page_number=1),
        WordData(word="example", confidence=0.8, page_number=1)
    ]
    line_data = [
        LineData(line="Line 1", page_number=1, length=5),
        LineData(line="Line 2", page_number=1, length=5)
    ]
    doc = Document(raw_text="Sample", language="en", words=word_data, lines=line_data)

    assert doc.find_word_confidence("test") == 0.9
    assert doc.find_word_confidence("example") == 0.8
    assert doc.find_word_confidence("missing") is None


def test_dump_all_content():
    doc = Document(
        raw_text="Sample",
        cleaned_text="Clean text",
        language="en",
        words=[],
        lines=[]
    )

    content = doc.dump_all_content()
    assert content["cleaned_text"] == "Clean text"
    assert content["language"] == "en"


def test_dump_plain_text():
    doc = Document(
        raw_text="Sample",
        cleaned_text="Clean text",
        language="en",
        words=[],
        lines=[]
    )

    # Since keywords are no longer part of Document, dump_plain_text() only returns cleaned_text
    assert doc.dump_plain_text() == "Clean text"

    # Test with different text
    doc_other = Document(raw_text="Other sample", cleaned_text="Other clean text", language="en", words=[], lines=[])
    assert doc_other.dump_plain_text() == "Other clean text"
