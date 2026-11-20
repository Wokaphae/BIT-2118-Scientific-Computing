"""
Task 08 (Modified): Groundwater Contaminant Seepage Dispersion via Iterative Linear Solvers

Problem Statement:
An environmental engineering team models the 1D steady-state dispersion of a chemical solvent
(trichloroethylene) leaching through a permeable underground barrier towards a drinking water aquifer.
The governing advection-diffusion transport equation is discretized across 6 internal spatial sampling
cells between the contaminant source (upstream boundary = 50.0 mg/L) and the extraction trench
(downstream boundary = 2.0 mg/L). Due to sparse structure and large scale in multi-dimensional extensions,
iterative linear algebraic solvers (Jacobi vs Gauss-Seidel) are evaluated to observe convergence
rates under strict environmental tolerance thresholds (tol = 1e-8).

Mathematical Concept:
Iterative solution of diagonally dominant linear systems Ax = b using Jacobi and Gauss-Seidel algorithms,
tracking infinity-norm convergence error history ||x_{k+1} - x_k||_inf.

Assumptions & Input Data:
- 6 interior grid cells with coupled tridiagonal Peclet-dispersion coefficients.
- Diagonally dominant matrix A (2.4 on diagonal, -0.7 on sub-diagonal, -0.5 on super-diagonal).
- Dirichlet boundaries: upstream C_0 = 50.0 mg/L, downstream C_7 = 2.0 mg/L.
- Convergence tolerance = 1e-8, max iterations = 500.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Ensure outputs directory exists
os.makedirs("outputs", exist_ok=True)

print("=== Task 08 Modified: Aquifer Contaminant Dispersion Analysis ===")

# 6 interior nodes with Peclet advection asymmetry
A = np.array([
    [ 2.4, -0.5,  0.0,  0.0,  0.0,  0.0],
    [-0.7,  2.4, -0.5,  0.0,  0.0,  0.0],
    [ 0.0, -0.7,  2.4, -0.5,  0.0,  0.0],
    [ 0.0,  0.0, -0.7,  2.4, -0.5,  0.0],
    [ 0.0,  0.0,  0.0, -0.7,  2.4, -0.5],
    [ 0.0,  0.0,  0.0,  0.0, -0.7,  2.4]
])

# Boundary vector: Upstream source C0 = 50 mg/L enters node 1 (0.7 * 50 = 35.0)
# Downstream extraction C7 = 2.0 mg/L influences node 6 (0.5 * 2.0 = 1.0)
b = np.array([35.0, 0.0, 0.0, 0.0, 0.0, 1.0])

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

c_jacobi, err_jacobi = jacobi(A, b)
c_gs, err_gs = gauss_seidel(A, b)
c_exact = np.linalg.solve(A, b)

print(f"Jacobi Iterations:       {len(err_jacobi)}")
print(f"Gauss-Seidel Iterations: {len(err_gs)}")
print("Jacobi Concentrations (mg/L):      ", np.round(c_jacobi, 4))
print("Gauss-Seidel Concentrations (mg/L):", np.round(c_gs, 4))
print("Direct Analytical Solution (mg/L): ", np.round(c_exact, 4))

# Visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8))

# Subplot 1: Convergence profile
ax1.semilogy(err_jacobi, 'b-', linewidth=1.8, label=f'Jacobi ({len(err_jacobi)} iters)')
ax1.semilogy(err_gs, 'r--', linewidth=1.8, label=f'Gauss-Seidel ({len(err_gs)} iters)')
ax1.axhline(1e-8, color='black', linestyle=':', label='Target Tolerance (1e-8)')
ax1.set_xlabel("Iteration Step")
ax1.set_ylabel("Infinity-Norm Error $\\|x_{k+1}-x_k\\|_\\infty$")
ax1.set_title("Iterative Error Decay Rate")
ax1.grid(True, which="both", linestyle=':', alpha=0.6)
ax1.legend()

# Subplot 2: Physical spatial contaminant profile
grid_x = np.arange(1, 7)
ax2.plot(grid_x, c_exact, 'g-o', linewidth=2, label='Steady-State Concentration')
ax2.set_xlabel("Aquifer Barrier Grid Section (1 to 6)")
ax2.set_ylabel("Contaminant Concentration (mg/L)")
ax2.set_title("Physical Contaminant Plume Gradient")
ax2.grid(True, linestyle=':', alpha=0.6)
ax2.legend()

plt.tight_layout()
plt.savefig("outputs/mod_task_08.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/mod_task_08.png")
