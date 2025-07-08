# trading api app

# you are an expert python programmer with expert trading experience, code the following requirements:
# -trade top 10 item on market with a starting total budget of $1000
# -$100 for each top 10 item
# -buy when each top 10 item is -3% below close price?
# -trailing-stop-lose when item is +5% above last corresponding buy
# -trade until balance for each item is < $5 & >= $2
# -repeat for top 10
# -backtest previous 3, 5, 10 years before production with visuals


# Here’s a comprehensive Python script implementing your strategy on Binance US data with a 15‑minute timeframe, selecting the top 10 assets by market cap. It runs a backtest over the past 3, 5, and 10 years, plotting results using `matplotlib` and `pandas`. This uses the `ccxt` library for data retrieval and a simple backtest engine.

# ---

# ```python
# import ccxt
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from datetime import datetime, timedelta
# import time

# # 🛠 Setup Exchange
# exchange = ccxt.binanceus({'enableRateLimit': True})

# # Parameters
# INITIAL_BUDGET = 1000
# ASSET_BUDGET = 100
# BUY_THRESHOLD = -0.03    # -3%
# STOP_TRAIL = 0.05        # +5% trailing stop
# MIN_BALANCE = 2
# MIN_TRADE_BALANCE = 5
# TIMEFRAME = '15m'
# BACKTEST_YEARS = [3, 5, 10]

# def get_top_10():
#     tickers = exchange.fetch_tickers()
#     # filter USDT or USD pairs only
#     pairs = [t for t in tickers if t.endswith('/USD') or t.endswith('/USDT')]
#     # fetch market caps approximated by quoteVolume * close
#     data = []
#     for p in pairs:
#         d = tickers[p]
#         market_cap = d['quoteVolume'] * d['close'] if 'quoteVolume' in d and 'close' in d else 0
#         if market_cap == 0:
#             continue
#         data.append((p, market_cap))
#     top = sorted(data, key=lambda x: x[1], reverse=True)[:10]
#     return [t[0] for t in top]

# def fetch_ohlcv(symbol, since):
#     all_ohlc = []
#     since_ms = int(since.timestamp() * 1000)
#     while True:
#         ohlc = exchange.fetch_ohlcv(symbol, timeframe=TIMEFRAME, since=since_ms, limit=1000)
#         if not ohlc:
#             break
#         all_ohlc += ohlc
#         since_ms = ohlc[-1][0] + 1
#         time.sleep(exchange.rateLimit / 1000)
#         if len(ohlc) < 1000:
#             break
#     df = pd.DataFrame(all_ohlc, columns=['ts','open','high','low','close','vol'])
#     df['dt'] = pd.to_datetime(df['ts'], unit='ms')
#     df.set_index('dt', inplace=True)
#     return df

# def backtest(symbol, df):
#     cash = ASSET_BUDGET
#     pos = 0.0
#     buy_price = None
#     trial_max = -np.inf
#     history = []
#     for i in range(1, len(df)):
#         row = df.iloc[i]
#         prev = df.iloc[i-1]
#         price = row['close']
#         pct_move = (price - prev['close']) / prev['close']

#         # buy condition
#         if pos == 0 and pct_move <= BUY_THRESHOLD and cash >= MIN_TRADE_BALANCE:
#             pos = cash / price
#             buy_price = price
#             trial_max = price
#             cash = 0
#             history.append((row.name, 'BUY', price, pos))
        
#         # in position: update trailing max
#         if pos > 0:
#             trial_max = max(trial_max, price)
#             if price <= trial_max * (1 - STOP_TRAIL):
#                 cash = pos * price
#                 history.append((row.name, 'SELL', price, pos))
#                 pos = 0
#                 buy_price = None

#         # if cash left < thresholds, stop trading
#         if 0 < cash < MIN_BALANCE:
#             cash = 0
#             break

