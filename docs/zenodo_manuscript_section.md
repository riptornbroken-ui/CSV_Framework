## 2. Notation, Conventions, and Dissipative Overtone Mapping

To ensure rigorous mathematical consistency between the microscopic quantum dispersion relation and macroscopic gravitational-wave ringdown observables, the Chromatic Spacetime Viscosity (CSV) framework v2.5 adopts standardized conventions aligned with modern black hole perturbation theory and third-generation (3G) detector pipelines.

### 2.1 The $\Gamma_{\hbar}$ Normalization Convention

In high-curvature spacetime regimes, quantum-corrected dissipative effects are governed by the strain-gated dissipation rate. We define the fundamental energy-dependent rate utilizing the reduced Planck constant ($\hbar = \frac{h}{2\pi}$):

$$\Gamma_{\hbar} = \beta \left(\frac{\nu_{\text{eff}}}{c^2}\right) \frac{E^3}{\hbar}$$

where $\nu_{\text{eff}}$ represents the effective spacetime kinematic viscosity, $\beta$ is a dimensionless coupling constant, $c$ is the speed of light, and $E = \hbar \omega$ is the quantum energy associated with mode angular frequency $\omega = 2\pi f$. 

Adopting $\Gamma_{\hbar}$ rather than standard Planck's constant ($h$) ensures clean dimensional cancellation when deriving the imaginary damping frequency component ($\omega_I$). Because quantum energy scales linearly with angular frequency, dividing the dissipation rate by $2\hbar E$ eliminates $\hbar$ directly without introducing extraneous $2\pi$ scaling factors into exponential phase expressions ($e^{-i\tilde{\omega} t}$):

$$\omega_{I, \text{CSV}} = \frac{\beta \, \nu_{\text{eff}} \, \omega^2}{2c^2}$$

### 2.2 Berti-Cardoso-Starinets (BCS) Kerr Quasinormal Mode Mapping

Quasinormal mode (QNM) ringdown waveforms are decomposed into a superposition of damped sinusoids characterized by complex frequencies $\tilde{\omega}_n$:

$$\tilde{\omega}_n = \omega_n - i\omega_{I,n} = 2\pi f_n - \frac{i}{\tau_n^{\text{GR}}}$$

where $n \in \{0, 1, 2\}$ indexes the fundamental mode and higher overtones, $f_n$ represents the oscillation frequency, and $\tau_n^{\text{GR}}$ denotes the characteristic General Relativity damping time derived from Kerr analytical fits. 

Under the CSV framework, the inclusion of strain-gated spacetime viscosity modifies the effective inverse decay time $\tau_n^{\text{eff}}$ through an additive dissipative rate proportional to $\omega_n^2$:

$$\frac{1}{\tau_n^{\text{eff}}} = \frac{1}{\tau_n^{\text{GR}}} + \frac{\beta \, \nu_{\text{eff}} \, \omega_n^2}{2c^2}$$

This formulation guarantees that the damping shift scales quadratically with overtone frequency, providing a distinct spectral signature that distinguishes fluidic vacuum shear from standard general relativistic damping.

### 2.3 Strain-Gated Activation

Dissipative modifications are constrained to extreme curvature environments via a dynamic master gate function governed by local gravitational-wave strain $S$:

$$S \ge S_{\text{crit}}$$

When the local strain exceeds the critical threshold ($S_{\text{crit}} = 0.005$), the viscosity ceiling ($\nu_{\text{eff}} \le 1.0 \times 10^{12} \text{ m}^2/\text{s}$) is engaged, preventing unphysical dissipation in weak-field cosmological domains while retaining full predictive power across binary black hole merger horizons.
