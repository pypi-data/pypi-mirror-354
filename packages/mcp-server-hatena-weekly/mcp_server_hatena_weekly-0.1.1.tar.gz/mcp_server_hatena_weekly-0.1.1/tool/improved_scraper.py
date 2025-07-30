#!/usr/bin/env python3
"""
Improved Hatena Bookmark Weekly/Monthly Ranking Data Scraper

This version focuses on better URL extraction by analyzing the actual HTML structure
of the ranking pages.
"""

import os
import json
import re
import time
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import logging
from urllib.parse import urljoin

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ImprovedHatenaBookmarkScraper:
    def __init__(self):
        self.base_url = "https://bookmark.hatenastaff.com"
        self.archive_url = f"{self.base_url}/archive/category/ランキング"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

        # Create data directories
        self.data_dir = os.path.join(os.path.dirname(__file__), "..", "src", "mcp_server_hatena_weekly", "data")
        self.week_dir = os.path.join(self.data_dir, "week")
        self.month_dir = os.path.join(self.data_dir, "month")

        os.makedirs(self.week_dir, exist_ok=True)
        os.makedirs(self.month_dir, exist_ok=True)

    def get_page(self, url: str) -> Optional[BeautifulSoup]:
        """Get a page and return BeautifulSoup object"""
        try:
            logger.info(f"Fetching: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.content, "html.parser")
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None

    def extract_ranking_data_improved(
        self, url: str, expected_count: int
    ) -> List[Dict[str, str]]:
        """Extract ranking data with improved URL detection"""
        soup = self.get_page(url)
        if not soup:
            return []

        entries = []

        # Get the main content area
        content = soup.find("div", class_="entry-content") or soup.find(
            "div", class_="hatena-body"
        )
        if not content:
            content = soup

        # Look for table or list structures that contain ranking data
        tables = content.find_all("table")
        if tables:
            # Process table-based ranking
            for table in tables:
                rows = table.find_all("tr")
                for row in rows:
                    cells = row.find_all(["td", "th"])
                    if len(cells) >= 2:
                        # Try to extract rank and title
                        rank_text = cells[0].get_text().strip()
                        title_cell = cells[1] if len(cells) > 1 else cells[0]

                        # Extract rank number
                        rank_match = re.search(r"(\d+)", rank_text)
                        if rank_match:
                            rank = int(rank_match.group(1))

                            # Extract title and URL
                            title = title_cell.get_text().strip()

                            # Look for links in the title cell
                            link = title_cell.find("a", href=True)
                            url_link = ""
                            hatena_url = ""

                            if link:
                                href = link.get("href")
                                if href:
                                    if (
                                        "bookmark.hatena.ne.jp" in href
                                        or "b.hatena.ne.jp" in href
                                    ):
                                        hatena_url = href
                                    elif href.startswith("http"):
                                        url_link = href
                                    else:
                                        # Try to construct full URL
                                        full_url = urljoin(url, href)
                                        if "bookmark.hatena" in full_url:
                                            hatena_url = full_url
                                        else:
                                            url_link = full_url

                            if title and rank <= expected_count:
                                entries.append(
                                    {
                                        "rank": rank,
                                        "title": title,
                                        "url": url_link,
                                        "hatena_url": hatena_url,
                                    }
                                )

        # If no table found, try alternative extraction methods
        if not entries:
            # Method 2: Look for numbered list patterns
            text_content = content.get_text()
            lines = [line.strip() for line in text_content.split("\n") if line.strip()]

            # Find all links in the content
            all_links = content.find_all("a", href=True)
            link_map = {}

            for link in all_links:
                text = link.get_text().strip()
                href = link.get("href")
                if text and href:
                    link_map[text] = href

            # Extract entries using line-by-line analysis
            rank_pattern = re.compile(r"(\d+)位")
            current_rank = None

            for i, line in enumerate(lines):
                rank_match = rank_pattern.search(line)
                if rank_match:
                    rank = int(rank_match.group(1))

                    # Get title (might be in same line or next line)
                    title_part = rank_pattern.sub("", line).strip()
                    if not title_part and i + 1 < len(lines):
                        title_part = lines[i + 1].strip()

                    if title_part and title_part not in ["順位", "タイトル"]:
                        # Clean up title
                        title = title_part

                        # Try to find matching URL
                        url_link = ""
                        hatena_url = ""

                        # Look for exact match or partial match in link_map
                        for link_text, href in link_map.items():
                            if (
                                title in link_text
                                or link_text in title
                                or self.similarity_score(title, link_text) > 0.8
                            ):
                                if (
                                    "bookmark.hatena.ne.jp" in href
                                    or "b.hatena.ne.jp" in href
                                ):
                                    hatena_url = href
                                elif (
                                    href.startswith("http")
                                    and "hatenastaff.com" not in href
                                ):
                                    url_link = href
                                break

                        if rank <= expected_count:
                            entries.append(
                                {
                                    "rank": rank,
                                    "title": title,
                                    "url": url_link,
                                    "hatena_url": hatena_url,
                                }
                            )

                            if len(entries) >= expected_count:
                                break

        # Sort by rank and limit to expected count
        entries.sort(key=lambda x: x["rank"])
        entries = entries[:expected_count]

        logger.info(f"Extracted {len(entries)} entries from {url}")

        # Log first few entries for debugging
        for i, entry in enumerate(entries[:3]):
            logger.debug(
                f"Entry {i + 1}: Rank={entry['rank']}, Title='{entry['title'][:50]}...', URL='{entry['url'][:50]}...', Hatena='{entry['hatena_url'][:50]}...'"
            )

        return entries

    def similarity_score(self, text1: str, text2: str) -> float:
        """Calculate similarity score between two texts"""
        text1_words = set(text1.lower().split())
        text2_words = set(text2.lower().split())

        if not text1_words or not text2_words:
            return 0.0

        intersection = text1_words.intersection(text2_words)
        union = text1_words.union(text2_words)

        return len(intersection) / len(union) if union else 0.0

    def extract_archive_links(self) -> Dict[str, List[tuple]]:
        """Extract weekly and monthly ranking article links from archive page"""
        soup = self.get_page(self.archive_url)
        if not soup:
            return {"weekly": [], "monthly": []}

        weekly_links = []
        monthly_links = []

        # Find all links in the archive page
        for link in soup.find_all("a", href=True):
            href = link.get("href")
            text = link.get_text().strip()

            if not href or not text:
                continue

            # Make absolute URL
            if href.startswith("/"):
                href = self.base_url + href

            # Check for weekly ranking pattern
            if "今週のはてなブックマーク数ランキング（2025年" in text:
                match = re.search(r"2025年(\d+)月第(\d+)週", text)
                if match:
                    month = int(match.group(1))
                    week = int(match.group(2))
                    if 1 <= month <= 5:
                        weekly_links.append((href, month, week))

            # Check for monthly ranking pattern
            elif "月間はてなブックマーク数ランキング（2025年" in text:
                match = re.search(r"2025年(\d+)月", text)
                if match:
                    month = int(match.group(1))
                    if 1 <= month <= 5:
                        monthly_links.append((href, month))

        logger.info(
            f"Found {len(weekly_links)} weekly links and {len(monthly_links)} monthly links"
        )
        return {"weekly": weekly_links, "monthly": monthly_links}

    def rescrape_specific_files(
        self, weekly_files: List[str] = None, monthly_files: List[str] = None
    ):
        """Re-scrape specific files"""

        if weekly_files is None:
            weekly_files = []
        if monthly_files is None:
            monthly_files = []

        # Get all archive links
        links = self.extract_archive_links()

        # Re-scrape weekly files
        if weekly_files:
            logger.info(f"Re-scraping {len(weekly_files)} weekly files...")
            for url, month, week in links["weekly"]:
                filename = f"2025-{month:02d}-{week}.json"
                if filename in weekly_files:
                    filepath = os.path.join(self.week_dir, filename)
                    logger.info(
                        f"Re-scraping weekly data: {month}月第{week}週 -> {filename}"
                    )

                    entries = self.extract_ranking_data_improved(url, 30)

                    if entries and len(entries) == 30:
                        with open(filepath, "w", encoding="utf-8") as f:
                            json.dump(entries, f, ensure_ascii=False, indent=2)
                        logger.info(f"Re-saved {len(entries)} entries to {filename}")
                    else:
                        logger.warning(
                            f"Failed to get complete data for {filename}: got {len(entries)} entries"
                        )

                    time.sleep(2)

        # Re-scrape monthly files
        if monthly_files:
            logger.info(f"Re-scraping {len(monthly_files)} monthly files...")
            for url, month in links["monthly"]:
                filename = f"2025-{month:02d}.json"
                if filename in monthly_files:
                    filepath = os.path.join(self.month_dir, filename)
                    logger.info(f"Re-scraping monthly data: {month}月 -> {filename}")

                    entries = self.extract_ranking_data_improved(url, 50)

                    if entries and len(entries) == 50:
                        with open(filepath, "w", encoding="utf-8") as f:
                            json.dump(entries, f, ensure_ascii=False, indent=2)
                        logger.info(f"Re-saved {len(entries)} entries to {filename}")
                    else:
                        logger.warning(
                            f"Failed to get complete data for {filename}: got {len(entries)} entries"
                        )

                    time.sleep(2)

    def rescrape_all_with_urls(self):
        """Re-scrape all files with improved URL extraction"""
        logger.info("Re-scraping all files with improved URL extraction...")

        # Get all archive links
        links = self.extract_archive_links()

        # Re-scrape all weekly data
        logger.info("Re-scraping all weekly ranking data...")
        for url, month, week in links["weekly"]:
            filename = f"2025-{month:02d}-{week}.json"
            filepath = os.path.join(self.week_dir, filename)

            logger.info(f"Re-scraping weekly data: {month}月第{week}週 -> {filename}")
            entries = self.extract_ranking_data_improved(url, 30)

            if entries:
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(entries, f, ensure_ascii=False, indent=2)
                logger.info(f"Saved {len(entries)} entries to {filename}")
            else:
                logger.warning(f"No entries found for {filename}")

            time.sleep(2)

        # Re-scrape all monthly data
        logger.info("Re-scraping all monthly ranking data...")
        for url, month in links["monthly"]:
            filename = f"2025-{month:02d}.json"
            filepath = os.path.join(self.month_dir, filename)

            logger.info(f"Re-scraping monthly data: {month}月 -> {filename}")
            entries = self.extract_ranking_data_improved(url, 50)

            if entries:
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(entries, f, ensure_ascii=False, indent=2)
                logger.info(f"Saved {len(entries)} entries to {filename}")
            else:
                logger.warning(f"No entries found for {filename}")

            time.sleep(2)

        logger.info("Re-scraping completed!")


if __name__ == "__main__":
    scraper = ImprovedHatenaBookmarkScraper()

    # Re-scrape all files with improved URL extraction
    scraper.rescrape_all_with_urls()
