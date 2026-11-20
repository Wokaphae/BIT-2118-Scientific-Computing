"""
Task 07 (Modified): Multi-Story Building Lateral Drift under Dynamic Wind Storm Cases via LU Decomposition

Problem Statement:
In structural earthquake and wind engineering, a 4-story commercial building frame is modeled
by its lateral structural stiffness matrix K (kN/m). During a severe typhoon, meteorological sensors
record fluctuating lateral wind load vectors F (kN) at each floor level every hour. Solving K * d = F
from scratch for every recorded wind profile via Gaussian elimination is computationally redundant.
By factoring K into its LU decomposition once, subsequent lateral floor displacement responses d
can be solved in O(n^2) back-substitution operations for each load case.

Mathematical Concept:
LU Decomposition with partial pivoting (scipy.linalg.lu_factor and lu_solve) for repeated efficient
linear system solutions.

Assumptions & Input Data:
- 4-story lateral shear frame stiffness matrix K (tridiagonal structure in kN/m).
- 4 dynamic wind load test vectors corresponding to:
    F1: Moderate Sea Breeze [15, 25, 30, 35] kN
    F2: Gale Force Winds   [30, 45, 60, 75] kN
    F3: Severe Storm Surge [50, 75, 95, 120] kN
    F4: Peak Typhoon Gust  [70, 110, 140, 180] kN
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import lu_factor, lu_solve

# Ensure outputs directory exists
os.makedirs("outputs", exist_ok=True)

print("=== Task 07 Modified: Structural Lateral Drift Analysis via LU ===")

# 4-story building lateral stiffness matrix K (kN/m)
K = np.array([
    [ 1200.0, -500.0,    0.0,    0.0],
    [ -500.0, 1000.0, -400.0,    0.0],
    [    0.0, -400.0,  800.0, -300.0],
    [    0.0,    0.0, -300.0,  500.0]
])

wind_load_cases = {
    "Moderate Breeze": np.array([15.0, 25.0, 30.0, 35.0]),
    "Gale Force":     np.array([30.0, 45.0, 60.0, 75.0]),
    "Severe Storm":   np.array([50.0, 75.0, 95.0, 120.0]),
    "Peak Typhoon":   np.array([70.0, 110.0, 140.0, 180.0])
}

# Factorize K once
lu, piv = lu_factor(K)

displacements = {}
print("LU Factorization successful. Solving dynamic load cases:")
for case_name, F in wind_load_cases.items():
    d = lu_solve((lu, piv), F)
    residual = F - K @ d
    displacements[case_name] = d
    print(f"\nLoad Case: {case_name}")
    print("  Lateral Force F (kN):", F)
    print(f"  Floor Deflections (mm): {d * 1000.0}")  # convert m to mm
    print(f"  Max Roof Drift: {d[-1] * 1000.0:.2f} mm")
    print(f"  Residual Norm: {np.linalg.norm(residual):.3e} kN")

# Visualization: Story drift profile
floors = [0, 1, 2, 3, 4]  # Ground + 4 floors

plt.figure(figsize=(7, 6))
for case_name, d in displacements.items():
    drift_profile = np.insert(d * 1000.0, 0, 0.0)  # 0 at ground
    plt.plot(drift_profile, floors, marker='o', linewidth=2, label=case_name)

plt.axvline(25.0, color='red', linestyle='--', label='Serviceability Limit (25 mm)')
plt.title("Task 07 Mod: Building Lateral Displacement Profiles under Wind Scenarios")
plt.xlabel("Lateral Deflection (mm)")
plt.ylabel("Floor Level (0 = Foundation)")
plt.yticks(floors, ["Ground", "Floor 1", "Floor 2", "Floor 3", "Roof"])
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.savefig("outputs/mod_task_07.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/mod_task_07.png")
