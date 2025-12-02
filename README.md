# Stock Agent Langchain

**Stock Agent Langchain** is a module within the [AnalystAgent](https://github.com/thaihuyzone/analystagent) ecosystem. It utilizes [LangChain](https://python.langchain.com/) to build AI agents for stock analysis and interactive Q&A.

## Purpose

- Automatically analyze stock information from multiple data sources.
- Support question answering (Q&A) related to stocks and the stock market.
- Extensible for integration with various AI models and data APIs.

## Key Features

- **LangChain integration:** Quickly build stock analysis pipelines using Large Language Models (LLMs).
- **Flexible data ingestion:** Configure to aggregate, crawl, and summarize stock news or market data.
- **Conversational AI agent:** Easily build interactive agents for stock insights and Q&A.

## Installation

```bash
git clone https://github.com/thaihuyzone/analystagent.git
cd analystagent/stock-agent-langchain
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Or install the main dependencies directly:
```bash
pip install -U langchain openai pandas yfinance
```

## Quick Start

Simple example to initialize the agent and ask for stock analysis:

```python
from stock_agent import StockAgent

agent = StockAgent()
result = agent.query("Analyze the stock symbol FPT")
print(result)
```

## Folder Structure

- `agent/`: Core codebase for LangChain agents and related middlewares.
- `data/`: Utilities for crawling, cleaning, and transforming stock data.
- `prompts/`: Prompt engineering and agent logic.
- `test/`: Unit and integration test cases.
- `README.md`: Project documentation (this file).

## Requirements

- Python >= 3.8
- Necessary API keys (e.g. OPENAI_API_KEY) for LLM features

## Contribution

Contributions are welcome! Please open an [issue](https://github.com/thaihuyzone/analystagent/issues) or a pull request for any feature or improvement.

## License

MIT License © [thaihuyzone](https://github.com/thaihuyzone)
