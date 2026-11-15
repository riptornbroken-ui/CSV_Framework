"""
CSV Framework: Overdensity-Corrected Predictive Test
Applies local virialized halo overdensity (Delta ~ 200) to the 
cosmological condensate density baseline.
"""

import numpy as np

# Fundamental Constants
G = 6.67430e-11   # Gravitational constant (m^3 kg^-1 s^-2)
c = 2.99792458e8  # Speed of light (m/s)

# Cosmological Parameters
rho_crit = 8.53e-27  # Critical density of the universe (kg/m^3)
Omega_Lambda = 0.684 # Dark energy density parameter
rho_de_background = rho_crit * Omega_Lambda  

# Local Virial Overdensity Factor for Galactic Halos
delta_vir = 200.0
rho_local = rho_de_background * delta_vir

# Geometric Invariant K_c = 1 / (8 * pi)
Kc = 1 / (8 * np.pi)

def predict_acceleration_scale(rho_0):
    term_geometry = Kc * np.sqrt(Kc)
    term_field = np.sqrt(4 * np.pi * G * rho_0)
    return term_geometry * c * term_field

# Execution
a_0_derived = predict_acceleration_scale(rho_local)
observed_sparc_a0 = 1.2e-10  # SPARC benchmark (m/s^2)

print("=== CSV Overdensity-Corrected Test ===")
print(f"Local Condensate Density (rho_local): {rho_local:.4e} kg/m^3")
print(f"Predicted Acceleration Scale (a_0):    {a_0_derived:.4e} m/s^2")
print(f"Observed Galactic Benchmark (a_0):     {observed_sparc_a0:.4e} m/s^2")
print(f"Residual Offset:                       {np.log10(a_0_derived / observed_sparc_a0):.2f} dex shift")
