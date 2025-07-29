from typing import List, Any, Optional
from urllib.parse import urlencode
from enum import Enum
import logging

import feedparser
from fastmcp import FastMCP
from mcp.shared.exceptions import McpError
from mcp.types import ErrorData, INVALID_PARAMS, INTERNAL_ERROR
from pydantic import BaseModel, Field, ConfigDict

# Configure logging
logger = logging.getLogger(__name__)

# Create an MCP server instance
mcp = FastMCP("Google News Server")

# Google News RSS base URLs
GOOGLE_NEWS_BASE_URL = "https://news.google.com/rss"
GOOGLE_NEWS_SEARCH_URL = f"{GOOGLE_NEWS_BASE_URL}/search"
GOOGLE_NEWS_TOPICS_URL = f"{GOOGLE_NEWS_BASE_URL}/headlines/section/topic"


# Enum for topic IDs
class TopicId(str, Enum):
    """Available Google News topics."""

    TOP = "TOP"  # トップニュース (default)
    NATION = "NATION"  # 国内
    WORLD = "WORLD"  # 国際
    BUSINESS = "BUSINESS"  # ビジネス
    TECHNOLOGY = "TECHNOLOGY"  # テクノロジー
    ENTERTAINMENT = "ENTERTAINMENT"  # エンタメ
    SPORTS = "SPORTS"  # スポーツ
    SCIENCE = "SCIENCE"  # 科学
    HEALTH = "HEALTH"  # 健康


# Pydantic models
class NewsArticle(BaseModel):
    """Model for a news article."""

    model_config = ConfigDict(extra="forbid")

    title: str = Field(description="Article title")
    link: str = Field(description="Article URL")
    published: str = Field(description="Publication date")
    description: str = Field(description="Article description/summary")
    source: str = Field(description="News source name")


class SearchRequest(BaseModel):
    """Model for search request parameters."""

    model_config = ConfigDict(extra="forbid")

    query: str = Field(description="Search query string")
    limit: int = Field(
        default=10, ge=1, le=100, description="Maximum number of articles to return"
    )
    hl: str = Field(default="ja", description="Language code")
    gl: Optional[str] = Field(default=None, description="Geographic location code")


class TopicsRequest(BaseModel):
    """Model for topics request parameters."""

    model_config = ConfigDict(extra="forbid")

    topic_id: TopicId = Field(
        default=TopicId.TOP, description="Topic ID for specific news category"
    )
    limit: int = Field(
        default=10, ge=1, le=100, description="Maximum number of articles to return"
    )
    hl: str = Field(default="ja", description="Language code")
    gl: Optional[str] = Field(default=None, description="Geographic location code")


def parse_feed_entries(entries: List[Any], limit: int) -> List[NewsArticle]:
    """
    Parse RSS feed entries and return structured news articles.

    Args:
        entries: List of RSS feed entries
        limit: Maximum number of articles to return

    Returns:
        List of NewsArticle models containing article information
    """

    logger.info(f"Parsing {len(entries)} feed entries with limit {limit}")
    articles = []

    for i, entry in enumerate(entries[:limit]):
        try:
            # Extract article data
            title = entry.get("title", "")
            link = entry.get("link", "")
            published = entry.get("published", "")
            description = entry.get("summary", "")
            source = (
                entry.get("source", {}).get("title", "") if "source" in entry else ""
            )

            # Clean up the description (remove HTML tags if present)
            if description:
                # Simple HTML tag removal
                import re

                description = re.sub("<[^<]+?>", "", description)

            # Create NewsArticle model
            article = NewsArticle(
                title=title,
                link=link,
                published=published,
                description=description,
                source=source,
            )

            articles.append(article)

        except Exception as e:
            logger.error(f"Failed to parse entry {i}: {str(e)}")
            continue

    return articles


