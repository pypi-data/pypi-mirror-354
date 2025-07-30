import json
import logging
from pathlib import Path
from typing import List

from fastmcp import FastMCP
from mcp.shared.exceptions import McpError
from mcp.types import INTERNAL_ERROR, INVALID_PARAMS, ErrorData
from pydantic import BaseModel, ConfigDict, Field, model_validator

# Configure logging
logger = logging.getLogger(__name__)

# Create an MCP server instance
mcp = FastMCP("Hatena Bookmark Weekly/Monthly Ranking Server")


# Pydantic models
class BookmarkEntry(BaseModel):
    """Model for a bookmark entry."""

    model_config = ConfigDict(extra="forbid")

    rank: int = Field(description="Ranking position")
    title: str = Field(description="Article title")
    url: str = Field(description="Original article URL")
    hatena_url: str = Field(description="Hatena bookmark URL")


class WeeklyRequest(BaseModel):
    """Model for weekly ranking request parameters."""

    model_config = ConfigDict(extra="forbid")

    year: int = Field(description="Year (2023-2025)", ge=2023, le=2025)
    month: int = Field(description="Month (2023-2024: 1-12, 2025: 1-6)", ge=1, le=12)
    week: int = Field(description="Week number (1-5)", ge=1, le=5)

    @model_validator(mode='after')
    def validate_year_month_combination(self):
        if self.year == 2025 and self.month > 6:
            raise ValueError("2025年では1-6月のみ利用可能です")
        return self


class MonthlyRequest(BaseModel):
    """Model for monthly ranking request parameters."""

    model_config = ConfigDict(extra="forbid")

    year: int = Field(description="Year (2023-2025)", ge=2023, le=2025)
    month: int = Field(description="Month (2023-2024: 1-12, 2025: 1-5)", ge=1, le=12)

    @model_validator(mode='after')
    def validate_year_month_combination(self):
        if self.year == 2025 and self.month > 5:
            raise ValueError("2025年では1-5月のみ利用可能です")
        return self


def get_data_directory() -> Path:
    """Get the data directory path"""
    # Get the directory where this file is located
    current_file = Path(__file__)
    # data directory is now within the same package directory
    data_dir = current_file.parent / "data"
    return data_dir


def load_weekly_data(year: int, month: int, week: int) -> List[BookmarkEntry]:
    """Load weekly ranking data from JSON file"""
    data_dir = get_data_directory()
    file_path = data_dir / "week" / f"{year}-{month:02d}-{week}.json"

    if not file_path.exists():
        raise McpError(
            ErrorData(
                code=INVALID_PARAMS,
                message=f"Weekly data not found for {year}年{month}月第{week}週. File: {file_path}",
            )
        )

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        entries = []
        for item in data:
            entries.append(
                BookmarkEntry(
                    rank=item["rank"],
                    title=item["title"],
                    url=item["url"],
                    hatena_url=item["hatena_url"],
                )
            )

        logger.info(f"Loaded {len(entries)} weekly entries for {year}-{month:02d}-{week}")
        return entries

    except Exception as e:
        logger.error(f"Error loading weekly data from {file_path}: {e}")
        raise McpError(
            ErrorData(code=INTERNAL_ERROR, message=f"Failed to load weekly data: {str(e)}")
        )


def load_monthly_data(year: int, month: int) -> List[BookmarkEntry]:
    """Load monthly ranking data from JSON file"""
    data_dir = get_data_directory()
    file_path = data_dir / "month" / f"{year}-{month:02d}.json"

    if not file_path.exists():
        raise McpError(
            ErrorData(
                code=INVALID_PARAMS,
                message=f"Monthly data not found for {year}年{month}月. File: {file_path}",
            )
        )

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        entries = []
        for item in data:
            entries.append(
                BookmarkEntry(
                    rank=item["rank"],
                    title=item["title"],
                    url=item["url"],
                    hatena_url=item["hatena_url"],
                )
            )

        logger.info(f"Loaded {len(entries)} monthly entries for {year}-{month:02d}")
        return entries

    except Exception as e:
        logger.error(f"Error loading monthly data from {file_path}: {e}")
        raise McpError(
            ErrorData(code=INTERNAL_ERROR, message=f"Failed to load monthly data: {str(e)}")
        )


@mcp.tool()
async def weekly(year: int, month: int, week: int) -> List[BookmarkEntry]:
    """
    週次人気はてなブックマーク情報の取得

    Get weekly popular Hatena bookmark ranking data.

    Args:
        year: 年度 (2023-2025年対応)
        month: 月 (2023-2024年: 1-12, 2025年: 1-6)
        week: 週番号 (1-5、5週目が存在しない月もあります)

    Returns:
        List of BookmarkEntry models containing ranking data with:
        - rank: ランキング順位
        - title: 記事タイトル
        - url: 元記事のURL
        - hatena_url: はてなブックマークURL

        週次ランキングは30件のエントリーを返します。

    Raises:
        McpError: パラメータが無効、またはデータの読み込みに失敗した場合
    """
    # Validate and create request model
    try:
        request = WeeklyRequest(year=year, month=month, week=week)
    except Exception as e:
        logger.error(f"Weekly request validation failed: {str(e)}")
        raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Invalid parameters: {str(e)}"))

    try:
        entries = load_weekly_data(request.year, request.month, request.week)
        return entries

    except McpError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in weekly tool: {str(e)}")
        raise McpError(
            ErrorData(
                code=INTERNAL_ERROR,
                message=f"Unexpected error while fetching weekly data: {str(e)}",
            )
        )


@mcp.tool()
async def monthly(year: int, month: int) -> List[BookmarkEntry]:
    """
    月次人気はてなブックマーク情報の取得

    Get monthly popular Hatena bookmark ranking data.

    Args:
        year: 年度 (2023-2025年対応)
        month: 月 (2023-2024年: 1-12, 2025年: 1-5)

    Returns:
        List of BookmarkEntry models containing ranking data with:
        - rank: ランキング順位
        - title: 記事タイトル
        - url: 元記事のURL
        - hatena_url: はてなブックマークURL

        月次ランキングは50件のエントリーを返します。

    Raises:
        McpError: パラメータが無効、またはデータの読み込みに失敗した場合
    """
    # Validate and create request model
    try:
        request = MonthlyRequest(year=year, month=month)
    except Exception as e:
        logger.error(f"Monthly request validation failed: {str(e)}")
        raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Invalid parameters: {str(e)}"))

    try:
        entries = load_monthly_data(request.year, request.month)
        return entries

    except McpError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in monthly tool: {str(e)}")
        raise McpError(
            ErrorData(
                code=INTERNAL_ERROR,
                message=f"Unexpected error while fetching monthly data: {str(e)}",
            )
        )
