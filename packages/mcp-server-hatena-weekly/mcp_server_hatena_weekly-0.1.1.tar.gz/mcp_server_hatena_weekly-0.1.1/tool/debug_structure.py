#!/usr/bin/env python3
"""
Debug script to analyze the actual HTML structure of Hatena ranking pages
"""

import requests
from bs4 import BeautifulSoup
import re


def analyze_page_structure(url):
    """Analyze the structure of a ranking page"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    print(f"Analyzing: {url}")
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    print("=" * 80)
    print("PAGE TITLE:")
    print(soup.title.text if soup.title else "No title")

    print("\n" + "=" * 80)
    print("LOOKING FOR RANKING PATTERNS:")

    # Look for rank patterns
    text_content = soup.get_text()
    rank_patterns = re.findall(r"\d+位.*", text_content)

    print(f"Found {len(rank_patterns)} rank patterns:")
    for i, pattern in enumerate(rank_patterns[:10]):  # Show first 10
        print(f"{i + 1}. {pattern.strip()}")

    print("\n" + "=" * 80)
    print("LOOKING FOR TABLES:")
    tables = soup.find_all("table")
    print(f"Found {len(tables)} tables")

    for i, table in enumerate(tables):
        print(f"\nTable {i + 1}:")
        rows = table.find_all("tr")
        print(f"  Rows: {len(rows)}")
        if rows:
            first_row = rows[0]
            cells = first_row.find_all(["td", "th"])
            print(f"  First row cells: {len(cells)}")
            for j, cell in enumerate(cells[:3]):
                print(f"    Cell {j + 1}: {cell.get_text().strip()[:50]}...")

    print("\n" + "=" * 80)
    print("LOOKING FOR LISTS:")
    lists = soup.find_all(["ol", "ul"])
    print(f"Found {len(lists)} lists")

    for i, lst in enumerate(lists):
        items = lst.find_all("li")
        print(f"List {i + 1}: {len(items)} items")
        if items:
            print(f"  First item: {items[0].get_text().strip()[:100]}...")

    print("\n" + "=" * 80)
    print("LOOKING FOR LINKS:")
    links = soup.find_all("a", href=True)
    external_links = [
        link
        for link in links
        if link.get("href").startswith("http")
        and "hatenastaff.com" not in link.get("href")
    ]

    print(f"Total links: {len(links)}")
    print(f"External links: {len(external_links)}")

    print("\nFirst 10 external links:")
    for i, link in enumerate(external_links[:10]):
        href = link.get("href")
        text = link.get_text().strip()
        print(f"{i + 1}. {text[:50]}... -> {href[:60]}...")

    print("\n" + "=" * 80)
    print("LOOKING FOR DIVS WITH RANKING DATA:")

    # Look for specific div structures
    entry_content = soup.find("div", class_="entry-content")
    if entry_content:
        print("Found entry-content div")
        # Look for patterns within entry content
        text = entry_content.get_text()
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        rank_lines = [line for line in lines if re.search(r"\d+位", line)]
        print(f"Rank lines in entry-content: {len(rank_lines)}")

        for i, line in enumerate(rank_lines[:10]):
            print(f"  {i + 1}. {line}")

    return soup


if __name__ == "__main__":
    # Test with a specific ranking page
    test_url = "https://bookmark.hatenastaff.com/entry/2025/03/11/113220"
    soup = analyze_page_structure(test_url)

    # Save the full HTML for manual inspection
    with open(
        "/Users/go/Desktop/dev/mcp-servers/src/hatena-weekly/tool/debug_page.html",
        "w",
        encoding="utf-8",
    ) as f:
        f.write(str(soup))
    print("\nFull HTML saved to debug_page.html")
