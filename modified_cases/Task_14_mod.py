"""
Task 14 (Modified): Microbial Fermentation Biomass Growth via Logistic Curve Fitting

Problem Statement:
In bioprocess engineering, an industrial bioreactor cultures recombinant E. coli to produce
therapeutic insulin. The biomass concentration N(t) (g/L) is sampled over a 14-hour fermentation
batch. Biological population growth typically follows the nonlinear S-shaped logistic model:
    N(t) = K / [1 + exp(-r * (t - t0))]
where 'K' is the asymptotic carrying capacity (maximum cell density), 'r' is the maximum specific
growth rate (hr^-1), and 't0' is the inflection midpoint time (hours). SciPy's curve_fit is used
to estimate the kinetic biological parameters, quantify fitting accuracy via Root Mean Squared
Error (RMSE), and forecast biomass production at t = 18 hours.

Mathematical Concept:
Nonlinear Least Squares Regression (scipy.optimize.curve_fit) using the Levenberg-Marquardt
algorithm to minimize the sum of squared residuals.

Assumptions & Input Data:
- Sampling times: t = [0, 2, 4, 6, 8, 10, 12, 14] hours.
- Measured biomass dry cell weight (g/L): [0.45, 0.85, 2.10, 5.40, 9.80, 13.50, 15.20, 15.90].
- Initial parameter guesses: p0 = [16.0, 0.5, 7.0].
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Ensure outputs directory exists
os.makedirs("outputs", exist_ok=True)

print("=== Task 14 Modified: Bioreactor Logistic Growth Fitting ===")

time_hours = np.array([0, 2, 4, 6, 8, 10, 12, 14], dtype=float)
biomass_measured = np.array([0.45, 0.85, 2.10, 5.40, 9.80, 13.50, 15.20, 15.90], dtype=float)

# Logistic growth model function
def logistic_model(t, K, r, t0):
    return K / (1.0 + np.exp(-r * (t - t0)))

# Fit parameters
p0 = [16.0, 0.6, 7.0]
params, cov = curve_fit(logistic_model, time_hours, biomass_measured, p0=p0)
K_opt, r_opt, t0_opt = params
param_std_err = np.sqrt(np.diag(cov))

# Fitted values and RMSE
predicted = logistic_model(time_hours, *params)
residuals = biomass_measured - predicted
rmse = np.sqrt(np.mean(residuals**2))

# Prediction at t = 18 hours
t_forecast = 18.0
biomass_18h = logistic_model(t_forecast, *params)

print(f"Fitted Carrying Capacity K: {K_opt:.3f} ± {param_std_err[0]:.3f} g/L")
print(f"Fitted Growth Rate r:       {r_opt:.4f} ± {param_std_err[1]:.4f} hr⁻¹")
print(f"Fitted Inflection Time t0:  {t0_opt:.3f} ± {param_std_err[2]:.3f} hours")
print(f"Model RMSE:                 {rmse:.4f} g/L")
print(f"Forecast Biomass at 18 hrs: {biomass_18h:.2f} g/L (Carrying Capacity Saturation: {biomass_18h/K_opt*100:.1f}%)")

# Visualization
t_plot = np.linspace(0, 20, 300)
n_plot = logistic_model(t_plot, *params)

plt.figure(figsize=(8, 4.8))
plt.scatter(time_hours, biomass_measured, color='black', s=55, zorder=5, label='Bioreactor Samples')
plt.plot(t_plot, n_plot, 'b-', linewidth=2, label=f'Fitted Logistic Curve (RMSE: {rmse:.2f} g/L)')
plt.axhline(K_opt, color='red', linestyle='--', label=f'Carrying Capacity K={K_opt:.2f} g/L')
plt.axvline(t0_opt, color='green', linestyle=':', label=f'Inflection Point t0={t0_opt:.2f}h')
plt.scatter([t_forecast], [biomass_18h], color='purple', s=80, marker='*', zorder=6, label=f'18h Forecast ({biomass_18h:.2f} g/L)')
plt.title("Task 14 Mod: E. Coli Biomass Growth Kinetics via Logistic Regression")
plt.xlabel("Fermentation Time (hours)")
plt.ylabel("Biomass Concentration (g/L)")
plt.xlim(-0.5, 20.5)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.savefig("outputs/mod_task_14.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved visualization to outputs/mod_task_14.png")
