# stock_domain.py
"""
Tầng domain: toàn bộ logic chứng khoán nằm ở đây.
Không phụ thuộc LangChain hay FastMCP.
"""

import yfinance as yf
from statistics import pstdev


def get_recent_price(ticker: str) -> dict:
    """
    Lấy giá gần nhất cho một mã chứng khoán.
    Trả về dict để dễ dùng cho Agent hoặc MCP.
    """
    if not ticker:
        raise ValueError("Ticker không được rỗng")

    hist = yf.download(
        tickers=ticker,
        period="5d",
        interval="1d",
        progress=False,
    )

    if hist.empty:
        raise ValueError(f"Không có dữ liệu cho mã {ticker}")

    last_row = hist.tail(1).iloc[0]
    return {
        "ticker": ticker,
        "last_close": float(last_row["Close"]),
        "open": float(last_row["Open"]),
        "high": float(last_row["High"]),
        "low": float(last_row["Low"]),
        "volume": int(last_row["Volume"]),
    }


def get_history_data(
    ticker: str,
    period: str = "3mo",
    interval: str = "1d",
    limit: int = 60,
) -> dict:
    """
    Lấy lịch sử giá, trả về list dict.
    """
    if not ticker:
        raise ValueError("Ticker không được rỗng")

    df = yf.download(
        tickers=ticker,
        period=period,
        interval=interval,
        progress=False,
    )

    if df.empty:
        raise ValueError(f"Không có lịch sử giá cho {ticker}")

    df = df.tail(limit).reset_index()
    points = []
    for _, row in df.iterrows():
        points.append(
            {
                "date": row["Date"].strftime("%Y-%m-%d"),
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"]),
                "volume": int(row["Volume"]),
            }
        )

    return {
        "ticker": ticker,
        "period": period,
        "interval": interval,
        "points": points,
    }


def analyze_stock_basic(
    ticker: str,
    period: str = "3mo",
    interval: str = "1d",
    short_window: int = 20,
    long_window: int = 50,
) -> dict:
    """
    Phân tích cơ bản: MA ngắn, MA dài, trend và volatility đơn giản.
    """
    if not ticker:
        raise ValueError("Ticker không được rỗng")

    df = yf.download(
        tickers=ticker,
        period=period,
        interval=interval,
        progress=False,
    )

    if df.empty:
        raise ValueError(f"Không có dữ liệu cho {ticker}")

    df = df.reset_index()
    closes = df["Close"].tolist()

    if len(closes) < max(short_window, long_window):
        raise ValueError(
            f"Dữ liệu quá ngắn ({len(closes)} điểm) cho MA {short_window} / {long_window}"
        )

    df["MA_short"] = df["Close"].rolling(window=short_window).mean()
    df["MA_long"] = df["Close"].rolling(window=long_window).mean()

    last = df.tail(1).iloc[0]
    ma_short = float(last["MA_short"])
    ma_long = float(last["MA_long"])
    last_close = float(last["Close"])

    # Tính volatility đơn giản từ return ngày
    returns = []
    for i in range(1, len(closes)):
        prev = closes[i - 1]
        if prev > 0:
            r = (closes[i] - prev) / prev
            returns.append(r)

    volatility = float(pstdev(returns)) if returns else 0.0

    if ma_short > ma_long:
        trend = "uptrend_ngắn_hạn"
    elif ma_short < ma_long:
        trend = "downtrend_ngắn_hạn"
        # sideway nôm na
    else:
        trend = "sideway"

    return {
        "ticker": ticker,
        "period": period,
        "last_close": last_close,
        "ma_short": ma_short,
        "ma_long": ma_long,
        "trend": trend,
        "volatility_estimate": volatility,
        "note": (
            "Trend được xác định dựa trên giao cắt MA ngắn/dài; "
            "volatility là độ lệch chuẩn của return ngày."
        ),
    }
