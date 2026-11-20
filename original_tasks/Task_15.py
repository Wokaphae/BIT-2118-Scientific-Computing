"""
Task 15: Numerical Differentiation
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
print("=== Task 15: Original Implementation ===")

# GPS samples: time in seconds and position in metres
time = np.array([0, 1, 2, 3, 4, 5, 6], dtype=float)
position = np.array([0.0, 4.8, 10.2, 16.1, 22.7, 30.0, 38.0])

speed = np.zeros_like(position)

# Forward difference at the beginning
speed[0] = (position[1] - position[0]) / (time[1] - time[0])

# Central differences for interior points
for i in range(1, len(time) - 1):
    speed[i] = (
        position[i + 1] - position[i - 1]
    ) / (
        time[i + 1] - time[i - 1]
    )

# Backward difference at the end
speed[-1] = (
    position[-1] - position[-2]
) / (
    time[-1] - time[-2]
)

for t, x, v in zip(time, position, speed):
    print(f"t={t:.0f}s, position={x:.1f}m, estimated speed={v:.2f}m/s")

# ==========================================
# SECTION 2: PARAMETER MODIFICATION (Requirement C)
# ==========================================
print("\n=== Task 15: Parameter Modification (Acceleration / 2nd Derivative) ===")
# Second derivative calculation: Acceleration a(t) via central difference of velocity
# and direct 3-point central second difference: (x[i+1] - 2*x[i] + x[i-1]) / dt^2
dt = 1.0  # uniform 1-second interval
acceleration = np.zeros_like(position)

# Forward diff for acceleration at t=0
acceleration[0] = (speed[1] - speed[0]) / dt
# Central diff for interior acceleration
for i in range(1, len(time) - 1):
    acceleration[i] = (speed[i + 1] - speed[i - 1]) / (2 * dt)
# Backward diff for acceleration at end
acceleration[-1] = (speed[-1] - speed[-2]) / dt

for t, v, a in zip(time, speed, acceleration):
    print(f"t={t:.0f}s, speed={v:.2f}m/s, acceleration={a:.2f}m/s^2")

# Dual-axis / Subplot Visualization
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 7), sharex=True)

ax1.plot(time, speed, 'b-o', label='Estimated Speed (m/s)')
ax1.plot(time, position, 'g--s', alpha=0.5, label='Position (m)')
ax1.set_ylabel("Speed (m/s) / Pos (m)")
ax1.set_title("Task 15: GPS Kinematic Differentiation (Velocity & Acceleration)")
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.legend()

ax2.plot(time, acceleration, 'r-^', label='Estimated Acceleration (m/s²)')
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Acceleration (m/s²)")
ax2.grid(True, linestyle=':', alpha=0.6)
ax2.legend()

plt.savefig("outputs/orig_task_15.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/orig_task_15.png")
