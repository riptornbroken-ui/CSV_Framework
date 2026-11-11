#!/usr/bin/env python3
import numpy as np

h = 6.62607015e-34
c = 299792458.0
nu = 1e10
freqs = [250.0, 500.0, 750.0]

for n, f in enumerate(freqs):
    E = h * f
    gamma = (nu / c**2) * (E**3) / (h / (2 * np.pi))
    gamma_h = (nu / c**2) * (E**3) / h
    print(f"n={n}, f={f}: gamma_hbar={gamma:.4e}, gamma_h={gamma_h:.4e}")
