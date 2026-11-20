"""
Task 06: Solution of Systems of Linear Equations
Original Implementation (with OCR syntax fixes) and Parameter Modification.
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
print("=== Task 06: Original Implementation ===")

# x = number of Type A servers
# y = number of Type B servers
#
# Type A uses 4 CPU units and 8 GB memory
# Type B uses 2 CPU units and 12 GB memory
# Total observed usage: 20 CPU units and 72 GB memory

A = np.array([
    [4.0, 2.0],
    [8.0, 12.0]
])

b = np.array([20.0, 72.0])

solution = np.linalg.solve(A, b)
# OCR FIX: original PDF text was 'residual = bA @ solution' -> 'residual = b - A @ solution'
residual = b - A @ solution

print(f"Type A servers: {solution[0]:.0f}")
print(f"Type B servers: {solution[1]:.0f}")
print("Verification A @ solution:", A @ solution)
print("Residual:", residual)
print("Residual norm:", np.linalg.norm(residual))

# ==========================================
# SECTION 2: PARAMETER MODIFICATION (Requirement C)
# ==========================================
print("\n=== Task 06: Parameter Modification ===")
# Scaled cluster demand: 52 CPU units and 168 GB memory
b_mod = np.array([52.0, 168.0])
solution_mod = np.linalg.solve(A, b_mod)
residual_mod = b_mod - A @ solution_mod

print(f"Modified Type A servers: {solution_mod[0]:.0f}")
print(f"Modified Type B servers: {solution_mod[1]:.0f}")
print("Modified Residual norm:", np.linalg.norm(residual_mod))

# Generate Comparative Visualization of Linear Constraints
x_vals = np.linspace(0, 15, 200)
# Eq 1: 4x + 2y = b1 => y = (b1 - 4x) / 2
# Eq 2: 8x + 12y = b2 => y = (b2 - 8x) / 12
y1_orig = (b[0] - 4.0 * x_vals) / 2.0
y2_orig = (b[1] - 8.0 * x_vals) / 12.0

y1_mod = (b_mod[0] - 4.0 * x_vals) / 2.0
y2_mod = (b_mod[1] - 8.0 * x_vals) / 12.0

plt.figure(figsize=(8, 6))
plt.plot(x_vals, y1_orig, 'b-', label='Orig CPU Constraint (4A + 2B = 20)')
plt.plot(x_vals, y2_orig, 'b--', label='Orig RAM Constraint (8A + 12B = 72)')
plt.plot(solution[0], solution[1], 'bo', markersize=8, label=f'Orig Solution ({solution[0]:.0f}, {solution[1]:.0f})')

plt.plot(x_vals, y1_mod, 'r-', label='Mod CPU Constraint (4A + 2B = 52)')
plt.plot(x_vals, y2_mod, 'r--', label='Mod RAM Constraint (8A + 12B = 168)')
plt.plot(solution_mod[0], solution_mod[1], 'ro', markersize=8, label=f'Mod Solution ({solution_mod[0]:.0f}, {solution_mod[1]:.0f})')

plt.xlim(0, 15)
plt.ylim(0, 15)
plt.title("Task 06: Geometric Intersection of Linear Server Constraints")
plt.xlabel("Number of Type A Servers")
plt.ylabel("Number of Type B Servers")
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.savefig("outputs/orig_task_06.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/orig_task_06.png")
