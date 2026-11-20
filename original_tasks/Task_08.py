"""
Task 08: Iterative Methods for Linear Systems
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
print("=== Task 08: Original Implementation ===")

# Simplified steady-state temperature model for five interior grid points.
# Diagonal dominance makes Jacobi and Gauss-Seidel converge.
A = np.array([
    [ 2., -1.,  0.,  0.,  0.],
    [-1.,  2., -1.,  0.,  0.],
    [ 0., -1.,  2., -1.,  0.],
    [ 0.,  0., -1.,  2., -1.],
    [ 0.,  0.,  0., -1.,  2.]
])

# Boundary influence: left boundary = 100 C, right boundary = 20 C
b = np.array([100., 0., 0., 0., 20.])

def jacobi(A, b, tol=1e-8, max_iter=500):
    D = np.diag(A)
    R = A - np.diagflat(D)
    x = np.zeros_like(b)
    errors = []
    for _ in range(max_iter):
        x_new = (b - R @ x) / D
        error = np.linalg.norm(x_new - x, ord=np.inf)
        errors.append(error)
        if error < tol:
            return x_new, errors
        x = x_new
    return x, errors

def gauss_seidel(A, b, tol=1e-8, max_iter=500):
    x = np.zeros_like(b)
    errors = []
    for _ in range(max_iter):
        old = x.copy()
        for i in range(len(b)):
            x[i] = (
                b[i]
                - A[i, :i] @ x[:i]
                - A[i, i+1:] @ old[i+1:]
            ) / A[i, i]
        error = np.linalg.norm(x - old, ord=np.inf)
        errors.append(error)
        if error < tol:
            return x, errors
    return x, errors

x_j, err_j = jacobi(A, b)
x_gs, err_gs = gauss_seidel(A, b)
x_exact = np.linalg.solve(A, b)

print("Jacobi temperatures:", x_j)
print(f"Jacobi iterations: {len(err_j)}")
print("Gauss-Seidel temperatures:", x_gs)
print(f"Gauss-Seidel iterations: {len(err_gs)}")
print("Direct solution:", x_exact)

# ==========================================
# SECTION 2: PARAMETER MODIFICATION (Requirement C)
# ==========================================
print("\n=== Task 08: Parameter Modification ===")
# Stricter tolerance (1e-12) and modified boundary condition: left=150C, right=80C
b_mod = np.array([150., 0., 0., 0., 80.])
x_j_mod, err_j_mod = jacobi(A, b_mod, tol=1e-12)
x_gs_mod, err_gs_mod = gauss_seidel(A, b_mod, tol=1e-12)
x_exact_mod = np.linalg.solve(A, b_mod)

print("Modified Jacobi iterations (tol=1e-12):", len(err_j_mod))
print("Modified Gauss-Seidel iterations (tol=1e-12):", len(err_gs_mod))
print("Modified Jacobi temperatures:", x_j_mod)
print("Modified Exact temperatures:", x_exact_mod)

# Comparative Visualization
plt.figure(figsize=(9, 5))
plt.semilogy(err_j, 'b-', label=f"Jacobi (tol=1e-8, iters={len(err_j)})")
plt.semilogy(err_gs, 'b--', label=f"Gauss-Seidel (tol=1e-8, iters={len(err_gs)})")
plt.semilogy(err_j_mod, 'r-', alpha=0.7, label=f"Jacobi (tol=1e-12, iters={len(err_j_mod)})")
plt.semilogy(err_gs_mod, 'r--', alpha=0.7, label=f"Gauss-Seidel (tol=1e-12, iters={len(err_gs_mod)})")
plt.xlabel("Iteration")
plt.ylabel("Maximum change ($\\|x_{k+1}-x_k\\|_\\infty$)")
plt.title("Task 08: Convergence Rates of Jacobi vs Gauss-Seidel Methods")
plt.legend()
plt.grid(True, which="both", linestyle=':', alpha=0.6)
plt.savefig("outputs/orig_task_08.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/orig_task_08.png")
