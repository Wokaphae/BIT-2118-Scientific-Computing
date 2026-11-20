"""
Task 09 (Modified): Telecommunications Backbone Router Centrality and Spectral Graph Analysis

Problem Statement:
A regional Internet Service Provider (ISP) operates an autonomous system (AS) network
comprising 6 critical backbone routing centers: Frankfurt, London, Amsterdam, Paris,
Zurich, and Milan. Network engineers must assess topological vulnerability to identify
the most strategically influential core routing node. Standard degree count (number of links)
fails to reflect transit influence; hence, eigenvector centrality is employed to determine
nodal prominence based on connections to other highly connected nodes.

Mathematical Concept:
Spectral Graph Theory: Dominant eigenvalue and corresponding eigenvector of an adjacency matrix
satisfying A * v = lambda * v (Perron-Frobenius theorem), normalized to represent centrality scores.

Assumptions & Input Data:
- 6-node undirected core fiber network topology.
- Node order: [FRA, LON, AMS, PAR, ZUR, MIL].
- Dense interconnected transit triangle between FRA, LON, and AMS, with peripheral gateway links.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Ensure outputs directory exists
os.makedirs("outputs", exist_ok=True)

print("=== Task 09 Modified: Backbone Network Eigenvector Centrality ===")

# Symmetric 6x6 adjacency matrix
# Nodes: 0: Frankfurt, 1: London, 2: Amsterdam, 3: Paris, 4: Zurich, 5: Milan
A = np.array([
    # FRA  LON  AMS  PAR  ZUR  MIL
    [ 0.0, 1.0, 1.0, 1.0, 1.0, 0.0],  # FRA
    [ 1.0, 0.0, 1.0, 1.0, 0.0, 0.0],  # LON
    [ 1.0, 1.0, 0.0, 0.0, 0.0, 0.0],  # AMS
    [ 1.0, 1.0, 0.0, 0.0, 0.0, 1.0],  # PAR
    [ 1.0, 0.0, 0.0, 0.0, 0.0, 1.0],  # ZUR
    [ 0.0, 0.0, 0.0, 1.0, 1.0, 0.0]   # MIL
])

nodes = ["Frankfurt", "London", "Amsterdam", "Paris", "Zurich", "Milan"]

# Compute all eigenvalues and eigenvectors
eigenvalues, eigenvectors = np.linalg.eig(A)

# Find dominant (spectral radius) eigenvalue and eigenvector
dom_idx = np.argmax(np.real(eigenvalues))
lambda_max = np.real(eigenvalues[dom_idx])
v_dom = np.abs(np.real(eigenvectors[:, dom_idx]))
centrality = v_dom / v_dom.sum()

# Verification ||A*v - lambda*v||
verif_error = np.linalg.norm(A @ v_dom - lambda_max * v_dom)

print(f"Dominant Spectral Radius (Lambda Max): {lambda_max:.4f}")
print("Eigenvector Centrality Scores:")
ranked_indices = np.argsort(centrality)[::-1]
for rank, idx in enumerate(ranked_indices, start=1):
    print(f"  {rank}. {nodes[idx]:<12}: {centrality[idx]:.4f} ({centrality[idx]*100:.2f}%)")

print(f"Spectral Verification Error: {verif_error:.3e}")

# Visualization: Centrality bar chart
sorted_nodes = [nodes[i] for i in ranked_indices]
sorted_centralities = [centrality[i] for i in ranked_indices]
colors = ['#d62728' if i == 0 else '#1f77b4' for i in range(len(nodes))]

plt.figure(figsize=(8, 4.8))
bars = plt.bar(sorted_nodes, sorted_centralities, color=colors, edgecolor='black', width=0.55)
for bar, val in zip(bars, sorted_centralities):
    plt.text(bar.get_x() + bar.get_width()/2.0, val + 0.005, f"{val*100:.1f}%", ha='center', fontweight='bold')

plt.title("Task 09 Mod: ISP Backbone Router Centrality (Vulnerability Ranking)")
plt.xlabel("Backbone Core Routing Hub")
plt.ylabel("Normalized Eigenvector Centrality")
plt.ylim(0, max(sorted_centralities) * 1.2)
plt.grid(axis='y', linestyle=':', alpha=0.6)
plt.savefig("outputs/mod_task_09.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/mod_task_09.png")
