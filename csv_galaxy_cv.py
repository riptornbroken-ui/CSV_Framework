#!/usr/bin/env python3
"""
Galaxy-level 5-fold cross-validation, repeated over 5 seeds.
Models: Newtonian baryons, simple MOND, bounded CSV (K * a0/(a0+g_bar)).
Each galaxy is entirely in train or entirely in test.
"""
import glob, os
import numpy as np

KPC = 3.0857e19
KMS = 1.0e3
DIR = os.path.expanduser("~/projects/csv_data_vault/rotmod_data")
ERR_FLOOR = 5.0      # km/s, added in quadrature (a choice; change if needed)
N_FOLDS = 5
SEEDS = range(5)

def load():
    gal, r, v, e, vb = [], [], [], [], []
    for fp in sorted(glob.glob(os.path.join(DIR, "*_rotmod.dat"))):
        name = os.path.basename(fp).replace("_rotmod.dat", "")
        d = np.loadtxt(fp, comments="#", ndmin=2)
        R, Vobs, errV, Vgas, Vdisk, Vbul = [d[:, i] for i in range(6)]
        s = Vgas * np.abs(Vgas) + Vdisk * np.abs(Vdisk) + Vbul * np.abs(Vbul)
        Vbar = np.sign(s) * np.sqrt(np.abs(s))
        keep = (R > 0) & (Vobs > 0) & (Vbar > 0)
        gal += [name] * keep.sum()
        r.append(R[keep]); v.append(Vobs[keep])
        e.append(np.sqrt(errV[keep] ** 2 + ERR_FLOOR ** 2))
        vb.append(Vbar[keep])
    return (np.array(gal), np.concatenate(r), np.concatenate(v),
            np.concatenate(e), np.concatenate(vb))

def g_from(vb, r):
    return (vb * KMS) ** 2 / (r * KPC)

def v2_newton(vb):
    return vb ** 2

def v2_csv(vb, r, K, a0):
    f = a0 / (a0 + g_from(vb, r))
    return vb ** 2 * (1.0 + K * f)

def v2_mond(vb, r, a0):
    gb = g_from(vb, r)
    y = gb / a0
    gobs = gb * (0.5 + np.sqrt(0.25 + 1.0 / y))
    return gobs * r * KPC / KMS ** 2

def chi2(v2m, v, e):
    vp = np.sqrt(np.maximum(v2m, 0.0))
    return np.sum(((v - vp) / e) ** 2)

def fit_csv(r, v, e, vb):
    best = (np.inf, None, None)
    for K in np.linspace(0.0, 10.0, 101):
        for a0 in np.logspace(-11.5, -9.0, 81):
            c = chi2(v2_csv(vb, r, K, a0), v, e)
            if c < best[0]:
                best = (c, K, a0)
    return best[1], best[2]

def fit_mond(r, v, e, vb):
    best = (np.inf, None)
    for a0 in np.logspace(-11.5, -9.0, 301):
        c = chi2(v2_mond(vb, r, a0), v, e)
        if c < best[0]:
            best = (c, a0)
    return best[1]

def main():
    gal, r, v, e, vb = load()
    names = np.unique(gal)
    print(f"galaxies: {len(names)}   points after cuts: {len(r)}")
    rows = []
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        folds = np.array_split(rng.permutation(names), N_FOLDS)
        for k, f in enumerate(folds):
            te = np.isin(gal, f)
            tr = ~te
            K, a0c = fit_csv(r[tr], v[tr], e[tr], vb[tr])
            a0m = fit_mond(r[tr], v[tr], e[tr], vb[tr])
            n = te.sum()
            cn = chi2(v2_newton(vb[te]), v[te], e[te]) / n
            cc = chi2(v2_csv(vb[te], r[te], K, a0c), v[te], e[te]) / n
            cm = chi2(v2_mond(vb[te], r[te], a0m), v[te], e[te]) / n
            rows.append((seed, k, K, a0c, a0m, cn, cc, cm))
            print(f"seed {seed} fold {k}: K={K:.2f} a0_csv={a0c:.2e} a0_mond={a0m:.2e} "
                  f"chi2/N newton={cn:.2f} csv={cc:.2f} mond={cm:.2f}", flush=True)

    R = np.array(rows)
    out = os.path.expanduser("~/projects/CSV_Framework/csv_cv_results.csv")
    np.savetxt(out, R, delimiter=",", fmt="%.6g",
               header="seed,fold,K,a0_csv,a0_mond,chi2_newton,chi2_csv,chi2_mond", comments="")
    cn, cc, cm = R[:, 5], R[:, 6], R[:, 7]
    print("\n=== Held-out chi2/N across all folds (mean +/- sd) ===")
    print(f"  Newtonian baryons : {cn.mean():.3f} +/- {cn.std():.3f}")
    print(f"  MOND (simple)     : {cm.mean():.3f} +/- {cm.std():.3f}")
    print(f"  CSV (bounded)     : {cc.mean():.3f} +/- {cc.std():.3f}")
    d = cc - cm
    print(f"\nCSV minus MOND per fold: mean {d.mean():+.3f}, CSV better in "
          f"{(d < 0).sum()} of {len(d)} folds")
    print(f"K spread across folds: {R[:,2].min():.2f} to {R[:,2].max():.2f}")
    print(f"\nWrote {out}")

if __name__ == "__main__":
    main()
