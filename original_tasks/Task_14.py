"""
Task 14: Curve Fitting and Approximation
Original Implementation and Parameter Modification.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Ensure outputs directory exists
os.makedirs("outputs", exist_ok=True)

# ==========================================
# SECTION 1: ORIGINAL IMPLEMENTATION
# ==========================================
print("=== Task 14: Original Implementation ===")

# Concurrent users and measured server response time (milliseconds)
users = np.array([50, 100, 150, 200, 250, 300, 350], dtype=float)
response_ms = np.array([82, 95, 115, 145, 185, 238, 305], dtype=float)

# A simple quadratic model for increasing delay
def model(x, a, b, c):
    return a * x**2 + b * x + c

parameters, covariance = curve_fit(model, users, response_ms)
a, b, c = parameters

predicted = model(users, a, b, c)
rmse = np.sqrt(np.mean((response_ms - predicted)**2))

print(f"Fitted model: y = {a:.6f}x^2 + {b:.4f}x + {c:.2f}")
print(f"RMSE: {rmse:.2f} ms")
print(f"Predicted response at 400 users: {model(400, a, b, c):.2f} ms")

# ==========================================
# SECTION 2: PARAMETER MODIFICATION (Requirement C)
# ==========================================
print("\n=== Task 14: Parameter Modification (Exponential Fit Comparison) ===")
# Hypothesize an exponential queueing saturation model: y = a0 * exp(b0 * x) + c0
def exp_model(x, a0, b0, c0):
    return a0 * np.exp(b0 * x) + c0

p0 = [10.0, 0.005, 70.0]
exp_params, exp_cov = curve_fit(exp_model, users, response_ms, p0=p0, maxfev=10000)
a_exp, b_exp, c_exp = exp_params

exp_predicted = exp_model(users, a_exp, b_exp, c_exp)
exp_rmse = np.sqrt(np.mean((response_ms - exp_predicted)**2))

print(f"Fitted Exponential Model: y = {a_exp:.4f} * exp({b_exp:.6f} * x) + {c_exp:.2f}")
print(f"Exponential RMSE: {exp_rmse:.2f} ms (Quadratic RMSE: {rmse:.2f} ms)")
print(f"Exponential prediction at 400 users: {exp_model(400, a_exp, b_exp, c_exp):.2f} ms")
print(f"Exponential prediction at 500 users: {exp_model(500, a_exp, b_exp, c_exp):.2f} ms")

# Comparative Visualization
x_plot = np.linspace(users.min(), 500, 300)
plt.figure(figsize=(9, 5))
plt.scatter(users, response_ms, color='black', s=50, zorder=5, label="Benchmark Measurements")
plt.plot(x_plot, model(x_plot, a, b, c), 'b-', label=f"Quadratic Model (RMSE={rmse:.2f} ms)")
plt.plot(x_plot, exp_model(x_plot, a_exp, b_exp, c_exp), 'r--', label=f"Exponential Model (RMSE={exp_rmse:.2f} ms)")
plt.axvline(400, color='gray', linestyle=':', label='Extrapolation Boundary (400 users)')
plt.xlabel("Concurrent users")
plt.ylabel("Response time (ms)")
plt.title("Task 14: Server Response Time Nonlinear Regression & Extrapolation")
plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)
plt.savefig("outputs/orig_task_14.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/orig_task_14.png")
