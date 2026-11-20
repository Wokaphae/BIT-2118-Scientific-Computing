"""
Task 18 (Modified): SIR Epidemiological Outbreak Dynamic Modeling via SciPy solve_ivp

Problem Statement:
In public health epidemiology, the outbreak of an airborne viral epidemic across a metropolitan
population N = 100,000 is governed by the nonlinear Kermack-McKendrick SIR differential equations:
    dS/dt = -beta * S * I / N
    dI/dt =  beta * S * I / N - gamma * I
    dR/dt =  gamma * I
where 'S' is the susceptible cohort, 'I' is the actively infectious cohort, and 'R' is the
recovered/immunized cohort. Here 'beta' represents the transmission contact rate, and 'gamma' is
the recovery rate (1 / infectious period). The epidemiological team uses scipy.integrate.solve_ivp
with an adaptive Runge-Kutta 4th/5th order method (RK45) to project the peak epidemic burden,
the day of peak hospital infection, and the final herd immunity attack rate.

Mathematical Concept:
Numerical Integration of Systems of Coupled Nonlinear Ordinary Differential Equations using
adaptive step-size Runge-Kutta methods (scipy.integrate.solve_ivp).

Assumptions & Input Data:
- Total population N = 100,000.
- Initial state: S0 = 99,950, I0 = 50, R0 = 0.
- Transmission rate beta = 0.35 day^-1.
- Recovery rate gamma = 0.10 day^-1 (average infectious duration = 10 days).
- Basic reproduction number R0 = beta / gamma = 3.5.
- Simulation horizon: 0 to 120 days.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

# Ensure outputs directory exists
os.makedirs("outputs", exist_ok=True)

print("=== Task 18 Modified: SIR Outbreak Epidemic Dynamics via SciPy ===")

N = 100_000.0
beta = 0.35       # transmission rate per day
gamma = 0.10      # recovery rate per day
R0_reproduction = beta / gamma

# Initial state vector [S, I, R]
y0 = [N - 50.0, 50.0, 0.0]

def sir_system(t, y):
    S, I, R = y
    dS_dt = -beta * S * I / N
    dI_dt =  beta * S * I / N - gamma * I
    dR_dt =  gamma * I
    return [dS_dt, dI_dt, dR_dt]

t_span = (0.0, 120.0)
t_eval = np.linspace(0.0, 120.0, 300)

solution = solve_ivp(
    sir_system,
    t_span,
    y0,
    t_eval=t_eval,
    method='RK45',
    rtol=1e-8,
    atol=1e-10
)

S_curve = solution.y[0]
I_curve = solution.y[1]
R_curve = solution.y[2]

peak_infected = np.max(I_curve)
peak_day = solution.t[np.argmax(I_curve)]
final_recovered = R_curve[-1]
attack_rate = (final_recovered / N) * 100.0

print(f"Basic Reproduction Number R0:   {R0_reproduction:.2f}")
print(f"Solver Success Status:          {solution.success}")
print(f"Peak Infectious Population:     {peak_infected:,.0f} individuals ({peak_infected/N*100:.2f}% of population)")
print(f"Peak Epidemic Burden Timing:    Day {peak_day:.1f}")
print(f"Final Total Infected/Recovered: {final_recovered:,.0f} individuals")
print(f"Overall Epidemic Attack Rate:   {attack_rate:.2f}%")

# Visualization
plt.figure(figsize=(9, 5))
plt.plot(solution.t, S_curve / 1000.0, 'b-', linewidth=2, label='Susceptible S(t)')
plt.plot(solution.t, I_curve / 1000.0, 'r-', linewidth=2.5, label='Infectious I(t)')
plt.plot(solution.t, R_curve / 1000.0, 'g-', linewidth=2, label='Recovered R(t)')
plt.plot(peak_day, peak_infected / 1000.0, 'k*', markersize=14, label=f'Peak: {peak_infected/1000:.1f}k at Day {peak_day:.0f}')

plt.title(f"Task 18 Mod: SIR Outbreak Trajectory (R₀ = {R0_reproduction:.1f}, N = 100,000)")
plt.xlabel("Days since Outbreak Inception")
plt.ylabel("Population (Thousands)")
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc='center right')
plt.savefig("outputs/mod_task_18.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/mod_task_18.png")
