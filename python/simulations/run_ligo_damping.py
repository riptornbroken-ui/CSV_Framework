#!/usr/bin/env python3
"""
Chromatic Spacetime Viscosity (CSV) Framework v2.5
Berti-Cardoso-Starinets Kerr QNM & Viscous Damping Comparison
"""

import numpy as np

def simulate_bcs_kerr_overtones():
    print("[*] Initializing CSV BCS Kerr Overtone & GR Baseline Simulation...")
    
    M = 60.0 # Solar masses
    # Fundamental frequency scale for 60 M_sun in Hz (approx 533 Hz base)
    f_base = 32.0 / M * 1000.0
    
    # BCS-inspired fitting parameters for frequency and GR baseline damping as a function of spin a* and overtone n
    # Format: overtone_index: (frequency_scaling_factor, base_gr_damping_rate_s-1)
    # Note: In GR, higher overtones have significantly larger base damping rates.
    
    spins = [0.0, 0.7, 0.9]
    nu_bound = 1.0e12 # m^2/s observational ceiling
    c = 3.0e8
    
    print("    ---------------------------------------------------------------------------------------")
    print(f"    {'Overtone (n)':<14} {'Spin (a*)':<10} {'Freq (Hz)':<12} {'GR Damp (s^-1)':<15} {'CSV Damp (s^-1)':<16} {'Status':<10}")
    print("    ---------------------------------------------------------------------------------------")
    
    for n in [0, 1, 2]:
        for a in spins:
            # BCS frequency behavior: real frequency slightly decreases with high spin for certain modes or scales smoothly
            freq_factor = (1.0 + 0.15 * a - 0.05 * (a**2)) * (1.0 - 0.1 * n)
            f_qnm = f_base * freq_factor
            
            # GR baseline damping increases with overtone n and spin a*
            gamma_gr = 250.0 * (1.0 + 0.8 * n) * (1.0 + 0.5 * a)
            
            # CSV viscous damping contribution
            k_gw = (2 * np.pi * f_qnm) / c
            gamma_csv = nu_bound * (k_gw ** 2)
            
            total_damping = gamma_gr + gamma_csv
            status = "Constrained" if gamma_csv > (0.2 * gamma_gr) else "Safe/Sub-Dominant"
            
            print(f"    n = {n:<11} {a:<10.1f} {f_qnm:<12.1f} {gamma_gr:<15.1f} {gamma_csv:<16.2e} {status:<10}")
            
    print("    ---------------------------------------------------------------------------------------")
    print("[+] BCS Kerr Overtone Simulation Complete.")

if __name__ == '__main__':
    simulate_bcs_kerr_overtones()