@mcp.tool()
async def google_news_search(
    query: str, limit: int = 10, hl: str = "ja", gl: Optional[str] = None
) -> List[NewsArticle]:
    """
    Search for news articles using a query.

    This function searches Google News RSS feed for articles matching the query.

    Args:
        query: Search query string
        limit: Maximum number of articles to return (default: 10)
        hl: Language code (default: "ja")
        gl: Geographic location code (optional)

    Returns:
        List of NewsArticle models with title, link, published date, description, and source

    Raises:
        McpError: When query is invalid or fetching fails
    """
    # Validate and create request model
    try:
        request = SearchRequest(query=query, limit=limit, hl=hl, gl=gl)
    except Exception as e:
        logger.error(f"Search request validation failed: {str(e)}")
        raise McpError(
            ErrorData(code=INVALID_PARAMS, message=f"Invalid parameters: {str(e)}")
        )

    try:
        # Build the search URL with query parameters
        params = {
            "q": request.query,
            "hl": request.hl,  # Language
        }

        # Add geographic location if provided
        if request.gl:
            params["gl"] = request.gl

        url = f"{GOOGLE_NEWS_SEARCH_URL}?{urlencode(params)}"

        # Parse the RSS feed
        feed = feedparser.parse(url)

        # Check for feed parsing errors
        if feed.bozo:
            logger.error(f"Feed parsing error: {feed.bozo_exception}")
            raise McpError(
                ErrorData(
                    code=INTERNAL_ERROR,
                    message=f"Failed to parse RSS feed: {feed.bozo_exception}",
                )
            )

        # Parse and return the entries
        return parse_feed_entries(feed.entries, request.limit)

    except McpError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in news search: {str(e)}")
        raise McpError(
            ErrorData(
                code=INTERNAL_ERROR,
                message=f"Unexpected error while searching Google News: {str(e)}",
            )
        )


@mcp.tool()
async def google_news_topics(
    topic_id: TopicId = TopicId.TOP,
    limit: int = 10,
    hl: str = "ja",
    gl: Optional[str] = None,
) -> List[NewsArticle]:
    """
    Get news articles by topic.

    This function fetches news articles from a specific Google News topic.

    Available topics:
    - TOP: トップニュース (default)
    - NATION: 国内
    - WORLD: 国際
    - BUSINESS: ビジネス
    - TECHNOLOGY: テクノロジー
    - ENTERTAINMENT: エンタメ
    - SPORTS: スポーツ
    - SCIENCE: 科学
    - HEALTH: 健康

    Args:
        topic_id: Topic ID for specific news category (default: TOP)
        limit: Maximum number of articles to return (default: 10)
        hl: Language code (default: "ja")
        gl: Geographic location code (optional)

    Returns:
        List of NewsArticle models with title, link, published date, description, and source

    Raises:
        McpError: When topic_id is invalid or fetching fails
    """
    # Validate and create request model
    try:
        request = TopicsRequest(topic_id=topic_id, limit=limit, hl=hl, gl=gl)
    except Exception as e:
        logger.error(f"Topics request validation failed: {str(e)}")
        raise McpError(
            ErrorData(code=INVALID_PARAMS, message=f"Invalid parameters: {str(e)}")
        )

    try:
        # Build the topic URL
        params = {
            "hl": request.hl,  # Language
        }

        # Add geographic location if provided
        if request.gl:
            params["gl"] = request.gl

        if request.topic_id == TopicId.TOP:
            url = f"{GOOGLE_NEWS_BASE_URL}?{urlencode(params)}"
        else:
            url = (
                f"{GOOGLE_NEWS_TOPICS_URL}/{request.topic_id.value}?{urlencode(params)}"
            )

        # Parse the RSS feed
        feed = feedparser.parse(url)

        # Check for feed parsing errors
        if feed.bozo:
            logger.error(f"Feed parsing error: {feed.bozo_exception}")
            raise McpError(
                ErrorData(
                    code=INTERNAL_ERROR,
                    message=f"Failed to parse RSS feed: {feed.bozo_exception}",
                )
            )

        # Check if feed is empty (might indicate invalid topic ID)
        if not feed.entries:
            logger.error(f"No articles found for topic {topic_id.value}")
            raise McpError(
                ErrorData(
                    code=INVALID_PARAMS,
                    message="No articles found. The topic ID might be invalid.",
                )
            )

        # Parse and return the entries
        return parse_feed_entries(feed.entries, request.limit)

    except McpError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in topics request: {str(e)}")
        raise McpError(
            ErrorData(
                code=INTERNAL_ERROR,
                message=f"Unexpected error while fetching topic news: {str(e)}",
            )
        )
