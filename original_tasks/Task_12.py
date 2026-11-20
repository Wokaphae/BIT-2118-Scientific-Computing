"""
Task 12: Polynomial and Nonlinear Equation Solving
Original Implementation and Parameter Modification.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import root

# Ensure outputs directory exists
os.makedirs("outputs", exist_ok=True)

# ==========================================
# SECTION 1: ORIGINAL IMPLEMENTATION
# ==========================================
print("=== Task 12: Original Implementation ===")

# Find intersections of:
# Circle: x^2 + y^2 = 4
# Parabola: y = x^2 - 1

def equations(z):
    x, y = z
    return [
        x**2 + y**2 - 4,
        y - (x**2 - 1)
    ]

orig_solutions = []
for guess in ([1.0, 1.0], [-1.0, 1.0]):
    solution = root(equations, guess)
    orig_solutions.append(solution.x)
    print("Initial guess:", guess)
    print("Intersection:", solution.x)
    print("Residuals:", equations(solution.x))
    print("Converged:", solution.success)
    print()

# ==========================================
# SECTION 2: PARAMETER MODIFICATION (Requirement C)
# ==========================================
print("\n=== Task 12: Parameter Modification ===")
# Scaled geometry: Circle of radius R=sqrt(7) (r^2=7) and shifted parabola y = 0.5*x^2 - 2
def equations_mod(z):
    x, y = z
    return [
        x**2 + y**2 - 7.0,
        y - (0.5 * x**2 - 2.0)
    ]

mod_solutions = []
for guess in ([2.0, 1.0], [-2.0, 1.0]):
    solution_mod = root(equations_mod, guess)
    mod_solutions.append(solution_mod.x)
    print("Modified Initial guess:", guess)
    print("Modified Intersection:", solution_mod.x)
    print("Modified Residuals:", equations_mod(solution_mod.x))
    print("Converged:", solution_mod.success)
    print()

# Comparative Visualization
theta = np.linspace(0, 2*np.pi, 200)
x_parab = np.linspace(-3, 3, 300)

plt.figure(figsize=(7, 7))
# Original curves
plt.plot(2 * np.cos(theta), 2 * np.sin(theta), 'b-', label='Circle ($x^2 + y^2 = 4$)')
plt.plot(x_parab, x_parab**2 - 1, 'b--', label='Parabola ($y = x^2 - 1$)')
for pt in orig_solutions:
    plt.plot(pt[0], pt[1], 'bo', markersize=8, label=f'Orig Intersect ({pt[0]:.2f}, {pt[1]:.2f})')

# Modified curves
plt.plot(np.sqrt(7) * np.cos(theta), np.sqrt(7) * np.sin(theta), 'r-', label='Mod Circle ($x^2 + y^2 = 7$)')
plt.plot(x_parab, 0.5 * x_parab**2 - 2.0, 'r--', label='Mod Parabola ($y = 0.5x^2 - 2$)')
for pt in mod_solutions:
    plt.plot(pt[0], pt[1], 'rs', markersize=8, label=f'Mod Intersect ({pt[0]:.2f}, {pt[1]:.2f})')

plt.xlim(-3.5, 3.5)
plt.ylim(-3.5, 3.5)
plt.gca().set_aspect('equal')
plt.title("Task 12: Nonlinear System Solutions via Multidimensional Root Finding")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True, linestyle=':', alpha=0.6)
# Group legend to avoid duplicate labels
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys(), loc='upper right', fontsize=8)
plt.savefig("outputs/orig_task_12.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/orig_task_12.png")
