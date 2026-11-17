import numpy as np

def verify_csv_dispersion():
    c = 299792458.0                     # Speed of light in m/s
    M_pl_GeV = 1.22e19                  # Planck energy scale in GeV
    E_low = 1.0                         # Low-energy photon (1 GeV)
    E_high = 100.0                      # High-energy gamma-ray photon (100 GeV)
    distance_mpc = 3000.0               # Cosmological distance (~3 billion light-years in Mpc)
    meters_per_mpc = 3.0857e22          # Conversion factor
    L_dist = distance_mpc * meters_per_mpc
    
    xi_2 = 1.0                          # CSV Quadratic coupling coefficient
    
    delta_t_quadratic = (xi_2 / 2.0) * (L_dist / c) * ((E_high**2 - E_low**2) / (M_pl_GeV**2))
    
    print("=== CSV DISPERSION SUPPRESSION VERIFICATION ===")
    print(f"Distance Baseline : {distance_mpc} Mpc")
    print(f"Energy Window     : {E_low} GeV to {E_high} GeV")
    print(f"Calculated Delta T: {delta_t_quadratic:.4e} seconds")
    
    if abs(delta_t_quadratic) < 0.03:
        print("[SUCCESS] Quadratic dispersion delay is within Fermi-LAT limits.")
    else:
        print("[WARNING] Dispersion delay exceeds observational bounds.")

if __name__ == "__main__":
    verify_csv_dispersion()
