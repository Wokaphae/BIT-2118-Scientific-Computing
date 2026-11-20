"""
Task 07: Gaussian Elimination and LU Decomposition
Original Implementation and Parameter Modification.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import lu_factor, lu_solve

# Ensure outputs directory exists
os.makedirs("outputs", exist_ok=True)

# ==========================================
# SECTION 1: ORIGINAL IMPLEMENTATION
# ==========================================
print("=== Task 07: Original Implementation ===")

# The same coefficient matrix is reused for several measurement vectors.
A = np.array([
    [4.0, -1.0,  0.0],
    [-1.0, 4.0, -1.0],
    [0.0, -1.0,  3.0]
])

measurement_sets = [
    np.array([15.0, 10.0, 10.0]),
    np.array([16.0, 11.0,  9.0]),
    np.array([14.0, 12.0, 11.0])
]

# Factor A only once
lu, piv = lu_factor(A)

solutions = []
for i, b in enumerate(measurement_sets, start=1):
    x = lu_solve((lu, piv), b)
    residual = b - A @ x
    solutions.append(x)
    print(f"Measurement set {i}")
    print("Solution:", x)
    print("Residual norm:", np.linalg.norm(residual))
    print()

# Direct solution for comparison
print("Direct solution for first set:", np.linalg.solve(A, measurement_sets[0]))

# ==========================================
# SECTION 2: PARAMETER MODIFICATION (Requirement C)
# ==========================================
print("\n=== Task 07: Parameter Modification (Expanded Measurement Sets) ===")
# Testing expanded measurement vectors representing extreme load conditions
new_measurement_sets = [
    np.array([25.0, 18.0, 22.0]),
    np.array([5.0,  2.0,  4.0])
]

for j, b in enumerate(new_measurement_sets, start=4):
    x_new = lu_solve((lu, piv), b)
    res_new = b - A @ x_new
    solutions.append(x_new)
    print(f"Modified Measurement set {j}: b = {b}")
    print("  Solution x:", x_new)
    print("  Residual norm:", np.linalg.norm(res_new))

# Generate Visualization of State Variables across Sets
sol_array = np.array(solutions)  # shape (5, 3)
plt.figure(figsize=(8, 4.8))
sets = [f"Set {k}" for k in range(1, 6)]
plt.plot(sets, sol_array[:, 0], marker='o', label='Variable x1')
plt.plot(sets, sol_array[:, 1], marker='s', label='Variable x2')
plt.plot(sets, sol_array[:, 2], marker='^', label='Variable x3')
plt.axvline(2.5, color='gray', linestyle=':', label='Original vs Modified Boundary')
plt.title("Task 07: LU Decomposition Solutions across Repeated Right-Hand Vectors")
plt.xlabel("Measurement Vector Set")
plt.ylabel("Solution Vector Values")
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.savefig("outputs/orig_task_07.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/orig_task_07.png")
