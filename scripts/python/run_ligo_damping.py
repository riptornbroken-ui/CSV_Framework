#!/usr/bin/env python3
"""
Chromatic Spacetime Viscosity (CSV) Framework v2.5
Kerr Spin & Overtone Mode (n=0,1,2) Damping Simulation
"""

import numpy as np

def simulate_kerr_overtones():
    print("[*] Initializing CSV Kerr Spin & Overtone Damping Simulation...")
    
    M = 60.0 # Solar masses
    # Characteristic fundamental QNM frequency for Schwarzschild/slow Kerr (approximate scaling)
    f_base = 32.0 / M * 1000.0 # Hz roughly ~533 Hz for 60 M_sun
    
    # Overtone multiplier factors (n=0, n=1, n=2)
    overtones = {
        "n=0 (Fundamental)": 1.0,
        "n=1 (1st Overtone)": 1.18,
        "n=2 (2nd Overtone)": 1.35
    }
    
    spins = [0.0, 0.7, 0.9] # Dimensionless spin parameter a*
    nu_bound = 1.0e12 # m^2/s observational ceiling
    c = 3.0e8
    
    print("    -------------------------------------------------------------------")
    print(f"    {'Overtone':<22} {'Spin (a*)':<10} {'Freq (Hz)':<12} {'Damping (s^-1)':<15} {'Status':<10}")
    print("    -------------------------------------------------------------------")
    
    for name, mult in overtones.items():
        for a in spins:
            # Spin correction factor for frequency roughly (1 + 0.3 * a)
            f_qnm = f_base * mult * (1.0 + 0.3 * a)
            k_gw = (2 * np.pi * f_qnm) / c
            gamma = nu_bound * (k_gw ** 2)
            status = "Constrained" if gamma > 25.0 else "Safe"
            print(f"    {name:<22} {a:<10.1f} {f_qnm:<12.1f} {gamma:<15.2e} {status:<10}")
            
    print("    -------------------------------------------------------------------")
    print("[+] Kerr Overtone Simulation Complete.")

if __name__ == '__main__':
    simulate_kerr_overtones()

