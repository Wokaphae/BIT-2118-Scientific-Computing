"""
Task 09: Eigenvalues and Eigenvectors
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
print("=== Task 09: Original Implementation ===")

# Adjacency matrix for a small undirected network.
# Node order: A, B, C, D
A = np.array([
    [0., 1., 1., 0.],
    [1., 0., 1., 1.],
    [1., 1., 0., 1.],
    [0., 1., 1., 0.]
])

eigenvalues, eigenvectors = np.linalg.eig(A)

# Dominant eigenvalue/eigenvector
index = np.argmax(np.real(eigenvalues))
dominant_value = np.real(eigenvalues[index])
dominant_vector = np.abs(np.real(eigenvectors[:, index]))
centrality = dominant_vector / dominant_vector.sum()

nodes = ["A", "B", "C", "D"]

print("Dominant eigenvalue:", dominant_value)
print("Eigenvector-based importance:")
for node, score in zip(nodes, centrality):
    print(f"{node}: {score:.4f}")

# Verify Av = lambda*v
v = np.real(eigenvectors[:, index])
print("Verification error:", np.linalg.norm(A @ v - dominant_value * v))

# ==========================================
# SECTION 2: PARAMETER MODIFICATION (Requirement C)
# ==========================================
print("\n=== Task 09: Parameter Modification ===")
# Add link between nodes A and D (forming a ring topology with cross-chords)
A_mod = A.copy()
A_mod[0, 3] = 1.0
A_mod[3, 0] = 1.0

evals_mod, evecs_mod = np.linalg.eig(A_mod)
idx_mod = np.argmax(np.real(evals_mod))
dom_val_mod = np.real(evals_mod[idx_mod])
dom_vec_mod = np.abs(np.real(evecs_mod[:, idx_mod]))
centrality_mod = dom_vec_mod / dom_vec_mod.sum()

print("Modified Dominant eigenvalue:", dom_val_mod)
print("Modified Eigenvector-based importance (with edge A-D added):")
for node, score in zip(nodes, centrality_mod):
    print(f"{node}: {score:.4f}")

# Comparative Visualization
x_pos = np.arange(len(nodes))
width = 0.35

plt.figure(figsize=(7, 4.8))
plt.bar(x_pos - width/2, centrality, width, label='Original Topology', color='#1f77b4')
plt.bar(x_pos + width/2, centrality_mod, width, label='Modified (Added Edge A-D)', color='#ff7f0e')
plt.xticks(x_pos, nodes)
plt.xlabel("Network Node")
plt.ylabel("Eigenvector Centrality (Normalized)")
plt.title("Task 09: Eigenvector Centrality Response to Structural Network Modification")
plt.grid(axis='y', linestyle=':', alpha=0.6)
plt.legend()
plt.savefig("outputs/orig_task_09.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/orig_task_09.png")
