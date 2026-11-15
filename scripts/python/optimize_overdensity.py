"""
CSV Framework: Overdensity Optimization Loop
Solves for the exact local virial factor Delta that maps 
cosmological condensate density to the exact SPARC a_0 benchmark.
"""

import numpy as np
from scipy.optimize import minimize_scalar

G = 6.67430e-11   
c = 2.99792458e8  
rho_crit = 8.53e-27  
Omega_Lambda = 0.684 
rho_de_background = rho_crit * Omega_Lambda  
Kc = 1 / (8 * np.pi)
observed_sparc_a0 = 1.2e-10  

def objective(delta):
    rho_local = rho_de_background * delta
    a_0_pred = Kc * np.sqrt(Kc) * c * np.sqrt(4 * np.pi * G * rho_local)
    # Minimize squared logarithmic residual
    return (np.log10(a_0_pred / observed_sparc_a0))**2

# Optimize Delta between 10 and 1000
result = minimize_scalar(objective, bounds=(10.0, 1000.0), method='bounded')
optimal_delta = result.x
matched_a0 = Kc * np.sqrt(Kc) * c * np.sqrt(4 * np.pi * G * (rho_de_background * optimal_delta))

print("=== CSV Overdensity Optimization Results ===")
print(f"Optimal Virial Factor (Delta):     {optimal_delta:.2f}")
print(f"Matched Acceleration Scale (a_0):  {matched_a0:.4e} m/s^2")
print(f"Target SPARC Benchmark (a_0):      {observed_sparc_a0:.4e} m/s^2")
print(f"Residual Offset:                   {np.log10(matched_a0 / observed_sparc_a0):.6f} dex")
