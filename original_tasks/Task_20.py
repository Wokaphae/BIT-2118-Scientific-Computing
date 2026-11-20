"""
Task 20: Random Numbers and Monte Carlo Methods
Original Implementation and Parameter Modification.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Ensure outputs directory exists
os.makedirs("outputs", exist_ok=True)

# ==========================================
# SECTION 1: ORIGINAL IMPLEMENTATION
# ==========================================
print("=== Task 20: Original Implementation ===")

rng = np.random.default_rng(42)
capacity = 1000.0
mean_demand = 850.0
std_demand = 120.0
N = 100_000

# Random demand scenarios
demand = rng.normal(mean_demand, std_demand, N)
overloaded = demand > capacity
overload_probability = overloaded.mean()

print(f"Estimated overload probability: {overload_probability:.4%}")
print(f"Number of overload cases: {overloaded.sum()} out of {N}")

# Running probability to show convergence
running_probability = np.cumsum(overloaded) / np.arange(1, N + 1)
indices = np.unique(
    np.logspace(1, np.log10(N), 200).astype(int)
) - 1

# ==========================================
# SECTION 2: PARAMETER MODIFICATION (Requirement C)
# ==========================================
print("\n=== Task 20: Parameter Modification (Stress Testing) ===")
# Stress condition 1: Increased demand volatility (std = 180.0)
demand_high_vol = rng.normal(mean_demand, 180.0, N)
overload_prob_high_vol = (demand_high_vol > capacity).mean()

# Stress condition 2: High base demand (mean = 920.0, std = 120.0)
demand_high_mean = rng.normal(920.0, std_demand, N)
overload_prob_high_mean = (demand_high_mean > capacity).mean()

print(f"Baseline Overload Probability (μ=850, σ=120): {overload_probability:.4%}")
print(f"High Volatility Overload (μ=850, σ=180):      {overload_prob_high_vol:.4%}")
print(f"Surge Base Load Overload (μ=920, σ=120):      {overload_prob_high_mean:.4%}")

running_prob_vol = np.cumsum(demand_high_vol > capacity) / np.arange(1, N + 1)
running_prob_mean = np.cumsum(demand_high_mean > capacity) / np.arange(1, N + 1)

# Visualization
plt.figure(figsize=(9, 5))
plt.semilogx(indices + 1, running_probability[indices], 'b-', label=f"Baseline (μ=850, σ=120): {overload_probability:.2%}")
plt.semilogx(indices + 1, running_prob_vol[indices], 'g--', label=f"High Volatility (μ=850, σ=180): {overload_prob_high_vol:.2%}")
plt.semilogx(indices + 1, running_prob_mean[indices], 'r-.', label=f"Surge Base (μ=920, σ=120): {overload_prob_high_mean:.2%}")
plt.xlabel("Number of simulations (Log Scale)")
plt.ylabel("Estimated Overload Probability")
plt.title("Task 20: Monte Carlo Server Risk Convergence & Sensitivity Analysis")
plt.grid(True, which="both", linestyle=':', alpha=0.6)
plt.legend()
plt.savefig("outputs/orig_task_20.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/orig_task_20.png")
