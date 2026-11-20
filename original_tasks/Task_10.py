"""
Task 10: Root Finding: Bisection and Fixed-Point Methods
Original Implementation and Parameter Modification.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import root_scalar

# Ensure outputs directory exists
os.makedirs("outputs", exist_ok=True)

# ==========================================
# SECTION 1: ORIGINAL IMPLEMENTATION
# ==========================================
print("=== Task 10: Original Implementation ===")

# Heat-balance model:
# f(T) = 0 means heat gain equals heat loss.
def heat_balance(T):
    return T - 25 - 10 * np.exp(-T / 20)

# Bisection: bracket a sign change
solution = root_scalar(
    heat_balance,
    bracket=[20, 40],
    method="bisect",
    xtol=1e-10
)

# Fixed-point form:
# T = 25 + 10*exp(-T/20)
def g(T):
    return 25 + 10 * np.exp(-T / 20)

T = 30.0
history = [T]

for _ in range(100):
    T_new = g(T)
    history.append(T_new)
    if abs(T_new - T) < 1e-10:
        break
    T = T_new

print(f"Bisection equilibrium temperature: {solution.root:.6f} C")
print(f"Fixed-point equilibrium temperature: {history[-1]:.6f} C")
print("Fixed-point iterations:", len(history) - 1)

# ==========================================
# SECTION 2: PARAMETER MODIFICATION (Requirement C)
# ==========================================
print("\n=== Task 10: Parameter Modification ===")
# Modifying thermal parameters: Ambient temp raised from 25°C to 35°C, heat generation 10 -> 15
def heat_balance_mod(T):
    return T - 35 - 15 * np.exp(-T / 20)

def g_mod(T):
    return 35 + 15 * np.exp(-T / 20)

solution_mod = root_scalar(
    heat_balance_mod,
    bracket=[30, 55],
    method="bisect",
    xtol=1e-10
)

T_mod = 30.0
history_mod = [T_mod]
for _ in range(100):
    T_new = g_mod(T_mod)
    history_mod.append(T_new)
    if abs(T_new - T_mod) < 1e-10:
        break
    T_mod = T_new

print(f"Modified Bisection equilibrium: {solution_mod.root:.6f} C")
print(f"Modified Fixed-point equilibrium: {history_mod[-1]:.6f} C")
print("Modified Fixed-point iterations:", len(history_mod) - 1)

# Comparative Visualization
temps = np.linspace(20, 55, 300)
plt.figure(figsize=(8, 5))
plt.plot(temps, heat_balance(temps), 'b-', label='Original f(T) [Tamb=25°C, Q=10]')
plt.plot(temps, heat_balance_mod(temps), 'r-', label='Modified f(T) [Tamb=35°C, Q=15]')
plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
plt.axvline(solution.root, color='blue', linestyle=':', label=f'Orig Root: {solution.root:.2f}°C')
plt.axvline(solution_mod.root, color='red', linestyle=':', label=f'Mod Root: {solution_mod.root:.2f}°C')
plt.xlabel("Temperature (°C)")
plt.ylabel("Net Heat-Balance Function f(T)")
plt.title("Task 10: Thermal Equilibrium Root Finding (Bisection vs Fixed-Point)")
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.savefig("outputs/orig_task_10.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/orig_task_10.png")
