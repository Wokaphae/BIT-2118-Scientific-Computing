"""
Task 03: Mathematical Functions and Vectorization
Original Implementation (with OCR syntax fixes) and Parameter Modification.
"""

import os
import timeit
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Ensure outputs directory exists
os.makedirs("outputs", exist_ok=True)

# ==========================================
# SECTION 1: ORIGINAL IMPLEMENTATION
# ==========================================
print("=== Task 03: Original Implementation ===")

# Simulated network latency readings in milliseconds
rng = np.random.default_rng(42)
latency_ms = rng.uniform(5, 250, 1_000_000)

def loop_version():
    squared = []
    for value in latency_ms:
        # OCR FIX: original PDF was missing assignment '=' -> 'seconds value / 1000.0'
        seconds = value / 1000.0
        squared.append(seconds ** 2)
    return squared

def vectorized_version():
    seconds = latency_ms / 1000.0
    return seconds ** 2

loop_time = timeit.timeit(loop_version, number=1)
vector_time = timeit.timeit(vectorized_version, number=3) / 3
result = vectorized_version()

print("First five squared latency values:", result[:5])
print(f"Loop time: {loop_time:.4f} s")
print(f"Vectorized time: {vector_time:.4f} s")
speedup = loop_time / vector_time
print(f"Approximate speed-up: {speedup:.1f}x")

# ==========================================
# SECTION 2: PARAMETER MODIFICATION (Requirement C)
# ==========================================
print("\n=== Task 03: Parameter Modification ===")
# Parameter variation: Test scaling over different array sizes N
sample_sizes = [10_000, 50_000, 200_000, 500_000]
loop_timings = []
vector_timings = []

for N in sample_sizes:
    data = rng.uniform(5, 250, N)
    
    def test_loop():
        sq = []
        for v in data:
            s = v / 1000.0
            sq.append(s ** 2)
        return sq
        
    def test_vector():
        s = data / 1000.0
        return s ** 2
        
    t_loop = timeit.timeit(test_loop, number=1)
    t_vec = timeit.timeit(test_vector, number=5) / 5
    loop_timings.append(t_loop)
    vector_timings.append(t_vec)
    print(f"Size N={N:7d} -> Loop: {t_loop:.5f}s, Vector: {t_vec:.5f}s, Speedup: {t_loop/t_vec:.1f}x")

# Generate Comparative Visualization
plt.figure(figsize=(8, 4.5))
plt.plot(sample_sizes, loop_timings, marker='o', color='#d62728', label='Python Loop')
plt.plot(sample_sizes, vector_timings, marker='s', color='#2ca02c', label='NumPy Vectorized')
plt.title("Task 03: Execution Time vs Dataset Size (Vectorization Benchmark)")
plt.xlabel("Sample Size (N elements)")
plt.ylabel("Execution Time (seconds)")
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.savefig("outputs/orig_task_03.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/orig_task_03.png")
