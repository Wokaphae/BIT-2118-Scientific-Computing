"""
Task 19 (Modified): Hybrid Renewable Microgrid Dispatch Optimization

Problem Statement:
An isolated island microgrid must satisfy a continuous industrial electrical demand of 500 MW
at minimum total levelized operating cost ($/hour). The utility operates three power generation
assets:
    x1: Solar PV Farm       (Cost: $18 / MWh, Carbon: 0 kg CO2 / MWh, Max Capacity: 250 MW)
    x2: Wind Turbine Farm   (Cost: $24 / MWh, Carbon: 0 kg CO2 / MWh, Max Capacity: 300 MW)
    x3: Natural Gas Peaker  (Cost: $65 / MWh, Carbon: 450 kg CO2 / MWh, Max Capacity: 400 MW)
Environmental regulations mandate that total hourly carbon emissions cannot exceed 60,000 kg CO2.
The mathematical program minimizes:
    Total Cost = 18*x1 + 24*x2 + 65*x3
subject to:
    x1 + x2 + x3 >= 500 MW (Demand Satisfaction)
    450*x3 <= 60,000 kg CO2 (Emissions Ceiling)
    0 <= x1 <= 250, 0 <= x2 <= 300, 0 <= x3 <= 400.
The problem is solved using Sequential Least Squares Programming (SLSQP).

Mathematical Concept:
Constrained Multivariate Numerical Optimization with linear inequality constraints and
bound constraints using scipy.optimize.minimize.

Assumptions & Input Data:
- Unit costs: [18, 24, 65] $/MWh.
- Target load demand = 500 MW.
- Carbon emission limit = 60,000 kg CO2/hr.
- Generation bounds: Solar [0, 250], Wind [0, 300], Gas [0, 400].
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize

# Ensure outputs directory exists
os.makedirs("outputs", exist_ok=True)

print("=== Task 19 Modified: Hybrid Microgrid Dispatch Optimization ===")

# Objective: Minimize hourly generation cost
def total_cost(z):
    x1, x2, x3 = z
    return 18.0 * x1 + 24.0 * x2 + 65.0 * x3

# Constraint 1: Generation >= 500 MW
def demand_constraint(z):
    x1, x2, x3 = z
    return (x1 + x2 + x3) - 500.0

# Constraint 2: Carbon emissions <= 60,000 kg (60,000 - 450*x3 >= 0)
def emissions_constraint(z):
    x1, x2, x3 = z
    return 60_000.0 - 450.0 * x3

constraints = [
    {"type": "ineq", "fun": demand_constraint},
    {"type": "ineq", "fun": emissions_constraint}
]

bounds = [
    (0.0, 250.0),  # Solar bounds
    (0.0, 300.0),  # Wind bounds
    (0.0, 400.0)   # Gas Peaker bounds
]

# Initial guess: 100 MW Solar, 100 MW Wind, 300 MW Gas
x0 = [100.0, 100.0, 300.0]

solution = minimize(
    total_cost,
    x0,
    method="SLSQP",
    bounds=bounds,
    constraints=constraints
)

x1_opt, x2_opt, x3_opt = solution.x
total_gen = x1_opt + x2_opt + x3_opt
total_emission = 450.0 * x3_opt

print("Optimization Successful:", solution.success)
print(f"Optimal Solar Dispatch (x1):   {x1_opt:.2f} MW (Capacity Utilization: {x1_opt/250*100:.1f}%)")
print(f"Optimal Wind Dispatch (x2):    {x2_opt:.2f} MW (Capacity Utilization: {x2_opt/300*100:.1f}%)")
print(f"Optimal Gas Peaker Dispatch:   {x3_opt:.2f} MW (Capacity Utilization: {x3_opt/400*100:.1f}%)")
print(f"Total Power Generated:         {total_gen:.2f} MW (Required: 500.00 MW)")
print(f"Total Carbon Emissions:        {total_emission:,.1f} kg CO2/hr (Cap: 60,000 kg)")
print(f"Minimum Hourly Operating Cost: ${solution.fun:,.2f} / hr")
print(f"Blended Levelized Cost:        ${solution.fun / total_gen:.2f} / MWh")

# Visualization: Optimal generation dispatch pie / bar chart
assets = ['Solar PV', 'Wind Turbine', 'Gas Peaker']
dispatches = [x1_opt, x2_opt, x3_opt]
colors = ['#ff7f0e', '#2ca02c', '#d62728']

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8))

# Bar chart of power dispatches
bars = ax1.bar(assets, dispatches, color=colors, edgecolor='black', width=0.55)
for bar, val in zip(bars, dispatches):
    ax1.text(bar.get_x() + bar.get_width()/2.0, val + 5.0, f"{val:.1f} MW", ha='center', fontweight='bold')
ax1.set_ylabel("Power Dispatched (MW)")
ax1.set_ylim(0, 350)
ax1.set_title("Optimal Generation Dispatch Schedule")
ax1.grid(axis='y', linestyle=':', alpha=0.6)

# Cost breakdown pie chart
costs = [18.0 * x1_opt, 24.0 * x2_opt, 65.0 * x3_opt]
ax2.pie(costs, labels=assets, autopct='%1.1f%%', colors=colors, startangle=140, explode=(0.05, 0.05, 0.05))
ax2.set_title(f"Operating Cost Breakdown (Total: ${solution.fun:,.0f}/hr)")

plt.suptitle("Task 19 Mod: Constrained Optimal Power Dispatch (SLSQP)")
plt.savefig("outputs/mod_task_19.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/mod_task_19.png")
