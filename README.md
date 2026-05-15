# Option Pricing & Volatility Analysis

Implementation of European option pricing using Cox-Ross-Rubinstein Binomial and Black-Scholes models with implied volatility, volatility smile analysis, convergence testing, and put-call parity validation in Python.


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

### 1. Binomial Model
- Discrete-time option pricing framework
- Risk-neutral valuation
- Backward induction pricing

### 2. Black-Scholes Model
- Closed-form European option pricing
- Continuous-time GBM assumptions
- Comparison against binomial convergence

---

## Data Sources

- Yahoo Finance (`yfinance`)
- NSE Option Chain CSV exports

---

## Technologies Used

- Python
- NumPy
- Pandas
- Matplotlib
- SciPy
- yfinance

---

## Key Concepts Covered

- Risk-Neutral Pricing
- Geometric Brownian Motion
- Volatility Estimation
- Implied Volatility
- Volatility Smile
- Put-Call Parity
- Numerical Methods in Finance

---

## Example Output

```text
Binomial Call = 63.20
Black-Scholes Call = 63.49

Implied Volatility = 0.2410
