import numpy as np

class MicrostructureEngine:
    def __init__(self, n_ticks: int = 500):
        self.n_ticks = n_ticks
        # Markov Transition Matrix Framework (Lectures 1-5)
        self.true_tpm = np.array([
            [0.7, 0.2, 0.1],
            [0.2, 0.6, 0.2],
            [0.1, 0.4, 0.5]
        ])
        
    def generate_synthetic_chain(self):
        """Simulates high-frequency asset pricing and order flow via regimes."""
        np.random.seed(42)
        states = [0]
        
        # Vectorized choice simulation framework
        for _ in range(self.n_ticks - 1):
            states.append(np.random.choice([0, 1, 2], p=self.true_tpm[states[-1]]))
            
        prices = [100.0]
        order_arrivals = []
        
        # Multi-Regime mapping parameters
        regime_params = {
            0: {"mu": 0.0002, "sigma": 0.005, "lambda": 5},   # Trend / Low Vol
            1: {"mu": 0.0,    "sigma": 0.015, "lambda": 15},  # Mean-Reverting
            2: {"mu": -0.005,  "sigma": 0.04,  "lambda": 30}   # Liquidity Shock
        }
        
        for s in states:
            p = regime_params[s]
            ret = np.random.normal(p["mu"], p["sigma"])
            prices.append(prices[-1] * (1 + ret))
            order_arrivals.append(np.random.poisson(p["lambda"])) # Inhomogeneous Poisson simulation
            
        returns = np.diff(prices) / prices[:-1]
        return np.array(prices[:-1]), returns, np.array(states), np.array(order_arrivals)

    @staticmethod
    def compute_empirical_tpm(states) -> np.ndarray:
        """Calculates 3x3 empirical state matrix transitions."""
        tpm = np.zeros((3, 3))
        for t in range(len(states) - 1):
            tpm[states[t], states[t+1]] += 1
        # Add epsilon stability for zero-division avoidance
        return tpm / (tpm.sum(axis=1, keepdims=True) + 1e-9)

    @staticmethod
    def compute_stationary_distribution(tpm) -> np.ndarray:
        """Solves operational steady-state invariant probabilities via matrix inversion."""
        try:
            Q = tpm.T - np.eye(3)
            Q[-1] = np.ones(3)
            rhs = np.zeros(3)
            rhs[-1] = 1.0
            return np.linalg.solve(Q, rhs)
        except np.linalg.LinAlgError:
            return np.array([1/3, 1/3, 1/3])

    @staticmethod
    def compute_pure_acf(returns, max_lag: int = 20) -> np.ndarray:
        """Pure vectorized AutoCorrelation implementation bypassing heavy tsmodels overhead."""
        mean = np.mean(returns)
        var = np.var(returns) + 1e-9
        norm_returns = returns - mean
        acf_vals = []
        for lag in range(max_lag + 1):
            if lag == 0:
                acf_vals.append(1.0)
            else:
                covariance = np.mean(norm_returns[:-lag] * norm_returns[lag:])
                acf_vals.append(covariance / var)
        return np.array(acf_vals)