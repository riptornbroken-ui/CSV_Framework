#!/usr/bin/env python3
"""
CSV Framework V3.0: SPARC Data Ingest & Evaluation Pipeline
Author: Jesse Arron Gillispie
"""

import os
import glob
import numpy as np
import csv_baseline_v3 as csv3

def evaluate_sparc_directory(data_dir="data/"):
    print(f"=== CSV V3.0 SPARC EMPIRICAL AUDIT PIPELINE ===")
    
    if not os.path.exists(data_dir):
        print(f"[WARNING] Directory '{data_dir}' not found. Looking for CSVs in current path...")
        search_path = "*.csv"
    else:
        search_path = os.path.join(data_dir, "*.csv")
        
    files = glob.glob(search_path)
    if not files:
        print("[NO CSV DATA FOUND] Please place SPARC rotation curve CSVs in data/ or current directory.")
        return

    print(f"[FOUND] {len(files)} SPARC galaxy data files. Processing baseline fit...")
    
    total_chi2_csv = 0.0
    total_chi2_mond = 0.0
    valid_galaxies = 0

    for filepath in files:
        try:
            # Expected format: Radius(kpc), V_obs, error, V_gas, V_disk, V_bulge
            data = np.loadtxt(filepath, delimiter=",", skiprows=1)
            if data.size == 0:
                continue
                
            r_kpc = data[:, 0]
            v_obs = data[:, 1]
            v_err = data[:, 2]
            v_gas = data[:, 3]
            v_disk = data[:, 4]
            v_bulge = data[:, 5] if data.shape[1] > 5 else np.zeros_like(r_kpc)
            
            r_m = r_kpc * 3.085677581e19  # kpc to meters
            
            # Baryonic mass profile estimation
            v_bar_sq = np.abs(v_gas)*v_gas + 0.5*np.abs(v_disk)*v_disk + 0.7*np.abs(v_bulge)*v_bulge
            m_bar = (v_bar_sq * r_m) / csv3.G_NEWTON
            
            chi2_csv = 0.0
            for i in range(len(r_m)):
                if r_m[i] <= 0 or m_bar[i] <= 0:
                    continue
                res = csv3.predict_velocity(r_m[i], m_bar[i], alpha=1.0)
                v_model = res["v_total"] / 1e3  # convert to km/s
                err = max(v_err[i], 2.0)  # floor error at 2 km/s
                chi2_csv += ((v_obs[i] - v_model) / err) ** 2
                
            valid_galaxies += 1
            total_chi2_csv += chi2_csv / max(len(r_m), 1)
        except Exception as e:
            continue

    if valid_galaxies > 0:
        print(f"\n[AUDIT RESULTS ACROSS {valid_galaxies} GALAXIES]")
        print(f"  Mean CSV Baseline Chi2/N: {total_chi2_csv / valid_galaxies:.4f}")
    else:
        print("[INFO] Files found, but format parsing requires standard SPARC column mapping.")

if __name__ == "__main__":
    evaluate_sparc_directory()
