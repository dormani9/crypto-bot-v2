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
</p>

A comprehensive bilingual (Persian/English) Telegram bot for the crypto world. Live prices, Fear & Greed index, news, whale transactions, Ethereum gas fees, wallet monitoring across 23 EVM chains, USD/Toman rates, and an AI assistant — all in one bot.

---

## 📋 Table of Contents

- [Features](#-features)
- [Commands](#-commands)
- [Wallet Monitoring](#-wallet-monitoring)
- [Installation](#-installation)
- [Environment Variables](#-environment-variables)
- [Project Structure](#-project-structure)
- [APIs Used](#-apis-used)
- [Railway Deployment](#-railway-deployment)
- [License](#-license)

---

## ✨ Features

### 🔸 Live Crypto Prices
Display prices for 28+ top coins with 24h change indicators (🟢 up / 🔴 down). Supports aliases: `btc` → `bitcoin`, `eth` → `ethereum`, `sol` → `solana` → ` and 50+ other tokens.

### 🔸 Fear & Greed Index
Market sentiment over the last 7 days with emojis: 😱 Extreme Fear → 🤑 Extreme Greed.

### 🔸 Crypto News
- Cached English news from CoinDesk + CoinTelegraph (refreshed hourly)
- Persian users get AI-translated headlines automatically

### 🔸 Whale Transactions
Track transactions over $1M on Ethereum via Etherscan API.

### 🔸 Ethereum Gas Fees
Display Safe, Normal, and Fast gas prices with live ETH price.

### 🔸 Wallet Monitoring (23 EVM Chains)
Monitor any wallet across 23 EVM-compatible chains. Get instant Telegram notifications on new transactions.

**Supported chains:** Ethereum, BSC, Polygon, Arbitrum, Optimism, Base, Avalanche, Cronos, Fantom, Gnosis, zkSync Era, Linea, Scroll, Blast, Mantle, Moonbeam, Celo, Polygon zkEVM, Aurora, Metis, HyperEVM, Unichain, Robinhood Chain

### 🔸 USD/Toman Rate
Live USDT and USD to Iranian Toman rates from Wallex exchange.

### 🔸 Interactive Menu
All features accessible through inline buttons with refresh support for live data.

### 🔸 AI Assistant
- `/ask <question>` or send any text message (free-form)
- Expert responses on blockchain, DeFi, market analysis
- Persian/English — follows your selected language
- Powered by `gpt-5.4-mini` via freemodel.dev

### 🔸 Bilingual Interface
Full Persian and English support. Language selection on first `/start`, change anytime with `/lang`.

---

## 📖 Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Start the bot & select language | `/start` |
| `/help` | Show help | `/help` |
| `/price [coin...]` | Live prices for one or more coins | `/price btc eth sol` |
| `/fng` | Fear & Greed index | `/fng` |
| `/news` | Latest crypto news | `/news` |
| `/whale` | Whale transactions | `/whale` |
| `/gas` | Ethereum gas fees | `/gas` |
| `/toman` | USD/Toman rate | `/toman` |
| `/ask <question>` | Ask the AI assistant | `/ask what is DeFi?` |
| `/watch <address> [chain]` | Start monitoring a wallet | `/watch 0x... eth` |
| `/unwatch <address> [chain]` | Stop monitoring | `/unwatch 0x...` |
| `/wallets` | List all watched wallets | `/wallets` |
| `/check` | Force a manual wallet scan | `/check` |
| `/lang` | Change language | `/lang` |

Any non-command text also triggers the AI assistant automatically.

---

## 👁 Wallet Monitoring

Monitor any EVM wallet across 23 chains with real-time Telegram notifications.

```
/watch 0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18     → monitors on ALL 23 chains
/watch 0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18 bsc → monitors only on BSC
/wallets                                                 → list your watched wallets
/unwatch 0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18     → remove from watchlist
/check                                                   → force scan right now
```

**How it works:** The bot checks all watched wallets every 15 seconds via the Covalent API. When a new transaction is detected (incoming or outgoing, native or token), you receive an instant notification with:

- 🔔 Transaction type (Native / Token)
- 💱 Amount and symbol
- 📤 Sender address
- 📥 Recipient address
- 🔗 Link to block explorer

No polling delays — background job queue handles everything automatically.

---

## 🛠 Installation

### Prerequisites
- Python 3.10+
- pip
- (Optional) Free API keys from the sources below

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/dormani9/crypto-bot-v2.git
cd crypto-bot-v2

# 2. Create virtual environment (recommended)
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
copy .env.example .env   # Windows
cp .env.example .env     # Linux/Mac

# 5. Edit .env — add your bot token and API keys

# 6. Run
python main.py
```

---

## 🔐 Environment Variables

| Variable | Required | Description | Get it from |
|----------|----------|-------------|-------------|
| `TELEGRAM_BOT_TOKEN` | ✅ Yes | Telegram bot token | [BotFather](https://t.me/BotFather) |
| `COVALENT_API_KEY` | ✅ For wallet monitoring | Covalent unified API key | [Covalent](https://www.covalenthq.com/) |
| `COINGECKO_API_KEY` | ❌ Optional | Higher rate limit for prices | [CoinGecko](https://www.coingecko.com/en/api) |
| `FREEMODEL_API_KEY` | ❌ Optional | AI assistant (free) | [freemodel.dev](https://freemodel.dev) |
| `ETHERSCAN_API_KEY` | ❌ Optional | Gas & whale tracking | [Etherscan](https://etherscan.io/myapikey) |
| `BLOCKSCOUT_API_KEY` | ❌ Optional | Blockscout Pro (Robinhood Chain) | [Blockscout](https://blockscout.com) |

> Without `COVALENT_API_KEY`, wallet monitoring won't work. Without `FREEMODEL_API_KEY`, the AI assistant won't work. Other features work without API keys.

---

## 📁 Project Structure

```
crypto-bot-v2/
├── main.py                  # Entry point — handler registration & bot startup
├── utils.py                 # Helpers: CoinGecko prices, Toman rates, COIN_ALIASES
├── lang.py                  # Bilingual FA/EN dictionary + user language management
├── requirements.txt         # Project dependencies
├── .env.example             # Sample environment file
├── wallet-monitor.json      # Watched wallets (auto-created)
├── last-block.json          # Last-checked blocks (auto-created)
├── README.md                # This file
│
└── handlers/                # Handler modules
    ├── start.py             # /start (language selection) + /help + /lang + main menu
    ├── price.py             # /price + /alert
    ├── news.py              # /news — cached CoinDesk + CoinTelegraph, AI-translated for FA
    ├── fng.py               # /fng — Fear & Greed Index
    ├── whale.py             # /whale — whale transactions
    ├── gas.py               # /gas — Ethereum gas fees
    ├── toman.py             # /toman — USD/Toman rate
    ├── watch.py             # /watch, /unwatch, /wallets, /check — wallet monitoring (23 chains)
    ├── ai.py                # /ask — AI assistant via freemodel.dev
    ├── menu.py              # Interactive inline menu with callbacks
```

### Flow

```
User → /start → Language select → Main menu
    ├── 🔹 Prices (menu_price) ← CoinGecko
    ├── 🔹 Fear & Greed (menu_fng) ← alternative.me
    ├── 🔹 USD/Toman (menu_toman) ← Wallex
    ├── 🔹 News (menu_news) ← RSS feeds + AI translation
    ├── 🔹 Whale (menu_whale) ← Etherscan
    ├── 🔹 Gas (menu_gas) ← Etherscan
    ├── 🔹 Wallet (menu_wallet) ← Covalent API (23 chains)
    └── 🔹 AI (menu_ai) ← freemodel.dev
```

---

## 🌐 APIs Used

| Service | Usage | Docs | License |
|---------|-------|------|---------|
| **Covalent** | Wallet monitoring across 23 EVM chains | [docs](https://www.covalenthq.com/docs/api/) | Free tier (75k req/mo) |
| **CoinGecko** | Live prices for 28+ coins with 24h change | [docs](https://docs.coingecko.com) | Free with API key |
| **Etherscan v2** | Gas fees & whale transactions | [docs](https://docs.etherscan.io) | Free tier |
| **alternative.me** | Fear & Greed market index | [docs](https://alternative.me/crypto/fear-and-greed-index) | Free |
| **freemodel.dev** | AI assistant (gpt-5.4-mini) | [freemodel.dev](https://freemodel.dev) | Free |
| **Wallex** | USDT/Toman rate | [wallex.ir](https://wallex.ir) | Free |
| **CoinDesk / CoinTelegraph** | English news (RSS) | — | RSS free |

---

## 🚀 Railway Deployment

This bot runs on Railway. Steps:

1. Push the repository to GitHub
2. Create a new project on [Railway](https://railway.app) and connect your GitHub repo
3. In Railway settings, add environment variables:
   - `TELEGRAM_BOT_TOKEN`
   - `COVALENT_API_KEY`
   - `COINGECKO_API_KEY` (optional)
   - `FREEMODEL_API_KEY` (optional)
   - `ETHERSCAN_API_KEY` (optional)
   - `BLOCKSCOUT_API_KEY` (optional)
4. Railway automatically runs `pip install -r requirements.txt` and `python main.py`
5. Every push to GitHub triggers an automatic redeploy

> Note: Iranian exchanges (Nobitex, Bit24) are DNS-blocked on Railway. Wallex is the only working source for Toman rates.

---

## 🤝 Contributing

PRs and Issues are welcome. Before submitting a PR:
- Test your changes
- Ensure code quality
- Write clear commit messages

---

## 📝 License

This project is licensed under the MIT License.

---

## 🙏 Special Thanks

<p align="center">
  <a href="https://github.com/Misagh95/">
    <img src="assets/thanks-misagh.jpg" alt="Thanks to Misagh" width="300"/>
  </a>
</p>

Special thanks to **Misagh** for his invaluable collaboration and support throughout this project.

---

<p align="center">
  Made with ❤️ for the crypto community
</p>
