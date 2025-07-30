#!/usr/bin/env python3
"""
Final improved Hatena Bookmark scraper with accurate URL extraction
"""

import os
import json
import re
import time
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import logging
from urllib.parse import unquote, parse_qs, urlparse

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class FinalHatenaBookmarkScraper:
    def __init__(self):
        self.base_url = "https://bookmark.hatenastaff.com"
        self.archive_url = f"{self.base_url}/archive/category/ランキング"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

        # Create data directories
        self.data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
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

    def extract_original_url_from_hatena_link(self, hatena_bookmark_url: str) -> str:
        """Extract original URL from Hatena bookmark URL"""
        try:
            parsed = urlparse(hatena_bookmark_url)
            if "b.hatena.ne.jp" in parsed.netloc:
                query_params = parse_qs(parsed.query)
                if "url" in query_params:
                    return unquote(query_params["url"][0])
        except Exception:
            pass
        return ""

    def extract_ranking_data_from_table(
        self, url: str, expected_count: int
    ) -> List[Dict[str, str]]:
        """Extract ranking data from the table structure"""
        soup = self.get_page(url)
        if not soup:
            return []

        entries = []

        # Find the ranking table
        table = soup.find("table")
        if not table:
            logger.warning(f"No table found in {url}")
            return []

        rows = table.find_all("tr")
        logger.info(f"Found table with {len(rows)} rows")

        for row_index, row in enumerate(rows):
            if row_index == 0:  # Skip header row
                continue

            cells = row.find_all(["td", "th"])
            if len(cells) < 2:
                continue

            # Extract rank from first cell
            rank_cell = cells[0]
            rank_text = rank_cell.get_text().strip()
            rank_match = re.search(r"(\d+)位", rank_text)

            if not rank_match:
                continue

            rank = int(rank_match.group(1))

            # Extract title and URLs from second cell
            title_cell = cells[1]

            # Get the title text (clean version)
            title = title_cell.get_text().strip()

            # Find all links in the title cell
            links = title_cell.find_all("a", href=True)

            original_url = ""
            hatena_url = ""

            for link in links:
                href = link.get("href")
                if not href:
                    continue

                if "b.hatena.ne.jp/entry" in href:
                    # This is the hatena bookmark URL
                    hatena_url = href
                    # Extract original URL from the hatena bookmark URL
                    if not original_url:
                        original_url = self.extract_original_url_from_hatena_link(href)
                elif (
                    href.startswith("http")
                    and "hatenastaff.com" not in href
                    and "hatena.ne.jp" not in href
                ):
                    # This is likely the original URL
                    original_url = href

            if rank <= expected_count:
                entry = {
                    "rank": rank,
                    "title": title,
                    "url": original_url,
                    "hatena_url": hatena_url,
                }
                entries.append(entry)

                # Debug log for first few entries
                if len(entries) <= 5:
                    logger.debug(
                        f"Entry {rank}: {title[:50]}... | URL: {original_url[:60]}... | Hatena: {hatena_url[:60]}..."
                    )

        # Sort by rank and ensure we have the right count
        entries.sort(key=lambda x: x["rank"])
        entries = entries[:expected_count]

        logger.info(f"Successfully extracted {len(entries)} entries from {url}")
        return entries

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

    def rescrape_all_data(self):
        """Re-scrape all data with improved URL extraction"""
        logger.info("Starting complete re-scraping with improved URL extraction...")

        # Get all archive links
        links = self.extract_archive_links()

        # Re-scrape all weekly data
        logger.info("Re-scraping all weekly ranking data...")
        for url, month, week in links["weekly"]:
            filename = f"2025-{month:02d}-{week}.json"
            filepath = os.path.join(self.week_dir, filename)

            logger.info(f"Re-scraping weekly data: {month}月第{week}週 -> {filename}")
            entries = self.extract_ranking_data_from_table(url, 30)

            if len(entries) == 30:
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(entries, f, ensure_ascii=False, indent=2)
                logger.info(
                    f"✓ Successfully saved {len(entries)} entries to {filename}"
                )

                # Verify data quality
                urls_found = sum(1 for entry in entries if entry["url"])
                hatena_urls_found = sum(1 for entry in entries if entry["hatena_url"])
                logger.info(
                    f"  Data quality: {urls_found}/30 original URLs, {hatena_urls_found}/30 hatena URLs"
                )
            else:
                logger.error(
                    f"✗ Failed to get complete data for {filename}: got {len(entries)} entries instead of 30"
                )

            time.sleep(2)  # Be respectful to the server

        # Re-scrape all monthly data
        logger.info("Re-scraping all monthly ranking data...")
        for url, month in links["monthly"]:
            filename = f"2025-{month:02d}.json"
            filepath = os.path.join(self.month_dir, filename)

            logger.info(f"Re-scraping monthly data: {month}月 -> {filename}")
            entries = self.extract_ranking_data_from_table(url, 50)

            if len(entries) == 50:
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(entries, f, ensure_ascii=False, indent=2)
                logger.info(
                    f"✓ Successfully saved {len(entries)} entries to {filename}"
                )

                # Verify data quality
                urls_found = sum(1 for entry in entries if entry["url"])
                hatena_urls_found = sum(1 for entry in entries if entry["hatena_url"])
                logger.info(
                    f"  Data quality: {urls_found}/50 original URLs, {hatena_urls_found}/50 hatena URLs"
                )
            else:
                logger.error(
                    f"✗ Failed to get complete data for {filename}: got {len(entries)} entries instead of 50"
                )

            time.sleep(2)  # Be respectful to the server

        logger.info("Complete re-scraping finished!")

    def verify_data_quality(self):
        """Verify the quality of all scraped data"""
        logger.info("Verifying data quality...")

        # Check weekly data
        import glob

        week_files = glob.glob(os.path.join(self.week_dir, "*.json"))
        month_files = glob.glob(os.path.join(self.month_dir, "*.json"))

        print("\n=== WEEKLY DATA QUALITY REPORT ===")
        total_weekly_entries = 0
        total_weekly_urls = 0
        total_weekly_hatena_urls = 0

        for file_path in sorted(week_files):
            filename = os.path.basename(file_path)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                count = len(data)
                urls = sum(1 for entry in data if entry.get("url"))
                hatena_urls = sum(1 for entry in data if entry.get("hatena_url"))

                total_weekly_entries += count
                total_weekly_urls += urls
                total_weekly_hatena_urls += hatena_urls

                status = "✓" if count == 30 else "✗"
                print(
                    f"{status} {filename}: {count} entries, {urls} URLs, {hatena_urls} hatena URLs"
                )

            except Exception as e:
                print(f"✗ {filename}: Error - {e}")

        print(
            f"\nWeekly Summary: {total_weekly_entries} entries, {total_weekly_urls} URLs, {total_weekly_hatena_urls} hatena URLs"
        )

        print("\n=== MONTHLY DATA QUALITY REPORT ===")
        total_monthly_entries = 0
        total_monthly_urls = 0
        total_monthly_hatena_urls = 0

        for file_path in sorted(month_files):
            filename = os.path.basename(file_path)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                count = len(data)
                urls = sum(1 for entry in data if entry.get("url"))
                hatena_urls = sum(1 for entry in data if entry.get("hatena_url"))

                total_monthly_entries += count
                total_monthly_urls += urls
                total_monthly_hatena_urls += hatena_urls

                status = "✓" if count == 50 else "✗"
                print(
                    f"{status} {filename}: {count} entries, {urls} URLs, {hatena_urls} hatena URLs"
                )

            except Exception as e:
                print(f"✗ {filename}: Error - {e}")

        print(
            f"\nMonthly Summary: {total_monthly_entries} entries, {total_monthly_urls} URLs, {total_monthly_hatena_urls} hatena URLs"
        )

        total_entries = total_weekly_entries + total_monthly_entries
        total_urls = total_weekly_urls + total_monthly_urls
        total_hatena_urls = total_weekly_hatena_urls + total_monthly_hatena_urls

        print("\n=== OVERALL SUMMARY ===")
        print(f"Total entries: {total_entries}")
        print(f"Total original URLs: {total_urls}")
        print(f"Total hatena URLs: {total_hatena_urls}")
        print(f"URL completion rate: {total_urls / total_entries * 100:.1f}%")
        print(
            f"Hatena URL completion rate: {total_hatena_urls / total_entries * 100:.1f}%"
        )


if __name__ == "__main__":
    scraper = FinalHatenaBookmarkScraper()

    # Re-scrape all data with improved extraction
    scraper.rescrape_all_data()

    # Verify data quality
    scraper.verify_data_quality()
