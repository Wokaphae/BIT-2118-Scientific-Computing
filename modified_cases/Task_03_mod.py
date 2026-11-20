"""
Task 03 (Modified): High-Frequency Option Pricing Delta Calculation via Vectorization

Problem Statement:
In high-frequency quantitative market making, an options market maker receives 1,000,000
streaming quotes per second. The risk engine must evaluate the Black-Scholes call option
delta for each quote:
    d1 = [ln(S / K) + (r + 0.5 * sigma^2) * T] / [sigma * sqrt(T)]
    delta = 0.5 * [1 + erf(d1 / sqrt(2))]
Performing this via iterative Python loops introduces unacceptable order latency.
This task benchmarks a standard Python loop against vectorized NumPy execution.

Mathematical Concept:
Vectorized mathematical functions (logarithm, square root, error function) over large arrays
to achieve orders-of-magnitude execution speed-ups.

Assumptions & Input Data:
- 1,000,000 synthetic quotes with underlying stock price S ~ Uniform(90, 110)
- Strike price K = 100.0, risk-free interest rate r = 0.05, volatility sigma = 0.20, time-to-expiry T = 0.5 years.
"""

import math
import os
import timeit
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.special import erf

# Ensure outputs directory exists
os.makedirs("outputs", exist_ok=True)

print("=== Task 03 Modified: Options Market-Maker Delta Vectorization ===")

# Generate 1,000,000 quotes
rng = np.random.default_rng(101)
N = 1_000_000
S_arr = rng.uniform(85.0, 115.0, N)
K = 100.0
r = 0.05
sigma = 0.20
T = 0.5
sqrt_T = np.sqrt(T)

def loop_black_scholes_delta():
    deltas = []
    drift = (r + 0.5 * sigma**2) * T
    denom = sigma * math.sqrt(T)
    inv_sqrt2 = 1.0 / math.sqrt(2.0)
    for S in S_arr:
        d1 = (math.log(S / K) + drift) / denom
        delta = 0.5 * (1.0 + math.erf(d1 * inv_sqrt2))
        deltas.append(delta)
    return deltas

def vectorized_black_scholes_delta():
    drift = (r + 0.5 * sigma**2) * T
    denom = sigma * sqrt_T
    d1 = (np.log(S_arr / K) + drift) / denom
    delta = 0.5 * (1.0 + erf(d1 / np.sqrt(2.0)))
    return delta

loop_time = timeit.timeit(loop_black_scholes_delta, number=1)
vector_time = timeit.timeit(vectorized_black_scholes_delta, number=3) / 3
deltas_vec = vectorized_black_scholes_delta()

print(f"Dataset Size: {N:,} option contracts")
print("First five option deltas:", np.round(deltas_vec[:5], 4))
print(f"Mean Portfolio Delta: {np.mean(deltas_vec):.4f}")
print(f"Python Loop Time:     {loop_time:.4f} s")
print(f"Vectorized NumPy Time: {vector_time:.4f} s")
speedup = loop_time / vector_time
print(f"Algorithmic Speed-up: {speedup:.1f}x")

# Benchmark across multiple scale tiers for visualization
batch_sizes = [5_000, 25_000, 100_000, 500_000]
loop_bench = []
vec_bench = []

for b in batch_sizes:
    sub_S = S_arr[:b]
    def sub_loop():
        res = []
        for s in sub_S:
            d1 = (math.log(s / K) + (r + 0.5 * sigma**2)*T) / (sigma * math.sqrt(T))
            res.append(0.5 * (1.0 + math.erf(d1 / math.sqrt(2.0))))
        return res
    def sub_vec():
        d1 = (np.log(sub_S / K) + (r + 0.5 * sigma**2)*T) / (sigma * sqrt_T)
        return 0.5 * (1.0 + erf(d1 / np.sqrt(2.0)))

    loop_bench.append(timeit.timeit(sub_loop, number=1))
    vec_bench.append(timeit.timeit(sub_vec, number=5) / 5)

# Visualization
plt.figure(figsize=(8, 4.8))
plt.plot(batch_sizes, loop_bench, marker='o', color='#d62728', linewidth=2, label='Sequential Python Loop')
plt.plot(batch_sizes, vec_bench, marker='s', color='#2ca02c', linewidth=2, label='Vectorized SIMD NumPy/SciPy')
plt.title("Task 03 Mod: Black-Scholes Risk Evaluation Latency Scaling")
plt.xlabel("Order Book Quote Volume (N options)")
plt.ylabel("Processing Time (seconds)")
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.savefig("outputs/mod_task_03.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/mod_task_03.png")
