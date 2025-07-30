#!/usr/bin/env python3
"""
Hatena Bookmark Weekly/Monthly Ranking Data Scraper

This script scrapes Hatena Bookmark ranking data from bookmark.hatenastaff.com
and saves it as JSON files for use with the MCP server.
"""

import os
import json
import re
import time
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class HatenaBookmarkScraper:
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

    def extract_archive_links(self) -> Dict[str, List[str]]:
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
                # Extract month and week from text like "今週のはてなブックマーク数ランキング（2025年3月第2週）"
                match = re.search(r"2025年(\d+)月第(\d+)週", text)
                if match:
                    month = int(match.group(1))
                    week = int(match.group(2))
                    if 1 <= month <= 5:  # Only collect January to May
                        weekly_links.append((href, month, week))

            # Check for monthly ranking pattern
            elif "月間はてなブックマーク数ランキング（2025年" in text:
                # Extract month from text like "月間はてなブックマーク数ランキング（2025年2月）"
                match = re.search(r"2025年(\d+)月", text)
                if match:
                    month = int(match.group(1))
                    if 1 <= month <= 5:  # Only collect January to May
                        monthly_links.append((href, month))

        logger.info(
            f"Found {len(weekly_links)} weekly links and {len(monthly_links)} monthly links"
        )
        return {"weekly": weekly_links, "monthly": monthly_links}

    def extract_ranking_data(
        self, url: str, expected_count: int
    ) -> List[Dict[str, str]]:
        """Extract ranking data from a ranking page"""
        soup = self.get_page(url)
        if not soup:
            return []

        entries = []

        # Look for ranking entries in the page
        # The pattern seems to be: rank, title, and links are in specific structures
        # We need to find the actual ranking table/list

        # Try different selectors to find the ranking data
        # Looking for patterns like "1位", "2位", etc.
        rank_pattern = re.compile(r"(\d+)位")

        # Find all text that contains rank information
        text_content = soup.get_text()
        lines = [line.strip() for line in text_content.split("\n") if line.strip()]

        current_rank = None
        current_title = None

        for i, line in enumerate(lines):
            # Check if this line contains a rank
            rank_match = rank_pattern.search(line)
            if rank_match:
                rank = int(rank_match.group(1))

                # Look for the title in the same line or next lines
                title_part = rank_pattern.sub("", line).strip()
                if title_part:
                    current_title = title_part
                else:
                    # Title might be in the next line
                    if i + 1 < len(lines):
                        current_title = lines[i + 1].strip()

                if current_title and current_title not in ["順位", "タイトル"]:
                    entries.append(
                        {
                            "rank": rank,
                            "title": current_title,
                            "url": "",  # We'll try to find this
                            "hatena_url": "",  # We'll try to find this
                        }
                    )

                    if len(entries) >= expected_count:
                        break

        # Now try to find URLs for the entries
        # Look for all links in the page
        links = soup.find_all("a", href=True)

        for entry in entries:
            title = entry["title"]
            # Try to find a link that matches this title
            for link in links:
                link_text = link.get_text().strip()
                if title in link_text or link_text in title:
                    href = link.get("href")
                    if href:
                        if href.startswith("http") and "bookmark.hatena" not in href:
                            entry["url"] = href
                        elif "bookmark.hatena" in href or href.startswith("/"):
                            if href.startswith("/"):
                                entry["hatena_url"] = (
                                    "https://bookmark.hatena.ne.jp" + href
                                )
                            else:
                                entry["hatena_url"] = href
                    break

        logger.info(f"Extracted {len(entries)} entries from {url}")
        return entries[:expected_count]  # Ensure we don't exceed expected count

    def scrape_weekly_data(self, links: List[tuple]) -> None:
        """Scrape weekly ranking data"""
        for url, month, week in links:
            filename = f"2025-{month:02d}-{week}.json"
            filepath = os.path.join(self.week_dir, filename)

            if os.path.exists(filepath):
                logger.info(f"Skipping {filename} - already exists")
                continue

            logger.info(f"Scraping weekly data: {month}月第{week}週")
            entries = self.extract_ranking_data(url, 30)  # Weekly has 30 entries

            if entries:
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(entries, f, ensure_ascii=False, indent=2)
                logger.info(f"Saved {len(entries)} entries to {filename}")
            else:
                logger.warning(f"No entries found for {filename}")

            time.sleep(2)  # Be respectful to the server

    def scrape_monthly_data(self, links: List[tuple]) -> None:
        """Scrape monthly ranking data"""
        for url, month in links:
            filename = f"2025-{month:02d}.json"
            filepath = os.path.join(self.month_dir, filename)

            if os.path.exists(filepath):
                logger.info(f"Skipping {filename} - already exists")
                continue

            logger.info(f"Scraping monthly data: {month}月")
            entries = self.extract_ranking_data(url, 50)  # Monthly has 50 entries

            if entries:
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(entries, f, ensure_ascii=False, indent=2)
                logger.info(f"Saved {len(entries)} entries to {filename}")
            else:
                logger.warning(f"No entries found for {filename}")

            time.sleep(2)  # Be respectful to the server

    def run(self):
        """Main scraping function"""
        logger.info("Starting Hatena Bookmark ranking data scraping...")

        # Get all archive links
        links = self.extract_archive_links()

        # Scrape weekly data
        if links["weekly"]:
            logger.info("Scraping weekly ranking data...")
            self.scrape_weekly_data(links["weekly"])

        # Scrape monthly data
        if links["monthly"]:
            logger.info("Scraping monthly ranking data...")
            self.scrape_monthly_data(links["monthly"])

        logger.info("Scraping completed!")


if __name__ == "__main__":
    scraper = HatenaBookmarkScraper()
    scraper.run()
