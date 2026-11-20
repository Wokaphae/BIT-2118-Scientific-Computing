"""
Task 04 (Modified): Aerodynamic Drag and Catastrophic Cancellation in Quadratic Equations

Problem Statement:
In aerospace re-entry dynamics, aerodynamic deceleration is modeled by the quadratic equation:
    a * x^2 + b * x + c = 0
where 'a' is the nonlinear compressibility factor, 'b' is the high supersonic drag coefficient,
and 'c' is the altitude perturbation thrust. When b^2 >> 4*a*c, standard quadratic formula:
    x1 = (-b + sqrt(b^2 - 4*a*c)) / (2*a)
suffers severe catastrophic cancellation because two almost identical quantities are subtracted.
The numerically stable Citardauq / rationalized formula:
    x1_stable = (2 * c) / (-b - sqrt(b^2 - 4*a*c))
avoids cancellation entirely.

Mathematical Concept:
Floating-point subtraction of nearly equal floating-point numbers causes severe loss of precision.
Algebraic reformulation guarantees numerical stability down to machine epsilon.

Assumptions & Input Data:
- a = 1.0, b = 10^4 (large drag term), c varies from 10^-2 down to 10^-14.
- Compare standard formula against stable formula and analytical limit c / (-b).
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Ensure outputs directory exists
os.makedirs("outputs", exist_ok=True)

print("=== Task 04 Modified: Aerodynamic Quadratic Cancellation ===")

a = 1.0
b = 10000.0  # large linear coefficient

# Demonstrate standard vs stable formulation across decaying perturbation terms c
c_values = np.logspace(-2, -14, 13)
direct_roots = []
stable_roots = []
relative_errors = []

for c in c_values:
    # Standard high-school formula (unstable for root closest to 0 when b > 0)
    disc = b**2 - 4 * a * c
    x1_direct = (-b + np.sqrt(disc)) / (2 * a)
    
    # Stable algebraic reformulation (Citardauq formula)
    x1_stable = (-2 * c) / (b + np.sqrt(disc))
    
    rel_err = abs(x1_direct - x1_stable) / abs(x1_stable) if x1_stable != 0 else 0
    direct_roots.append(x1_direct)
    stable_roots.append(x1_stable)
    relative_errors.append(rel_err)

print(f"{'Perturbation c':<16} {'Direct Root':<22} {'Stable Root':<22} {'Rel Error':<12}")
print("-" * 75)
for c, d, s, err in zip(c_values[::2], direct_roots[::2], stable_roots[::2], relative_errors[::2]):
    print(f"{c:<16.1e} {d:<22.14e} {s:<22.14e} {err:<12.2e}")

# Visualization of Error Explosion
plt.figure(figsize=(8, 4.8))
plt.loglog(c_values, [max(e, 1e-17) for e in relative_errors], 'ro-', linewidth=2, label='Direct Quadratic Formula Rel Error')
plt.axhline(1.0, color='black', linestyle='--', label='100% Catastrophic Error (Complete Precision Loss)')
plt.title("Task 04 Mod: Catastrophic Cancellation in Aerospace Quadratic Drag Formulation")
plt.xlabel("Perturbation Coefficient c ($b^2 / (4ac)$ increases $\\to$)")
plt.ylabel("Relative Error compared to Stable Formula")
plt.gca().invert_xaxis()
plt.grid(True, which="both", linestyle=':', alpha=0.6)
plt.legend()
plt.savefig("outputs/mod_task_04.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/mod_task_04.png")
