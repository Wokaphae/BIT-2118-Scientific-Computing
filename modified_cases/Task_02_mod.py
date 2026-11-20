"""
Task 02 (Modified): Solar Photovoltaic (PV) Plant Diurnal Generation and Efficiency Analysis

Problem Statement:
A 50 kWp commercial solar PV plant monitors solar irradiance (W/m^2) every hour across a
24-hour cycle. The plant engineering team needs to compute daily total solar insolation,
daily average daytime irradiance, peak solar irradiance, and convert all raw irradiance
readings to estimated AC electric power output (kW) after factoring in solar panel temperature
coefficients and inverter efficiency (96.5%).

Mathematical Concept:
NumPy Arrays and Numerical Computation (1D arrays, vectorized arithmetic, aggregate functions:
np.mean, np.min, np.max, np.sum).

Assumptions & Input Data:
- 24 hourly irradiance readings in W/m^2.
- Nominal array DC rating = 50.0 kW at 1000 W/m^2 Standard Test Conditions (STC).
- System efficiency factor (inverter, wiring, thermal derating) = 0.82.
- AC Power (kW) = (Irradiance / 1000) * 50.0 * 0.82.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Ensure outputs directory exists
os.makedirs("outputs", exist_ok=True)

print("=== Task 02 Modified: Solar PV Generation Analysis ===")

# 24-hour solar irradiance readings (W/m^2) from midnight to 23:00
irradiance_wm2 = np.array([
    0.0, 0.0, 0.0, 0.0, 0.0, 15.0,
    85.0, 240.0, 460.0, 680.0, 850.0, 940.0,
    970.0, 930.0, 810.0, 620.0, 390.0, 160.0,
    30.0, 0.0, 0.0, 0.0, 0.0, 0.0
])

# Aggregate calculations
peak_irradiance = np.max(irradiance_wm2)
mean_24h_irradiance = np.mean(irradiance_wm2)
daytime_mask = irradiance_wm2 > 0
mean_daytime_irradiance = np.mean(irradiance_wm2[daytime_mask])

# Vectorized conversion to AC electric power (kW)
# 50 kWp system derated by overall 82% performance ratio
system_capacity_kw = 50.0
performance_ratio = 0.82
ac_power_kw = (irradiance_wm2 / 1000.0) * system_capacity_kw * performance_ratio

# Daily total energy generation (kWh) using 1-hour time intervals
daily_energy_kwh = np.sum(ac_power_kw)
peak_ac_power_kw = np.max(ac_power_kw)
capacity_factor = (daily_energy_kwh / (system_capacity_kw * 24)) * 100

print(f"Peak Solar Irradiance: {peak_irradiance:.1f} W/m²")
print(f"24-Hour Average Irradiance: {mean_24h_irradiance:.1f} W/m²")
print(f"Daylight Average Irradiance: {mean_daytime_irradiance:.1f} W/m²")
print(f"Peak AC Power Output: {peak_ac_power_kw:.2f} kW")
print(f"Daily Total Electric Energy: {daily_energy_kwh:.2f} kWh")
print(f"Daily Plant Capacity Factor: {capacity_factor:.2f}%")
print("Midday AC Generation Profile (10:00 to 15:00):", np.round(ac_power_kw[10:16], 2))

# Visualization
hours = np.arange(24)
fig, ax1 = plt.subplots(figsize=(9, 4.8))

color = '#ff7f0e'
ax1.set_xlabel('Hour of Day (24-Hour Clock)')
ax1.set_ylabel('Solar Irradiance (W/m²)', color=color)
ax1.plot(hours, irradiance_wm2, color=color, marker='o', linewidth=2, label='Solar Irradiance')
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid(True, linestyle=':', alpha=0.6)

ax2 = ax1.twinx()
color = '#1f77b4'
ax2.set_ylabel('AC Electric Power (kW)', color=color)
ax2.fill_between(hours, ac_power_kw, alpha=0.3, color=color, label='AC Power Generated')
ax2.plot(hours, ac_power_kw, color=color, marker='s', linewidth=2)
ax2.tick_params(axis='y', labelcolor=color)

plt.title("Task 02 Mod: Commercial Solar PV Farm Daily Generation Profile")
fig.tight_layout()
plt.savefig("outputs/mod_task_02.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/mod_task_02.png")
