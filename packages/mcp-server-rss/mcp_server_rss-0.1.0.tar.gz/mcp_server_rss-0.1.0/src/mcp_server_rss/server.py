from typing import List, Any, Optional, Dict
import logging
from urllib.parse import urlparse
import re

import feedparser
from fastmcp import FastMCP
from mcp.shared.exceptions import McpError
from mcp.types import ErrorData, INVALID_PARAMS, INTERNAL_ERROR
from pydantic import BaseModel, Field, ConfigDict, field_validator

from .feed_detect import FeedDetector

# Configure logging
logger = logging.getLogger(__name__)

# Create an MCP server instance
mcp = FastMCP("RSS Feed Server")


# Pydantic models
class FeedEntry(BaseModel):
    """Model for a feed entry/article."""

    model_config = ConfigDict(extra="forbid")

    title: str = Field(description="Entry title")
    link: str = Field(description="Entry URL")
    published: str = Field(description="Publication date")
    description: str = Field(description="Entry description/summary")
    author: str = Field(description="Entry author", default="")
    guid: str = Field(description="Entry GUID/ID", default="")


class FeedInfo(BaseModel):
    """Model for feed metadata."""

    model_config = ConfigDict(extra="forbid")

    title: str = Field(description="Feed title")
    link: str = Field(description="Feed website URL")
    description: str = Field(description="Feed description")
    language: str = Field(description="Feed language", default="")
    last_updated: str = Field(description="Last update time", default="")
    generator: str = Field(description="Feed generator", default="")
    feed_type: str = Field(description="Feed type (rss/atom)", default="")


class FeedResponse(BaseModel):
    """Model for complete feed response."""

    model_config = ConfigDict(extra="forbid")

    feed_info: FeedInfo = Field(description="Feed metadata")
    entries: List[FeedEntry] = Field(description="Feed entries")
    metadata: Dict[str, Any] = Field(description="Response metadata")


class FeedRequest(BaseModel):
    """Model for feed request parameters."""

    model_config = ConfigDict(extra="forbid")

    url: str = Field(description="Target URL")
    limit: int = Field(
        default=10, ge=1, le=100, description="Maximum number of entries to return"
    )

    @field_validator("url")
    @classmethod
    def validate_url(cls, v):
        """Validate URL format."""
        if not v.strip():
            raise ValueError("URL cannot be empty")

        # Basic URL validation
        parsed = urlparse(v)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError("Invalid URL format")

        if parsed.scheme not in ["http", "https"]:
            raise ValueError("Only HTTP and HTTPS URLs are supported")

        return v.strip()


def clean_html(text: Optional[str]) -> str:
    """Remove HTML tags from text."""
    if not text:
        return ""

    # Simple HTML tag removal
    clean_text = re.sub(r"<[^<]+?>", "", text)

    # Clean up whitespace
    clean_text = re.sub(r"\s+", " ", clean_text).strip()

    return clean_text


def parse_feed_entries(entries: List[Any], limit: int) -> List[FeedEntry]:
    """
    Parse RSS/Atom feed entries and return structured data.

    Args:
        entries: List of feed entries
        limit: Maximum number of entries to return

    Returns:
        List of FeedEntry models containing entry information
    """
    logger.info(f"Parsing {len(entries)} feed entries with limit {limit}")
    parsed_entries = []

    for i, entry in enumerate(entries[:limit]):
        try:
            # Extract entry data with fallbacks
            title = entry.get("title", "No title")
            link = entry.get("link", "")
            published = entry.get("published", entry.get("updated", ""))

            # Handle description (summary, content, or description)
            description = ""
            if "summary" in entry:
                description = entry["summary"]
            elif hasattr(entry, "summary"):
                description = entry.summary
            elif hasattr(entry, "content") and entry.content:
                # Take first content item if it's a list
                content = (
                    entry.content[0]
                    if isinstance(entry.content, list)
                    else entry.content
                )
                description = (
                    content.get("value", "")
                    if hasattr(content, "get")
                    else str(content)
                )
            elif hasattr(entry, "description"):
                description = entry.description
            elif "description" in entry:
                description = entry["description"]

            # Clean HTML from description
            description = clean_html(description)

            # Extract author
            author = ""
            if "author" in entry:
                author = entry["author"]
            elif hasattr(entry, "author"):
                author = entry.author
            elif hasattr(entry, "author_detail") and entry.author_detail:
                author = entry.author_detail.get("name", "")

            # Extract GUID
            guid = entry.get("id", entry.get("guid", ""))

            # Create FeedEntry model
            feed_entry = FeedEntry(
                title=clean_html(title),
                link=link,
                published=published,
                description=description,
                author=author,
                guid=guid,
            )

            parsed_entries.append(feed_entry)

        except Exception as e:
            logger.error(f"Failed to parse entry {i}: {str(e)}")
            continue

    return parsed_entries


