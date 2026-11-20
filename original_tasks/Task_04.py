"""
Task 04: Floating-Point Arithmetic and Numerical Errors
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
print("=== Task 04: Original Implementation ===")

# Floating-point comparison
calculated = 0.1 + 0.2
expected = 0.3
print("0.1 + 0.2 =", calculated)
print("Exact comparison:", calculated == expected)
print("Tolerance-based comparison:", np.isclose(calculated, expected))

# Absolute and relative error
true_value = np.sqrt(2)
approx_value = 1.414
absolute_error = abs(true_value - approx_value)
relative_error = absolute_error / abs(true_value)
print(f"Absolute error: {absolute_error:.8f}")
print(f"Relative error: {relative_error:.8%}")

# Numerically unstable vs stable formulation
for x in [1e-4, 1e-8, 1e-12]:
    direct = (np.sqrt(1 + x) - 1) / x
    stable = 1 / (np.sqrt(1 + x) + 1)
    print(f"x={x:.0e}: direct={direct:.12f}, stable={stable:.12f}")

# ==========================================
# SECTION 2: PARAMETER MODIFICATION (Requirement C)
# ==========================================
print("\n=== Task 04: Parameter Modification (Sub-epsilon Analysis) ===")
# Extending x to machine precision limits and sub-epsilon values
test_x = np.logspace(-1, -18, 18)
direct_vals = []
stable_vals = []
direct_errs = []

for x in test_x:
    d = (np.sqrt(1 + x) - 1) / x
    s = 1.0 / (np.sqrt(1 + x) + 1.0)
    direct_vals.append(d)
    stable_vals.append(s)
    err = abs(d - s) / s
    direct_errs.append(err)

print("Severe cancellation regime:")
for x, d, s, err in zip(test_x[10:], direct_vals[10:], stable_vals[10:], direct_errs[10:]):
    print(f"x={x:.1e}: direct={d:.14f}, stable={s:.14f}, rel_err={err:.2e}")

# Generate Comparative Visualization
plt.figure(figsize=(8, 4.5))
plt.loglog(test_x, [max(e, 1e-17) for e in direct_errs], marker='o', color='#d62728', label='Direct Formula Rel Error')
plt.axvline(np.finfo(float).eps, color='black', linestyle='--', label=f'Float64 Epsilon ({np.finfo(float).eps:.1e})')
plt.title("Task 04: Loss of Significance & Catastrophic Cancellation")
plt.xlabel("Perturbation magnitude x")
plt.ylabel("Relative Error compared to Stable Formula")
plt.grid(True, which="both", ls=":", alpha=0.6)
plt.legend()
plt.savefig("outputs/orig_task_04.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/orig_task_04.png")