#     # close any open at end
#     if pos > 0:
#         cash = pos * df['close'].iloc[-1]
#         history.append((df.index[-1], 'SELL', df['close'].iloc[-1], pos))
#         pos = 0

#     return cash, history

# def run_backtests():
#     top10 = get_top_10()
#     results = {}
#     for years in BACKTEST_YEARS:
#         print(f"\n📊 Running {years}-year backtest...")
#         since = datetime.utcnow() - timedelta(days=365 * years)
#         agg_hist = {}
#         tot_value = 0
#         for sym in top10:
#             print(f"  {sym}...")
#             df = fetch_ohlcv(sym, since)
#             cash, hist = backtest(sym, df)
#             agg_hist[sym] = hist
#             tot_value += cash
#         results[years] = (tot_value, agg_hist)
#     return results

# def plot_results(results):
#     years = []
#     values = []
#     for y, (val, _) in results.items():
#         years.append(y)
#         values.append(val)
#     plt.figure(figsize=(8,5))
#     plt.bar([str(y) for y in years], values, color='skyblue')
#     plt.xlabel('Backtest Length (years)')
#     plt.ylabel('Final Portfolio Value ($)')
#     plt.title('Strategy Performance Over Different Time Windows')
#     plt.show()

# if __name__ == '__main__':
#     res = run_backtests()
#     for y,(val,hist) in res.items():
#         print(f"\n=== {y} years: Final value = ${val:.2f}")
#         for sym, h in hist.items():
#             print(f"{sym}: {len(h)/2:.1f} trades")
#     plot_results(res)
# ```

# ---

# ### 🧠 Key Details

# | Feature              | Implementation                                              |
# | -------------------- | ----------------------------------------------------------- |
# | **Top 10 Selection** | Market cap via 15m quote volume × last price using `ccxt`.  |
# | **Buy Rule**         | Buy when price dips ≥ 3% from previous close.               |
# | **Trailing Stop**    | Tracks max since buy; sell when price drops ≥ 5% from that. |
# | **Budget**           | \$100 per asset, trades until <\$5 cash remains.            |
# | **Data**             | 15-minute OHLCV intervals from Binance US.                  |
# | **Backtests**        | Over 3, 5, and 10 years.                                    |
# | **Visualisation**    | Bar chart of final portfolios by period.                    |

# ---

# ### ✅ Next Steps

# 1. **API Keys**: For live trading or improved rate limits, configure Binance US API credentials via `exchange.apiKey` & `exchange.secret`.
# 2. **Enhancements**: Consider slippage, fees (\~0.1% per trade), or switch to a framework like `backtrader` for more rigorous results.
# 3. **Live Mode**: Integrate scheduling (e.g., cron) to fetch real-time ticks, trigger signals, and execute orders in production.

# Let me know if you'd like me to add fees, incorporate a deeper analytics dashboard, or transform into a `backtrader` strategy class!


import enum
import ccxt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, timezone
import time


# from flask import get

# 🛠 Setup Exchange
exchange = ccxt.binanceus({'enableRateLimit': True})

# Parameters
INITIAL_BUDGET = 1000
ASSET_BUDGET = 100
BUY_THRESHOLD = -0.03    # -3%
STOP_TRAIL = 0.50        # +5% trailing stop
MIN_BALANCE = 2
MIN_TRADE_BALANCE = 5
TIMEFRAME = '15m'
BACKTEST_YEARS = [1,2,3,4]

def get_top_25():
    tickers = exchange.fetch_tickers()  # filter USDT or USD pairs only
    pairs = [t for t in tickers if t.endswith('USD') or t.endswith('USDT')]
    # fetch market caps approximated by quoteVolume * close
    data = []
    for p in pairs:
        d = tickers[p]
        clean_d = {k: v for k, v in d.items() if v is not None}
        if 'quoteVolume' not in clean_d or 'last' not in clean_d:
            continue
        # print(p, d['last'], d['quoteVolume'])
        market_cap = d['quoteVolume'] * d['last']

        data.append((p, market_cap))
    top = sorted(data, key=lambda x: x[1], reverse=True)[:25]
    return [t[0] for t in top]  # filter out any with zero market cap

