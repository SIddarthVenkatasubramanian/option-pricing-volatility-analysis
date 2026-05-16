# TCS Options Pricing — Black-Scholes, Volatility Smile & Implied Volatility
**Stage 1 | May 2026**

---

## Objective

To implement the Black-Scholes pricing model, compare it against the Binomial model, extract implied volatility from live NSE options data, and empirically demonstrate where Black-Scholes breaks down through the volatility smile.

---

## Model Parameters

| Parameter | Value |
|-----------|-------|
| Underlying | TCS.NS |
| Current Stock Price (S) | ₹2,264.00 |
| Strike Price (K) | ₹2,264.00 (ATM) |
| Risk-Free Rate (r) | 6.92% (Indian 10Y G-sec) |
| Time to Expiry (T) | 12 days (May 28, 2026 expiry) |
| Historical Volatility (σ) | 21.88% |
| ATM Implied Volatility (IV) | 16.23% (NSE published, strike 2260) |

---

## Black-Scholes Implementation

The Black-Scholes formula prices European options in closed form under the following assumptions:

- Stock prices follow Geometric Brownian Motion (log-normal returns)
- Constant volatility across all strikes and maturities
- No dividends during the option's life
- No transaction costs; continuous trading
- Risk-free rate is constant

The formula:

**C = S·N(d₁) − K·e^(−rT)·N(d₂)**

**P = K·e^(−rT)·N(−d₂) − S·N(−d₁)**

Where:

- d₁ = [ln(S/K) + (r + σ²/2)·T] / σ√T
- d₂ = d₁ − σ√T
- N(·) = cumulative standard normal distribution
- N(d₂) = risk-neutral probability of expiring in the money
- N(d₁) = delta — shares held in the replicating portfolio

---

## Binomial Convergence to Black-Scholes

As the number of steps n increases, the discrete binomial random walk converges to GBM via the Central Limit Theorem — and binomial price converges to the Black-Scholes closed-form limit.

| n | Call Price (₹) |
|---|---------------|
| 3 | 41.47 |
| 5 | 40.24 |
| 10 | 37.54 |
| 25 | 38.79 |
| 50 | 38.25 |
| 100 | 38.34 |
| 200 | 38.38 |
| 500 | 38.41 |
| **B-S** | **38.43** |

The price oscillates before stabilising near n=50 — a known odd/even step artefact of the binomial model. By n=500, the binomial price (₹38.41) sits within ₹0.02 of the Black-Scholes price (₹38.43), confirming convergence.

---

## Model Price Comparison

The central question: which volatility input better prices the option?

| Model | Call Price (₹) | Put Price (₹) |
|-------|---------------|--------------|
| Binomial (hist vol 21.88%) | 38.25 | 33.10 |
| Binomial (ATM IV 16.23%) | 29.07 | 23.92 |
| B-S (hist vol 21.88%) | 38.43 | — |
| B-S (ATM IV 16.23%) | 29.20 | — |
| **Market LTP (ATM strike 2260)** | **32.90** | — |

Market price (₹32.90) falls between the two model estimates. Neither historical volatility nor ATM implied volatility alone reproduces the market price exactly. The true market-implied volatility lies between 16.23% and 21.88% — indicating the market is pricing in more uncertainty than IV suggests but less than realised history implies.

---

## Put-Call Parity Check

C − P = S − Ke^(−rT) confirms internal model consistency across all three pricing approaches.

| Model | C − P | S − Ke^(−rT) | Difference |
|-------|-------|--------------|-----------|
| Binomial (hist vol) | 5.14 | 5.14 | 0.0 |
| Binomial (ATM IV) | 5.14 | 5.14 | 0.0 |
| B-S (hist vol) | 5.14 | 5.14 | 0.0 |

All three pass with zero difference — confirming numerical consistency. Note: this verifies internal model coherence, not market no-arbitrage (which would require comparing live call and put market prices).

---

## Volatility Summary

| Measure | Value |
|---------|-------|
| 30-day rolling vol | 29.38% |
| 90-day rolling vol | 28.36% |
| 1-year historical vol | 21.88% |
| ATM Implied Vol (NSE) | 16.23% |

**Interpretation:** ATM IV (16.23%) is significantly below both rolling vol measures (29–28%) and 1-year historical vol (21.88%). With only 12 days to expiry, the option prices only the next 12 days of uncertainty. The elevated rolling vol reflects a turbulent recent period that TCS has already passed through — the market does not expect that same volatility to persist into the final 12 days before expiry. This is consistent with no major catalysts (earnings, macro events) expected before May 28.

---

## Volatility Smile

Black-Scholes assumes a single constant σ for all strikes. If this were true, implied volatility computed from market prices would be flat across all strikes. The NSE options chain shows otherwise:

- **Call IV** rises monotonically from ~13% near ATM to ~24% at deep OTM strikes — the call-side smirk
- **Put IV** remains elevated at ~29–32% across all strikes — structurally higher than call IV at equivalent distances from ATM
- **The gap between put IV and call IV** (approximately 10–13 percentage points at ATM-adjacent strikes) is the volatility skew

**Why the skew exists:**

Institutional investors are structurally long equities and continuously buy OTM puts as crash insurance — permanently bidding up put prices above Black-Scholes fair value. Additionally, when equity prices fall, leverage rises mechanically, making the stock genuinely riskier. Both effects concentrate on the put side with no equivalent structural buyer of OTM calls.

**Implication for Black-Scholes:** A single constant σ cannot simultaneously price calls and puts correctly across all strikes. Using historical vol (21.88%) overprices ATM calls (₹38.43 vs market ₹32.90). Using ATM IV (16.23%) underprices them (₹29.20 vs market ₹32.90). The model is systematically wrong at the wings — underpricing OTM options where fat tails matter most.

---

## Assumptions and Where the Model Fails

| Assumption | Reality |
|------------|---------|
| Constant volatility | Vol varies across strikes (smile) and over time (clustering) |
| Log-normal returns | Real returns have fat tails and negative skew |
| No dividends | TCS pays dividends; model slightly misprices accordingly |
| Continuous trading | Markets close; discrete rebalancing creates hedging error |
| Constant risk-free rate | Rates change, especially for longer-dated options |

---

## What Comes Next

The volatility smile is the primary empirical failure of Black-Scholes. The two natural extensions are:

- **GARCH** — models time-varying volatility (clustering); Stage 2
- **Heston model** — stochastic volatility; directly fits the vol smile that Black-Scholes cannot; Stage 4
