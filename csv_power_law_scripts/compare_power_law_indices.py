import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import os

class MultiIndexXelLattice:
    def __init__(self, grid_size=64, K=1.2, n=0.8, dt=0.01):
        self.N = grid_size
        self.K = K
        self.n = n
        self.dt = dt
        self.velocity = np.zeros((grid_size, grid_size, 2))
        self.density = np.ones((grid_size, grid_size))
        
        # Inject localized momentum disturbance
        center = grid_size // 2
        self.velocity[center-4:center+4, center-4:center+4, 0] = 3.0

    def step(self):
        du_dx = np.gradient(self.velocity[:, :, 0], axis=1)
        du_dy = np.gradient(self.velocity[:, :, 0], axis=0)
        dv_dx = np.gradient(self.velocity[:, :, 1], axis=1)
        dv_dy = np.gradient(self.velocity[:, :, 1], axis=0)
        
        s_xx = du_dx
        s_yy = dv_dy
        s_xy = 0.5 * (du_dy + dv_dx)
        
        gamma_dot = np.sqrt(2.0 * (s_xx**2 + s_yy**2 + 2.0 * s_xy**2))
        gamma_dot = np.maximum(gamma_dot, 1e-6)
        
        eta_eff = self.K * (gamma_dot ** (self.n - 1.0))
        
        stress_x = np.gradient(2.0 * eta_eff * s_xx, axis=1) + np.gradient(2.0 * eta_eff * s_xy, axis=0)
        stress_y = np.gradient(2.0 * eta_eff * s_xy, axis=1) + np.gradient(2.0 * eta_eff * s_yy, axis=0)
        
        self.velocity[:, :, 0] += self.dt * (stress_x / self.density)
        self.velocity[:, :, 1] += self.dt * (stress_y / self.density)
        
        return float(np.max(np.linalg.norm(self.velocity, axis=2)))

# Run simulations for different flow behavior indices
indices = {
    "Shear-Thinning (n = 0.5)": 0.5,
    "Newtonian (n = 1.0)": 1.0,
    "Shear-Thickening (n = 1.5)": 1.5
}

steps = 40
plt.figure(figsize=(9, 5))

for label, n_val in indices.items():
    lattice = MultiIndexXelLattice(grid_size=64, K=1.2, n=n_val)
    velocities = []
    for s in range(steps):
        max_v = lattice.step()
        velocities.append(max_v)
    plt.plot(range(steps), velocities, label=label, linewidth=2.5)

plt.title("Xel Lattice Peak Velocity Decay Across Power-Law Indices", fontsize=12, fontweight='bold')
plt.xlabel("Simulation Step", fontsize=11)
plt.ylabel("Maximum Velocity Magnitude [m/s]", fontsize=11)
plt.legend(frameon=True)
plt.grid(True, linestyle=':', alpha=0.7)
plt.tight_layout()
plt.savefig("power_law_comparison.png", dpi=300)
print("Generated: power_law_comparison.png")
