import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
from datetime import date

# =========================================================
# 1. DATA + HISTORICAL RETURNS + VOLATILITY
# =========================================================

data = yf.download(
    "TCS.NS",
    period="1y",
    auto_adjust=False
)["Close"].squeeze()

if data.isna().all():
    raise ValueError("No valid price data downloaded")

returns = np.log(data / data.shift(1)).dropna()

mean_return = returns.mean() * 252   # descriptive only — not used in pricing
sigma = returns.std() * np.sqrt(252) # annualised historical volatility

print("\nMean return (descriptive) =", round(mean_return, 4))
print("Historical Volatility     =", round(sigma, 4))


# =========================================================
# 2. MODEL PARAMETERS
# =========================================================

stock_df = pd.read_csv('tcs_stock_data.csv')

stock_df['CLOSE'] = pd.to_numeric(
    stock_df['CLOSE'].astype(str).str.replace(',', ''),
    errors='coerce'
)

stock_df['DATE'] = pd.to_datetime(stock_df['DATE'], format='%d-%b-%Y')
stock_df = stock_df.sort_values('DATE', ascending=False)

S = float(stock_df['CLOSE'].iloc[0])
K = S
r = 0.0692
n = 50

# FIX 1: use date.today() and date() to avoid datetime flooring issue
today      = date.today()
expiry     = date(2026, 5, 28)          # replaces strptime — no flooring risk
days_to_expiry = (expiry - today).days
T = days_to_expiry / 365

print('\nS from NSE stock data =', round(S, 2))
print('Date                  =', stock_df['DATE'].iloc[0].date())
print("Time to Expiry        =", days_to_expiry, "days")


# =========================================================
# 3. BINOMIAL MODEL
# =========================================================

def binomial_price(sigma, n, option_type='call'):

    delta_t = T / n
    u = np.exp(sigma * np.sqrt(delta_t))
    d = 1 / u
    p = (np.exp(r * delta_t) - d) / (u - d)

    if not (0 < p < 1):
        raise ValueError("Arbitrage condition violated")

    stock_tree = []
    for i in range(n + 1):
        row = []
        for j in range(i + 1):
            row.append(S * (u ** j) * (d ** (i - j)))
        stock_tree.append(row)

    option_tree = []
    for i in range(n + 1):
        option_tree.append([0] * (i + 1))

    for j in range(n + 1):
        ST = stock_tree[n][j]
        if option_type == 'call':
            option_tree[n][j] = max(ST - K, 0)
        else:
            option_tree[n][j] = max(K - ST, 0)

    for i in range(n - 1, -1, -1):
        for j in range(i + 1):
            option_tree[i][j] = np.exp(-r * delta_t) * (
                p * option_tree[i + 1][j + 1] +
                (1 - p) * option_tree[i + 1][j]
            )

    return float(option_tree[0][0])


# =========================================================
# 4. BLACK-SCHOLES MODEL
# =========================================================

def black_scholes(S, K, r, sigma, T, option_type='call'):

    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    call = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    put  = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    return call if option_type == 'call' else put


# =========================================================
# 5. LOAD OPTION CHAIN + EXTRACT ATM IV
# =========================================================

df = pd.read_csv('option_chain_data.csv', skiprows=1)

chain = df[['STRIKE', 'LTP', 'IV', 'LTP.1', 'IV.1']].copy()
chain.columns = ['strike', 'call_ltp', 'call_iv', 'put_ltp', 'put_iv']

for col in chain.columns:
    chain[col] = pd.to_numeric(
        chain[col].astype(str)
                  .str.replace(',', '')
                  .str.replace('%', '')
                  .str.strip()
                  .str.replace(r'^-+$', '', regex=True),
        errors='coerce'
    )

chain = chain.dropna(subset=['strike']).sort_values('strike')
chain['call_iv'] = chain['call_iv'] / 100
chain['put_iv']  = chain['put_iv']  / 100

# Find ATM IV from nearest strike with valid call IV
valid_iv = chain.dropna(subset=['call_iv'])
valid_iv = valid_iv[valid_iv['call_iv'] > 0.10]
atm_iv_row = valid_iv.loc[(valid_iv['strike'] - S).abs().idxmin()]
call_iv = float(atm_iv_row['call_iv'])

print('\nATM Strike (IV)   =', round(atm_iv_row['strike'], 2))
print('ATM IV (NSE)      =', round(call_iv, 4))


# =========================================================
# 6. MODEL PRICES — HISTORICAL VOL AND IV COMPARISON
# =========================================================

# FIX 2: price with both historical vol and ATM IV, compare to market
call_hist  = binomial_price(sigma,   n, 'call')
put_hist   = binomial_price(sigma,   n, 'put')
call_iv_p  = binomial_price(call_iv, n, 'call')
put_iv_p   = binomial_price(call_iv, n, 'put')

bs_call_hist = black_scholes(S, K, r, sigma,   T, 'call')
bs_call_iv   = black_scholes(S, K, r, call_iv, T, 'call')

