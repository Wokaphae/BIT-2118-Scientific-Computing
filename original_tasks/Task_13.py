"""
Task 13: Interpolation
Original Implementation and Parameter Modification.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d, CubicSpline

# Ensure outputs directory exists
os.makedirs("outputs", exist_ok=True)

# ==========================================
# SECTION 1: ORIGINAL IMPLEMENTATION
# ==========================================
print("=== Task 13: Original Implementation ===")

# Hourly temperature measurements
hours = np.array([8, 9, 10, 11, 12, 13, 14], dtype=float)
temperature = np.array([18.0, 20.0, 22.5, 24.0, 25.0, 25.5, 25.0])

linear = interp1d(hours, temperature, kind="linear")
cubic = CubicSpline(hours, temperature)

# Estimate every 10 minutes = 1/6 hour
ten_minute_times = np.arange(8, 14 + 1/6, 1/6)
linear_estimates = linear(ten_minute_times)
cubic_estimates = cubic(ten_minute_times)

target_time = 10.5  # 10:30
print(f"Linear estimate at 10:30: {float(linear(target_time)):.2f} C")
print(f"Cubic estimate at 10:30: {float(cubic(target_time)):.2f} C")

# ==========================================
# SECTION 2: PARAMETER MODIFICATION (Requirement C)
# ==========================================
print("\n=== Task 13: Parameter Modification ===")
# Quadratic interpolation comparison and multiple evaluation timestamps
quadratic = interp1d(hours, temperature, kind="quadratic")
quad_estimates = quadratic(ten_minute_times)

eval_times = [9.25, 10.5, 11.75, 13.333]
time_labels = ["09:15", "10:30", "11:45", "13:20"]

print("Comparative Interpolation at Discrete Timestamps:")
for t, lbl in zip(eval_times, time_labels):
    lin_val = float(linear(t))
    quad_val = float(quadratic(t))
    cub_val = float(cubic(t))
    print(f"Time {lbl} (t={t:.3f}h) -> Linear: {lin_val:.2f} C | Quadratic: {quad_val:.2f} C | Cubic: {cub_val:.2f} C")

# Visualization
plt.figure(figsize=(9, 5))
plt.scatter(hours, temperature, color='black', s=50, zorder=5, label="Hourly measurements")
plt.plot(ten_minute_times, linear_estimates, 'b--', label="Linear Interpolation")
plt.plot(ten_minute_times, quad_estimates, 'g-.', label="Quadratic Spline (Mod)")
plt.plot(ten_minute_times, cubic_estimates, 'r-', label="Cubic Spline")
plt.xlabel("Hour of day")
plt.ylabel("Temperature (°C)")
plt.title("Task 13: Comparison of Linear, Quadratic, and Cubic Spline Interpolation")
plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)
plt.savefig("outputs/orig_task_13.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/orig_task_13.png")
