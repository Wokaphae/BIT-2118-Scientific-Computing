"""
Task 10 (Modified): Non-Ideal Gas Molar Volume via Bisection and Fixed-Point Iteration

Problem Statement:
In petrochemical process design, Carbon Dioxide (CO2) is compressed into a supercritical state
inside an industrial reactor at pressure P = 55.0 atm (5.572e6 Pa) and temperature T = 315.0 K.
Under high pressures, the ideal gas law fails, and the real gas behaviour obeys the Van der Waals
equation of state:
    (P + a / V^2) * (V - b) = R * T
where 'V' is the molar volume (L/mol). To find the operating molar volume, the equation is rearranged
into the root-finding residual form:
    f(V) = (P + a / V^2) * (V - b) - R * T = 0
and the contractive fixed-point mapping:
    V_{k+1} = b + (R * T) / (P + a / V_k^2)
Both Bisection and Fixed-Point numerical solvers are implemented and benchmarked.

Mathematical Concept:
1D Root Finding: Interval bisection method with guaranteed bracketing convergence, and fixed-point
iteration x_{k+1} = g(x_k).

Assumptions & Input Data:
- Van der Waals constants for CO2:
    a = 3.592 L^2*atm / mol^2
    b = 0.04267 L / mol
- Universal gas constant R = 0.082057 L*atm / (mol*K)
- Operating conditions: P = 55.0 atm, T = 315.0 K.
- Bisection bracket: [0.05, 1.0] L/mol.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import root_scalar

# Ensure outputs directory exists
os.makedirs("outputs", exist_ok=True)

print("=== Task 10 Modified: Van der Waals Molar Volume Root Finding ===")

P = 55.0         # atm
T = 315.0        # Kelvin
R = 0.082057     # L*atm / (mol*K)
a = 3.592        # L^2*atm / mol^2
b = 0.04267      # L / mol

# Ideal gas volume for comparison: V_ideal = RT / P
V_ideal = (R * T) / P

def vdw_residual(V):
    return (P + a / (V**2)) * (V - b) - R * T

# 1. Bisection method
bisect_sol = root_scalar(
    vdw_residual,
    bracket=[0.05, 1.0],
    method="bisect",
    xtol=1e-10
)

# 2. Fixed-point iteration
def g_fixed_point(V):
    return b + (R * T) / (P + a / (V**2))

V_fp = V_ideal
fp_history = [V_fp]
for _ in range(100):
    V_next = g_fixed_point(V_fp)
    fp_history.append(V_next)
    if abs(V_next - V_fp) < 1e-10:
        break
    V_fp = V_next

print(f"Ideal Gas Volume:      {V_ideal:.6f} L/mol")
print(f"Bisection Root:        {bisect_sol.root:.6f} L/mol (Iters: {bisect_sol.iterations})")
print(f"Fixed-Point Root:      {fp_history[-1]:.6f} L/mol (Iters: {len(fp_history)-1})")
compression_factor_Z = (P * bisect_sol.root) / (R * T)
print(f"Compressibility Factor Z = PV/(RT): {compression_factor_Z:.4f} (Real Gas Correction)")

# Visualization
v_range = np.linspace(0.06, 0.70, 300)
f_vals = vdw_residual(v_range)

plt.figure(figsize=(8, 4.8))
plt.plot(v_range, f_vals, 'b-', linewidth=2, label='Van der Waals Residual f(V)')
plt.axhline(0, color='black', linestyle='--', linewidth=0.8)
plt.axvline(bisect_sol.root, color='red', linestyle=':', label=f'Real Volume ({bisect_sol.root:.4f} L/mol)')
plt.axvline(V_ideal, color='gray', linestyle='-.', label=f'Ideal Volume ({V_ideal:.4f} L/mol)')
plt.title("Task 10 Mod: Van der Waals Supercritical CO₂ Equation of State Root")
plt.xlabel("Molar Volume V (Liters / mole)")
plt.ylabel("Equation Residual f(V)")
plt.ylim(-15, 25)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.savefig("outputs/mod_task_10.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/mod_task_10.png")
