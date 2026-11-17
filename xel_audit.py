#!/usr/bin/env python3
"""
CSV Framework V3.0: Audit of the xel shear term.
Reports both the raw (unbounded) and tanh-bounded expansion parameter,
so the bounding choice is visible rather than hidden.
"""
import math
import numpy as np

# --- CONSTANTS (as in the submitted script; none derived here) ---
L_XEL = 1.0e-40
C_LIGHT = 299792458.0
G_NEWTON = 6.67430e-11
HBAR = 1.054571817e-34
RHO_PLANCK = 5.155e96
RHO_CEIL = RHO_PLANCK * ((1.616255e-35 / L_XEL) ** 3)
RHO_0 = 1.0e-24
KAPPA_G = 1.8734
G_STAR = 1.2e-10

# Dimensionless viscous coupling: (kappa/rho0) has m^2/s; (c * L_XEL) has m^2/s.
VISC_SCALE = (KAPPA_G / RHO_0) / (C_LIGHT * L_XEL)


def density(g_bar):
    return min(RHO_0 * (1.0 + g_bar / KAPPA_G), RHO_CEIL)


def eps_raw(rho):
    energy = HBAR * C_LIGHT / (L_XEL ** 4)
    pressure = RHO_CEIL * C_LIGHT ** 2
    return (rho / RHO_0) * (energy / pressure)


def v_shear_sq(r, m, g_bar, mode="raw", coupling=VISC_SCALE):
    if m <= 0 or r <= 0:
        return 0.0, 0.0
    potential = G_NEWTON * m / r
    accel_frac = g_bar / (G_STAR + g_bar)
    e = eps_raw(density(g_bar))
    if mode == "bounded":
        e = math.tanh(e)
    corr = sum(((-1) ** (n + 1)) * e ** n / math.factorial(n) for n in range(1, 5))
    mult = 1.0 + coupling * corr
    return max(0.0, potential * accel_frac * mult), e


def predict(r, m, mode="raw", coupling=VISC_SCALE):
    g = G_NEWTON * m / r ** 2
    v_n_sq = G_NEWTON * m / r
    vs_sq, e = v_shear_sq(r, m, g, mode=mode, coupling=coupling)
    v_tot = math.sqrt(v_n_sq + vs_sq)
    return math.sqrt(v_n_sq), v_tot, e


def main():
    m = 1.0e10 * 1.98847e30   # 10 billion solar masses
    r = 1.0e20                # ~3.2 kpc

    print("=== 1. Newtonian limit (coupling = 0) must equal sqrt(GM/r) exactly ===")
    v_n, v_zero, _ = predict(r, m, coupling=0.0)
    print(f"   v_N = {v_n/1e3:.4f} km/s   v_model(coupling=0) = {v_zero/1e3:.4f} km/s")
    print(f"   PASS" if np.isclose(v_n, v_zero, rtol=1e-12) else "   FAIL")

    print("\n=== 2. Dimensional sanity of the expansion parameter ===")
    g = G_NEWTON * m / r ** 2
    e = eps_raw(density(g))
    print(f"   g_bar = {g:.3e} m/s^2")
    print(f"   eps_raw = {e:.4e}   (dimensionless; a perturbative series needs eps << 1)")

    print("\n=== 3. Prediction at r = 1e20 m, raw vs bounded ===")
    for mode in ("raw", "bounded"):
        v_n, v_tot, e_used = predict(r, m, mode=mode)
        print(f"   [{mode:7s}] eps = {e_used:.4e}  v_N = {v_n/1e3:.4f} km/s  "
              f"v_total = {v_tot/1e3:.4e} km/s  v_total/c = {v_tot/C_LIGHT:.4e}")

    print("\n=== 4. Inner-disk check at r = 1e17 m ===")
    r_in = 1.0e17
    for mode in ("raw", "bounded"):
        v_n, v_tot, _ = predict(r_in, m, mode=mode)
        print(f"   [{mode:7s}] v_N = {v_n/1e3:.2f} km/s  v_total/v_N = {v_tot/v_n:.4e}")

    print("\nNote: the 'bounded' rows are a sensitivity test, not physics. "
          "tanh caps eps at 1 but does not make the series valid.")


if __name__ == "__main__":
    main()
