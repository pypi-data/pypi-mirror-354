from unittest.mock import patch, MagicMock

from rettxmutation.config import DefaultConfig
from rettxmutation.services.ai_search import AISearchService


@patch("rettxmutation.repositories.ai_search_repository.QueryType")
@patch("rettxmutation.repositories.ai_search_repository.SearchClient")
def test_semantic_search_calls_client(mock_client_class, mock_query_type):
    config = DefaultConfig()
    config.RETTX_AI_SEARCH_SERVICE = "test-service"
    config.RETTX_AI_SEARCH_API_KEY = "test-key"
    config.RETTX_AI_SEARCH_INDEX_NAME = "my-index"
    config.RETTX_AI_SEARCH_SEMANTIC_CONFIGURATION = "default"

    mock_client = MagicMock()
    mock_client.search.return_value = ["result1", "result2"]
    mock_client_class.return_value = mock_client

    service = AISearchService(config)
    results = service.search("hello world")

    mock_client_class.assert_called_once_with(
        endpoint="https://test-service.search.windows.net",
        index_name="my-index",
        credential=mock_client_class.call_args.kwargs["credential"],
    )
    mock_client.search.assert_called_once_with(
        search_text="hello world",
        query_type=mock_query_type.SEMANTIC,
        semantic_configuration_name="default",
    )
    assert results == ["result1", "result2"]

@patch("rettxmutation.repositories.ai_search_repository.QueryType")
@patch("rettxmutation.repositories.ai_search_repository.SearchClient")
def test_keyword_search_calls_client(mock_client_class, mock_query_type):
    config = DefaultConfig()
    config.RETTX_AI_SEARCH_SERVICE = "test-service"
    config.RETTX_AI_SEARCH_API_KEY = "test-key"
    config.RETTX_AI_SEARCH_INDEX_NAME = "my-index"

    mock_client = MagicMock()
    mock_client.search.return_value = ["kw"]
    mock_client_class.return_value = mock_client
    service = AISearchService(config)
    results = service.keyword_search(query="gene", select_fields=None, search_mode="all")

    mock_client.search.assert_called_once_with(
        search_text="gene",
        query_type=mock_query_type.SIMPLE,
        search_fields=["literal_mutation_tokens"],
        search_mode="all",
    )
    assert results == ["kw"]


@patch("rettxmutation.repositories.ai_search_repository.QueryType")
@patch("rettxmutation.repositories.ai_search_repository.SearchClient")
def test_text_search_calls_client(mock_client_class, mock_query_type):
    config = DefaultConfig()
    config.RETTX_AI_SEARCH_SERVICE = "test-service"
    config.RETTX_AI_SEARCH_API_KEY = "test-key"
    config.RETTX_AI_SEARCH_INDEX_NAME = "my-index"

    mock_client = MagicMock()
    mock_client.search.return_value = ["txt"]
    mock_client_class.return_value = mock_client

    service = AISearchService(config)
    results = service.text_search("field:value")

    mock_client.search.assert_called_once_with(
        search_text="field:value",
        query_type=mock_query_type.FULL,
        search_fields=["literal_mutation_tokens"],
    )
    assert results == ["txt"]