"""
Task 16: Numerical Integration
Original Implementation and Parameter Modification.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import simpson
from scipy.interpolate import CubicSpline

# Ensure outputs directory exists
os.makedirs("outputs", exist_ok=True)

# ==========================================
# SECTION 1: ORIGINAL IMPLEMENTATION
# ==========================================
print("=== Task 16: Original Implementation ===")

# Smart-meter readings taken every two hours
time_hours = np.array([0, 2, 4, 6, 8, 10, 12], dtype=float)
power_kw = np.array([0.8, 1.0, 1.4, 1.8, 1.6, 1.2, 0.9])

energy_trapezoid = np.trapezoid(power_kw, time_hours)
energy_simpson = simpson(power_kw, x=time_hours)

print(f"Energy using trapezoidal rule: {energy_trapezoid:.3f} kWh")
print(f"Energy using Simpson's rule: {energy_simpson:.3f} kWh")
print(f"Difference between estimates: {abs(energy_simpson - energy_trapezoid):.3f} kWh")

# ==========================================
# SECTION 2: PARAMETER MODIFICATION (Requirement C)
# ==========================================
print("\n=== Task 16: Parameter Modification (Mesh Refinement) ===")
# Interpolate power load onto finer grids (1-hour and 15-minute intervals)
cs = CubicSpline(time_hours, power_kw)

fine_time_1h = np.linspace(0, 12, 13)       # dt = 1.0 hr
fine_power_1h = cs(fine_time_1h)

fine_time_15m = np.linspace(0, 12, 49)      # dt = 0.25 hr (15 min)
fine_power_15m = cs(fine_time_15m)

trap_1h = np.trapezoid(fine_power_1h, fine_time_1h)
simp_1h = simpson(fine_power_1h, x=fine_time_1h)

trap_15m = np.trapezoid(fine_power_15m, fine_time_15m)
simp_15m = simpson(fine_power_15m, x=fine_time_15m)

print(f"1-hour Grid  (N=13) -> Trap: {trap_1h:.4f} kWh, Simpson: {simp_1h:.4f} kWh (Diff: {abs(trap_1h-simp_1h):.4e})")
print(f"15-min Grid  (N=49) -> Trap: {trap_15m:.4f} kWh, Simpson: {simp_15m:.4f} kWh (Diff: {abs(trap_15m-simp_15m):.4e})")

# Visualization
t_dense = np.linspace(0, 12, 200)
p_dense = cs(t_dense)

plt.figure(figsize=(9, 5))
plt.plot(t_dense, p_dense, 'k-', alpha=0.7, label='Continuous Power Profile (Spline)')
plt.step(time_hours, power_kw, where='mid', color='gray', linestyle=':', label='Discrete Readings')
plt.fill_between(time_hours, power_kw, alpha=0.25, color='orange', label=f'Trapezoid Integration Area ({energy_trapezoid:.2f} kWh)')
plt.plot(time_hours, power_kw, 'ro', markersize=7, label='Meter Samples (2-hr)')
plt.xlabel("Time of Day (Hours)")
plt.ylabel("Electric Power Load (kW)")
plt.title("Task 16: Electric Energy Consumption via Numerical Quadrature")
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.savefig("outputs/orig_task_16.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/orig_task_16.png")
