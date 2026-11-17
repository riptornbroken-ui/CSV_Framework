import glob
import numpy as np

V_PLATEAU = 150.0   # km/s, from the report
R_SCALE = 5.0       # kpc, from the report

def v2_bar(vgas, vdisk, vbulge):
    return vgas * np.abs(vgas) + vdisk * np.abs(vdisk) + vbulge * np.abs(vbulge)

def predict(rad, vgas, vdisk, vbulge, use_visc):
    v2 = v2_bar(vgas, vdisk, vbulge)
    if use_visc:
        v2 = v2 + V_PLATEAU**2 * rad / (R_SCALE + rad)
    return np.sqrt(np.maximum(0.0, v2))

def main(rotmod_dir):
    files = sorted(glob.glob(f"{rotmod_dir}/*_rotmod.dat"))
    res = {"baryons": [], "v25": []}
    n_gal = 0
    for f in files:
        d = np.loadtxt(f, comments="#")
        rad, vobs = d[:, 0], d[:, 1]
        vgas, vdisk, vbulge = d[:, 3], d[:, 4], d[:, 5]
        n_gal += 1
        res["baryons"].append(vobs - predict(rad, vgas, vdisk, vbulge, False))
        res["v25"].append(vobs - predict(rad, vgas, vdisk, vbulge, True))

    print(f"Galaxies: {n_gal}")
    for name, chunks in res.items():
        r = np.concatenate(chunks)
        print(f"{name:8s}  N={r.size}  mean residual={r.mean():8.2f} km/s  "
              f"RMSE={np.sqrt(np.mean(r**2)):8.2f} km/s")

if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/projects/csv_data_vault/rotmod_data")
    main(path)
