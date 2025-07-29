"""
Simple tests for Google News MCP Server with error logging
"""

from mcp_server_google_news.server import (
    TopicId,
    NewsArticle,
    parse_feed_entries,
    SearchRequest,
    TopicsRequest,
)


class TestBasicFunctionality:
    """Test basic functionality"""

    def test_news_article_creation(self):
        """Test NewsArticle model creation"""
        article = NewsArticle(
            title="Test Title",
            link="https://example.com",
            published="2025-01-01",
            description="Test description",
            source="Test Source",
        )
        assert article.title == "Test Title"
        assert article.link == "https://example.com"

    def test_search_request_defaults(self):
        """Test SearchRequest default values"""
        request = SearchRequest(query="test")
        assert request.query == "test"
        assert request.limit == 10
        assert request.hl == "ja"
        assert request.gl is None

    def test_topics_request_defaults(self):
        """Test TopicsRequest default values"""
        request = TopicsRequest()
        assert request.topic_id == TopicId.TOP
        assert request.limit == 10
        assert request.hl == "ja"
        assert request.gl is None

    def test_parse_feed_entries_basic(self):
        """Test basic feed parsing"""
        mock_entries = [
            {
                "title": "Test Title",
                "link": "https://example.com",
                "published": "2025-01-01",
                "summary": "Test summary",
                "source": {"title": "Test Source"},
            }
        ]

        result = parse_feed_entries(mock_entries, 10)

        assert len(result) == 1
        assert isinstance(result[0], NewsArticle)
        assert result[0].title == "Test Title"
