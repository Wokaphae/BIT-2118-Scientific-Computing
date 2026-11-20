"""
Task 15 (Modified): Arterial Blood Pressure Waveform Analysis and Maximum Contractility (dP/dt)

Problem Statement:
In clinical cardiology and intensive care unit (ICU) hemodynamic monitoring, continuous arterial
blood pressure (ABP in mmHg) is sampled over a cardiac cycle (period ~ 0.8 seconds, heart rate ~ 75 bpm).
The maximum rate of left ventricular pressure rise, (dP/dt)_max, is a critical clinical index
of myocardial contractility. When analytical pressure functions are absent from arterial catheter
measurements, numerical differentiation must be applied:
    - Forward difference at systolic onset (t = 0)
    - Central difference across interior pulse samples
    - Backward difference at end-diastole (t = T)
The algorithm estimates instantaneous dP/dt and identifies the peak contractility surge point.

Mathematical Concept:
Numerical Differentiation:
    Forward: f'(x) ~ [f(x+h) - f(x)] / h      (O(h))
    Central: f'(x) ~ [f(x+h) - f(x-h)] / (2h)  (O(h^2))
    Backward: f'(x) ~ [f(x) - f(x-h)] / h     (O(h))

Assumptions & Input Data:
- Time samples t across one heartbeat from 0.00 to 0.70 seconds (dt = 0.05 s).
- Arterial pressure readings P (mmHg) tracking diastolic pressure (80 mmHg), rapid systolic upstroke
  (peaking at 120 mmHg), dicrotic notch, and diastolic runoff.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Ensure outputs directory exists
os.makedirs("outputs", exist_ok=True)

print("=== Task 15 Modified: Arterial Blood Pressure Hemodynamics ===")

# Time in seconds (sample dt = 0.05 s)
time_s = np.array([
    0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30,
    0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70
], dtype=float)

# Arterial Blood Pressure in mmHg
pressure_mmhg = np.array([
    80.0, 82.5, 96.0, 116.0, 122.0, 118.0, 105.0,
    98.0, 102.0, 95.0, 90.0, 86.0, 83.0, 81.0, 80.0
])

dp_dt = np.zeros_like(pressure_mmhg)

# Forward difference at initial sample
dp_dt[0] = (pressure_mmhg[1] - pressure_mmhg[0]) / (time_s[1] - time_s[0])

# Central differences for all interior samples
for i in range(1, len(time_s) - 1):
    dp_dt[i] = (
        pressure_mmhg[i + 1] - pressure_mmhg[i - 1]
    ) / (
        time_s[i + 1] - time_s[i - 1]
    )

# Backward difference at final sample
dp_dt[-1] = (pressure_mmhg[-1] - pressure_mmhg[-2]) / (time_s[-1] - time_s[-2])

max_dp_dt = np.max(dp_dt)
max_idx = np.argmax(dp_dt)
t_max_contractility = time_s[max_idx]

print(f"{'Time (s)':<10} {'Pressure (mmHg)':<18} {'dP/dt (mmHg/s)':<16}")
print("-" * 46)
for t, p, dp in zip(time_s, pressure_mmhg, dp_dt):
    print(f"{t:<10.2f} {p:<18.1f} {dp:<16.2f}")

print(f"\nPeak Systolic Contractility (dP/dt)_max: {max_dp_dt:.2f} mmHg/s at t = {t_max_contractility:.2f} s")
print(f"Pulse Pressure: {np.max(pressure_mmhg) - np.min(pressure_mmhg):.1f} mmHg (Systolic: {np.max(pressure_mmhg):.1f}, Diastolic: {np.min(pressure_mmhg):.1f})")

# Dual-panel Visualization
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 7), sharex=True)

# Blood pressure pulse
ax1.plot(time_s, pressure_mmhg, 'b-o', linewidth=2, label='Arterial Pulse Wave P(t)')
ax1.axhline(np.max(pressure_mmhg), color='gray', linestyle=':', label=f'Systolic Peak ({np.max(pressure_mmhg)} mmHg)')
ax1.axhline(np.min(pressure_mmhg), color='gray', linestyle='--', label=f'Diastolic Baseline ({np.min(pressure_mmhg)} mmHg)')
ax1.set_ylabel("Pressure (mmHg)")
ax1.set_title("Task 15 Mod: ICU Arterial Blood Pressure & Contractility Rate")
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.legend(loc='upper right')

# Rate of pressure change (dP/dt)
ax2.plot(time_s, dp_dt, 'r-s', linewidth=2, label='Rate of Change (dP/dt)')
ax2.plot(t_max_contractility, max_dp_dt, 'k*', markersize=14, label=f'Peak Contractility ({max_dp_dt:.1f} mmHg/s)')
ax2.axhline(0, color='black', linewidth=0.8)
ax2.set_xlabel("Cardiac Cycle Time (seconds)")
ax2.set_ylabel("dP/dt (mmHg / second)")
ax2.grid(True, linestyle=':', alpha=0.6)
ax2.legend(loc='upper right')

plt.tight_layout()
plt.savefig("outputs/mod_task_15.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/mod_task_15.png")