# ===========================================================================
# ===========================================================================

def fetch_ohlcv(symbol, since):
    all_ohlc = []
    since_ms = int(since.timestamp() * 1000)
    while True:
        try:
            ohlc = exchange.fetch_ohlcv(symbol, timeframe=TIMEFRAME, since=since_ms, limit=1000)
        except Exception as e:
            print(f"Error fetching OHLCV for {symbol}: {e}")
            break
        # ohlc = exchange.fetch_ohlcv(symbol, timeframe=TIMEFRAME, since=since_ms, limit=1000)
        if not ohlc:
            break
        all_ohlc += ohlc
        since_ms = ohlc[-1][0] + 1
        time.sleep(exchange.rateLimit / 1000)
        if len(ohlc) < 1000:
            break
    df = pd.DataFrame(all_ohlc, columns=['ts','open','high','low','close','vol'])
    df['dt'] = pd.to_datetime(df['ts'], unit='ms')
    df.set_index('dt', inplace=True)
    if df.empty:
        print(f"No OHLCV data for {symbol}")
        return pd.DataFrame()
    return df

# ===========================================================================
# ===========================================================================

def backtest(symbol, df):
    cash = ASSET_BUDGET
    pos = 0.0
    buy_price = None
    trial_max = -np.inf
    history = []
    for i in range(1, len(df)):
        row = df.iloc[i]
        prev = df.iloc[i-1]
        price = row['close']
        pct_move = (price - prev['close']) / prev['close']

        # buy condition
        if pos == 0 and pct_move <= BUY_THRESHOLD and cash >= MIN_TRADE_BALANCE:
            pos = cash / price
            buy_price = price
            trial_max = price
            cash = 0
            history.append((row.name, 'BUY', price, pos))
        
        # in position: update trailing max
        if pos > 0:
            trial_max = max(trial_max, price)
            if price <= trial_max * (1 - STOP_TRAIL):
                cash = pos * price
                history.append((row.name, 'SELL', price, pos))
                pos = 0
                buy_price = None

        # if cash left < thresholds, stop trading
        if 0 < cash < MIN_BALANCE:
            cash = 0
            break

    # close any open at end
    if pos > 0:
        cash = pos * df['close'].iloc[-1]
        history.append((df.index[-1], 'SELL', df['close'].iloc[-1], pos))
        pos = 0

    return cash, history

# ===========================================================================
# ===========================================================================

def run_backtests():
    top25 = get_top_25()
    results = {}
    for years in BACKTEST_YEARS:
        print(f"\n📊 Running {years}-year backtest...")
        since = datetime.now(timezone.utc) - timedelta(days=365 * years)
        agg_hist = {}
        tot_value = 0
        for sym in top25:
            print(f"  {sym}...")
            df = fetch_ohlcv(sym, since)
            cash, hist = backtest(sym, df)
            agg_hist[sym] = hist
            tot_value += cash
        results[years] = (tot_value, agg_hist)
        if df.empty:
            print(f"Skipping {sym} due to lack of data.")
            continue
    return results

def plot_results(results):
    years = []
    values = []
    for y, (val, _) in results.items():
        years.append(y)
        values.append(val)
    plt.figure(figsize=(8,5))
    plt.bar([str(y) for y in years], values, color='skyblue')
    plt.xlabel('Backtest Length (years)')
    plt.ylabel('Final Portfolio Value ($)')
    plt.title('Strategy Performance Over Different Time Windows')
    plt.show()

if __name__ == '__main__':
    res = run_backtests()
    for y,(val,hist) in res.items():
        print(f"\n=== {y} years: Final value = ${val:.2f}")
        for sym, h in hist.items():
            print(f"{sym}: {len(h)/2:.1f} trades")
    plot_results(res)

# get_top_10()
