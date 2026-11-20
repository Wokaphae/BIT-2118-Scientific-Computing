"""
Task 18: Numerical Solution of ODEs Using SciPy
Original Implementation and Parameter Modification.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

# Ensure outputs directory exists
os.makedirs("outputs", exist_ok=True)

# ==========================================
# SECTION 1: ORIGINAL IMPLEMENTATION
# ==========================================
print("=== Task 18: Original Implementation ===")

# RC charging circuit:
# dV/dt = (Vs - V)/(R*C)
Vs = 5.0        # supply voltage (V)
R = 1000.0      # resistance (ohms)
C = 0.001       # capacitance (farads)
V0 = 0.0        # initial capacitor voltage

def rc_circuit(t, V):
    return [(Vs - V[0]) / (R * C)]

t_eval = np.linspace(0, 5, 200)

solution = solve_ivp(
    rc_circuit,
    (0, 5),
    [V0],
    t_eval=t_eval,
    rtol=1e-9,
    atol=1e-11
)

# Exact RC charging curve for validation
exact = Vs * (1 - np.exp(-solution.t / (R * C)))

print("Solver success:", solution.success)
print(f"Capacitor voltage at 5 s: {solution.y[0, -1]:.4f} V")
print(f"Maximum error against exact solution: {np.max(np.abs(solution.y[0] - exact)):.3e} V")

# ==========================================
# SECTION 2: PARAMETER MODIFICATION (Requirement C)
# ==========================================
print("\n=== Task 18: Parameter Modification (Capacitor Discharge & Tau Scaling) ===")
# Parameter change 1: Doubled resistance R=2500 ohms (Tau = 2.5s)
R_slow = 2500.0
def rc_slow(t, V):
    return [(Vs - V[0]) / (R_slow * C)]

sol_slow = solve_ivp(rc_slow, (0, 5), [0.0], t_eval=t_eval, rtol=1e-9, atol=1e-11)

# Parameter change 2: Discharging cycle (Vs=0V, V0=5.0V, R=1000 ohms)
def rc_discharge(t, V):
    return [(0.0 - V[0]) / (R * C)]

sol_discharge = solve_ivp(rc_discharge, (0, 5), [5.0], t_eval=t_eval, rtol=1e-9, atol=1e-11)

print(f"Modified (Slow R=2500) Voltage at 5 s: {sol_slow.y[0, -1]:.4f} V")
print(f"Discharge cycle Voltage at 5 s: {sol_discharge.y[0, -1]:.4f} V")

# Comparative Visualization
plt.figure(figsize=(9, 5))
plt.plot(solution.t, solution.y[0], 'b-', label='Charging: R=1kΩ ($\\tau=1.0$s)')
plt.plot(solution.t, exact, 'k--', alpha=0.6, label='Analytical Exact Charging')
plt.plot(sol_slow.t, sol_slow.y[0], 'g-', label='Charging: R=2.5kΩ ($\\tau=2.5$s)')
plt.plot(sol_discharge.t, sol_discharge.y[0], 'r-', label='Discharging: $V_0=5$V')
plt.axhline(Vs * (1 - np.exp(-1)), color='blue', linestyle=':', label='1 $\\tau$ Charging (63.2%)')
plt.xlabel("Time (s)")
plt.ylabel("Capacitor Voltage (V)")
plt.title("Task 18: SciPy solve_ivp Simulation of RC Circuit Transients")
plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)
plt.savefig("outputs/orig_task_18.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/orig_task_18.png")
