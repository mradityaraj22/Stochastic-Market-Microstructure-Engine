import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from engine import MicrostructureEngine

# 1. Native Page Configuration
st.set_page_config(
    page_title="Quant Microstructure Engine", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Native Stealth Hack (Bypasses CSS Parser Completely)
st.html("<style>[data-testid='stHeader'], [data-testid='stToolbar'], .stAppDeployButton, #MainMenu, footer, header {display: none !important; visibility: hidden !important; height: 0px !important;}</style>")

st.title("🎲 Stochastic Market Microstructure Engine")
# Sidebar Dynamic Hyperparameters Configuration
n_ticks = st.sidebar.slider("Historical Ticks Vector Count", 200, 2000, 600)
n_steps = st.sidebar.slider("Chapman-Kolmogorov Horizon (N-Steps)", 1, 10, 3)

# Data Ingestion Engine Invocations
engine = MicrostructureEngine(n_ticks=n_ticks)
prices, returns, states, arrivals = engine.generate_synthetic_chain()
tpm = engine.compute_empirical_tpm(states)

# UI Layout Component Matrix Splits
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📈 Empirical Transition Probability Matrix (TPM)")
    st.dataframe(pd.DataFrame(tpm, columns=[f'To S{i}' for i in range(3)], index=[f'From S{i}' for i in range(3)]).style.format("{:.2%}"))

with col2:
    st.markdown("### 🔮 Chapman-Kolmogorov N-Step State Forecasts")
    tpm_n = np.linalg.matrix_power(tpm, n_steps)
    st.dataframe(pd.DataFrame(tpm_n, columns=[f'S{i}' for i in range(3)], index=[f'Start S{i}' for i in range(3)]).style.format("{:.2%}"))

# Long-Run Analytical Equilibrium Metrics Blocks
st.markdown("---")
stationary = engine.compute_stationary_distribution(tpm)
st.metric("Long-run Equilibrium Distribution", f"S0 (Low Vol): {stationary[0]:.1%} | S1 (Mean Reverting): {stationary[1]:.1%} | S2 (Liquidity Shock): {stationary[2]:.1%}")

col3, col4 = st.columns(2)

with col3:
    st.markdown("### 🧪 Vectorized AutoCorrelation (Returns Processing)")
    acf_vals = engine.compute_pure_acf(returns, max_lag=20)
    st.plotly_chart(px.bar(x=list(range(21)), y=acf_vals, labels={'x': 'Lag Vector ($\tau$)', 'y': 'Autocorrelation (ACF)'}), use_container_width=True)

with col4:
    st.markdown("### ⏱️ Inhomogeneous Poisson Order Flow Intensities")
    st.plotly_chart(px.line(y=arrivals, labels={'index': 'Tick Matrix Sequence', 'value': 'Arrival Events Count ($\lambda$)'}), use_container_width=True)

# Main High-Frequency Structural Data Stream Visualizations
st.markdown("---")
st.markdown("### 💹 Asset Price Path Intersected with Latent Volatility Regimes")
fig = px.line(x=range(len(prices)), y=prices, labels={'x': 'Ticks Sequence', 'y': 'Asset Price Vector'})
for s, col in zip([0, 1, 2], ['rgba(0,200,0,0.5)', 'rgba(230,230,0,0.6)', 'rgba(255,0,0,0.8)']):
    idx = np.where(states == s)[0]
    fig.add_trace(go.Scatter(x=idx, y=prices[idx], mode='markers', name=f'Regime State {s}', marker=dict(color=col, size=4.5)))
st.plotly_chart(fig, use_container_width=True)