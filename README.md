# 🎲 Stochastic Market Microstructure Engine

A production-grade, high-frequency quantitative analytics engine built entirely from scratch in pure vectorized Python. This system simulates, models, and visualizes asset price dynamics under latent market regimes and high-frequency order flow mechanics, implementing foundational principles of stochastic processes.

---
---

## ✍️ Scanned Mathematical Derivations & First-Principles Notes
To demonstrate the mathematical baseline validating this software architecture, I have open-sourced my exact handwritten lecture notes and matrix calculus proofs mapping out the underlying stochastic processes.

(./mathematical-notes/stochastic-microstructure-derivations.pdf)

---

## 🧠 Core Quantitative Architecture & Mathematical Mapping

This architecture translates pure stochastic process theory directly into algorithmic execution, mapping the theoretical framework to active production components:

### 1. Multi-Regime Markovian Dynamics (Lectures 1–5)
Asset volatility and drift are rarely constant. This engine implements a **Discrete-Time Markov Chain (DTMC)** traversing a $3 \times 3$ state-space mapping hidden market regimes:
* **State 0 (Low Volatility / Trend Persistence):** Characteristic of institutional accumulation blocks.
* **State 1 (Medium Volatility / Mean Reversion):** Reflects highly liquid, standard market-making intervals.
* **State 2 (High Volatility / Liquidity Shock):** Simulates sudden liquidity drawdowns or systemic shifts.

The transition kinematics adhere strictly to the true Transition Probability Matrix (TPM) $\mathbf{P}$:

$$\mathbf{P} = \begin{pmatrix} 0.7 & 0.2 & 0.1 \\ 0.2 & 0.6 & 0.2 \\ 0.1 & 0.4 & 0.5 \end{pmatrix}$$

#### Multi-Step State Forecasting
To project long-horizon regime structures, the engine solves the **Chapman-Kolmogorov Equations**, compounding transition maps across an operational horizon $n$:

$$\mathbf{P}^{(n)} = \mathbf{P}^n$$

#### Long-Run Invariant Equilibrium
The asymptotic steady-state probability vector $\boldsymbol{\pi}$ is extracted analytically by computing the invariant distribution bypassing localized bounds, satisfying:

$$\boldsymbol{\pi} \mathbf{P} = \boldsymbol{\pi}, \quad \sum_{i} \pi_i = 1$$

### 2. Inhomogeneous Poisson Order Flow (Lectures 6–7)
High-frequency order arrivals (limit and market executions) are simulated via a state-dependent **Inhomogeneous Poisson Process**. Rather than utilizing static arrival parameters, intensity vectors adapt dynamically:

$$P(N(t + \Delta t) - N(t) = k) = \frac{e^{-\int_t^{t+\Delta t} \lambda(s)ds} \left(\int_t^{t+\Delta t} \lambda(s)ds\right)^k}{k!}$$

Where the structural intensity function $\lambda(s)$ switches analytically with the underlying regime state, accurately capturing high-density order clustering during liquidity shocks ($S_2$).

### 3. Structural Stationarity & Autocorrelation (Lectures 8–12)
To validate the stochastic properties of simulated asset returns, the core processing layer calculates the empirical statistical structure. The asset return sequence must exhibit **Wide-Sense Stationarity (WSS)**:

$$\mathbb{E}[X_t] = \mu, \quad \text{Cov}(X_t, X_{t+\tau}) = \gamma(\tau)$$

The engine bypasses external statistical runtimes to execute a pure vectorized Autocorrelation Function (ACF) down to lag vectors $\tau$:

$$\rho(\tau) = \frac{\mathbb{E}[(X_t - \mu)(X_{t+\tau} - \mu)]}{\sigma^2}$$

---

## 📂 Project Repository Layout

```text
Stochastic-Market-Microstructure-Engine/
│
├── engine.py          # Core Math Layer (Markov Chain, Analytical TPM, Stationary Solvers)
├── app.py             # UI Dashboard Layer (Streamlit UI, Matrix Powers, Visualizations)
├── README.md          # Comprehensive Engineering Documentation
└── requirements.txt   # Runtime Dependencies List
└──/mathematical-notes/stochastic-microstructure-derivations.pdf