# Market LTP for nearest ATM strike
atm_ltp_row = chain.dropna(subset=['call_ltp'])
atm_ltp_row = atm_ltp_row.loc[(atm_ltp_row['strike'] - S).abs().idxmin()]
market_ltp  = float(atm_ltp_row['call_ltp'])

print('\n--- Call Price Comparison ---')
print('Binomial (hist vol)  =', round(call_hist, 2))
print('Binomial (ATM IV)    =', round(call_iv_p, 2))
print('B-S (hist vol)       =', round(bs_call_hist, 2))
print('B-S (ATM IV)         =', round(bs_call_iv, 2))
print('Market LTP (ATM)     =', round(market_ltp, 2))

print('\n--- Put Price Comparison ---')
print('Binomial (hist vol)  =', round(put_hist, 2))
print('Binomial (ATM IV)    =', round(put_iv_p, 2))


# =========================================================
# 7. CONVERGENCE TABLE + PLOT
# =========================================================

print("\nConvergence (n → call price, hist vol):")
steps_list = [3, 5, 10, 25, 50, 100, 200, 500]
prices = []

for steps in steps_list:
    price = binomial_price(sigma, steps, 'call')
    prices.append(price)
    print("  n =", steps, "→ ₹", round(price, 2))

print("  B-S → ₹", round(bs_call_hist, 2))

plt.figure(figsize=(8, 5))
plt.plot(steps_list, prices, marker='o', label='Binomial Price')
plt.axhline(y=bs_call_hist, linestyle='--', label='Black-Scholes Price')
plt.xscale('log')
plt.xlabel('Number of Binomial Steps (log scale)')
plt.ylabel('Call Option Price (₹)')
plt.title('Binomial Convergence to Black-Scholes')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("convergence_plot.png")
plt.show()


# =========================================================
# 8. PUT-CALL PARITY CHECK
# =========================================================

for label, c, p in [
    ("Binomial (hist vol)", call_hist, put_hist),
    ("Binomial (ATM IV)",   call_iv_p, put_iv_p),
    ("B-S (hist vol)",      bs_call_hist, black_scholes(S, K, r, sigma, T, 'put'))
]:
    lhs  = c - p
    rhs  = S - K * np.exp(-r * T)
    diff = lhs - rhs
    print("\nParity -", label)
    print("  C - P        =", round(lhs, 2))
    print("  S - Ke^(-rT) =", round(rhs, 2))
    print("  Difference   =", round(diff, 4))


# =========================================================
# 9. ROLLING VOLATILITY + PLOT
# =========================================================

rolling_vol_30 = returns.rolling(30).std().dropna().iloc[-1] * np.sqrt(252)
rolling_vol_90 = returns.rolling(90).std().dropna().iloc[-1] * np.sqrt(252)

print("\nVolatility Summary:")
print("  30-day rolling vol =", round(rolling_vol_30, 4))
print("  90-day rolling vol =", round(rolling_vol_90, 4))
print("  1-year hist vol    =", round(sigma, 4))
print("  ATM IV (NSE)       =", round(call_iv, 4))

rolling_30_series = returns.rolling(30).std() * np.sqrt(252)
rolling_90_series = returns.rolling(90).std() * np.sqrt(252)

plt.figure(figsize=(10, 5))
plt.plot(rolling_30_series.index, rolling_30_series, label='30-Day Rolling Vol')
plt.plot(rolling_90_series.index, rolling_90_series, label='90-Day Rolling Vol')
plt.axhline(y=sigma,   linestyle='--', label='1-Year Historical Vol')
plt.axhline(y=call_iv, linestyle=':',  label='ATM IV (NSE)')
plt.xlabel('Date')
plt.ylabel('Annualised Volatility')
plt.title('Rolling Volatility of TCS Returns')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("rolling_volatility.png")
plt.show()


# =========================================================
# 10. VOL SMILE PLOT
# =========================================================

# FIX 3: filter by IV bounds instead of LTP > 1
chain_plot = chain[
    chain['call_iv'].between(0.05, 1.0) |
    chain['put_iv'].between(0.05, 1.0)
].copy()

plt.figure(figsize=(11, 5))

call_data = chain_plot.dropna(subset=['call_iv'])
if not call_data.empty:
    plt.plot(call_data['strike'], call_data['call_iv'] * 100,
             marker='o', label='Call IV')

put_data = chain_plot.dropna(subset=['put_iv'])
if not put_data.empty:
    plt.plot(put_data['strike'], put_data['put_iv'] * 100,
             marker='o', label='Put IV')

plt.axvline(x=S, linestyle='--', label='ATM (₹' + str(round(S, 0)) + ')')
plt.xlabel('Strike Price (₹)')
plt.ylabel('Implied Volatility (%)')
plt.title('TCS Implied Volatility Curve — May 2026 Expiry')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("volatility_smile.png")
plt.show()
