"""
Task 13 (Modified): Engine Dynamometer Torque and Brake Horsepower Interpolation

Problem Statement:
During chassis dynamometer testing of a performance turbocharged engine, brake torque (lb-ft)
is measured at sparse engine speeds from 1,500 RPM to 6,500 RPM in 1,000 RPM increments. The
engine electronic control unit (ECU) requires continuous torque mapping at fine 50 RPM intervals
to schedule optimal spark timing and calculate brake horsepower (BHP):
    BHP = (Torque * RPM) / 5252
Using both Linear and Cubic Spline interpolation (scipy.interpolate), intermediate torque and
peak horsepower are estimated, demonstrating the importance of smooth continuous derivatives
in mechanical calibration.

Mathematical Concept:
1D Interpolation: Piecewise linear (C0 continuity) vs Cubic Spline (C2 second-derivative continuity)
interpolation.

Assumptions & Input Data:
- Discrete measured RPM points: [1500, 2500, 3500, 4500, 5500, 6500] RPM.
- Measured torque readings:    [185.0, 275.0, 340.0, 365.0, 330.0, 260.0] lb-ft.
- Query engine speed for mid-range torque estimation: 4,000 RPM.
- Dense evaluation grid: 1,500 to 6,500 RPM in 50 RPM steps.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d, CubicSpline

# Ensure outputs directory exists
os.makedirs("outputs", exist_ok=True)

print("=== Task 13 Modified: Engine Dynamometer Curve Interpolation ===")

rpm_measured = np.array([1500, 2500, 3500, 4500, 5500, 6500], dtype=float)
torque_measured = np.array([185.0, 275.0, 340.0, 365.0, 330.0, 260.0])

# Interpolation models
interp_linear = interp1d(rpm_measured, torque_measured, kind='linear')
interp_spline = CubicSpline(rpm_measured, torque_measured)

# Dense evaluation grid (every 50 RPM)
rpm_dense = np.arange(1500, 6550, 50)
torque_linear = interp_linear(rpm_dense)
torque_spline = interp_spline(rpm_dense)

# Brake Horsepower (BHP = Torque * RPM / 5252)
bhp_linear = (torque_linear * rpm_dense) / 5252.0
bhp_spline = (torque_spline * rpm_dense) / 5252.0

target_rpm = 4000.0
t_lin_target = float(interp_linear(target_rpm))
t_spl_target = float(interp_spline(target_rpm))

peak_spline_torque = np.max(torque_spline)
peak_torque_rpm = rpm_dense[np.argmax(torque_spline)]

peak_spline_bhp = np.max(bhp_spline)
peak_bhp_rpm = rpm_dense[np.argmax(bhp_spline)]

print(f"Torque at {target_rpm:.0f} RPM (Linear):      {t_lin_target:.2f} lb-ft")
print(f"Torque at {target_rpm:.0f} RPM (Cubic Spline): {t_spl_target:.2f} lb-ft")
print(f"Peak Torque (Cubic Spline): {peak_spline_torque:.2f} lb-ft at {peak_torque_rpm:.0f} RPM")
print(f"Peak Power (Cubic Spline):  {peak_spline_bhp:.2f} BHP at {peak_bhp_rpm:.0f} RPM")

# Visualization
fig, ax1 = plt.subplots(figsize=(9, 5))

color = '#1f77b4'
ax1.set_xlabel('Engine Speed (RPM)')
ax1.set_ylabel('Brake Torque (lb-ft)', color=color)
ax1.scatter(rpm_measured, torque_measured, color='black', s=60, zorder=5, label='Dyno Measurements')
ax1.plot(rpm_dense, torque_linear, color=color, linestyle='--', label='Torque (Linear)')
ax1.plot(rpm_dense, torque_spline, color=color, linewidth=2, label='Torque (Cubic Spline)')
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid(True, linestyle=':', alpha=0.6)

ax2 = ax1.twinx()
color = '#d62728'
ax2.set_ylabel('Brake Horsepower (BHP)', color=color)
ax2.plot(rpm_dense, bhp_spline, color=color, linewidth=2, linestyle='-.', label='Power (Cubic Spline BHP)')
ax2.tick_params(axis='y', labelcolor=color)

# Combine legends
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

plt.title("Task 13 Mod: Engine Dynamometer Torque & BHP Performance Curves")
plt.savefig("outputs/mod_task_13.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/mod_task_13.png")
