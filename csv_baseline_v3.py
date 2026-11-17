#!/usr/bin/env python3
"""
CSV Framework V3.0: Clean Mathematical Baseline Engine
Author: Jesse Arron Gillispie
"""

import math
import numpy as np

C_LIGHT = 299792458.0
G_NEWTON = 6.67430e-11
HBAR = 1.054571817e-34

L_XEL = 1.0e-40
RHO_PLANCK = 5.155e96
RHO_CEIL = RHO_PLANCK * ((1.616255e-35 / L_XEL) ** 3)
RHO_0 = 1.0e-24
KAPPA_G = 1.8734
G_DAGGER = 1.2e-10


def effective_lattice_density(g_bar: float) -> float:
    rho = RHO_0 * (1.0 + (g_bar / G_DAGGER))
    return min(rho, RHO_CEIL)


def dimensionless_weissenberg(r: float, v_n: float, rho_eff: float) -> float:
    denom = rho_eff * v_n * r
    if denom <= 0.0:
        return 0.0
    return KAPPA_G / denom


def constitutive_shear_response(w_num: float, alpha: float = 1.0) -> float:
    return alpha * (w_num / (1.0 + w_num))


def predict_velocity(r: float, m_bar: float, alpha: float = 1.0) -> dict:
    if r <= 0.0 or m_bar <= 0.0:
        return {"r": r, "g_bar": 0.0, "v_N": 0.0, "v_total": 0.0}

    g_bar = (G_NEWTON * m_bar) / (r ** 2)
    v_n_sq = (G_NEWTON * m_bar) / r
    v_n = math.sqrt(v_n_sq)

    gate = G_DAGGER / (G_DAGGER + g_bar)
    rho_eff = effective_lattice_density(g_bar)
    w_num = dimensionless_weissenberg(r, v_n, rho_eff)
    phi = constitutive_shear_response(w_num, alpha=alpha)

    # Asymptotic flat rotation scaling boost factor (1/4 power law for Tully-Fisher alignment)
    tf_scale = (G_DAGGER / max(g_bar, 1e-18)) ** 0.25

    v_shear_sq = v_n_sq * gate * tf_scale * phi
    v_total = math.sqrt(v_n_sq + v_shear_sq)

    return {
        "r": r,
        "g_bar": g_bar,
        "v_N": v_n,
        "v_total": v_total,
        "ratio_v": v_total / v_n
    }
