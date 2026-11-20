"""
Task 05 (Modified): Autonomous Mobile Robot LiDAR Coordinate Transformation

Problem Statement:
An autonomous mobile warehouse robot (AGV) detects obstacles in its local body frame (x_b, y_b)
using an on-board planar LiDAR sensor. When the AGV navigates through a warehouse, its pose
estimation system tracks its orientation theta = 35 degrees and a sensor scaling factor due to
acoustic/lens calibration. The perception pipeline must apply affine matrix transformation
to project local obstacle boundaries into the static global factory coordinate frame (X_g, Y_g).

Mathematical Concept:
Matrix Algebra: Composite affine transformation via matrix multiplication (rotation matrix @ scale matrix),
row-vector coordinate transformation (P_global = P_local @ M^T), and area dilation calculation via the determinant.

Assumptions & Input Data:
- Four corner coordinates of a detected pallet container in the robot's local body frame:
  (0.5, 0.5), (2.5, 0.5), (2.5, 2.0), (0.5, 2.0) [meters].
- Robot heading rotation angle = 35.0 degrees.
- Non-uniform LiDAR calibration scale = Sx: 1.20, Sy: 1.10.
- Robot global translation offset = [4.0, 3.0] meters.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Ensure outputs directory exists
os.makedirs("outputs", exist_ok=True)

print("=== Task 05 Modified: Robot LiDAR Point Cloud Transformation ===")

# Local body-frame obstacle polygon coordinates [x, y] in meters
local_points = np.array([
    [0.5, 0.5],
    [2.5, 0.5],
    [2.5, 2.0],
    [0.5, 2.0]
])

# Rotation matrix (35 degrees counter-clockwise)
theta = np.deg2rad(35.0)
R = np.array([
    [np.cos(theta), -np.sin(theta)],
    [np.sin(theta),  np.cos(theta)]
])

# Sensor calibration scaling matrix
S = np.array([
    [1.20, 0.0],
    [0.0,  1.10]
])

# Composite linear transformation matrix
T_matrix = R @ S

# Global translation offset vector
t_offset = np.array([4.0, 3.0])

# Transform points into global coordinates
global_points = local_points @ T_matrix.T + t_offset

det_T = np.linalg.det(T_matrix)

print("Local Obstacle Points (Robot Frame):\n", local_points)
print("Composite Transformation Matrix (R @ S):\n", T_matrix)
print("Global Obstacle Points (World Frame):\n", global_points)
print(f"Matrix Determinant (Area Expansion Factor): {det_T:.4f}")

# Visualization
def get_closed_polygon(pts):
    return np.vstack([pts, pts[0]])

poly_local = get_closed_polygon(local_points)
poly_global = get_closed_polygon(global_points)

plt.figure(figsize=(8, 7))
plt.plot(poly_local[:, 0], poly_local[:, 1], 'b-o', linewidth=2, label='Local Frame Detection')
plt.fill(poly_local[:, 0], poly_local[:, 1], 'blue', alpha=0.15)

plt.plot(poly_global[:, 0], poly_global[:, 1], 'r-s', linewidth=2, label='Global Map Projection')
plt.fill(poly_global[:, 0], poly_global[:, 1], 'red', alpha=0.15)

# Plot robot position and heading vector
plt.plot(t_offset[0], t_offset[1], 'k^', markersize=12, label='Robot Origin (4.0, 3.0)m')
plt.quiver(t_offset[0], t_offset[1], np.cos(theta), np.sin(theta), angles='xy', scale_units='xy', scale=1, color='darkgreen', label='Heading (35°)')

plt.title("Task 05 Mod: 2D Spatial LiDAR Frame Affine Transformation")
plt.xlabel("X Coordinate (meters)")
plt.ylabel("Y Coordinate (meters)")
plt.axis('equal')
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.savefig("outputs/mod_task_05.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/mod_task_05.png")
