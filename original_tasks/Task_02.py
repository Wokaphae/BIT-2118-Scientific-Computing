"""
Task 02: NumPy Arrays and Numerical Computation
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
print("=== Task 02: Original Implementation ===")

# 24 hourly temperature readings in degrees Celsius
temperatures_c = np.array([
    18.5, 18.0, 17.8, 17.5, 17.9, 19.0,
    21.5, 23.8, 25.6, 27.1, 28.3, 29.0,
    29.4, 29.1, 28.5, 27.6, 26.2, 24.8,
    23.4, 22.1, 21.0, 20.2, 19.6, 19.0
])

mean_temp = np.mean(temperatures_c)
min_temp = np.min(temperatures_c)
max_temp = np.max(temperatures_c)

# Vectorized Celsius-to-Fahrenheit conversion
temperatures_f = 1.8 * temperatures_c + 32

print(f"Daily mean temperature: {mean_temp:.2f} C")
print(f"Minimum temperature: {min_temp:.2f} C")
print(f"Maximum temperature: {max_temp:.2f} C")
print("First six Fahrenheit readings:", temperatures_f[:6])

# ==========================================
# SECTION 2: PARAMETER MODIFICATION (Requirement C)
# ==========================================
print("\n=== Task 02: Parameter Modification ===")
# Simulating a severe regional heatwave: baseline temperatures elevated by +5.5 °C
temp_heatwave_c = temperatures_c + 5.5
mean_heatwave = np.mean(temp_heatwave_c)
min_heatwave = np.min(temp_heatwave_c)
max_heatwave = np.max(temp_heatwave_c)
temp_heatwave_f = 1.8 * temp_heatwave_c + 32

print(f"Heatwave mean temperature: {mean_heatwave:.2f} C (delta: +{mean_heatwave - mean_temp:.2f} C)")
print(f"Heatwave min temperature: {min_heatwave:.2f} C (delta: +{min_heatwave - min_temp:.2f} C)")
print(f"Heatwave max temperature: {max_heatwave:.2f} C (delta: +{max_heatwave - max_temp:.2f} C)")
print("First six Heatwave Fahrenheit readings:", temp_heatwave_f[:6])

# Generate Comparative Visualization
hours = np.arange(24)
plt.figure(figsize=(9, 4.5))
plt.plot(hours, temperatures_c, marker='o', color='#1f77b4', label=f'Baseline (Mean: {mean_temp:.1f} °C)')
plt.plot(hours, temp_heatwave_c, marker='s', linestyle='--', color='#d62728', label=f'Heatwave +5.5°C (Mean: {mean_heatwave:.1f} °C)')
plt.title("Task 02: 24-Hour Diurnal Temperature Profile (Celsius)")
plt.xlabel("Hour of Day (00:00 - 23:00)")
plt.ylabel("Temperature (°C)")
plt.xticks(hours[::2])
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.savefig("outputs/orig_task_02.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/orig_task_02.png")
