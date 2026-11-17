#!/usr/bin/env python3
"""
Usage: python3 csv_cv_sweep.py UPS_DISK UPS_BUL ERR_FLOOR {all|ltg}
Reuses the CV code in csv_galaxy_cv.py; only the loader and settings change.
Vbar^2 = Vgas|Vgas| + UPS_DISK*Vdisk|Vdisk| + UPS_BUL*Vbul|Vbul|  (sign kept)
"""
import sys, os, glob, importlib.util
import numpy as np

ud, ub, floor, mode = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]

spec = importlib.util.spec_from_file_location("cv", "csv_galaxy_cv.py")
cv = importlib.util.module_from_spec(spec); spec.loader.exec_module(cv)

etg = set(open("etg_names.txt").read().split())

def load():
    gal, r, v, e, vb = [], [], [], [], []
    for fp in sorted(glob.glob(os.path.join(cv.DIR, "*_rotmod.dat"))):
        name = os.path.basename(fp).replace("_rotmod.dat", "")
        if mode == "ltg" and name in etg:
            continue
        d = np.loadtxt(fp, comments="#", ndmin=2)
        R, Vobs, errV, Vgas, Vdisk, Vbul = [d[:, i] for i in range(6)]
        s = (Vgas * np.abs(Vgas) + ud * Vdisk * np.abs(Vdisk) + ub * Vbul * np.abs(Vbul))
        Vbar = np.sign(s) * np.sqrt(np.abs(s))
        keep = (R > 0) & (Vobs > 0) & (Vbar > 0)
        gal += [name] * keep.sum()
        r.append(R[keep]); v.append(Vobs[keep])
        e.append(np.sqrt(errV[keep] ** 2 + floor ** 2))
        vb.append(Vbar[keep])
    return (np.array(gal), np.concatenate(r), np.concatenate(v),
            np.concatenate(e), np.concatenate(vb))

cv.load = load
cv.main()

tag = f"ud{ud}_ub{ub}_err{floor:g}_{mode}"
os.replace("csv_cv_results.csv", f"csv_cv_{tag}.csv")
print(f"\nSaved csv_cv_{tag}.csv")
