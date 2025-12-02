# server.py
"""
FastMCP server: xuất bản các hàm domain thành MCP tools.
"""

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from stock_domain import (
    get_recent_price,
    get_history_data,
    analyze_stock_basic,
)

mcp = FastMCP("StockServer")


@mcp.tool
def get_price(ticker: str) -> dict:
    """Lấy giá gần nhất cho một mã chứng khoán."""
    try:
        return get_recent_price(ticker)
    except Exception as e:
        # Chuyển lỗi Python sang MCP ToolError
        raise ToolError(str(e))


@mcp.tool
def get_history(
    ticker: str,
    period: str = "3mo",
    interval: str = "1d",
    limit: int = 60,
) -> dict:
    """Lấy lịch sử giá."""
    try:
        return get_history_data(ticker, period=period, interval=interval, limit=limit)
    except Exception as e:
        raise ToolError(str(e))


@mcp.tool
def analyze_stock(
    ticker: str,
    period: str = "3mo",
    interval: str = "1d",
    short_window: int = 20,
    long_window: int = 50,
) -> dict:
    """Phân tích cơ bản một mã chứng khoán."""
    try:
        return analyze_stock_basic(
            ticker=ticker,
            period=period,
            interval=interval,
            short_window=short_window,
            long_window=long_window,
        )
    except Exception as e:
        raise ToolError(str(e))


if __name__ == "__main__":
    mcp.run()
