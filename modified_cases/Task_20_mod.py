"""
Task 20 (Modified): Financial Portfolio Value at Risk (VaR) via Monte Carlo Simulation

Problem Statement:
An investment fund manages an equity and bond portfolio with total market valuation of
$10,000,000. Risk compliance regulations (Basel III) require calculating the 1-day 95% and 99%
Value at Risk (VaR) and Conditional Value at Risk (CVaR / Expected Shortfall) to assess extreme tail risk.
Daily portfolio returns follow a normal distribution with historical daily drift mu = +0.03% (0.0003)
and daily volatility sigma = 1.45% (0.0145). The risk management desk executes a Monte Carlo
simulation of N = 100,000 trading day scenarios to estimate the distribution of daily portfolio
profit/loss (P&L), quantify the running convergence rate of tail loss estimates, and evaluate solvency.

Mathematical Concept:
Monte Carlo Methods: Statistical estimation via pseudo-random number generation (NumPy default_rng),
empirical percentile estimation for Value at Risk, and cumulative sample mean convergence (Law of Large Numbers).

Assumptions & Input Data:
- Portfolio initial value V0 = $10,000,000.
- Daily return parameters: mu = 0.0003, sigma = 0.0145.
- Number of stochastic trials N = 100,000.
- Confidence levels: 95% and 99%.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Ensure outputs directory exists
os.makedirs("outputs", exist_ok=True)

print("=== Task 20 Modified: Monte Carlo Portfolio Value at Risk (VaR) ===")

rng = np.random.default_rng(2026)
V0 = 10_000_000.0  # $10 Million Portfolio
mu = 0.0003         # Daily expected return
sigma = 0.0145      # Daily volatility
N = 100_000

# Generate stochastic daily returns and P&L outcomes
simulated_returns = rng.normal(mu, sigma, N)
pnl_distribution = V0 * simulated_returns  # Profit and Loss in Dollars

# Value at Risk (VaR) at 95% and 99% confidence
var_95 = -np.percentile(pnl_distribution, 5.0)
var_99 = -np.percentile(pnl_distribution, 1.0)

# Expected Shortfall (CVaR: Average loss beyond VaR threshold)
cvar_95 = -np.mean(pnl_distribution[pnl_distribution <= -var_95])
cvar_99 = -np.mean(pnl_distribution[pnl_distribution <= -var_99])

# Probability of single-day loss exceeding $250,000
breach_threshold = -250_000.0
breach_events = pnl_distribution < breach_threshold
prob_severe_loss = np.mean(breach_events)

# Running Monte Carlo estimate of 95% loss probability
running_prob = np.cumsum(pnl_distribution <= -var_95) / np.arange(1, N + 1)
eval_indices = np.unique(np.logspace(1, np.log10(N), 200).astype(int)) - 1

print(f"Portfolio Market Value:            ${V0:,.0f}")
print(f"Simulated Trials N:                {N:,}")
print(f"1-Day 95% Value at Risk (VaR):     ${var_95:,.2f} ({var_95/V0*100:.2f}% of capital)")
print(f"1-Day 99% Value at Risk (VaR):     ${var_99:,.2f} ({var_99/V0*100:.2f}% of capital)")
print(f"1-Day 95% Expected Shortfall CVaR: ${cvar_95:,.2f}")
print(f"1-Day 99% Expected Shortfall CVaR: ${cvar_99:,.2f}")
print(f"Probability of Loss > $250,000:    {prob_severe_loss:.4%} ({breach_events.sum()} trials)")

# Dual Subplot Visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8))

# Subplot 1: P&L histogram with VaR lines
ax1.hist(pnl_distribution / 1000.0, bins=80, density=True, color='#1f77b4', alpha=0.7, edgecolor='black', linewidth=0.5)
ax1.axvline(-var_95 / 1000.0, color='orange', linestyle='--', linewidth=2, label=f'95% VaR: -${var_95/1000:.1f}k')
ax1.axvline(-var_99 / 1000.0, color='red', linestyle='-', linewidth=2, label=f'99% VaR: -${var_99/1000:.1f}k')
ax1.set_title("Simulated Daily Portfolio P&L Distribution")
ax1.set_xlabel("Daily P&L (Thousands USD)")
ax1.set_ylabel("Probability Density")
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.legend()

# Subplot 2: Running Monte Carlo probability convergence
ax2.semilogx(eval_indices + 1, running_prob[eval_indices] * 100.0, 'b-', linewidth=1.8, label='Empirical 5% Tail Frequency')
ax2.axhline(5.0, color='red', linestyle='--', label='Theoretical 5.0% Limit')
ax2.set_title("Law of Large Numbers: Tail Probability Convergence")
ax2.set_xlabel("Number of Monte Carlo Iterations (Log Scale)")
ax2.set_ylabel("Observed Tail Frequency (%)")
ax2.grid(True, which="both", linestyle=':', alpha=0.6)
ax2.legend()

plt.tight_layout()
plt.savefig("outputs/mod_task_20.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/mod_task_20.png")
