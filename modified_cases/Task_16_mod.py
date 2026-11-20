"""
Task 16 (Modified): River Flood Surge Hydrograph Runoff Volume Integration

Problem Statement:
During a severe tropical cyclone, a municipal water catchment agency monitors the streamflow
discharge rate Q(t) (cubic meters per second, m^3/s) of a major river basin over a 24-hour storm
hydrograph period. Gauging stations record river discharge every 3 hours. Hydraulic engineers
must compute the total cumulative flood runoff volume V (in cubic meters and megaliters) to assess
reservoir spillway capacity and flood inundation risk:
    V = integral_{0}^{24} Q(t) dt
The integration is performed using both the composite Trapezoidal rule and composite Simpson's rule.

Mathematical Concept:
Numerical Integration: Newton-Cotes Quadratures (Trapezoidal rule vs Simpson's 1/3 parabolic rule)
over discrete non-analytical time-series data.

Assumptions & Input Data:
- Time intervals: t = [0, 3, 6, 9, 12, 15, 18, 21, 24] hours (constant step dt = 3.0 hr = 10,800 s).
- River discharge Q(t): [45.0, 68.0, 142.0, 310.0, 480.0, 395.0, 240.0, 125.0, 60.0] m^3/s.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import simpson

# Ensure outputs directory exists
os.makedirs("outputs", exist_ok=True)

print("=== Task 16 Modified: River Hydrograph Flood Volume Integration ===")

# Time in hours and seconds
time_hours = np.array([0, 3, 6, 9, 12, 15, 18, 21, 24], dtype=float)
time_seconds = time_hours * 3600.0  # convert hours to seconds for SI integration

# River streamflow rate in m^3/s
discharge_m3s = np.array([45.0, 68.0, 142.0, 310.0, 480.0, 395.0, 240.0, 125.0, 60.0])

# Numerical Integration
volume_trapezoid_m3 = np.trapezoid(discharge_m3s, time_seconds)
volume_simpson_m3 = simpson(discharge_m3s, x=time_seconds)

# Convert to Megaliters (1 ML = 1,000 m^3)
vol_trap_ml = volume_trapezoid_m3 / 1000.0
vol_simp_ml = volume_simpson_m3 / 1000.0
diff_ml = abs(vol_simp_ml - vol_trap_ml)

peak_flow = np.max(discharge_m3s)
peak_time = time_hours[np.argmax(discharge_m3s)]

print(f"Peak Storm Discharge:          {peak_flow:.1f} m³/s at t = {peak_time:.0f} hours")
print(f"Total Runoff (Trapezoidal):    {volume_trapezoid_m3:,.0f} m³ ({vol_trap_ml:,.1f} Megaliters)")
print(f"Total Runoff (Simpson's Rule): {volume_simpson_m3:,.0f} m³ ({vol_simp_ml:,.1f} Megaliters)")
print(f"Discrepancy between Methods:   {abs(volume_simpson_m3 - volume_trapezoid_m3):,.0f} m³ ({diff_ml:,.2f} ML, {diff_ml/vol_simp_ml*100:.3f}%)")

# Visualization: Hydrograph & Cumulative Volume
cumulative_trap = np.array([np.trapezoid(discharge_m3s[:k+1], time_seconds[:k+1])/1000.0 for k in range(len(time_hours))])

fig, ax1 = plt.subplots(figsize=(9, 5))

color = '#1f77b4'
ax1.set_xlabel("Storm Duration (Hours)")
ax1.set_ylabel("River Discharge Rate (m³/s)", color=color)
ax1.plot(time_hours, discharge_m3s, color=color, marker='o', linewidth=2.5, label='Discharge Hydrograph Q(t)')
ax1.fill_between(time_hours, discharge_m3s, color=color, alpha=0.25, label=f'Runoff Volume ({vol_simp_ml:,.0f} ML)')
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid(True, linestyle=':', alpha=0.6)

ax2 = ax1.twinx()
color = '#2ca02c'
ax2.set_ylabel("Accumulated Runoff (Megaliters)", color=color)
ax2.plot(time_hours, cumulative_trap, color=color, linestyle='--', marker='s', linewidth=2, label='Cumulative Volume (ML)')
ax2.tick_params(axis='y', labelcolor=color)

plt.title("Task 16 Mod: Storm Hydrograph and Cumulative Watershed Runoff")
fig.tight_layout()
plt.savefig("outputs/mod_task_16.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/mod_task_16.png")
