"""
Task 17: Ordinary Differential Equations – Euler Method
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
print("=== Task 17: Original Implementation ===")

# Newton's law of cooling:
# dT/dt = -k(T - T_ambient)
T_ambient = 25.0
T_initial = 90.0
k = 0.12
h = 1.0  # minutes
end_time = 30.0

def cooling_rate(T):
    return -k * (T - T_ambient)

time = np.arange(0, end_time + h, h)
temperature = np.zeros_like(time)
temperature[0] = T_initial

for i in range(len(time) - 1):
    temperature[i + 1] = (
        temperature[i] + h * cooling_rate(temperature[i])
    )

# Exact solution for validation
exact = T_ambient + (T_initial - T_ambient) * np.exp(-k * time)

print(f"Euler temperature after 30 min: {temperature[-1]:.2f} C")
print(f"Exact temperature after 30 min: {exact[-1]:.2f} C")
print(f"Final absolute error: {abs(temperature[-1] - exact[-1]):.4f} C")

# ==========================================
# SECTION 2: PARAMETER MODIFICATION (Requirement C)
# ==========================================
print("\n=== Task 17: Parameter Modification (Step Size Convergence Study) ===")
# Study effect of varying Euler step size h: [3.0, 1.0, 0.5, 0.1, 0.02]
step_sizes = [3.0, 1.0, 0.5, 0.1, 0.02]
errors_at_30 = []
exact_30 = T_ambient + (T_initial - T_ambient) * np.exp(-k * 30.0)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Plot exact curve on ax1
t_smooth = np.linspace(0, 30, 300)
ax1.plot(t_smooth, T_ambient + (T_initial - T_ambient) * np.exp(-k * t_smooth), 'k-', linewidth=2, label='Exact Analytical')

for step in step_sizes:
    t_arr = np.arange(0, 30.0 + step, step)
    T_arr = np.zeros_like(t_arr)
    T_arr[0] = T_initial
    for idx in range(len(t_arr) - 1):
        T_arr[idx + 1] = T_arr[idx] + step * cooling_rate(T_arr[idx])
    err = abs(T_arr[-1] - exact_30)
    errors_at_30.append(err)
    print(f"Step h = {step:4.2f} min -> Final Temp: {T_arr[-1]:.4f} °C, Absolute Error: {err:.4f} °C")
    if step in [3.0, 1.0, 0.1]:
        ax1.plot(t_arr, T_arr, label=f'Euler h={step} min')

ax1.set_xlabel("Time (minutes)")
ax1.set_ylabel("Temperature (°C)")
ax1.set_title("Cooling Dynamics under Varying Euler Step Sizes")
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.legend()

# Error scaling plot on ax2 (log-log showing O(h) first-order convergence)
ax2.loglog(step_sizes, errors_at_30, 'ro-', label='Euler Error at t=30m')
ax2.loglog(step_sizes, [e * (step_sizes[0]/step_sizes[0]) for e in step_sizes], 'k--', alpha=0.5, label='Reference O(h) Slope')
ax2.set_xlabel("Step Size h (min)")
ax2.set_ylabel("Absolute Error at t=30 min (°C)")
ax2.set_title("Euler Global Truncation Error O(h)")
ax2.grid(True, which='both', linestyle=':', alpha=0.6)
ax2.legend()

plt.tight_layout()
plt.savefig("outputs/orig_task_17.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/orig_task_17.png")
