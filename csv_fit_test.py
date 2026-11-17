#!/usr/bin/env python3
"""
Bounded CSV interpolation vs Newtonian baryons vs MOND, fit on train, scored on test.

Input CSV (optional): columns r_kpc, v_obs, v_err, v_bar  (km/s, km/s, km/s)
  e.g. SPARC mass models. Pass the path as argv[1].
If no file is given, a SYNTHETIC test set is generated. Synthetic results only
check that the pipeline works; they say nothing about nature.

Units: v in km/s, r in kpc, accelerations in m/s^2 (a0 ~ 1.2e-10 m/s^2).
"""
import sys
import numpy as np

KPC = 3.0857e19   # m
KMS = 1.0e3       # m/s per km/s

def g_from(v_kms, r_kpc):
    return (v_kms * KMS) ** 2 / (r_kpc * KPC)

def v2_newton(vbar):
    return vbar ** 2

def v2_csv(vbar, r, K, a0):
    """Bounded interpolation: f = a0/(a0+g_bar) in (0,1]; K >= 0 is the amplitude."""
    gbar = g_from(vbar, r)
    f = a0 / (a0 + gbar)
    return vbar ** 2 * (1.0 + K * f)

def v2_mond(vbar, r, a0):
    """Milgrom simple interpolation: g_obs = g_bar * nu(g_bar/a0), nu(y)=1/2+sqrt(1/4+1/y)."""
    gbar = g_from(vbar, r)
    y = gbar / a0
    gobs = gbar * (0.5 + np.sqrt(0.25 + 1.0 / y))
    return gobs * r * KPC / KMS ** 2   # back to (km/s)^2

def chi2(v2_model, vobs, verr):
    v_pred = np.sqrt(np.maximum(v2_model, 0.0))
    return np.sum(((vobs - v_pred) / verr) ** 2)

def load_or_synth(path):
    if path:
        d = np.genfromtxt(path, delimiter=",", names=True)
        return d["r_kpc"], d["v_obs"], d["v_err"], d["v_bar"], "REAL: " + path
    rng = np.random.default_rng(0)
    n = 120
    r = rng.uniform(1.0, 30.0, n)
    vbar = 80 * np.sqrt(r / (r + 3.0)) + rng.normal(0, 3, n)
    vbar = np.clip(vbar, 5, None)
    a0_true = 1.2e-10
    vobs_true = np.sqrt(v2_mond(vbar, r, a0_true))
    verr = np.full(n, 5.0)
    vobs = vobs_true + rng.normal(0, 5.0, n)
    return r, vobs, verr, vbar, "SYNTHETIC (pipeline check only)"

def grid_fit_csv(r, vobs, verr, vbar):
    best = (np.inf, None, None)
    for K in np.linspace(0.0, 10.0, 201):
        for a0 in np.logspace(-11.5, -9.0, 101):
            c = chi2(v2_csv(vbar, r, K, a0), vobs, verr)
            if c < best[0]:
                best = (c, K, a0)
    return best

def grid_fit_mond(r, vobs, verr, vbar):
    best = (np.inf, None)
    for a0 in np.logspace(-11.5, -9.0, 301):
        c = chi2(v2_mond(vbar, r, a0), vobs, verr)
        if c < best[0]:
            best = (c, a0)
    return best

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else None
    r, vobs, verr, vbar, label = load_or_synth(path)
    print(f"Data source: {label}   N = {len(r)}")

    # --- Limit checks (must hold regardless of data) ---
    print("\n[Limit checks]")
    K_test, a0_test = 5.0, 1.2e-10
    r_hi = np.array([1.0e-3])          # 1 pc: very high acceleration
    vb = np.array([100.0])
    ratio_hi = v2_csv(vb, r_hi, K_test, a0_test)[0] / vb[0] ** 2
    print(f"  high-g  v_csv^2/v_bar^2 = {ratio_hi:.12f}  (expect 1)")
    r_lo = np.array([1.0e6])           # very low acceleration
    vb_lo = np.array([1.0])
    ratio_lo = v2_csv(vb_lo, r_lo, K_test, a0_test)[0] / vb_lo[0] ** 2
    print(f"  low-g   v_csv^2/v_bar^2 = {ratio_lo:.6f}  (expect 1+K = {1+K_test})")

    # --- Train/test split (fixed seed, half and half) ---
    rng = np.random.default_rng(1)
    idx = rng.permutation(len(r))
    tr, te = idx[: len(r) // 2], idx[len(r) // 2:]

    c_csv, K_hat, a0_csv = grid_fit_csv(r[tr], vobs[tr], verr[tr], vbar[tr])
    c_mond, a0_mond = grid_fit_mond(r[tr], vobs[tr], verr[tr], vbar[tr])

    print("\n[Fit on train half]")
    print(f"  CSV   : K_c = {K_hat:.3f}, a0 = {a0_csv:.3e} m/s^2, chi2/N = {c_csv/len(tr):.3f}")
    print(f"  MOND  : a0  = {a0_mond:.3e} m/s^2, chi2/N = {c_mond/len(tr):.3f}")

    # --- Held-out test ---
    t = (r[te], vobs[te], verr[te], vbar[te])
    chi_newt = chi2(v2_newton(t[3]), t[1], t[2]) / len(te)
    chi_csv = chi2(v2_csv(t[3], t[0], K_hat, a0_csv), t[1], t[2]) / len(te)
    chi_mond = chi2(v2_mond(t[3], t[0], a0_mond), t[1], t[2]) / len(te)

    print("\n[Held-out test half, chi2/N]")
    print(f"  Newtonian baryons only : {chi_newt:.3f}")
    print(f"  CSV (bounded)          : {chi_csv:.3f}")
    print(f"  MOND (simple)          : {chi_mond:.3f}")
    best = min([("Newtonian", chi_newt), ("CSV", chi_csv), ("MOND", chi_mond)], key=lambda x: x[1])
    print(f"\nLowest held-out chi2: {best[0]}")
    print("A win on held-out data is evidence only for this dataset; it does not confirm K_c or the framework.")

if __name__ == "__main__":
    main()
