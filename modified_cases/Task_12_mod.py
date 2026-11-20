"""
Task 12 (Modified): 2-Link Articulated Robotic Manipulator Inverse Kinematics

Problem Statement:
In industrial robotic automation, a 2-degree-of-freedom (2-DOF) planar articulated arm operates
in a manufacturing cell. The arm consists of link 1 of length L1 = 1.2 m and link 2 of length
L2 = 0.9 m. To pick up a component at target spatial coordinate (X, Y) = (1.30, 0.85) meters,
the kinematic controller must determine the two joint angles (theta_1, theta_2) by solving the
coupled nonlinear kinematic system:
    f1(theta_1, theta_2) = L1 * cos(theta_1) + L2 * cos(theta_1 + theta_2) - X = 0
    f2(theta_1, theta_2) = L1 * sin(theta_1) + L2 * sin(theta_1 + theta_2) - Y = 0
Because the system exhibits two distinct physical postures (elbow-up and elbow-down configurations),
scipy.optimize.root is deployed from different initial guesses to converge to both valid solutions.

Mathematical Concept:
Multidimensional Nonlinear Equation Systems: Vector root finding (scipy.optimize.root)
using Powell's hybrid method / MINPACK root algorithms.

Assumptions & Input Data:
- Link lengths: L1 = 1.2 m, L2 = 0.9 m.
- Target Cartesian location: X = 1.30 m, Y = 0.85 m (within reach: sqrt(X^2+Y^2) = 1.55m < 2.1m).
- Initial guess 1 (Elbow-down): [0.2, 0.8] radians.
- Initial guess 2 (Elbow-up):   [0.9, -0.8] radians.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import root

# Ensure outputs directory exists
os.makedirs("outputs", exist_ok=True)

print("=== Task 12 Modified: 2-DOF Robot Arm Inverse Kinematics ===")

L1 = 1.20   # Link 1 length (m)
L2 = 0.90   # Link 2 length (m)
X_target = 1.30
Y_target = 0.85

def forward_kinematics(theta):
    t1, t2 = theta
    x = L1 * np.cos(t1) + L2 * np.cos(t1 + t2)
    y = L1 * np.sin(t1) + L2 * np.sin(t1 + t2)
    return x, y

def kinematics_residuals(theta):
    x, y = forward_kinematics(theta)
    return [x - X_target, y - Y_target]

# Search for both elbow configurations
guesses = {
    "Elbow Down": np.array([0.2, 0.8]),
    "Elbow Up":   np.array([0.9, -0.8])
}

solutions = {}
for name, guess in guesses.items():
    sol = root(kinematics_residuals, guess, method='hybr')
    t1, t2 = sol.x
    solutions[name] = (t1, t2)
    print(f"\nConfiguration: {name}")
    print(f"  Initial Guess: {guess} rad")
    print(f"  Solved Theta 1: {t1:.4f} rad ({np.rad2deg(t1):.2f}°)")
    print(f"  Solved Theta 2: {t2:.4f} rad ({np.rad2deg(t2):.2f}°)")
    x_achieved, y_achieved = forward_kinematics((t1, t2))
    print(f"  Achieved End-Effector: ({x_achieved:.4f}, {y_achieved:.4f}) m")
    print(f"  Residual Norm: {np.linalg.norm(sol.fun):.3e} m")
    print(f"  Convergence Status: {sol.success}")

# Visualization of both arm postures reaching the target
plt.figure(figsize=(7, 7))

# Draw reachable workspace boundary
phi = np.linspace(0, 2*np.pi, 200)
plt.plot((L1 + L2)*np.cos(phi), (L1 + L2)*np.sin(phi), 'k:', alpha=0.4, label='Workspace Reach (2.1m)')

colors = {'Elbow Down': 'blue', 'Elbow Up': 'red'}
for name, (t1, t2) in solutions.items():
    c = colors[name]
    # Joint positions
    p0 = np.array([0.0, 0.0])
    p1 = np.array([L1 * np.cos(t1), L1 * np.sin(t1)])
    p2 = np.array([p1[0] + L2 * np.cos(t1 + t2), p1[1] + L2 * np.sin(t1 + t2)])
    
    plt.plot([p0[0], p1[0], p2[0]], [p0[1], p1[1], p2[1]], color=c, marker='o', linewidth=3, label=f'{name} Posture')

# Target component
plt.plot(X_target, Y_target, 'g*', markersize=14, label=f'Target ({X_target}, {Y_target})m')
plt.plot(0, 0, 'ks', markersize=10, label='Base Joint (0,0)')

plt.xlim(-0.5, 2.3)
plt.ylim(-0.5, 2.3)
plt.gca().set_aspect('equal')
plt.title("Task 12 Mod: Robot Inverse Kinematics Dual Elbow Postures")
plt.xlabel("X Coordinate (m)")
plt.ylabel("Y Coordinate (m)")
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc='upper right')
plt.savefig("outputs/mod_task_12.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/mod_task_12.png")
