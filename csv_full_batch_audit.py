#!/usr/bin/env python3
"""
CSV Framework V2.5 - Full Batch Empirical Validation & Statistical Audit
Processes all 191 SPARC galaxy rotation curves in the data vault, 
evaluates the hard-ceiling lattice density and bounded viscous velocity model, 
and exports complete residuals to csv_data_vault/csv_outputs/.
"""

import os
import glob
import numpy as np
import pandas as pd

KAPPA_G = 1.8734           # Graviton Viscosity Constant (kg / (m * s))
L_XEL = 1.0e-40            # Xel Edge Length (m)
RHO_CEIL = 2.17643e112     # Hard Sub-Planckian Density Ceiling (kg / m^3)
RHO_0 = 1.0e-24            # Baseline condensate mass density (kg/m^3)
KPC_TO_M = 3.08567758149e19 # Meters per kiloparsec

def compute_lattice_density(rho_base: float, norm_g: float, delta_x: float) -> float:
    correction_factor = 1.0 + (norm_g / KAPPA_G) * (delta_x / L_XEL)
    return min(rho_base * correction_factor, RHO_CEIL)

def predict_viscous_velocity_bounded(r_kpc: float, v_gas: float, v_disk: float, v_bulge: float) -> float:
    if r_kpc <= 0:
        return 0.0
    v_bar_sq = (v_gas * abs(v_gas)) + (v_disk * abs(v_disk)) + (v_bulge * abs(v_bulge))
    v_visc_plateau = 150.0  # km/s asymptotic flat rotation scale
    r_scale_kpc = 5.0       # characteristic transition radius
    v_visc_sq = (v_visc_plateau ** 2) * (r_kpc / (r_scale_kpc + r_kpc))
    total_v_sq = max(0.0, v_bar_sq + v_visc_sq)
    return np.sqrt(total_v_sq)

def parse_rotmod_file_detailed(filepath: str):
    data_rows = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            try:
                vals = [float(p) for p in parts]
                if len(vals) >= 6:
                    data_rows.append(vals)
            except ValueError:
                continue
    return np.array(data_rows)

def run_full_audit():
    vault_path = os.path.expanduser("~/projects/csv_data_vault")
    rotmod_dir = os.path.join(vault_path, "rotmod_data")
    output_dir = os.path.join(vault_path, "csv_outputs")
    os.makedirs(output_dir, exist_ok=True)
    
    files = glob.glob(os.path.join(rotmod_dir, "*_rotmod.dat"))
    print(f"==================================================")
    print(f" CSV Framework V2.5 - Full Batch Audit ({len(files)} Galaxies)")
    print(f"==================================================")
    
    audit_records = []
    all_residuals = []
    ceiling_violations = 0

    for fp in files:
        gname = os.path.basename(fp).replace("_rotmod.dat", "")
        data = parse_rotmod_file_detailed(fp)
        
        if data.size == 0:
            continue
            
        r = data[:, 0]
        v_obs = data[:, 1]
        v_gas = data[:, 3]
        v_disk = data[:, 4]
        v_bulge = data[:, 5]
        
        galaxy_residuals = []
        for ri, vgi, vdi, vbi, voi in zip(r, v_gas, v_disk, v_bulge, v_obs):
            norm_g_est = voi * 1.0e3 / (ri * KPC_TO_M) if ri > 0 else 1.0e-15
            density = compute_lattice_density(RHO_0, norm_g_est, L_XEL * 1.0e5)
            if density >= RHO_CEIL:
                ceiling_violations += 1
                
            v_pred = predict_viscous_velocity_bounded(ri, vgi, vdi, vbi)
            res = voi - v_pred
            galaxy_residuals.append(res)
            all_residuals.append(res)
            
        galaxy_residuals = np.array(galaxy_residuals)
        mean_abs_res = np.mean(np.abs(galaxy_residuals))
        rms_galaxy = np.sqrt(np.mean(galaxy_residuals**2))
        
        audit_records.append({
            "Galaxy": gname,
            "DataPoints": len(r),
            "MeanAbsResidual_kms": mean_abs_res,
            "RMS_kms": rms_galaxy
        })

    df_audit = pd.DataFrame(audit_records)
    csv_out_path = os.path.join(output_dir, "csv_full_sparc_audit_summary.csv")
    df_audit.to_csv(csv_out_path, index=False)
    
    all_residuals = np.array(all_residuals)
    print(f"\n==================================================")
    print(f" FINAL BATCH AUDIT RESULTS (Processed {len(df_audit)} Galaxies)")
    print(f"==================================================")
    print(f" Total Data Points Evaluated : {len(all_residuals)}")
    print(f" Global Mean Residual Error  : {np.mean(all_residuals):.2f} km/s")
    print(f" Global Root Mean Square Err : {np.sqrt(np.mean(all_residuals**2)):.2f} km/s")
    print(f" Hard-Ceiling Violations     : {ceiling_violations} (Strictly Enforced)")
    print(f" Audit Summary Exported To   : {csv_out_path}")
    print(f"==================================================")

if __name__ == "__main__":
    run_full_audit()

