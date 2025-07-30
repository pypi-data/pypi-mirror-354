#!/usr/bin/env python3
"""
Extract table content from the debug HTML file
"""

from bs4 import BeautifulSoup


def extract_table_content():
    """Extract and analyze table content"""

    with open(
        "/Users/go/Desktop/dev/mcp-servers/src/hatena-weekly/tool/debug_page.html",
        "r",
        encoding="utf-8",
    ) as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")

    tables = soup.find_all("table")
    print(f"Found {len(tables)} tables")

    for i, table in enumerate(tables):
        print(f"\n--- TABLE {i + 1} ---")

        rows = table.find_all("tr")
        print(f"Rows: {len(rows)}")

        for j, row in enumerate(rows[:10]):  # Show first 10 rows
            cells = row.find_all(["td", "th"])
            print(f"\nRow {j + 1} ({len(cells)} cells):")

            for k, cell in enumerate(cells):
                cell_text = cell.get_text().strip()

                # Check for links in the cell
                links = cell.find_all("a", href=True)
                link_info = ""
                if links:
                    link_info = f" [Links: {len(links)}]"
                    for link in links[:2]:  # Show first 2 links
                        href = link.get("href")
                        link_text = link.get_text().strip()
                        link_info += f"\n    -> {link_text[:30]}... => {href[:60]}..."

                print(f"  Cell {k + 1}: {cell_text[:100]}...{link_info}")

        # Print the raw HTML of the table for analysis
        print(f"\n--- RAW HTML OF TABLE {i + 1} (first 2000 chars) ---")
        print(str(table)[:2000])


if __name__ == "__main__":
    extract_table_content()
