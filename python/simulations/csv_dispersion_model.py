#!/usr/bin/env python3
"""
Chromatic Spacetime Viscosity (CSV) Framework v2.5
Master Dispersion & Strain-Gated Viscous Damping Module
"""

import numpy as np

def compute_csv_dispersion(E_vals, p_vals, nu_eff, local_strain, s_crit=1e-3, alpha_0=1e-3, n=1):
    """
    Computes the strain-gated CSV master dispersion relation:
    E^2 = p^2 c^2 [1 + alpha(S) * (E / E_P)^n] - i * Gamma(E, nu_eff)
    
    Parameters:
    - E_vals: Array of particle/wave energies (J or eV)
    - p_vals: Array of momenta
    - nu_eff: Effective kinematic viscosity (m^2/s), bounded by <= 1.0e12
    - local_strain (S): Background spacetime strain invariant
    - s_crit: Critical Master Instability Criterion threshold
    - alpha_0: Base chromatic dispersion coupling constant
    - n: Chromatic power-law index
    """
    c = 3.0e8          # Speed of light (m/s)
    hbar = 1.05457e-34 # Reduced Planck constant (J s)
    E_P = 1.22e28      # Planck Energy scale (~1.22 x 10^19 GeV in Joules)
    
    # 1. Sub-Planckian Lattice Regularization Floor
    l_step = 1.0e-40   # meters (5 orders below classical Planck length)
    
    # 2. Master Instability Criterion Gate (Heaviside step function on strain)
    theta_gate = 1.0 if local_strain >= s_crit else 0.0
    alpha_eff = alpha_0 * theta_gate
    
    # 3. Chromatic Energy-Dependent Dispersion Factor
    chromatic_correction = 1.0 + alpha_eff * ((E_vals / E_P) ** n)
    
    # 4. Dimensional Damping Term Gamma(E, nu_eff) [Units: Energy^2]
    # Scaled to maintain Navier-Stokes acoustic attenuation equivalence
    gamma_damping = (nu_eff / (c**2)) * ((E_vals**3) / hbar)
    
    # Assembled Master Dispersion (Complex Energy Squared)
    E_sq_real = (p_vals * c)**2 * chromatic_correction
    E_sq_imag = -1j * gamma_damping
    
    E_sq_total = E_sq_real + E_sq_imag
    
    return {
        "E_squared": E_sq_total,
        "alpha_effective": alpha_eff,
        "sub_planckian_floor_m": l_step,
        "damping_rate_gamma": gamma_damping
    }

if __name__ == "__main__":
    print("[*] Testing CSV Master Dispersion Module...")
    test_E = np.array([1.0e-13, 1.0e-12]) # Joules
    test_p = test_E / 3.0e8
    
    result = compute_csv_dispersion(
        E_vals=test_E,
        p_vals=test_p,
        nu_eff=1.0e10,       # Within constrained limit
        local_strain=2.5e-3  # Above s_crit = 1e-3 (Gate OPEN)
    )
    
    print(f"[+] Computed E^2 Array: {result['E_squared']}")
    print(f"[+] Active Alpha Effective: {result['alpha_effective']}")
    print(f"[+] Sub-Planckian Floor: {result['sub_planckian_floor_m']} m")
