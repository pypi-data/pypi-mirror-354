#!/usr/bin/env python3
"""
Test script for Hatena Bookmark MCP server
"""

import asyncio
import sys

from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from mcp_server_hatena_weekly.server import weekly, monthly


async def test_weekly():
    """Test the weekly tool"""
    print("=== Testing Weekly Tool ===")

    # Test valid data
    try:
        print("Testing 2025年3月第2週...")
        result = await weekly(year=2025, month=3, week=2)
        print(f"✓ Success: Got {len(result)} entries")
        print(f"First entry: {result[0].rank}位 - {result[0].title[:60]}...")
        print(f"URL: {result[0].url}")
        print(f"Hatena URL: {result[0].hatena_url}")

    except Exception as e:
        print(f"✗ Error: {e}")

    # Test another valid data
    try:
        print("\nTesting 2025年1月第1週...")
        result = await weekly(year=2025, month=1, week=1)
        print(f"✓ Success: Got {len(result)} entries")
        print(f"First entry: {result[0].rank}位 - {result[0].title[:60]}...")

    except Exception as e:
        print(f"✗ Error: {e}")

    # Test invalid data (should fail)
    try:
        print("\nTesting invalid data (2025年1月第6週)...")
        result = await weekly(year=2025, month=1, week=6)
        print(f"✗ Unexpected success: Got {len(result)} entries")

    except Exception as e:
        print(f"✓ Expected error: {e}")

    # Test invalid year (should fail)
    try:
        print("\nTesting invalid year (2024年1月第1週)...")
        result = await weekly(year=2024, month=1, week=1)
        print(f"✗ Unexpected success: Got {len(result)} entries")

    except Exception as e:
        print(f"✓ Expected error: {e}")


async def test_monthly():
    """Test the monthly tool"""
    print("\n=== Testing Monthly Tool ===")

    # Test valid data
    try:
        print("Testing 2025年3月...")
        result = await monthly(year=2025, month=3)
        print(f"✓ Success: Got {len(result)} entries")
        print(f"First entry: {result[0].rank}位 - {result[0].title[:60]}...")
        print(f"URL: {result[0].url}")
        print(f"Hatena URL: {result[0].hatena_url}")

    except Exception as e:
        print(f"✗ Error: {e}")

    # Test another valid data
    try:
        print("\nTesting 2025年1月...")
        result = await monthly(year=2025, month=1)
        print(f"✓ Success: Got {len(result)} entries")
        print(f"First entry: {result[0].rank}位 - {result[0].title[:60]}...")

    except Exception as e:
        print(f"✗ Error: {e}")

    # Test invalid month (should fail)
    try:
        print("\nTesting invalid month (2025年6月)...")
        result = await monthly(year=2025, month=6)
        print(f"✗ Unexpected success: Got {len(result)} entries")

    except Exception as e:
        print(f"✓ Expected error: {e}")


async def test_data_quality():
    """Test data quality across all files"""
    print("\n=== Testing Data Quality ===")

    total_weekly_tested = 0
    total_monthly_tested = 0

    # Test all weekly data
    print("Testing all weekly data...")
    for month in range(1, 6):  # 1-5
        max_week = 5 if month == 3 else 4  # March has 5 weeks
        for week in range(1, max_week + 1):
            try:
                result = await weekly(year=2025, month=month, week=week)
                if len(result) == 30:
                    total_weekly_tested += 1
                    print(f"✓ 2025-{month:02d}-{week}: {len(result)} entries")
                else:
                    print(
                        f"✗ 2025-{month:02d}-{week}: Expected 30, got {len(result)} entries"
                    )

            except Exception as e:
                print(f"✗ 2025-{month:02d}-{week}: Error - {e}")

    # Test all monthly data
    print("\nTesting all monthly data...")
    for month in range(1, 6):  # 1-5
        try:
            result = await monthly(year=2025, month=month)
            if len(result) == 50:
                total_monthly_tested += 1
                print(f"✓ 2025-{month:02d}: {len(result)} entries")
            else:
                print(f"✗ 2025-{month:02d}: Expected 50, got {len(result)} entries")

        except Exception as e:
            print(f"✗ 2025-{month:02d}: Error - {e}")

    print("\n=== Summary ===")
    print(f"Weekly files tested successfully: {total_weekly_tested}")
    print(f"Monthly files tested successfully: {total_monthly_tested}")


async def main():
    """Main test function"""
    print("🧪 Testing Hatena Bookmark MCP Server")
    print("=" * 50)

    await test_weekly()
    await test_monthly()
    await test_data_quality()

    print("\n🎉 Testing completed!")


if __name__ == "__main__":
    asyncio.run(main())
