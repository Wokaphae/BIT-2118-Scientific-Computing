"""
Task 11 (Modified): Satellite Orbital Mechanics & Kepler's Equation via Newton-Raphson & Secant Methods

Problem Statement:
In aerospace flight dynamics and satellite orbit determination, a communications satellite orbits
Earth on a high-eccentricity Molniya elliptical orbit (eccentricity e = 0.72). To determine the
satellite's exact Cartesian position in space at time t, aerospace guidance computers must solve
Kepler's transcendental equation for the eccentric anomaly E (radians):
    M = E - e * sin(E)  =>  f(E) = E - e * sin(E) - M = 0
where 'M' is the mean anomaly calculated from elapsed flight time. Because Kepler's equation has
no closed-form algebraic inverse, iterative root finding is required. We evaluate Newton-Raphson
using the analytical derivative f'(E) = 1 - e * cos(E) versus the derivative-free Secant method.

Mathematical Concept:
Newton-Raphson quadratic convergence using analytical derivatives vs Secant superlinear convergence.

Assumptions & Input Data:
- Orbital eccentricity e = 0.72 (highly elliptical Molniya orbit).
- Mean anomaly M = 1.35 radians (~77.3 degrees after perigee passage).
- Initial guess E0 = M for Newton; E0 = M, E1 = M + 0.2 for Secant.
- Convergence tolerance xtol = 1e-12.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import root_scalar

# Ensure outputs directory exists
os.makedirs("outputs", exist_ok=True)

print("=== Task 11 Modified: Kepler's Equation Orbit Determination ===")

e = 0.72          # Eccentricity
M = 1.35          # Mean anomaly in radians

def kepler_residual(E):
    return E - e * np.sin(E) - M

def kepler_derivative(E):
    return 1.0 - e * np.cos(E)

# 1. Newton-Raphson Method
sol_newton = root_scalar(
    kepler_residual,
    fprime=kepler_derivative,
    x0=M,
    method="newton",
    xtol=1e-12
)

# 2. Secant Method
sol_secant = root_scalar(
    kepler_residual,
    x0=M,
    x1=M + 0.25,
    method="secant",
    xtol=1e-12
)

E_solution = sol_newton.root
# Calculate true anomaly nu from eccentric anomaly E:
# tan(nu / 2) = sqrt((1 + e) / (1 - e)) * tan(E / 2)
nu = 2.0 * np.arctan(np.sqrt((1 + e) / (1 - e)) * np.tan(E_solution / 2.0))

print(f"Mean Anomaly M:            {M:.4f} rad ({np.rad2deg(M):.2f}°)")
print(f"Newton-Raphson Root (E):   {sol_newton.root:.10f} rad ({np.rad2deg(sol_newton.root):.4f}°)")
print(f"Newton-Raphson Iterations: {sol_newton.iterations}")
print(f"Secant Root (E):           {sol_secant.root:.10f} rad ({np.rad2deg(sol_secant.root):.4f}°)")
print(f"Secant Iterations:         {sol_secant.iterations}")
print(f"True Anomaly (nu):         {nu:.6f} rad ({np.rad2deg(nu):.2f}°)")
print(f"Residual at Newton Root:   {kepler_residual(sol_newton.root):.3e}")

# Visualization: Kepler Function and Tangent Line
E_vals = np.linspace(0.5, 3.0, 300)
f_vals = kepler_residual(E_vals)

# Tangent line at initial guess E0 = M
tangent_line = kepler_residual(M) + kepler_derivative(M) * (E_vals - M)

plt.figure(figsize=(8, 4.8))
plt.plot(E_vals, f_vals, 'b-', linewidth=2, label='Kepler Residual $f(E) = E - e\\sin(E) - M$')
plt.plot(E_vals, tangent_line, 'g--', label=f'Newton 1st Tangent at $E_0={M:.2f}$')
plt.axhline(0, color='black', linestyle=':', linewidth=0.8)
plt.plot(sol_newton.root, 0, 'ro', markersize=8, label=f'Eccentric Anomaly Root $E^*={sol_newton.root:.4f}$ rad')
plt.plot(M, kepler_residual(M), 'ks', label=f'Initial Guess $E_0=M$')
plt.title("Task 11 Mod: Satellite Orbital Position via Kepler Equation Root Finding")
plt.xlabel("Eccentric Anomaly E (radians)")
plt.ylabel("Residual Value")
plt.ylim(-1.5, 1.5)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.savefig("outputs/mod_task_11.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/mod_task_11.png")
