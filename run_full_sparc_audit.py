#!/usr/bin/env python3
"""
CSV Framework V3.0: Full-Scale SPARC Empirical Audit & MOND Comparison Suite
Author: Jesse Arron Gillispie
"""

import os
import sys
import glob
import math
import numpy as np

# Ensure CSV_Framework directory is in path to import baseline engine
sys.path.append(os.path.abspath("CSV_Framework"))
import csv_baseline_v3 as csv3

G_STAR_MOND = 1.2e-10  # MOND acceleration scale a0

def mond_velocity(v_bar_sq, r_m):
    val = 1.0 + (4.0 * G_STAR_MOND * r_m) / np.maximum(v_bar_sq, 1.0)
    v_mond_sq = 0.5 * v_bar_sq * (1.0 + np.sqrt(np.maximum(val, 1.0)))
    return np.sqrt(v_mond_sq)

def evaluate_full_audit():
    print("=== CSV V3.0 FULL SPARC BATCH AUDIT SUITE ===")
    
    # Search for all disk profile files across current and subdirectories
    disk_files = glob.glob("*_disk.dat") + glob.glob("**/*_disk.dat", recursive=True)
    if not disk_files:
        disk_files = glob.glob("*.dat") + glob.glob("**/*.dat", recursive=True)
        
    if not disk_files:
        print("[NO GALAXY FILES FOUND] Please ensure SPARC profile files are present.")
        return

    # Deduplicate file paths
    disk_files = sorted(list(set(disk_files)))
    print(f"[FOUND] {len(disk_files)} galaxy profiles to process.")

    total_chi2_csv = 0.0
    total_chi2_mond = 0.0
    valid_count = 0

    for disk_path in disk_files:
        base_dir = os.path.dirname(disk_path)
        basename = os.path.basename(disk_path)
        prefix = basename.replace("_disk.dat", "").replace(".dat", "")
        bulge_path = os.path.join(base_dir, prefix + "_bulge.dat") if base_dir else prefix + "_bulge.dat"
        
        try:
            disk_data = np.loadtxt(disk_path)
            if disk_data.size == 0:
                continue
                
            if disk_data.ndim == 1:
                disk_data = np.array([disk_data])
                
            r_kpc = disk_data[:, 0]
            v_obs = disk_data[:, 1]
            v_err = disk_data[:, 2] if disk_data.shape[1] > 2 else np.full_like(r_kpc, 5.0)
            v_disk = disk_data[:, 4] if disk_data.shape[1] > 4 else disk_data[:, 1]
            v_gas = disk_data[:, 3] if disk_data.shape[1] > 3 else np.zeros_like(r_kpc)
            
            v_bulge = np.zeros_like(r_kpc)
            if os.path.exists(bulge_path):
                bulge_data = np.loadtxt(bulge_path)
                if bulge_data.size > 0:
                    if bulge_data.ndim == 1:
                        bulge_data = np.array([bulge_data])
                    if bulge_data.shape[1] > 1:
                        v_bulge = bulge_data[:, 1]

            r_m = r_kpc * 3.085677581e19
            
            chi2_c = 0.0
            chi2_m = 0.0
            points = 0

            for i in range(len(r_m)):
                r = r_m[i]
                if r <= 0:
                    continue
                
                vg = v_gas[i]
                vd = v_disk[i]
                vb = v_bulge[i]
                
                v_bar_sq = (np.sign(vg)*vg**2) + (0.5 * np.sign(vd)*vd**2) + (0.7 * np.sign(vb)*vb**2)
                m_bar = max((v_bar_sq * r) / csv3.G_NEWTON, 1.0e30)
                
                res_csv = csv3.predict_velocity(r, m_bar, alpha=1.0)
                v_c = res_csv["v_total"] / 1e3
                
                v_m = mond_velocity(np.array([max(v_bar_sq, 0.0)]), np.array([r]))[0] / 1e3
                
                err = max(v_err[i], 2.0)
                obs = v_obs[i]
                
                chi2_c += ((obs - v_c) / err) ** 2
                chi2_m += ((obs - v_m) / err) ** 2
                points += 1

            if points > 0:
                total_chi2_csv += (chi2_c / points)
                total_chi2_mond += (chi2_m / points)
                valid_count += 1

        except Exception as e:
            continue

    if valid_count > 0:
        print("\n" + "="*60)
        print(f" FULL BATCH AUDIT COMPLETE ({valid_count} Galaxies Evaluated)")
        print("="*60)
        print(f"  Mean CSV V3.0 Baseline χ²/N : {total_chi2_csv / valid_count:.4f}")
        print(f"  Mean MOND Baseline χ²/N    : {total_chi2_mond / valid_count:.4f}")
        print(f"  CSV minus MOND Difference  : {(total_chi2_csv - total_chi2_mond) / valid_count:+.4f}")
        print("="*60)
    else:
        print("[ERROR] No valid galaxy records could be successfully computed.")

if __name__ == "__main__":
    evaluate_full_audit()
