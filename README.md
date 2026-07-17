# 🤖 Crypto V2 Bot — Multi-Language Telegram Crypto Assistant

<p align="center">
  <img src="assets/header.png" alt="Crypto Bot v2" width="600"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" />
  <img src="https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram" />
  <img src="https://img.shields.io/badge/API-Covalent-ff69b4" />
  <img src="https://img.shields.io/badge/API-CoinGecko-green?logo=bitcoin" />
  <img src="https://img.shields.io/badge/deploy-Railway-purple?logo=railway" />
  <img src="https://img.shields.io/badge/license-MIT-brightgreen" />
</p>

A comprehensive bilingual (Persian/English) Telegram bot for everything crypto. Live prices for 28+ coins, Fear & Greed index, cached news with AI translation, whale transaction tracking, Ethereum gas fees, wallet monitoring across 23 EVM chains via the Covalent API, USD/Toman exchange rates, and an AI assistant powered by gpt-5.4-mini — all packed into one bot with an interactive inline menu.

---

## 📋 Table of Contents

- [What Can It Do?](#-what-can-it-do)
- [Commands Reference](#-commands-reference)
- [Wallet Monitoring Deep Dive](#-wallet-monitoring-deep-dive)
- [AI Assistant](#-ai-assistant)
- [Bilingual Interface](#-bilingual-interface)
- [Supported Coins & Aliases](#-supported-coins--aliases)
- [Installation Guide](#-installation-guide)
- [Environment Variables](#-environment-variables)
- [Project Architecture](#-project-architecture)
- [APIs & Services Used](#-apis--services-used)
- [Railway Deployment](#-railway-deployment)
- [Contributing](#-contributing)
- [License](#-license)
- [Special Thanks](#-special-thanks)

---

## ✨ What Can It Do?

### 🔸 Live Crypto Prices
Get real-time prices for 28 of the top cryptocurrencies by market cap. Each entry shows the current price in USD, the 24-hour percentage change with color-coded indicators (🟢 green for gains, 🔴 red for losses), and the coin name with its icon. You can query multiple coins at once, and the bot supports over 50 aliases so you can use short forms like `btc` instead of `bitcoin`, `eth` instead of `ethereum`, or `sol` instead of `solana`. The default list covers Bitcoin, Ethereum, Solana, Ripple, Cardano, Dogecoin, Polkadot, Chainlink, Avalanche, Polygon, Tron, Litecoin, Shiba Inu, Toncoin, BNB, Aptos, Arbitrum, Optimism, VeChain, Near, Injective, Sei, Starknet, Worldcoin, Pepe, Bonk, OneFootball Club, and Dogwifhat.

### 🔸 Fear & Greed Index
The Fear & Greed Index is a widely followed market sentiment indicator that ranges from 0 (Extreme Fear) to 100 (Extreme Greed). The bot fetches this data from alternative.me and displays the last 7 days of readings with intuitive emojis — 😱 for Extreme Fear, 😨 for Fear, 😐 for Neutral, 😏 for Greed, and 🤑 for Extreme Greed. This helps you gauge whether the market is driven by fear (possible buying opportunity) or greed (possible correction ahead).

### 🔸 Crypto News with AI Translation
The bot automatically fetches the latest news headlines from CoinDesk and CoinTelegraph every hour and caches them locally. When you request news, you get the most recent stories with their publication time. For Persian-speaking users, the bot goes a step further — it uses the AI assistant to translate each headline from English to Persian on the fly, so you get the news in your own language without needing a separate Persian news source. No more relying on RSS feeds that break or websites that are blocked.

### 🔸 Whale Transaction Tracking
Keep an eye on the big players. The bot monitors Ethereum transactions valued at over $1 million USD using the Etherscan API. Each alert includes the transaction hash (linked to Etherscan for verification), the amount transferred in ETH and its USD equivalent, the sender and recipient addresses, and a timestamp. This is useful for tracking large movements by whales, exchanges, or institutional investors.

### 🔸 Ethereum Gas Fees
Gas fees on Ethereum can be unpredictable. The bot fetches the latest gas prices from Etherscan and displays them in three categories: Safe (slow, cheapest), Normal (average), and Fast (priority, most expensive). Each is shown in Gwei alongside the current price of ETH so you can estimate transaction costs in dollar terms. Whether you're swapping tokens, minting an NFT, or moving funds, this helps you decide when to transact.

### 🔸 Wallet Monitoring Across 23 EVM Chains
This is the flagship feature. The bot can monitor any wallet address across 23 different EVM-compatible blockchains using a single Covalent API key. You get instant Telegram notifications for both native coin transfers and token transfers. The supported chains include: Ethereum, BSC (BNB Chain), Polygon, Arbitrum, Optimism, Base, Avalanche C-Chain, Cronos, Fantom, Gnosis, zkSync Era, Linea, Scroll, Blast, Mantle, Moonbeam, Celo, Polygon zkEVM, Aurora, Metis, HyperEVM, Unichain, and Robinhood Chain. Every 15 seconds, the bot checks for new blocks on each chain and scans for transactions involving your watched wallets.

### 🔸 USD/Toman Exchange Rate
For Iranian users, the bot provides live USDT and USD prices in Iranian Toman. It pulls data from Wallex (one of the few Iranian exchanges whose API isn't DNS-blocked on cloud platforms like Railway). This is especially useful for Iranian crypto traders who need to calculate their portfolio value in local currency.

### 🔸 Interactive Inline Menu
Every feature is accessible through a clean, intuitive inline menu. The main menu offers buttons for Prices, Fear & Greed, USD/Toman, News, Whales, Gas Fees, Wallet Monitoring, and AI Assistant. Many of these pages have a refresh button (🔄) that lets you update the data without leaving the chat. The menu adapts to your language preference — Persian or English.

### 🔸 AI Assistant Powered by gpt-5.4-mini
The bot includes a general-purpose AI assistant that can answer questions about blockchain technology, DeFi protocols, market analysis, trading strategies, smart contract development, and much more. You can either use the `/ask` command followed by your question, or simply send any text that isn't a recognized command — the bot will automatically route it to the AI for a response. The AI is powered by the gpt-5.4-mini model served through freemodel.dev, and it responds in whichever language you're using (Persian or English).

---

## 📖 Commands Reference

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Initialize the bot and select your language | `/start` |
| `/help` | Display the full help message with all commands | `/help` |
| `/price [coin...]` | Get live prices for one or more coins (space-separated). If no coins given, shows the default 28. | `/price btc eth sol` |
| `/alert <coin> <above/below> <price>` | Set a price alert. The bot will notify you when the coin crosses your threshold. | `/alert btc above 100000` |
| `/fng [days]` | Show the Fear & Greed index. Optionally specify the number of past days to display. | `/fng 30` |
| `/news [count]` | Show the latest crypto news. Optionally specify how many headlines to show. | `/news 5` |
| `/whale` | List the most recent large Ethereum transactions (over $1M). | `/whale` |
| `/gas` | Display current Ethereum gas fees in Gwei. | `/gas` |
| `/toman` | Get the latest USDT/USD price in Iranian Toman from Wallex. | `/toman` |
| `/ask <question>` | Ask the AI assistant anything about crypto, blockchain, or markets. | `/ask what is a liquidity pool?` |
| `/watch <address> [chain]` | Start monitoring a wallet. If no chain is specified, it monitors on all 23 chains. | `/watch 0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18` |
| `/unwatch <address> [chain]` | Stop monitoring a wallet. If no chain is specified, removes from all chains. | `/unwatch 0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18` |
| `/wallets` | List all wallets you are currently monitoring, grouped by chain. | `/wallets` |
| `/check` | Force an immediate scan of all watched wallets (bypasses the 15-second interval). | `/check` |
| `/lang` | Toggle between Persian and English. | `/lang` |

---

## 👁 Wallet Monitoring Deep Dive

### How It Works
The wallet monitoring system uses the **Covalent Unified API** to query transaction history across 23 EVM-compatible chains. Every 15 seconds, the bot's `check_wallets` job (registered via PTB's `JobQueue`) runs and does the following for each watched wallet on each chain:

1. Reads the last checked block number from `last-block.json`.
2. Calls the Covalent `transactions_v2` endpoint for native coin transfers and the `transfers_v2` endpoint for ERC-20 token transfers.
3. Parses the response, normalizing it to a common format regardless of the chain.
4. Compares the returned transactions against the last known block. Any transaction with a block number higher than the stored one is considered new.
5. For each new transaction, sends a Telegram notification to the user with full details.
6. Updates the stored block number to the latest block seen.

### Notification Format
When a new transaction is detected, you receive a message like this:

```
🔔 New Transaction on Ethereum
💱 Type: Native
   Amount: 0.05 ETH ($165.00)
📤 From: 0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18
📥 To:   0x1234567890abcdef1234567890abcdef12345678
🔗 https://etherscan.io/tx/0x...
```

### Commands in Detail

- `/watch 0x... eth` — adds the wallet to the Ethereum watchlist only.
- `/watch 0x...` — adds the wallet to **all 23 chains**. This is useful if you hold the same address on multiple networks (common with wallets like MetaMask that share the same address across EVM chains).
- `/unwatch 0x... eth` — removes the wallet from Ethereum only.
- `/unwatch 0x...` — removes the wallet from all chains.
- `/wallets` — shows a formatted list of your watched addresses grouped by chain with a total count.
- `/check` — runs the scan immediately and reports any new transactions found.

### Block Number Tracking
The bot maintains a `last-block.json` file that stores the last checked block number for each (user, address, chain) tuple. This prevents sending duplicate notifications for the same transaction. When the bot restarts, it picks up from where it left off. If a chain has been inactive (no new blocks), the bot will still check it every cycle but won't spam you with empty results.

### Chain Support Details
The 23 supported chains cover the vast majority of DeFi activity:

| # | Chain | Chain ID | Explorer |
|---|-------|----------|----------|
| 1 | Ethereum | 1 | etherscan.io |
| 2 | BSC (BNB Chain) | 56 | bscscan.com |
| 3 | Polygon | 137 | polygonscan.com |
| 4 | Arbitrum | 42161 | arbiscan.io |
| 5 | Optimism | 10 | optimistic.etherscan.io |
| 6 | Base | 8453 | basescan.org |
| 7 | Avalanche C-Chain | 43114 | snowtrace.io |
| 8 | Cronos | 25 | cronoscan.com |
| 9 | Fantom | 250 | ftmscan.com |
| 10 | Gnosis | 100 | gnosisscan.io |
| 11 | zkSync Era | 324 | explorer.zksync.io |
| 12 | Linea | 59144 | lineascan.build |
| 13 | Scroll | 534352 | scrollscan.com |
| 14 | Blast | 81457 | blastscan.io |
| 15 | Mantle | 5000 | mantlescan.xyz |
| 16 | Moonbeam | 1284 | moonbeam.moonscan.io |
| 17 | Celo | 42220 | celoscan.io |
| 18 | Polygon zkEVM | 1101 | zkevm.polygonscan.com |
| 19 | Aurora | 1313161554 | aurorascan.dev |
| 20 | Metis | 1088 | andromeda-explorer.metis.io |
| 21 | HyperEVM | 999 | hyperevm.blockscout.com |
| 22 | Unichain | 130 | unichain.blockscout.com |
| 23 | Robinhood Chain | 5536 | robinhood.blockscout.com |

### Limitations
- Covalent's free tier allows 75,000 requests per month. With 23 chains and a 15-second interval, you can monitor approximately 2-3 wallets comfortably. For more wallets, consider upgrading to Covalent's paid plan.
- Some smaller chains (like Polygon zkEVM and Aurora) may occasionally return errors on the free tier. The bot handles these gracefully and skips them.
- The bot must be running to detect transactions. If it's offline, it will catch up when restarted (up to the Covalent API's historical depth).

---

## 🤖 AI Assistant

The AI assistant is built on top of the **gpt-5.4-mini** model accessed through **freemodel.dev**'s free API. It's designed to answer crypto-related questions with depth and accuracy.

**How to use it:**
- Type `/ask what is Ethereum?` and get a detailed answer.
- Or simply send a message like "توضیح بده دیفای چیه" without any command prefix — the bot will recognize it's not a command and route it to the AI.

**Capabilities:**
- Explaining blockchain concepts (consensus mechanisms, sharding, rollups, etc.)
- DeFi protocol analysis (Uniswap, Aave, Curve, etc.)
- Market analysis and trading concepts
- Smart contract basics and security considerations
- Tokenomics evaluation
- Historical crypto events and their impact

**Language:** The AI responds in the same language you're using. If your bot language is set to Persian, the AI answers in Persian. If English, it answers in English.

**Note:** The free tier of freemodel.dev has rate limits. If you send too many requests in a short period, the API may temporarily throttle you.

---

## 🌐 Bilingual Interface

The bot fully supports both **English (EN)** and **Persian/Farsi (FA)**. The language system works as follows:

- On first `/start`, you choose your language from two inline buttons.
- The choice is stored in `user_lang.json` keyed by your Telegram user ID.
- Every menu, message, and command response is rendered in your selected language.
- You can switch at any time using `/lang`.
- The AI assistant also follows your language preference.

All text strings are stored in `lang.py` as two dictionaries — `EN` and `FA` — with identical keys. When a message needs to be sent, the bot looks up the key in the appropriate dictionary based on the user's language setting.

---

## 🪙 Supported Coins & Aliases

### Default 28 Coins (shown when `/price` is called without arguments)
```
bitcoin, ethereum, solana, ripple, cardano,
dogecoin, polkadot, chainlink, avalanche-2, matic-network,
tron, litecoin, shiba-inu, the-open-network,
binancecoin, aptos, arbitrum, optimism,
vechain, near, injective, sei-network,
starknet, worldcoin-wld, pepe, bonk,
onefootball-club, dogwifhat
```

### Available Aliases (50+)
```
btc→bitcoin, eth→ethereum, sol→solana, xrp→ripple,
ada→cardano, dot→polkadot, ltc→litecoin, link→chainlink,
matic→matic-network, avax→avalanche-2, bnb→binancecoin,
doge→dogecoin, trx→tron, atom→cosmos, uni→uniswap,
aave→aave, cro→crypto-com-chain, vet→vechain,
theta→theta-token, fil→filecoin, icp→internet-computer,
near→near, apt→aptos, sui→sui, arb→arbitrum,
op→optimism, inj→injective, ldo→lido-dao,
rune→thorchain, ftm→fantom, cake→pancakeswap,
ofc→onefootball-club, shib→shiba-inu, ton→the-open-network,
tia→celestia, sei→sei-network, stx→blockstack,
egld→elrond-erd-2, algo→algorand, frtn→forta,
pendle→pendle, ondo→ondo-finance, jto→jito-governance-token,
io→io-net, strk→starknet, wld→worldcoin-wld,
pepe→pepe, floki→floki, bonk→bonk,
wif→dogwifhat, meme→memecoin
```

You can define additional aliases by editing the `COIN_ALIASES` dictionary in `utils.py`.

---

## 🛠 Installation Guide

### Prerequisites
- **Python 3.10 or higher** — The bot uses modern Python features including async/await and type hints.
- **pip** — Python package manager.
- **A Telegram Bot Token** — Get yours from [@BotFather](https://t.me/BotFather) on Telegram.
- **API Keys** — Most features work with free API keys; see the Environment Variables section below.

### Step-by-Step Setup

```bash
# 1. Clone the repository
git clone https://github.com/dormani9/crypto-bot-v2.git
cd crypto-bot-v2

# 2. Create and activate a virtual environment (recommended)
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# 3. Install all dependencies
pip install -r requirements.txt

# 4. Create your environment file from the example
# On Windows:
copy .env.example .env
# On Linux/macOS:
cp .env.example .env

# 5. Open .env in your editor and fill in at least the TELEGRAM_BOT_TOKEN
#    See the Environment Variables section for details on each key.

# 6. Run the bot
python main.py
```

The bot will start polling Telegram for updates. You should see log messages confirming that the bot is online and that handlers have been registered.

### Running with Docker (Alternative)
If you prefer Docker, you can build and run the bot in a container:

```bash
docker build -t crypto-bot-v2 .
docker run -d --env-file .env --name crypto-bot crypto-bot-v2
```

---

## 🔐 Environment Variables

The bot uses environment variables for all configuration. These can be set in a `.env` file for local development or as environment variables in your deployment platform (Railway, Heroku, etc.).

| Variable | Required | Description | How to Get It |
|----------|----------|-------------|---------------|
| `TELEGRAM_BOT_TOKEN` | ✅ **Yes** | Your Telegram bot token from BotFather. Every Telegram bot needs this to authenticate with the Telegram API. | [@BotFather](https://t.me/BotFather) — create a bot and copy the token. |
| `COVALENT_API_KEY` | ✅ **For wallet monitoring** | The Covalent Unified API key. This single key gives you access to transaction data for all 23 supported EVM chains. Without this, the `/watch`, `/unwatch`, `/wallets`, and `/check` commands will not work. | [Covalent](https://www.covalenthq.com/) — sign up for a free account and get your API key from the dashboard. |
| `COINGECKO_API_KEY` | ❌ Optional | CoinGecko API key for price data. The free tier works without a key but has a rate limit of ~10-30 calls per minute. With a key, you get a higher rate limit and priority access. | [CoinGecko](https://www.coingecko.com/en/api) — register and get a free demo API key. |
| `FREEMODEL_API_KEY` | ❌ Optional | API key for the AI assistant (gpt-5.4-mini). Without this, the `/ask` command and free-form AI responses will not work. | [freemodel.dev](https://freemodel.dev) — register for a free account and get your API key. |
| `ETHERSCAN_API_KEY` | ❌ Optional | Etherscan API key used for the gas fee estimator and whale transaction tracking. Without it, `/gas` and `/whale` will not work. | [Etherscan](https://etherscan.io/myapikey) — create a free account and generate an API key. |
| `BLOCKSCOUT_API_KEY` | ❌ Optional | Blockscout Pro API key. Some chains (like Robinhood Chain) require a Blockscout Pro key for higher rate limits. The bot will work without it but may hit rate limits. | [Blockscout](https://blockscout.com) — sign up for a Pro account. |

### Quick Start Checklist
- ✅ `TELEGRAM_BOT_TOKEN` — mandatory for the bot to run at all.
- ✅ `COVALENT_API_KEY` — highly recommended if you want wallet monitoring.
- ✅ `FREEMODEL_API_KEY` — recommended if you want the AI assistant.
- ❌ Everything else is optional and can be added later.

---

## 📁 Project Architecture

```
crypto-bot-v2/
├── main.py                      # Application entry point. Sets up the bot, registers all
│                                # handlers, configures the JobQueue for wallet monitoring
│                                # and news refresh, and starts polling.
│
├── utils.py                     # Utility functions: fetch_prices() for CoinGecko data,
│                                # fetch_toman_price() for Wallex rates, and the
│                                # COIN_ALIASES dictionary mapping shortcuts to full names.
│
├── lang.py                      # Bilingual dictionary containing all UI text in both
│                                # English (EN) and Persian (FA). Also manages user
│                                # language preferences (get_lang, set_lang) with
│                                # persistent storage in user_lang.json.
│
├── requirements.txt             # Python package dependencies.
│
├── .env.example                 # Example environment file with all possible variables.
│
├── wallet-monitor.json          # Auto-generated file storing watched wallets per user,
│                                # keyed by Telegram user ID, with nested addresses and chains.
│
├── last-block.json              # Auto-generated file tracking the last scanned block
│                                # per (user, address, chain) tuple for efficient polling.
│
├── user_lang.json               # Auto-generated file storing each user's language
│                                # preference (persists across bot restarts).
│
├── README.md                    # This documentation file.
│
├── assets/                      # Static assets used by the bot.
│   ├── header.png               # Banner image sent on /start.
│   └── thanks-misagh.jpg        # Thank you image in the README.
│
└── handlers/                    # All command and callback handlers organized by feature.
    ├── __init__.py              # Empty init to make handlers a package.
    │
    ├── start.py                 # /start — sends the header image, shows language
    │                            # selection. /help — comprehensive help text with
    │                            # all commands explained. /lang — toggles language.
    │                            # Also contains the main menu rendering with
    │                            # all feature buttons.
    │
    ├── price.py                 # /price — fetches and displays live prices from
    │                            # CoinGecko for requested coins. Supports aliases
    │                            # and multiple coins in one command. /alert — sets
    │                            # price alerts (above/below) with persistent storage.
    │
    ├── news.py                  # /news — fetches cached news from CoinDesk and
    │                            # CoinTelegraph RSS feeds. Refreshes cache hourly.
    │                            # Translates headlines to Persian using AI for
    │                            # Persian-speaking users. Supports count parameter.
    │
    ├── fng.py                   # /fng — Fear & Greed Index from alternative.me.
    │                            # Shows the last 7 days by default, configurable
    │                            # with an optional day count parameter.
    │
    ├── whale.py                 # /whale — Large Ethereum transactions (>$1M) from
    │                            # Etherscan API. Shows tx hash, value, addresses,
    │                            # and link to Etherscan for verification.
    │
    ├── gas.py                   # /gas — Ethereum gas fees from Etherscan API.
    │                            # Displays Safe, Normal, and Fast in Gwei with
    │                            # current ETH price for USD estimation.
    │
    ├── toman.py                 # /toman — USDT and USD to Iranian Toman rates
    │                            # from Wallex exchange API. Used by Iranian users
    │                            # to track local currency values.
    │
    ├── watch.py                 # /watch, /unwatch, /wallets, /check — The wallet
    │                            # monitoring system. Manages watchlists, queries
    │                            # Covalent API across 23 chains, detects new
    │                            # transactions, and sends notifications. Uses
    │                            # block-number tracking to avoid duplicates.
    │
    ├── ai.py                    # /ask — AI assistant powered by gpt-5.4-mini via
    │                            # freemodel.dev. Handles free-form text as well.
    │                            # Language-aware: responds in the user's language.
    │                            # Implements retry logic for API failures.
    │
    └── menu.py                  # Inline menu system. Handles all callback queries
                               # from the interactive buttons. Routes to the
                               # appropriate handler based on callback data.
```

### Data Flow

```
User → /start → header image → language selection → main menu
                                                       │
                    ┌──────────────────────────────────┼──────────────────────────────────┐
                    │              │              │              │              │         │
                    ▼              ▼              ▼              ▼              ▼         ▼
               🔹 Prices     🔹 Fear&Greed   🔹 USD/Toman    🔹 News      🔹 Whale    🔹 Gas
               CoinGecko     alternative.me    Wallex       RSS+AI       Etherscan   Etherscan
                                                             
                    ┌──────────────────────────────────┐
                    │              │                   │
                    ▼              ▼                   ▼
               🔹 Wallet       🔹 AI            🔹 Help/Lang
               Covalent(23)   freemodel.dev       inline
```

---

## 🌐 APIs & Services Used

| Service | Purpose | Documentation | License / Cost |
|---------|---------|---------------|----------------|
| **Covalent** | Unified blockchain data API for wallet monitoring across 23 EVM chains. Provides transactions, token transfers, and balances through a single endpoint. | [docs](https://www.covalenthq.com/docs/api/) | **Free tier**: 75,000 requests/month. Paid plans for higher limits. |
| **CoinGecko** | Cryptocurrency price data for 28+ coins with 24-hour price change percentages. Used by `/price` and the menu. | [docs](https://docs.coingecko.com) | **Free** with API key (demo key available). Higher rate limits with paid plans. |
| **Etherscan v2** | Ethereum blockchain explorer API. Used for gas fee estimation and whale transaction detection. | [docs](https://docs.etherscan.io) | **Free tier**: 5 calls/second, 100,000 calls/day max. |
| **alternative.me** | Fear & Greed Index API. Simple REST endpoint returning historical market sentiment data. | [docs](https://alternative.me/crypto/fear-and-greed-index) | **Free**. No API key required. |
| **freemodel.dev** | AI model hosting service providing access to gpt-5.4-mini. Used by the AI assistant for question answering and news translation. | [freemodel.dev](https://freemodel.dev) | **Free tier** available with rate limits. |
| **Wallex** | Iranian cryptocurrency exchange. Provides USDT and USD to Iranian Toman rates through its public API. | [wallex.ir](https://wallex.ir) | **Free**. No API key required. |
| **CoinDesk / CoinTelegraph** | Leading crypto news publications. RSS feeds are fetched and cached by the news module. | — | **Free** (RSS). |

---

## 🚀 Railway Deployment

This bot is designed to run seamlessly on Railway, a cloud platform that automatically deploys from GitHub. Here's how to set it up:

### Step 1: Push to GitHub
```bash
git add .
git commit -m "ready for deploy"
git push
```

### Step 2: Create a Railway Project
1. Go to [Railway.app](https://railway.app) and log in with your GitHub account.
2. Click "New Project" → "Deploy from GitHub repo".
3. Select your `crypto-bot-v2` repository.
4. Railway will automatically detect the Python project and start building.

### Step 3: Configure Environment Variables
In the Railway dashboard, go to your project's settings and add the following variables under "Environment":

- `TELEGRAM_BOT_TOKEN` — required
- `COVALENT_API_KEY` — required for wallet monitoring
- `COINGECKO_API_KEY` — optional
- `FREEMODEL_API_KEY` — optional
- `ETHERSCAN_API_KEY` — optional
- `BLOCKSCOUT_API_KEY` — optional

### Step 4: Automatic Deploys
Railway is configured to auto-deploy whenever you push to your GitHub repository's main branch. You can also trigger manual deploys from the dashboard.

### Important Notes for Railway
- **Start Command**: Railway automatically runs `python main.py` based on the Procfile or the start script detection.
- **Build Command**: Railway runs `pip install -r requirements.txt` automatically.
- **Persistent Storage**: The bot writes JSON files (`wallet-monitor.json`, `last-block.json`, `user_lang.json`) to the local filesystem. On Railway, these will persist as long as the service isn't restarted. For production use with multiple instances, consider using a database or Redis.
- **Iranian Exchange DNS Block**: Nobitex and Bit24 APIs are DNS-blocked on Railway's infrastructure. Wallex is the only reliable Iranian exchange API for Toman rates.
- **Logs**: Use `railway logs` (CLI) or the dashboard to view real-time bot logs for debugging.

### Alternative: Docker Deployment
If you prefer Docker, a `Dockerfile` is included in the repository. Build and push it to any container registry, then deploy it on Railway, Fly.io, or any other container platform.

---

## 🤝 Contributing

Contributions of all kinds are welcome — bug reports, feature requests, documentation improvements, and code contributions.

### How to Contribute
1. **Fork the repository** on GitHub.
2. **Create a new branch** for your feature or fix:
   ```bash
   git checkout -b feature/my-new-feature
   ```
3. **Make your changes** following the existing code style. The codebase uses Python type hints, async patterns from python-telegram-bot, and simple dictionary-based language strings.
4. **Test your changes** by running the bot locally. Ensure existing commands still work as expected.
5. **Commit with a clear message**:
   ```bash
   git commit -m "feat: add support for chain XYZ in wallet monitor"
   ```
6. **Push to your fork** and open a Pull Request to the `main` branch.

### Guidelines
- Follow the existing code structure. New features should go in their own file under `handlers/` and be registered in `main.py`.
- All user-facing text should support both English and Persian. Add new strings to `lang.py` in both `EN` and `FA` dictionaries.
- Use the same dictionary keys for the same text in both languages.
- Keep function signatures consistent with the rest of the codebase.
- Don't add unnecessary comments to the code.

---

## 📝 License

This project is licensed under the MIT License. You are free to use, modify, distribute, and sell this software, provided that the original copyright notice and license text are included in all copies or substantial portions of the software.

See the `LICENSE` file for the full license text.

---

## 🙏 Special Thanks

<p align="center">
  <a href="https://github.com/Misagh95/">
    <img src="assets/thanks-misagh.jpg" alt="Thanks to Misagh" width="300"/>
  </a>
</p>

Special thanks to **Misagh** for his invaluable collaboration, support, and contributions throughout this project. From testing wallet monitoring across multiple chains to providing feedback on the user interface and helping refine the bot's features, his involvement has been instrumental in making this bot what it is today.

---

<p align="center">
  Made with ❤️ for the crypto community
</p>
