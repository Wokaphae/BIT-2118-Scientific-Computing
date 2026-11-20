"""
Task 19: Numerical Optimization
Original Implementation and Parameter Modification.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize

# Ensure outputs directory exists
os.makedirs("outputs", exist_ok=True)

# ==========================================
# SECTION 1: ORIGINAL IMPLEMENTATION
# ==========================================
print("=== Task 19: Original Implementation ===")

# x = number/capacity units of Type A server
# y = number/capacity units of Type B server
#
# Cost per unit: A = 12, B = 18
# Capacity per unit: A = 100, B = 170
# Required total capacity: at least 1000

def cost(z):
    x, y = z
    return 12 * x + 18 * y

def capacity_constraint(z):
    x, y = z
    return 100 * x + 170 * y - 1000

constraints = {
    "type": "ineq",
    "fun": capacity_constraint
}

bounds = [(0, None), (0, None)]

solution = minimize(
    cost,
    x0=[5, 3],
    method="SLSQP",
    bounds=bounds,
    constraints=constraints
)

x, y = solution.x

print("Optimization success:", solution.success)
print(f"Type A allocation: {x:.3f}")
print(f"Type B allocation: {y:.3f}")
print(f"Total capacity: {100 * x + 170 * y:.2f}")
print(f"Minimum planning cost: {solution.fun:.2f}")

# If whole servers are required, test nearby integer combinations.
best_integer = None
for a in range(0, 20):
    for b in range(0, 20):
        capacity = 100 * a + 170 * b
        if capacity >= 1000:
            total_cost = 12 * a + 18 * b
            if best_integer is None or total_cost < best_integer[0]:
                best_integer = (total_cost, a, b, capacity)

print("Best nearby integer solution:", best_integer)

# ==========================================
# SECTION 2: PARAMETER MODIFICATION (Requirement C)
# ==========================================
print("\n=== Task 19: Parameter Modification (Capacity Expansion & Price Change) ===")
# Expanded capacity target = 2500 units; updated server costs: A = $14, B = $26
def cost_mod(z):
    x, y = z
    return 14 * x + 26 * y

def capacity_constraint_mod(z):
    x, y = z
    return 100 * x + 170 * y - 2500

solution_mod = minimize(
    cost_mod,
    x0=[10, 10],
    method="SLSQP",
    bounds=bounds,
    constraints={"type": "ineq", "fun": capacity_constraint_mod}
)

x_m, y_m = solution_mod.x
print(f"Modified Optimal Type A: {x_m:.3f}")
print(f"Modified Optimal Type B: {y_m:.3f}")
print(f"Modified Minimum Planning Cost: ${solution_mod.fun:.2f}")

best_int_mod = None
for a in range(0, 35):
    for b in range(0, 35):
        cap = 100 * a + 170 * b
        if cap >= 2500:
            c = 14 * a + 26 * b
            if best_int_mod is None or c < best_int_mod[0]:
                best_int_mod = (c, a, b, cap)
print("Modified Best Integer Solution:", best_int_mod)

# Comparative Visualization: Feasible Region & Optimal Points
x_grid = np.linspace(0, 15, 200)
# Capacity boundary: 100x + 170y = 1000 => y = (1000 - 100x) / 170
y_bound = np.maximum(0, (1000 - 100 * x_grid) / 170)

plt.figure(figsize=(8, 6))
plt.plot(x_grid, y_bound, 'k-', label='Capacity Boundary ($100A + 170B = 1000$)')
plt.fill_between(x_grid, y_bound, 15, color='green', alpha=0.15, label='Feasible Region')

plt.plot(x, y, 'ro', markersize=9, label=f'Continuous Optimum ({x:.2f}, {y:.2f})')
plt.plot(best_integer[1], best_integer[2], 'bs', markersize=9, label=f'Integer Optimum ({best_integer[1]}, {best_integer[2]})')

plt.xlim(0, 15)
plt.ylim(0, 10)
plt.xlabel("Type A Servers ($12/unit, 100 cap)")
plt.ylabel("Type B Servers ($18/unit, 170 cap)")
plt.title("Task 19: Constrained Linear Programming & Integer Optimization")
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.savefig("outputs/orig_task_19.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/orig_task_19.png")
