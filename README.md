## Option Pricing & Volatility Analysis

Implementation of European option pricing using the Cox-Ross-Rubinstein (CRR) Binomial and Black-Scholes models, with implied volatility calculation, volatility smile analysis, convergence testing, and put-call parity validation in Python.


## Overview

This project prices European options on TCS (Tata Consultancy Services) using two industry-standard models — the CRR Binomial model and the Black-Scholes model — and compares their outputs. It further estimates historical and implied volatility from real market data, visualises the volatility smile across strike prices, and validates theoretical pricing relationships such as put-call parity.

The project uses live data from Yahoo Finance and NSE options chain exports, bridging theoretical finance with real market conditions.


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


## Data Sources

- Yahoo Finance (`yfinance`) — historical price data for volatility estimation
- NSE Option Chain CSV exports — real market option prices for implied volatility and smile analysis


## Technologies Used

- Python
- NumPy
- Pandas
- Matplotlib
- SciPy
- yfinance


## Key Findings

- Binomial model converged to Black-Scholes pricing at approximately 200 steps, confirming theoretical consistency
- Implied Volatility (24.1%) exceeded Historical Volatility (21.9%), suggesting markets priced in greater near-term uncertainty than recent price history implied
- Volatility smile observed across strike prices, consistent with market skew and deviation from Black-Scholes constant-volatility assumption
- Put-Call Parity validated within acceptable bounds across sampled contracts


## Example Output

```text
Binomial Call Price  = 63.20
Black-Scholes Call   = 63.49
Implied Volatility   = 0.2410
Historical Volatility= 0.2190
Put-Call Parity Check: PASSED (difference = 0.0023)
```

## Repository Contents

- `OptionPricing.py` → Main script with all models and analysis
- `data/` → NSE options chain CSV exports
- `charts/` → Volatility smile, convergence, and rolling volatility plots
