import numpy as np
import matplotlib.pyplot as plt

def power_law_pipe_velocity(r, R, delta_P, L, K, n):
    """Calculates the analytical velocity profile of a power-law fluid in a circular pipe."""
    term1 = n / (n + 1)
    term2 = (delta_P / (2 * K * L)) ** (1 / n)
    velocity = term1 * term2 * (R ** ((n + 1) / n) - r ** ((n + 1) / n))
    return velocity

# Simulation Parameters
R = 0.05        # Pipe radius in meters (5 cm)
delta_P = 1500.0  # Pressure drop in Pascals
L = 5.0         # Pipe length in meters
K = 4.0         # Consistency index (Pa s^n)

# Radial coordinates from center (r = 0) to wall (r = R)
r = np.linspace(0, R, 200)

n_cases = {
    "Shear-Thinning (n = 0.5)": 0.5,
    "Newtonian (n = 1.0)": 1.0,
    "Shear-Thickening (n = 1.5)": 1.5
}

plt.figure(figsize=(9, 6))
for label, n in n_cases.items():
    v = power_law_pipe_velocity(r, R, delta_P, L, K, n)
    plt.plot(v, r, label=label, linewidth=2.5)

plt.axhline(0, color='black', linestyle='--', alpha=0.5, label='Pipe Wall')
plt.title("Power-Law Fluid Velocity Profiles in Circular Pipe Flow", fontsize=12, fontweight='bold')
plt.xlabel("Velocity $u(r)$ [m/s]", fontsize=11)
plt.ylabel("Radial Position $r$ [m]", fontsize=11)
plt.gca().invert_yaxis()
plt.legend(frameon=True)
plt.grid(True, linestyle=':', alpha=0.7)
plt.tight_layout()
plt.savefig("power_law_pipe_profile.png", dpi=300)
print("Generated: power_law_pipe_profile.png")
