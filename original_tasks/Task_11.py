"""
Task 11: Root Finding: Newton-Raphson and Secant Methods
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
print("=== Task 11: Original Implementation ===")

# Initial investment followed by annual cash inflows
cash_flows = [-10000, 3000, 3500, 4000, 2500]

def npv(rate):
    return sum(
        cf / (1 + rate)**t
        for t, cf in enumerate(cash_flows)
    )

def d_npv(rate):
    return sum(
        -t * cf / (1 + rate)**(t + 1)
        for t, cf in enumerate(cash_flows)
        if t > 0
    )

newton = root_scalar(
    npv,
    fprime=d_npv,
    x0=0.10,
    method="newton",
    xtol=1e-12
)

secant = root_scalar(
    npv,
    x0=0.05,
    x1=0.20,
    method="secant",
    xtol=1e-12
)

print(f"IRR using Newton-Raphson: {newton.root:.6%}")
print(f"Newton iterations: {newton.iterations}")
print(f"IRR using Secant method: {secant.root:.6%}")
print(f"Secant iterations: {secant.iterations}")
print(f"NPV at Newton solution: {npv(newton.root):.6f}")

# ==========================================
# SECTION 2: PARAMETER MODIFICATION (Requirement C)
# ==========================================
print("\n=== Task 11: Parameter Modification ===")
# Capital expansion scenario: Initial outlay increased to $12,500, adding Year 5 return of $3,500
cash_flows_mod = [-12500, 3000, 3500, 4000, 2500, 3500]

def npv_mod(rate):
    return sum(
        cf / (1 + rate)**t
        for t, cf in enumerate(cash_flows_mod)
    )

def d_npv_mod(rate):
    return sum(
        -t * cf / (1 + rate)**(t + 1)
        for t, cf in enumerate(cash_flows_mod)
        if t > 0
    )

newton_mod = root_scalar(
    npv_mod,
    fprime=d_npv_mod,
    x0=0.10,
    method="newton",
    xtol=1e-12
)

secant_mod = root_scalar(
    npv_mod,
    x0=0.05,
    x1=0.20,
    method="secant",
    xtol=1e-12
)

print(f"Modified IRR (Newton): {newton_mod.root:.6%}")
print(f"Modified Newton iterations: {newton_mod.iterations}")
print(f"Modified IRR (Secant): {secant_mod.root:.6%}")
print(f"Modified Secant iterations: {secant_mod.iterations}")

# Comparative Visualization
rates = np.linspace(0.01, 0.30, 200)
npv_vals = [npv(r) for r in rates]
npv_mod_vals = [npv_mod(r) for r in rates]

plt.figure(figsize=(8, 4.8))
plt.plot(rates * 100, npv_vals, 'b-', label=f'Original Project (IRR: {newton.root:.2%})')
plt.plot(rates * 100, npv_mod_vals, 'r--', label=f'Expanded Project (IRR: {newton_mod.root:.2%})')
plt.axhline(0, color='gray', linestyle=':', linewidth=0.8)
plt.scatter([newton.root * 100], [0], color='blue', zorder=5)
plt.scatter([newton_mod.root * 100], [0], color='red', zorder=5)
plt.xlabel("Discount Rate / Cost of Capital (%)")
plt.ylabel("Net Present Value ($)")
plt.title("Task 11: Net Present Value Profile & Internal Rate of Return (IRR)")
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.savefig("outputs/orig_task_11.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/orig_task_11.png")
