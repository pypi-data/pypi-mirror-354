# TradeStation API Python Wrapper 🚀

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/tradestation-api-python.svg)](https://badge.fury.io/py/tradestation-api-python)

Hey there, Trader! 👋 Ready to connect your Python apps to the TradeStation universe? This library makes it easy-peasy.

Think of it as your friendly Pythonic remote control for TradeStation's API. Build trading bots, analyze data, manage your account – all with clean, asynchronous Python code.

## What Can You Do? ✨

*   **Log In Easily:** Handles the tricky OAuth 2.0 stuff (including token refreshes) so you don't have to.
*   **Market Pulse:** Grab real-time quotes, historical price bars, symbol details, and more.
*   **Account Access:** Check your balances, see your positions, and review order history.
*   **Trade Time:** Place, change, or cancel orders programmatically.
*   **Live Streams:** Get data beamed straight to you with WebSocket support.
*   **Plays Nicely:** Built-in rate limiting helps you avoid getting timed out by the API.

## What You'll Need 📋

*   Python 3.11 or newer (Gotta have that async power!)
*   A TradeStation Account (Real or Simulated)
*   Your TradeStation API Credentials (Client ID & Refresh Token - get these from the [Developer Portal](https://developer.tradestation.com/))

## Get It Installed! 💻

Open your terminal and let's get this library installed.

```bash
# Option 1: Install directly from PyPI (Easiest 🌟)
pip install tradestation-api-python

# Option 2: Clone the project (for developers)
git clone https://github.com/mxcoppell/tradestation-api-python.git
cd tradestation-api-python

# Then install using Poetry (Recommended for development ✨)
poetry install

# OR: Use pip if you prefer
# pip install -e .
```

## Quick Start: Your First API Call! 🚀

Let's fetch a stock quote right now!

1.  **Set up your secrets:** Copy `.env.sample` to `.env` and fill in your `CLIENT_ID`, `REFRESH_TOKEN`, and `ENVIRONMENT` (`Live` or `Simulation`).
    ```bash
    cp .env.sample .env
    # Now edit .env with your details!
    ```
2.  **Run this Python code:**

```python
import asyncio
import os
from dotenv import load_dotenv
from tradestation import TradeStationClient

async def get_a_quote():
    # Load secrets from .env file
    load_dotenv()
    print(f"Using Environment: {os.getenv('ENVIRONMENT')}")

    # Create the client (it reads your .env automatically!)
    client = TradeStationClient()

    try:
        print("Asking TradeStation for an AAPL quote...")
        # Use the market data service to get a quote snapshot
        quote_response = await client.market_data.get_quote_snapshots("AAPL")

        if quote_response and quote_response.Quotes:
            aapl_price = quote_response.Quotes[0].Last
            print(f"----> Got it! AAPL last price: ${aapl_price}")
        else:
            print("Hmm, couldn't get the quote. Error:", getattr(quote_response, 'Errors', 'Unknown error'))

    except Exception as e:
        print(f"Whoops! Something went wrong: {e}")
    finally:
        print("Closing the connection.")
        # Always close the client when you're finished!
        await client.close()

if __name__ == "__main__":
    asyncio.run(get_a_quote())
```

Want more? Check out the `examples/QuickStart` directory for scripts you can run immediately!

## Project Peek 👀

Curious how it's organized?

```
.
├── docs/                 # You are here! (Hopefully useful docs)
├── examples/             # Ready-to-run example scripts!
│   ├── QuickStart/       # Start here!
│   ├── Brokerage/        # Account & order history examples
│   ├── MarketData/       # Price, quote, & symbol examples
│   └── OrderExecution/   # Placing & managing orders examples
└── src/                  # The heart of the library
    └── tradestation/     # The importable package
        ├── client/       # The main TradeStationClient
        ├── services/     # API sections (MarketData, Brokerage, etc.)
        ├── streaming/    # WebSocket streaming code
        ├── ts_types/     # Data models (Pydantic types)
        └── utils/        # Helpers (Auth, Rate Limiting, etc.)
```

## Logging In (Authentication) 🔒

The library needs your API keys to talk to TradeStation. The easiest way is the `.env` file (shown in Quick Start).

Other ways:

1.  **Environment Variables:** Set `CLIENT_ID`, `REFRESH_TOKEN`, `ENVIRONMENT` directly in your system.
2.  **Python Dictionary:**
    ```python
    client = TradeStationClient({
        "client_id": "your_id",
        "refresh_token": "your_token",
        "environment": "Simulation"
    })
    ```
3.  **Direct Parameters:**
    ```python
    client = TradeStationClient(
        refresh_token="your_token",
        environment="Live" # CLIENT_ID still needs to be in env or config
    )
    ```

See [Authentication Guide](docs/authentication.md) for the full scoop.

## Dive Deeper (Documentation) 📚

Ready for more details?

*   [🚀 Quick Start Guide](https://github.com/mxcoppell/tradestation-api-python/blob/main/docs/quick_start.md)
*   [🔑 Authentication](https://github.com/mxcoppell/tradestation-api-python/blob/main/docs/authentication.md)
*   [📊 Market Data](https://github.com/mxcoppell/tradestation-api-python/blob/main/docs/market_data.md)
*   [💼 Brokerage](https://github.com/mxcoppell/tradestation-api-python/blob/main/docs/brokerage.md)
*   [📈 Order Execution](https://github.com/mxcoppell/tradestation-api-python/blob/main/docs/order_execution.md)
*   [⚡ Streaming Data](https://github.com/mxcoppell/tradestation-api-python/blob/main/docs/streaming.md)
*   [🚦 Rate Limiting](https://github.com/mxcoppell/tradestation-api-python/blob/main/docs/rate_limiting.md)

## Contributing 🤝

Got ideas or found a bug? Feel free to open an issue or submit a pull request!

## License 📜

This project is licensed under the MIT License - see the LICENSE file for details.

---

Happy Trading! 🎉 