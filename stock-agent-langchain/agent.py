# agent.py
"""
Tầng Agent sử dụng LangChain.
"""

import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

# ĐÚNG CHO 1.1.0: import từ submodule
from langchain.agents.tool_calling_agent.base import create_tool_calling_agent
from langchain.agents.agent import AgentExecutor

from stock_domain import (
    get_recent_price,
    get_history_data,
    analyze_stock_basic,
)

load_dotenv()  # đọc .env nếu có


# 1. Định nghĩa Tools

@tool
def lc_get_price(ticker: str) -> dict:
    """
    Lấy giá gần nhất cho mã chứng khoán.
    Dùng trong LangChain Agent, không phải MCP.
    """
    return get_recent_price(ticker)


@tool
def lc_get_history(
    ticker: str,
    period: str = "3mo",
    interval: str = "1d",
    limit: int = 60,
) -> dict:
    """
    Lấy lịch sử giá, trả về list điểm.
    """
    return get_history_data(ticker, period=period, interval=interval, limit=limit)


@tool
def lc_analyze_stock(
    ticker: str,
    period: str = "3mo",
    interval: str = "1d",
    short_window: int = 20,
    long_window: int = 50,
) -> dict:
    """
    Phân tích cơ bản mã chứng khoán.
    """
    return analyze_stock_basic(
        ticker=ticker,
        period=period,
        interval=interval,
        short_window=short_window,
        long_window=long_window,
    )


# 2. Khởi tạo LLM

def make_llm():
    """
    Tạo LLM dùng OpenAI.
    Mặc định ChatOpenAI sẽ đọc OPENAI_API_KEY từ env.
    """
    return ChatOpenAI(
        model="gpt-4.1-mini",  # tùy model mày có
        temperature=0.1,       # cho trả lời ổn định, ít random
    )


# 3. Prompt cho Agent

def make_prompt():
    """
    Prompt dạng ChatPromptTemplate cho agent.
    """
    system_msg = (
        "Mày là một AI Agent phân tích chứng khoán cho người dùng Việt Nam. "
        "Luôn luôn ưu tiên dùng các tool có sẵn để lấy dữ liệu thật thay vì đoán.\n"
        "- Nếu user hỏi về một mã cụ thể (ví dụ 'AAPL'), hãy dùng lc_analyze_stock "
        "để phân tích, hoặc lc_get_price/lc_get_history khi phù hợp.\n"
        "- Chỉ đưa ra thông tin cho mục đích giáo dục và tham khảo, "
        "không phải khuyến nghị đầu tư.\n"
        "- Giải thích rõ ràng, step-by-step, dễ hiểu cho người mới."
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_msg),
            ("user", "{input}"),
            # agent_scratchpad sẽ được LangChain dùng cho tool calls / reasoning
            ("placeholder", "{agent_scratchpad}"),
        ]
    )
    return prompt

def make_agent_executor():
    """
    Tạo AgentExecutor kết nối LLM + Tools + Prompt.
    """
    llm = make_llm()
    tools = [lc_get_price, lc_get_history, lc_analyze_stock]
    prompt = make_prompt()

    # Tạo agent sử dụng tool-calling
    agent = create_tool_calling_agent(
        llm=llm,
        tools=tools,
        prompt=prompt,
    )

    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,  # log ra step để mày thấy nó gọi tool gì
    )
    return executor


def main():
    executor = make_agent_executor()
    print("Agent chứng khoán đã sẵn sàng. Gõ 'exit' để thoát.")

    while True:
        user_input = input("\nUser: ")
        if user_input.strip().lower() in {"exit", "quit"}:
            break

        result = executor.invoke({"input": user_input})
        # result là dict, thường có key 'output'
        print("\nAgent:", result["output"])


if __name__ == "__main__":
    main()