def extract_feed_info(feed_data: Any) -> FeedInfo:
    """Extract feed metadata."""
    feed = feed_data.feed if hasattr(feed_data, "feed") else {}

    return FeedInfo(
        title=clean_html(feed.get("title", "Unknown Feed")),
        link=feed.get("link", ""),
        description=clean_html(feed.get("description", "")),
        language=feed.get("language", ""),
        last_updated=feed.get("updated", ""),
        generator=feed.get("generator", ""),
        feed_type=feed.get("version", ""),
    )


@mcp.tool()
async def feed(url: str, limit: int = 10) -> FeedResponse:
    """
    Detect and parse RSS/Atom feeds from a URL.

    This function will:
    1. Try to detect RSS/Atom feeds from the given URL
    2. Parse the first valid feed found
    3. Return structured feed data with entries

    Args:
        url: Target URL to analyze for feeds
        limit: Maximum number of entries to return (default: 10)

    Returns:
        FeedResponse containing feed metadata and entries

    Raises:
        McpError: When URL is invalid, no feeds found, or parsing fails
    """
    # Validate request parameters
    try:
        request = FeedRequest(url=url, limit=limit)
    except Exception as e:
        logger.error(f"Feed request validation failed: {str(e)}")
        raise McpError(
            ErrorData(code=INVALID_PARAMS, message=f"Invalid parameters: {str(e)}")
        )

    detector = None
    try:
        # Initialize feed detector
        detector = FeedDetector(timeout=30)

        # Detect feeds from the URL
        logger.info(f"Detecting feeds from URL: {request.url}")
        feed_urls = await detector.detect_feeds(request.url)

        if not feed_urls:
            raise McpError(
                ErrorData(
                    code=INTERNAL_ERROR,
                    message=f"No RSS/Atom feeds found at {request.url}",
                )
            )

        logger.info(f"Found {len(feed_urls)} potential feeds")

        # Try to parse each detected feed until we find a valid one
        last_error = None
        for feed_url in feed_urls:
            try:
                logger.info(f"Attempting to parse feed: {feed_url}")

                # Parse the RSS/Atom feed
                feed_data = feedparser.parse(feed_url)

                # Check for parsing errors
                if feed_data.bozo and hasattr(feed_data, "bozo_exception"):
                    logger.warning(
                        f"Feed parsing warning for {feed_url}: {feed_data.bozo_exception}"
                    )
                    # Continue anyway - some feeds work despite bozo flag

                # Check if we have entries
                if not hasattr(feed_data, "entries") or not feed_data.entries:
                    logger.warning(f"No entries found in feed: {feed_url}")
                    continue

                # Parse feed metadata and entries
                feed_info = extract_feed_info(feed_data)
                entries = parse_feed_entries(feed_data.entries, request.limit)

                if not entries:
                    logger.warning(f"No parseable entries in feed: {feed_url}")
                    continue

                # Create response metadata
                metadata = {
                    "feed_url": feed_url,
                    "total_entries": len(feed_data.entries),
                    "returned_entries": len(entries),
                    "detected_feeds": len(feed_urls),
                    "status": "success",
                }

                logger.info(f"Successfully parsed feed with {len(entries)} entries")

                return FeedResponse(
                    feed_info=feed_info, entries=entries, metadata=metadata
                )

            except Exception as e:
                logger.error(f"Failed to parse feed {feed_url}: {str(e)}")
                last_error = e
                continue

        # If we get here, all feeds failed to parse
        error_msg = f"Failed to parse any of the {len(feed_urls)} detected feeds"
        if last_error:
            error_msg += f". Last error: {str(last_error)}"

        raise McpError(ErrorData(code=INTERNAL_ERROR, message=error_msg))

    except McpError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in feed parsing: {str(e)}")
        raise McpError(
            ErrorData(
                code=INTERNAL_ERROR,
                message=f"Unexpected error while processing feed: {str(e)}",
            )
        )
    finally:
        # Clean up detector
        if detector:
            await detector.close()
