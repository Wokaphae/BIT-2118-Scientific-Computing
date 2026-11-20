"""
Task 06 (Modified): Electrical Microgrid Nodal Analysis via Systems of Linear Equations

Problem Statement:
A smart industrial microgrid consists of three electrical bus nodes interconnected by transmission
conductances. Independent current injections from a solar inverter, a wind turbine, and a grid intertie
are delivered to nodes 1, 2, and 3. In accordance with Kirchhoff's Current Law (KCL), the sum of currents
entering each node equals zero, resulting in the matrix equation:
    G * v = i
where 'G' is the 3x3 nodal conductance matrix (Siemens), 'v' is the vector of unknown node voltages (Volts),
and 'i' is the vector of net injected nodal currents (Amperes). The system must be solved for the operating
bus voltages and verified against the nodal residual norm.

Mathematical Concept:
Solution of Systems of Linear Equations using Gaussian elimination / LU-based solver (np.linalg.solve)
and backward error residual norm calculation ||i - G*v||.

Assumptions & Input Data:
- Bus 1: connected to Node 2 with conductance G12 = 0.5 S, and Node 3 with G13 = 0.2 S.
- Bus 2: connected to Node 3 with conductance G23 = 0.4 S.
- Shunt conductances to ground: G10 = 0.1 S, G20 = 0.1 S, G30 = 0.2 S.
- Net Current Injections: i1 = 25.0 A, i2 = 15.0 A, i3 = -10.0 A (load sink).
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Ensure outputs directory exists
os.makedirs("outputs", exist_ok=True)

print("=== Task 06 Modified: Electrical Bus Nodal Voltage Analysis ===")

# Build nodal conductance matrix G:
# G[k, k] = sum of conductances connected to node k
# G[j, k] = -conductance between node j and node k
G = np.array([
    [0.1 + 0.5 + 0.2, -0.5,           -0.2          ],
    [-0.5,            0.1 + 0.5 + 0.4, -0.4          ],
    [-0.2,           -0.4,             0.2 + 0.2 + 0.4]
])

# Current injection vector (Amperes)
i_inj = np.array([25.0, 15.0, -10.0])

# Solve for node voltages v
v_solution = np.linalg.solve(G, i_inj)
residual = i_inj - G @ v_solution
res_norm = np.linalg.norm(residual)

print("Nodal Conductance Matrix G (Siemens):\n", G)
print("Injected Current Vector i (Amperes):", i_inj)
print(f"Solved Node Voltage V1: {v_solution[0]:.2f} V")
print(f"Solved Node Voltage V2: {v_solution[1]:.2f} V")
print(f"Solved Node Voltage V3: {v_solution[2]:.2f} V")
print("Verification (G @ v):", G @ v_solution)
print("Residual Vector:", residual)
print(f"Residual L2 Norm: {res_norm:.3e} A")

# Visualization
nodes = ["Bus 1 (Solar)", "Bus 2 (Wind)", "Bus 3 (Load Sink)"]
colors = ['#ff7f0e', '#2ca02c', '#1f77b4']

plt.figure(figsize=(7, 4.8))
bars = plt.bar(nodes, v_solution, color=colors, width=0.5, edgecolor='black')
for bar, val in zip(bars, v_solution):
    plt.text(bar.get_x() + bar.get_width()/2.0, val + 1.0, f"{val:.1f} V", ha='center', fontweight='bold')

plt.title("Task 06 Mod: Steady-State Electrical Microgrid Bus Voltages (KCL Solution)")
plt.ylabel("Nodal Voltage (Volts)")
plt.ylim(0, max(v_solution) * 1.25)
plt.grid(axis='y', linestyle=':', alpha=0.6)
plt.savefig("outputs/mod_task_06.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/mod_task_06.png")
