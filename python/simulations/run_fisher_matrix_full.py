import numpy as np

# Physical Constants (SI)
C = 2.99792458e8
G = 6.67430e-11
M_SUN = 1.98847e30
MPC = 3.08567758e22

def bcs_kerr_modes(mass_msun, spin_j):
    """
    Berti-Cardoso-Starinets (BCS) analytical fits for Kerr (l=2, m=2, n=0,1,2).
    Returns list of dicts with angular frequency omega_0 (rad/s) and tau_gr (s).
    """
    t_m = (G * mass_msun * M_SUN) / (C**3)  # Geometric mass in seconds
    
    # BCS fit coefficients: (f1, f2, f3, q1, q2, q3)
    bcs_coeffs = [
        (1.5251, -1.1568, 0.1292, 0.7000, 1.4187, -0.4990),  # n = 0
        (1.3673, -1.0260, 0.1628, 0.1000, 0.5436, -0.4731),  # n = 1
        (1.1107, -0.8087, 0.2116, 0.0300, 0.3037, -0.4539),  # n = 2
    ]
    amps = [1.0, 0.45, 0.20]
    
    modes = []
    for n, (f1, f2, f3, q1, q2, q3) in enumerate(bcs_coeffs):
        m_omega_r = f1 + f2 * ((1.0 - spin_j) ** f3)
        q_factor = q1 + q2 * ((1.0 - spin_j) ** q3)
        
        omega_0 = m_omega_r / t_m
        tau_gr = (2.0 * q_factor) / omega_0
        modes.append({
            "n": n,
            "omega_0": omega_0,
            "tau_gr": tau_gr,
            "amp": amps[n]
        })
    return modes

def ringdown_strain_fd(freqs, modes, nu_eff, beta=1.0, strain_scale=1e-21):
    """
    Frequency-domain Lorentzian ringdown waveform h_tilde(f) under Gamma_hbar convention:
    1 / tau_eff = 1 / tau_gr + (beta * nu_eff * omega_0^2) / (2 * c^2)
    """
    omega = 2.0 * np.pi * freqs
    h_tilde = np.zeros_like(freqs, dtype=np.complex128)
    
    for m in modes:
        w0 = m["omega_0"]
        gamma_csv = (beta * nu_eff * (w0**2)) / (2.0 * C**2)
        gamma_tot = (1.0 / m["tau_gr"]) + gamma_csv
        
        # Damped sinusoid Fourier transform (cosine phase convention)
        denom = (gamma_tot + 1j * omega)**2 + w0**2
        h_tilde += strain_scale * m["amp"] * (gamma_tot + 1j * omega) / denom
        
    return h_tilde

def detector_psd(freqs, detector="LIGO"):
    """Analytical noise Power Spectral Density S_n(f) [1/Hz] approximations."""
    f = np.maximum(freqs, 5.0)
    if detector == "LIGO":
        # Advanced LIGO design sensitivity approximation
        f0 = 215.0
        x = f / f0
        return 1e-48 * (x**(-4.14) - 5.0 * x**(-2.0) + 111.0 * ((1.0 - x**2 + 0.5 * x**4) / (1.0 + 0.5 * x**2)))
    elif detector == "ET":
        # Einstein Telescope (ET-D) approximation
        x = f / 100.0
        return 1.5e-50 * (x**(-4.0) + 2.0 * x**(-1.5) + 0.8 * x**2)
    elif detector == "CE":
        # Cosmic Explorer (40 km) approximation
        x = f / 100.0
        return 8.0e-51 * (x**(-4.2) + 1.5 * x**(-1.2) + 0.6 * x**2)
    raise ValueError("Unknown detector")

def compute_fisher_bound(mass_msun=65.0, spin_j=0.68, dist_mpc=400.0, detector="LIGO"):
    """Computes Ringdown SNR and 1-sigma Fisher bound on nu_eff."""
    freqs = np.linspace(20.0, 2048.0, 16384)
    df = freqs[1] - freqs[0]
    
    # Scale characteristic ringdown amplitude with M / d_L
    h0 = 1.5e-21 * (mass_msun / 65.0) * (400.0 / dist_mpc)
    modes = bcs_kerr_modes(mass_msun, spin_j)
    psd = detector_psd(freqs, detector)
    
    # Baseline GR waveform (nu_eff = 0) and numerical derivative dh/d(nu_eff)
    d_nu = 1e6
    h_0 = ringdown_strain_fd(freqs, modes, nu_eff=0.0, strain_scale=h0)
    h_plus = ringdown_strain_fd(freqs, modes, nu_eff=d_nu, strain_scale=h0)
    dh_dnu = (h_plus - h_0) / d_nu
    
    # SNR and Fisher Element Gamma_{nu, nu}
    snr_sq = 4.0 * np.sum((np.abs(h_0)**2) / psd) * df
    gamma_nunu = 4.0 * np.sum((np.abs(dh_dnu)**2) / psd) * df
    
    sigma_nu = 1.0 / np.sqrt(gamma_nunu)
    return np.sqrt(snr_sq), sigma_nu

if __name__ == "__main__":
    print("[*] CSV Fisher Matrix Forecast (M = 65 M_sun, j = 0.68, d_L = 400 Mpc)")
    print("-" * 68)
    for det in ["LIGO", "ET", "CE"]:
        snr, bound = compute_fisher_bound(detector=det)
        print(f"{det:<6} | Ringdown SNR: {snr:7.2f} | 1-sigma Bound: nu_eff <= {bound:.3e} m^2/s")
