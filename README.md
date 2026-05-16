# Option Pricing & Volatility Analysis

Implementation of European option pricing using the Cox-Ross-Rubinstein (CRR) 
Binomial and Black-Scholes models, with implied volatility calculation, volatility 
smile analysis, convergence testing, and put-call parity validation in Python.

---

## Overview

This project prices European options on TCS (Tata Consultancy Services) using two 
industry-standard models — the CRR Binomial model and the Black-Scholes model — 
and compares their outputs against real NSE market prices. It estimates historical 
and implied volatility from real market data, visualises the volatility smile across 
strike prices, and validates theoretical pricing relationships such as put-call parity.

The project uses live data from Yahoo Finance and NSE options chain exports, 
bridging theoretical finance with real market conditions.

---

## Features

- Cox-Ross-Rubinstein (CRR) Binomial Option Pricing
- Black-Scholes Option Pricing
- Convergence of Binomial Model to Black-Scholes
- Put-Call Parity Validation
- Historical Volatility Estimation
- Rolling Volatility Analysis
- Implied Volatility Calculation using Numerical Methods
- Volatility Smile / Skew Visualization
- NSE Options Chain Data Cleaning & Processing

---

## Models Implemented

### 1. Binomial Model (CRR)
- Discrete-time option pricing framework
- Risk-neutral valuation
- Backward induction pricing
- Convergence tested across increasing step sizes

### 2. Black-Scholes Model
- Closed-form European option pricing
- Continuous-time GBM assumptions
- Used as benchmark for binomial convergence comparison

---

## Data Sources

- Yahoo Finance (`yfinance`) — historical price data for volatility estimation
- NSE Option Chain CSV exports — real market option prices for implied volatility 
  and smile analysis

---

## Technologies Used

- Python
- NumPy
- Pandas
- Matplotlib
- SciPy
- yfinance

---

## Market Parameters (Latest Run)

| Parameter | Value |
|---|---|
| TCS Stock Price (S) | ₹2264.00 |
| ATM Strike | ₹2260.00 |
| Time to Expiry | 12 days |
| ATM Implied Volatility (NSE) | 16.23% |
| 1-Year Historical Volatility | 21.88% |
| 30-Day Rolling Volatility | 29.38% |
| 90-Day Rolling Volatility | 28.36% |

---

## Key Findings

- Binomial model converged to Black-Scholes pricing at approximately 200 steps,
  confirming theoretical consistency
- ATM Implied Volatility (16.23%) is below Historical Volatility (21.88%),
  suggesting markets are pricing in lower near-term uncertainty relative to 
  recent realised volatility
- Model prices using historical volatility (Call: ₹38.25) overshoot the market 
  LTP (₹32.90), while ATM IV-based pricing (Call: ₹29.07) undershoots — 
  actual market price falls between the two estimates
- Put-Call Parity validated exactly (difference = 0.0000) across all model 
  specifications
- Volatility smile observed across strike prices, consistent with market skew 
  and deviation from Black-Scholes constant-volatility assumption

---

## Example Output

```text
S from NSE stock data     = ₹2264.00
ATM Strike                = ₹2260.00
Time to Expiry            = 12 days
ATM IV (NSE)              = 0.1623
1-Year Historical Vol     = 0.2188

--- Call Price Comparison ---
Binomial (hist vol)       = ₹38.25
Binomial (ATM IV)         = ₹29.07
B-S (hist vol)            = ₹38.43
B-S (ATM IV)              = ₹29.20
Market LTP (ATM)          = ₹32.90

Convergence (n → call price, hist vol):
  n=3   → ₹41.47
  n=50  → ₹38.25
  n=200 → ₹38.38
  n=500 → ₹38.41
  B-S   → ₹38.43

Put-Call Parity: PASSED (difference = 0.0000)
```

---

## Repository Contents

- `OptionPricing.py` → Main script with all models and analysis
- `data/` → NSE options chain CSV exports
- `charts/` → Volatility smile, convergence, and rolling volatility plots
- `output/` → Key numerical results and model comparison outputs
