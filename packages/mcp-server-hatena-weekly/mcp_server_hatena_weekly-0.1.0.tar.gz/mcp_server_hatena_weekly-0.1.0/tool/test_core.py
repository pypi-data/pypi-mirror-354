#!/usr/bin/env python3
"""
Test script for Hatena Bookmark MCP server core functions
"""

import sys
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from mcp_server_hatena_weekly.server import load_weekly_data, load_monthly_data


def test_weekly_data_loading():
    """Test the weekly data loading function"""
    print("=== Testing Weekly Data Loading ===")

    # Test valid data
    try:
        print("Testing 2025年3月第2週...")
        result = load_weekly_data(2025, 3, 2)
        print(f"✓ Success: Got {len(result)} entries")
        print(f"First entry: {result[0].rank}位 - {result[0].title[:60]}...")
        print(f"URL: {result[0].url}")
        print(f"Hatena URL: {result[0].hatena_url}")

    except Exception as e:
        print(f"✗ Error: {e}")

    # Test another valid data
    try:
        print("\nTesting 2025年1月第1週...")
        result = load_weekly_data(2025, 1, 1)
        print(f"✓ Success: Got {len(result)} entries")
        print(f"First entry: {result[0].rank}位 - {result[0].title[:60]}...")

    except Exception as e:
        print(f"✗ Error: {e}")

    # Test invalid data (should fail)
    try:
        print("\nTesting invalid data (2025年1月第6週)...")
        result = load_weekly_data(2025, 1, 6)
        print(f"✗ Unexpected success: Got {len(result)} entries")

    except Exception as e:
        print(f"✓ Expected error: {e}")


def test_monthly_data_loading():
    """Test the monthly data loading function"""
    print("\n=== Testing Monthly Data Loading ===")

    # Test valid data
    try:
        print("Testing 2025年3月...")
        result = load_monthly_data(2025, 3)
        print(f"✓ Success: Got {len(result)} entries")
        print(f"First entry: {result[0].rank}位 - {result[0].title[:60]}...")
        print(f"URL: {result[0].url}")
        print(f"Hatena URL: {result[0].hatena_url}")

    except Exception as e:
        print(f"✗ Error: {e}")

    # Test another valid data
    try:
        print("\nTesting 2025年1月...")
        result = load_monthly_data(2025, 1)
        print(f"✓ Success: Got {len(result)} entries")
        print(f"First entry: {result[0].rank}位 - {result[0].title[:60]}...")

    except Exception as e:
        print(f"✗ Error: {e}")

    # Test invalid month (should fail)
    try:
        print("\nTesting invalid month (2025年6月)...")
        result = load_monthly_data(2025, 6)
        print(f"✗ Unexpected success: Got {len(result)} entries")

    except Exception as e:
        print(f"✓ Expected error: {e}")


def test_data_quality():
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
                result = load_weekly_data(2025, month, week)
                if len(result) == 30:
                    total_weekly_tested += 1
                    # Check data completeness
                    urls_count = sum(1 for entry in result if entry.url)
                    hatena_urls_count = sum(1 for entry in result if entry.hatena_url)
                    print(
                        f"✓ 2025-{month:02d}-{week}: {len(result)} entries, {urls_count} URLs, {hatena_urls_count} hatena URLs"
                    )
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
            result = load_monthly_data(2025, month)
            if len(result) == 50:
                total_monthly_tested += 1
                # Check data completeness
                urls_count = sum(1 for entry in result if entry.url)
                hatena_urls_count = sum(1 for entry in result if entry.hatena_url)
                print(
                    f"✓ 2025-{month:02d}: {len(result)} entries, {urls_count} URLs, {hatena_urls_count} hatena URLs"
                )
            else:
                print(f"✗ 2025-{month:02d}: Expected 50, got {len(result)} entries")

        except Exception as e:
            print(f"✗ 2025-{month:02d}: Error - {e}")

    print("\n=== Summary ===")
    print(f"Weekly files tested successfully: {total_weekly_tested}")
    print(f"Monthly files tested successfully: {total_monthly_tested}")

    return total_weekly_tested, total_monthly_tested


def test_server_startup():
    """Test if the server can be imported and initialized"""
    print("\n=== Testing Server Startup ===")

    try:
        from mcp_server_hatena_weekly.server import mcp

        print("✓ Server module imported successfully")

        # Check if tools are registered
        tools = mcp.list_tools()
        print(f"✓ Found {len(tools)} tools registered:")
        for tool in tools:
            print(f"  - {tool['name']}: {tool['description'][:60]}...")

        return True

    except Exception as e:
        print(f"✗ Server startup error: {e}")
        return False


def main():
    """Main test function"""
    print("🧪 Testing Hatena Bookmark MCP Server Core Functions")
    print("=" * 60)

    test_weekly_data_loading()
    test_monthly_data_loading()
    weekly_success, monthly_success = test_data_quality()
    server_success = test_server_startup()

    print("\n🎯 Final Results:")
    print(f"Weekly data files working: {weekly_success}/21")
    print(f"Monthly data files working: {monthly_success}/5")
    print(f"Server startup: {'✓' if server_success else '✗'}")

    if weekly_success == 21 and monthly_success == 5 and server_success:
        print("🎉 All tests passed! MCP Server is ready to use.")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")


if __name__ == "__main__":
    main()
