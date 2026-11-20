"""
Task 17 (Modified): Pharmacokinetic Plasma Drug Clearance via Euler's Method

Problem Statement:
In clinical pharmacology, a patient receives an intravenous bolus injection of an antibiotic.
The drug concentration C(t) in the blood plasma (mg/L) declines over time via first-order renal
and hepatic elimination governed by the ordinary differential equation:
    dC/dt = -k_e * C
where 'k_e' is the elimination rate constant (hr^-1). Starting from an initial peak therapeutic
concentration C0 = 120.0 mg/L, the medical team models the concentration over 24 hours. The
Euler forward numerical integration scheme:
    C_{i+1} = C_i + h * (-k_e * C_i)
is evaluated across step sizes (h = 1.0 hr vs h = 0.25 hr) and validated against the exact analytical
exponential decay curve:
    C_exact(t) = C0 * exp(-k_e * t).

Mathematical Concept:
Numerical Solution of Initial Value Problems via Forward Euler Discretization and Truncation
Error Quantification.

Assumptions & Input Data:
- Initial plasma concentration C0 = 120.0 mg/L.
- Elimination rate constant k_e = 0.18 hr^-1 (biological half-life t_1/2 = ln(2)/0.18 = 3.85 hours).
- Simulation horizon = 24.0 hours.
- Step sizes: h = 1.0 hour (coarse) and h = 0.25 hour (fine).
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Ensure outputs directory exists
os.makedirs("outputs", exist_ok=True)

print("=== Task 17 Modified: Pharmacokinetic Clearance Euler Simulation ===")

C0 = 120.0        # Initial plasma concentration (mg/L)
k_e = 0.18        # Elimination rate constant (hr^-1)
t_end = 24.0      # Simulation duration (hours)

def elimination_rate(C):
    return -k_e * C

# Euler simulation 1: Coarse step h = 1.0 hr
h1 = 1.0
t1 = np.arange(0, t_end + h1, h1)
C_euler1 = np.zeros_like(t1)
C_euler1[0] = C0
for i in range(len(t1) - 1):
    C_euler1[i + 1] = C_euler1[i] + h1 * elimination_rate(C_euler1[i])

# Euler simulation 2: Fine step h = 0.25 hr
h2 = 0.25
t2 = np.arange(0, t_end + h2, h2)
C_euler2 = np.zeros_like(t2)
C_euler2[0] = C0
for i in range(len(t2) - 1):
    C_euler2[i + 1] = C_euler2[i] + h2 * elimination_rate(C_euler2[i])

# Analytical exact solution
t_exact = np.linspace(0, t_end, 300)
C_exact_curve = C0 * np.exp(-k_e * t_exact)
C_exact_24h = C0 * np.exp(-k_e * t_end)

err1_final = abs(C_euler1[-1] - C_exact_24h)
err2_final = abs(C_euler2[-1] - C_exact_24h)

half_life = np.log(2.0) / k_e

print(f"Drug Elimination Half-Life: {half_life:.2f} hours")
print(f"Exact Plasma Concentration at 24h: {C_exact_24h:.4f} mg/L")
print(f"Euler (h=1.00h) at 24h:             {C_euler1[-1]:.4f} mg/L (Error: {err1_final:.4f} mg/L)")
print(f"Euler (h=0.25h) at 24h:             {C_euler2[-1]:.4f} mg/L (Error: {err2_final:.4f} mg/L)")
print(f"Error Reduction Ratio (h/4):        {err1_final / err2_final:.2f}x (Expected ~ 4.0x for O(h))")

# Visualization
plt.figure(figsize=(8, 5))
plt.plot(t_exact, C_exact_curve, 'k-', linewidth=2, label='Analytical Exact Decay $C(t)=C_0 e^{-k_e t}$')
plt.plot(t1, C_euler1, 'b-o', markersize=5, label=f'Euler h=1.00h (Err: {err1_final:.2f} mg/L)')
plt.plot(t2, C_euler2, 'r--s', markersize=3, alpha=0.7, label=f'Euler h=0.25h (Err: {err2_final:.2f} mg/L)')
plt.axhline(C0 * 0.5, color='gray', linestyle=':', label=f'Half-Life Baseline ({C0*0.5:.0f} mg/L)')
plt.axvline(half_life, color='gray', linestyle=':')
plt.title("Task 17 Mod: Antibiotic Pharmacokinetic Elimination via Forward Euler")
plt.xlabel("Time after Administration (Hours)")
plt.ylabel("Plasma Drug Concentration (mg/L)")
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.savefig("outputs/mod_task_17.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/mod_task_17.png")
