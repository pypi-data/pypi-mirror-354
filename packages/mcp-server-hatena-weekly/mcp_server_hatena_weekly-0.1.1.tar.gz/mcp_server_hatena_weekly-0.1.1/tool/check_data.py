#!/usr/bin/env python3
"""
Check data file counts and identify files that need re-scraping
"""

import os
import json
import glob


def check_data_counts():
    """Check the count of entries in each data file"""

    base_dir = os.path.join(os.path.dirname(__file__), "..", "src", "mcp_server_hatena_weekly", "data")
    week_dir = os.path.join(base_dir, "week")
    month_dir = os.path.join(base_dir, "month")

    print("=== Weekly Data Check (Expected: 30 entries each) ===")
    week_files = glob.glob(os.path.join(week_dir, "*.json"))
    week_files.sort()

    insufficient_weekly = []
    for file_path in week_files:
        filename = os.path.basename(file_path)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                count = len(data)
                status = "✓" if count == 30 else "✗"
                print(f"{status} {filename}: {count} entries")
                if count < 30:
                    insufficient_weekly.append(filename)
        except Exception as e:
            print(f"✗ {filename}: Error reading file - {e}")
            insufficient_weekly.append(filename)

    print("\n=== Monthly Data Check (Expected: 50 entries each) ===")
    month_files = glob.glob(os.path.join(month_dir, "*.json"))
    month_files.sort()

    insufficient_monthly = []
    for file_path in month_files:
        filename = os.path.basename(file_path)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                count = len(data)
                status = "✓" if count == 50 else "✗"
                print(f"{status} {filename}: {count} entries")
                if count < 50:
                    insufficient_monthly.append(filename)
        except Exception as e:
            print(f"✗ {filename}: Error reading file - {e}")
            insufficient_monthly.append(filename)

    print("\n=== Summary ===")
    print(f"Weekly files needing re-scraping: {len(insufficient_weekly)}")
    if insufficient_weekly:
        print(f"Files: {', '.join(insufficient_weekly)}")

    print(f"Monthly files needing re-scraping: {len(insufficient_monthly)}")
    if insufficient_monthly:
        print(f"Files: {', '.join(insufficient_monthly)}")

    return insufficient_weekly, insufficient_monthly


if __name__ == "__main__":
    check_data_counts()
