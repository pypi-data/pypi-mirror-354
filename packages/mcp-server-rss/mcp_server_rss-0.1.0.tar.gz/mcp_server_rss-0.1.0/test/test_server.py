"""
Basic tests for the RSS Feed Server.

This module contains unit tests for the RSS feed parsing functionality.
"""

import pytest
from unittest.mock import AsyncMock, patch
from mcp_server_rss.server import clean_html, parse_feed_entries
from mcp_server_rss.feed_detect import FeedDetector


class TestCleanHTML:
    """Test HTML cleaning functionality."""
    
    def test_clean_html_removes_tags(self):
        """Test that HTML tags are properly removed."""
        html_text = "<p>This is a <strong>test</strong> with <em>HTML</em> tags.</p>"
        expected = "This is a test with HTML tags."
        assert clean_html(html_text) == expected
    
    def test_clean_html_handles_empty_string(self):
        """Test that empty strings are handled correctly."""
        assert clean_html("") == ""
        assert clean_html(None) == ""
    
    def test_clean_html_handles_no_tags(self):
        """Test that text without HTML tags is unchanged."""
        text = "This is plain text."
        assert clean_html(text) == text
    
    def test_clean_html_normalizes_whitespace(self):
        """Test that excessive whitespace is normalized."""
        html_text = "<p>Text   with\n\nexcessive   whitespace</p>"
        expected = "Text with excessive whitespace"
        assert clean_html(html_text) == expected


class TestFeedDetector:
    """Test feed detection functionality."""
    
    @pytest.fixture
    def detector(self):
        """Create a FeedDetector instance for testing."""
        return FeedDetector(timeout=10)
    
    def test_detector_initialization(self, detector):
        """Test that FeedDetector initializes correctly."""
        assert detector.timeout == 10
        assert detector.user_agent == "RSS Feed Detector 1.0"
        assert detector.session is not None
    
    def test_common_feed_paths(self, detector):
        """Test that common feed paths are defined."""
        assert "/rss.xml" in detector.COMMON_FEED_PATHS
        assert "/feed.xml" in detector.COMMON_FEED_PATHS
        assert "/atom.xml" in detector.COMMON_FEED_PATHS


class TestParseFeedEntries:
    """Test feed entry parsing functionality."""
    
    def test_parse_empty_entries(self):
        """Test parsing empty entry list."""
        result = parse_feed_entries([], 10)
        assert result == []
    
    def test_parse_basic_entry(self):
        """Test parsing a basic feed entry."""
        mock_entry = {
            "title": "Test Article",
            "link": "https://example.com/article",
            "published": "2025-01-01T00:00:00Z",
            "summary": "This is a test article summary.",
            "author": "Test Author",
            "id": "test-guid-123"
        }
        
        result = parse_feed_entries([mock_entry], 1)
        
        assert len(result) == 1
        assert result[0].title == "Test Article"
        assert result[0].link == "https://example.com/article"
        assert result[0].published == "2025-01-01T00:00:00Z"
        assert result[0].description == "This is a test article summary."
        assert result[0].author == "Test Author"
        assert result[0].guid == "test-guid-123"
    
    def test_parse_entry_with_html_content(self):
        """Test parsing entry with HTML content."""
        mock_entry = {
            "title": "<strong>Test</strong> Article",
            "link": "https://example.com/article",
            "published": "2025-01-01T00:00:00Z",
            "summary": "<p>This is a <em>test</em> article summary.</p>",
            "author": "",
            "id": ""
        }
        
        result = parse_feed_entries([mock_entry], 1)
        
        assert len(result) == 1
        assert result[0].title == "Test Article"
        assert result[0].description == "This is a test article summary."
    
    def test_parse_entries_respects_limit(self):
        """Test that entry parsing respects the limit parameter."""
        mock_entries = [
            {"title": f"Article {i}", "link": f"https://example.com/{i}", 
             "published": "", "summary": "", "author": "", "id": ""}
            for i in range(10)
        ]
        
        result = parse_feed_entries(mock_entries, 5)
        assert len(result) == 5
        
        result = parse_feed_entries(mock_entries, 3)
        assert len(result) == 3


# Simple integration test
@pytest.mark.asyncio
async def test_detector_initialization():
    """Test that we can create and close a detector."""
    detector = FeedDetector(timeout=5)
    assert detector is not None
    await detector.close()


if __name__ == "__main__":
    pytest.main([__file__])
