import re
import logging
from typing import List, Set, Optional, cast, Any
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup, Tag

logger = logging.getLogger(__name__)


class FeedDetector:
    """RSS/Atom feed detection utility."""

    # Common RSS/Atom file patterns
    FEED_PATTERNS = [
        r"rss\.xml$",
        r"feed\.xml$",
        r"atom\.xml$",
        r"rss$",
        r"feed$",
        r"atom$",
        r"index\.xml$",
        r"feeds/all\.atom\.xml$",
        r"feeds/all\.rss\.xml$",
        r"\?feed=rss$",
        r"\?feed=rss2$",
        r"\?feed=atom$",
    ]

    # Common feed paths to check
    COMMON_FEED_PATHS = [
        "/rss.xml",
        "/feed.xml",
        "/atom.xml",
        "/rss",
        "/feed",
        "/atom",
        "/index.xml",
        "/feeds/all.atom.xml",
        "/feeds/all.rss.xml",
        "/?feed=rss",
        "/?feed=rss2",
        "/?feed=atom",
        "/blog/rss.xml",
        "/blog/feed.xml",
        "/blog/atom.xml",
        "/news/rss.xml",
        "/news/feed.xml",
        "/news/atom.xml",
    ]

    def __init__(self, timeout: int = 30, user_agent: Optional[str] = None):
        """
        Initialize FeedDetector.

        Args:
            timeout: HTTP request timeout in seconds
            user_agent: Custom User-Agent string
        """
        self.timeout = timeout
        self.user_agent = user_agent if user_agent is not None else "RSS Feed Detector 1.0"
        self.session = httpx.AsyncClient(
            timeout=self.timeout, headers={"User-Agent": self.user_agent}
        )

    async def detect_feeds(self, url: str) -> List[str]:
        """
        Detect RSS/Atom feeds from a given URL.

        Args:
            url: Target URL to analyze

        Returns:
            List of discovered feed URLs
        """
        feeds = set()

        try:
            # First, check if the URL itself is a feed
            if await self._is_feed_url(url):
                feeds.add(url)
                return list(feeds)

            # Get the HTML content
            html_content = await self._fetch_html(url)
            if not html_content:
                logger.warning(f"Could not fetch HTML content from {url}")
                # Try common feed paths as fallback
                return await self._try_common_paths(url)

            # Parse HTML and look for feed links
            soup = BeautifulSoup(html_content, "html.parser")

            # Look for <link> tags with feed information
            link_feeds = self._find_link_feeds(soup, url)
            feeds.update(link_feeds)

            # Look for <a> tags pointing to feeds
            anchor_feeds = self._find_anchor_feeds(soup, url)
            feeds.update(anchor_feeds)

            # If no feeds found in HTML, try common paths
            if not feeds:
                common_feeds = await self._try_common_paths(url)
                feeds.update(common_feeds)

        except Exception as e:
            logger.error(f"Error detecting feeds from {url}: {str(e)}")
            # Try common paths as last resort
            try:
                common_feeds = await self._try_common_paths(url)
                feeds.update(common_feeds)
            except Exception as fallback_error:
                logger.error(f"Fallback feed detection failed: {str(fallback_error)}")

        return list(feeds)

    async def _fetch_html(self, url: str) -> Optional[str]:
        """Fetch HTML content from URL."""
        try:
            response = await self.session.get(url, follow_redirects=True)
            response.raise_for_status()

            # Check if content type is HTML
            content_type = response.headers.get("content-type", "").lower()
            if "html" not in content_type:
                return None

            return response.text

        except Exception as e:
            logger.error(f"Failed to fetch HTML from {url}: {str(e)}")
            return None

    async def _is_feed_url(self, url: str) -> bool:
        """Check if URL points to a feed."""
        try:
            # Check URL pattern first
            for pattern in self.FEED_PATTERNS:
                if re.search(pattern, url, re.IGNORECASE):
                    # Verify by making a HEAD request
                    response = await self.session.head(url, follow_redirects=True)
                    content_type = response.headers.get("content-type", "").lower()
                    if any(
                        feed_type in content_type
                        for feed_type in ["rss", "atom", "xml", "application/xml"]
                    ):
                        return True

            return False

        except Exception as e:
            logger.error(f"Error checking if {url} is a feed: {str(e)}")
            return False

    def _find_link_feeds(self, soup: BeautifulSoup, base_url: str) -> Set[str]:
        """Find feeds in <link> tags."""
        feeds = set()

        # Look for <link> tags with feed types
        link_tags = soup.find_all(
            "link", {"type": re.compile(r"application/(rss|atom)\+xml", re.IGNORECASE)}
        )

        for link in link_tags:
            # Cast to Tag to access methods safely
            link_tag = cast(Tag, link)
            href = link_tag.get("href")
            if href and isinstance(href, str):
                feed_url = urljoin(base_url, href)
                feeds.add(feed_url)
                logger.debug(f"Found feed in <link> tag: {feed_url}")

        return feeds

    def _find_anchor_feeds(self, soup: BeautifulSoup, base_url: str) -> Set[str]:
        """Find feeds in <a> tags."""
        feeds = set()

        # Look for <a> tags with feed-like href or text
        anchor_tags = soup.find_all("a", href=True)

        for anchor in anchor_tags:
            # Cast to Tag to access methods safely
            anchor_tag = cast(Tag, anchor)
            href = anchor_tag.get("href", "")
            if not isinstance(href, str):
                continue
            text = anchor_tag.get_text(strip=True).lower()

            # Check href pattern
            for pattern in self.FEED_PATTERNS:
                if re.search(pattern, href, re.IGNORECASE):
                    feed_url = urljoin(base_url, href)
                    feeds.add(feed_url)
                    logger.debug(f"Found feed in <a> href: {feed_url}")
                    break

            # Check anchor text for feed-related keywords
            feed_keywords = ["rss", "feed", "atom", "xml", "syndicate"]
            if any(keyword in text for keyword in feed_keywords):
                # Additional validation for href
                if any(
                    ext in href.lower() for ext in [".xml", ".rss", ".atom", "feed"]
                ):
                    feed_url = urljoin(base_url, href)
                    feeds.add(feed_url)
                    logger.debug(f"Found feed in <a> text: {feed_url}")

        return feeds

    async def _try_common_paths(self, base_url: str) -> List[str]:
        """Try common feed paths."""
        feeds = []

        parsed_url = urlparse(base_url)
        base = f"{parsed_url.scheme}://{parsed_url.netloc}"

        for path in self.COMMON_FEED_PATHS:
            feed_url = base + path

            try:
                response = await self.session.head(feed_url, follow_redirects=True)
                if response.status_code == 200:
                    content_type = response.headers.get("content-type", "").lower()
                    if any(
                        feed_type in content_type
                        for feed_type in ["rss", "atom", "xml", "application/xml"]
                    ):
                        feeds.append(feed_url)
                        logger.debug(f"Found feed at common path: {feed_url}")

            except Exception as e:
                logger.debug(f"Common path {feed_url} failed: {str(e)}")
                continue

        return feeds

    async def close(self):
        """Close the HTTP session."""
        await self.session.aclose()
