"""
Task 05: Matrix Algebra and Matrix Operations
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
print("=== Task 05: Original Implementation ===")

# Four corners of a square: each row is [x, y]
points = np.array([
    [0.0, 0.0],
    [1.0, 0.0],
    [1.0, 1.0],
    [0.0, 1.0]
])

angle = np.deg2rad(45)
rotation = np.array([
    [np.cos(angle), -np.sin(angle)],
    [np.sin(angle),  np.cos(angle)]
])

scale = np.array([
    [2.0, 0.0],
    [0.0, 1.5]
])

# Combined transformation
transformation = rotation @ scale

# Row-vector form requires multiplication by transpose
transformed_points = points @ transformation.T

print("Original points:\n", points)
print("Transformation matrix:\n", transformation)
print("Transformed points:\n", transformed_points)
det_orig = np.linalg.det(transformation)
print("Determinant:", det_orig)

# ==========================================
# SECTION 2: PARAMETER MODIFICATION (Requirement C)
# ==========================================
print("\n=== Task 05: Parameter Modification ===")
# Modify parameters: Rotation angle to 60 degrees, asymmetric scaling [1.5, 2.5]
mod_angle = np.deg2rad(60)
mod_rotation = np.array([
    [np.cos(mod_angle), -np.sin(mod_angle)],
    [np.sin(mod_angle),  np.cos(mod_angle)]
])

mod_scale = np.array([
    [1.5, 0.0],
    [0.0, 2.5]
])

mod_transformation = mod_rotation @ mod_scale
mod_transformed_points = points @ mod_transformation.T
det_mod = np.linalg.det(mod_transformation)

print("Modified Transformation Matrix (60 deg, Scale 1.5x2.5):\n", mod_transformation)
print("Modified Transformed Points:\n", mod_transformed_points)
print(f"Modified Determinant: {det_mod:.4f} (Original: {det_orig:.4f})")

# Generate Comparative Visualization
def close_poly(pts):
    return np.vstack([pts, pts[0]])

plt.figure(figsize=(7, 7))
p_orig = close_poly(points)
p_t1 = close_poly(transformed_points)
p_t2 = close_poly(mod_transformed_points)

plt.plot(p_orig[:, 0], p_orig[:, 1], 'k--', marker='o', label='Original Unit Square')
plt.plot(p_t1[:, 0], p_t1[:, 1], 'b-', marker='s', label='Original Transformed (45°, 2.0x1.5)')
plt.plot(p_t2[:, 0], p_t2[:, 1], 'r-', marker='^', label='Modified Transformed (60°, 1.5x2.5)')

plt.axhline(0, color='gray', linewidth=0.8, linestyle=':')
plt.axvline(0, color='gray', linewidth=0.8, linestyle=':')
plt.title("Task 05: 2D Geometric Affine Transformations")
plt.xlabel("X coordinate")
plt.ylabel("Y coordinate")
plt.axis('equal')
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.savefig("outputs/orig_task_05.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/orig_task_05.png")
