# 🤖 Crypto V2 Bot — راهنمای کامل ربات تلگرام ارز دیجیتال

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" />
  <img src="https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram" />
  <img src="https://img.shields.io/badge/API-CoinGecko-green?logo=bitcoin" />
  <img src="https://img.shields.io/badge/deploy-Railway-purple?logo=railway" />
</p>

یک ربات تلگرام جامع و دوزبانه (فارسی/انگلیسی) برای دنیای کریپتو. قیمت لحظه‌ای، شاخص ترس و طمع، اخبار، تراکنش‌های نهنگ‌ها، کارمزد گاز اتریوم، پورتفوی شخصی، قیمت تومان، و دستیار هوش مصنوعی — همه در یک ربات.

---

## 📋 فهرست

- [امکانات](#-امکانات)
- [راهنمای دستورات](#-راهنمای-دستورات)
- [نصب و اجرا](#-نصب-و-اجرا)
- [متغیرهای محیطی](#-متغیرهای-محیطی)
- [ساختار پروژه](#-ساختار-پروژه)
- [API‌های استفاده شده](#-apiهای-استفاده-شده)
- [استقرار روی Railway](#-استقرار-روی-railway)
- [مجوز](#-مجوز)

---

## ✨ امکانات

### 🔸 قیمت لحظه‌ای ارزها
نمایش قیمت ۲۸+ ارز برتر با تغییرات ۲۴ ساعته (🟢 مثبت / 🔴 منفی). از alias پشتیبانی می‌کند: `btc` → `bitcoin`، `eth` → `ethereum`، `sol` → `solana`، `ofc` → `onefootball-club` و بیش از ۵۰ توکن دیگر.

### 🔸 شاخص ترس و طمع (Fear & Greed)
شاخص احساسات بازار در ۷ روز اخیر با ایموجی: 😱 ترس شدید → 🤑 طمع شدید.

### 🔸 اخبار کریپتو
- `/news` — آخرین اخبار از CoinDesk + CoinTelegraph (انگلیسی)
- `/fnews` — آخرین اخبار از ارزدیجیتال (فارسی)

### 🔸 تراکنش‌های نهنگ
ردیابی تراکنش‌های بالای ۱ میلیون دلار در شبکه اتریوم با استفاده از Etherscan API.

### 🔸 کارمزد گاز اتریوم
نمایش `Safe`، `Normal` و `Fast` گس به همراه قیمت لحظه‌ای ETH.

### 🔸 پورتفوی شخصی
افزودن، حذف و مشاهده پورتفوی شخصی. قیمت‌ها به‌روز و مجموع ارزش به دلار محاسبه می‌شود.

### 🔸 قیمت تومان
دریافت قیمت لحظه‌ای USDT و USD به تومان از صرافی‌های ایرانی. والکس منبع اصلی، با فالبک نرخ ارز.

### 🔸 منوی تعاملی
همه قابلیت‌ها از طریق دکمه‌های شیشه‌ای در دسترس است. دکمه refresh برای به‌روزرسانی.

### 🔸 دستیار هوش مصنوعی
- `/ask <سوال>` یا ارسال مستقیم متن (free-form)
- پاسخ‌های دقیق و تخصصی در مورد بلاکچین، دیفای، تحلیل بازار و...
- فارسی/انگلیسی — بر اساس زبان انتخاب شده
- قدرت گرفته از `gpt-5.4-mini` از طریق freemodel.dev

### 🔸 دوزبانه
پشتیبانی کامل از فارسی و انگلیسی. انتخاب زبان در اولین `/start` با امکان تغییر با `/lang`.

---

## 📖 راهنمای دستورات

| دستور | توضیح | مثال |
|-------|-------|------|
| `/start` | شروع ربات و انتخاب زبان | `/start` |
| `/price [coin...]` | قیمت لحظه‌ای یک یا چند ارز | `/price btc eth sol ofc` |
| `/alert <coin> <above/below> <price>` | هشدار قیمت | `/alert btc above 100000` |
| `/fng [days]` | شاخص ترس و طمع | `/fng` |
| `/news [count]` | اخبار انگلیسی | `/news 3` |
| `/fnews [count]` | اخبار فارسی | `/fnews 3` |
| `/whale` | تراکنش‌های نهنگ | `/whale` |
| `/gas` | کارمزد گاز اتریوم | `/gas` |
| `/portfolio` | مشاهده پورتفوی | `/portfolio` |
| `/add <coin> <amount>` | افزودن به پورتفوی | `/add bitcoin 0.5` |
| `/remove <coin>` | حذف از پورتفوی | `/remove bitcoin` |
| `/toman` | قیمت USDT و USD به تومان | `/toman` |
| `/ask <question>` | سوال از هوش مصنوعی | `/ask what is DeFi?` |
| حالا هر متنی بفرستی (غیر از دستور) هم جواب می‌گیری | — | `اتریوم چیه؟` |
| `/help` | راهنما | `/help` |
| `/lang` | تغییر زبان | `/lang` |

### کوین‌های پشتیبانی شده در /price (پیش‌فرض ۲۸ عدد)
```
bitcoin, ethereum, solana, ripple, cardano,
dogecoin, polkadot, chainlink, avalanche-2, matic-network,
tron, litecoin, shiba-inu, the-open-network,
binancecoin, aptos, arbitrum, optimism,
vechain, near, injective, sei-network,
starknet, worldcoin-wld, pepe, bonk,
onefootball-club, dogwifhat
```

### Aliasهای موجود (بیش از ۵۰ عدد)
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

---

## 🛠 نصب و اجرا

### پیش‌نیازها
- Python 3.10+
- pip
- (اختیاری) API Keyهای رایگان از منابع زیر

### مراحل نصب

```bash
# 1. کلون کردن مخزن
git clone https://github.com/dormani9/crypto-bot-v2.git
cd crypto-bot-v2

# 2. ایجاد محیط مجازی (توصیه می‌شود)
python -m venv venv
# ویندوز:
venv\Scripts\activate
# لینوکس/مک:
source venv/bin/activate

# 3. نصب وابستگی‌ها
pip install -r requirements.txt

# 4. ایجاد فایل .env
copy .env.example .env   # ویندوز
cp .env.example .env     # لینوکس/مک

# 5. ویرایش .env — توکن ربات و API Keyها را وارد کنید

# 6. اجرا
python main.py
```

---

## 🔐 متغیرهای محیطی

| متغیر | الزامی | توضیح | دریافت از |
|-------|--------|-------|-----------|
| `TELEGRAM_BOT_TOKEN` | ✅ بله | توکن ربات تلگرام | [BotFather](https://t.me/BotFather) |
| `COINGECKO_API_KEY` | ❌ اختیاری | کلید API کوین‌گکو (نرخ بیشتر) | [CoinGecko](https://www.coingecko.com/en/api) |
| `FREEMODEL_API_KEY` | ❌ اختیاری | کلید هوش مصنوعی (رایگان) | [freemodel.dev](https://freemodel.dev) |
| `ETHERSCAN_API_KEY` | ❌ اختیاری | کلید API اتراسکن (گاز و نهنگ) | [Etherscan](https://etherscan.io/myapikey) |

> بدون `FREEMODEL_API_KEY`، دستیار AI کار نمی‌کند. بقیه ویژگی‌ها بدون API Key هم کار می‌کنند.

---

## 📁 ساختار پروژه

```
crypto-bot-v2/
├── main.py                  # نقطه ورود — ثبت handlerها و اجرای ربات
├── utils.py                 # توابع کمکی: قیمت‌گیری از CoinGecko، قیمت تومان، COIN_ALIASES
├── lang.py                  # دیکشنری دوزبانه فارسی/انگلیسی + مدیریت زبان کاربران
├── requirements.txt         # وابستگی‌های پروژه
├── .env.example             # نمونه فایل محیطی
├── portfolio.json           # ذخیره پورتفوی کاربران (ساخته می‌شود)
├── README.md                # همین فایل
│
└── handlers/                # ماژول‌های handler
    ├── start.py             # /start (انتخاب زبان) + /help + /lang + منوی اصلی
    ├── price.py             # /price + /alert
    ├── news.py              # /news (انگلیسی) + /fnews (فارسی)
    ├── fng.py               # /fng — شاخص ترس و طمع
    ├── whale.py             # /whale — تراکنش‌های نهنگ
    ├── gas.py               # /gas — کارمزد گاز
    ├── toman.py             # /toman — قیمت تومان
    ├── portfolio.py         # /portfolio + /add + /remove
    ├── ai.py                # /ask — دستیار هوش مصنوعی
    └── menu.py              # منوی تعاملی (callback handler)
```

### جریان کار (Flow)

```
کاربر → /start → انتخاب زبان → منوی اصلی
    ├── 🔹 قیمت (menu_price) ← CoinGecko
    ├── 🔹 ترس و طمع (menu_fng) ← alternative.me
    ├── 🔹 تومان (menu_toman) ← Wallex
    ├── 🔹 اخبار (menu_news) ← RSS feeds
    ├── 🔹 نهنگ (menu_whale) ← Etherscan
    ├── 🔹 گاز (menu_gas) ← Etherscan
    ├── 🔹 پورتفوی (menu_portfolio) ← portfolio.json
    └── 🔹 هوش مصنوعی (menu_ai) ← freemodel.dev
```

---

## 🌐 API‌های استفاده شده

| سرویس | کاربرد | مستندات | لایسنس |
|-------|--------|---------|--------|
| **CoinGecko** | قیمت لحظه‌ای ۲۸+ ارز با تغییرات ۲۴ ساعته | [docs](https://docs.coingecko.com) | رایگان با API Key |
| **Etherscan v2** | گس و تراکنش‌های نهنگ اتریوم | [docs](https://docs.etherscan.io) | رایگان |
| **alternative.me** | شاخص ترس و طمع بازار | [docs](https://alternative.me/crypto/fear-and-greed-index) | رایگان |
| **freemodel.dev** | دستیار AI (مدل gpt-5.4-mini) | [freemodel.dev](https://freemodel.dev) | رایگان |
| **Wallex** | قیمت USDT/Toman | [wallex.ir](https://wallex.ir) | رایگان |
| **ارزدیجیتال** | اخبار فارسی (RSS) | [arzdigital.com](https://arzdigital.com) | RSS رایگان |
| **CoinDesk / CoinTelegraph** | اخبار انگلیسی (RSS) | — | RSS رایگان |

---

## 🚀 استقرار روی Railway

این ربات روی Railway اجرا می‌شود. مراحل:

1. مخزن را به GitHub پوش کنید
2. در [Railway](https://railway.app) یک پروژه جدید بسازید و به مخزن GitHub متصل کنید
3. در تنظیمات Railway، متغیرهای محیطی را اضافه کنید:
   - `TELEGRAM_BOT_TOKEN`
   - `COINGECKO_API_KEY` (اختیاری)
   - `FREEMODEL_API_KEY` (اختیاری)
   - `ETHERSCAN_API_KEY` (اختیاری)
4. Railway خودکار `pip install -r requirements.txt` و `python main.py` را اجرا می‌کند
5. پس از هر پوش به GitHub، Railway خودکار دیپلوی می‌کند

> نکته: صرافی‌های ایرانی (نوبیتکس، بیت‌۲۴) روی Railway DNS مسدود هستند. والکس تنها منبع کارای قیمت تومان است.

---

## 🤝 مشارکت

PR و Issue با استقبال مواجه می‌شود. قبل از ارسال PR:
- کد را تست کنید
- از lint بودن اطمینان حاصل کنید
- Commit messageهای واضح بنویسید

---

## 📝 مجوز

این پروژه تحت مجوز MIT منتشر شده است.

---

<p align="center">
  ساخته شده با ❤️ برای جامعه کریپتو ایران
</p>
