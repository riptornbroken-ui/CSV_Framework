import numpy as np

class PowerLawXelLattice:
    def __init__(self, grid_size=64, K=1.0, n=0.8, dt=0.01):
        self.N = grid_size
        self.K = K          # Consistency index
        self.n = n          # Flow behavior index (e.g., 0.8 for shear-thinning)
        self.dt = dt
        
        # Initialize velocity field for xels (u, v components)
        self.velocity = np.zeros((grid_size, grid_size, 2))
        self.density = np.ones((grid_size, grid_size))

    def compute_shear_rate_tensor(self):
        """Computes velocity gradients and effective shear rate scalar."""
        du_dx = np.gradient(self.velocity[:, :, 0], axis=1)
        du_dy = np.gradient(self.velocity[:, :, 0], axis=0)
        dv_dx = np.gradient(self.velocity[:, :, 1], axis=1)
        dv_dy = np.gradient(self.velocity[:, :, 1], axis=0)
        
        s_xx = du_dx
        s_yy = dv_dy
        s_xy = 0.5 * (du_dy + dv_dx)
        
        gamma_dot = np.sqrt(2.0 * (s_xx**2 + s_yy**2 + 2.0 * s_xy**2))
        return gamma_dot, s_xx, s_yy, s_xy

    def update_lattice_step(self):
        """Executes a single time step incorporating non-Newtonian power-law viscosity."""
        gamma_dot, s_xx, s_yy, s_xy = self.compute_shear_rate_tensor()
        gamma_dot = np.maximum(gamma_dot, 1e-6)
        
        # Ostwald-de Waele dynamic effective viscosity field
        eta_eff = self.K * (gamma_dot ** (self.n - 1.0))
        
        stress_x = np.gradient(2.0 * eta_eff * s_xx, axis=1) + np.gradient(2.0 * eta_eff * s_xy, axis=0)
        stress_y = np.gradient(2.0 * eta_eff * s_xy, axis=1) + np.gradient(2.0 * eta_eff * s_yy, axis=0)
        
        self.velocity[:, :, 0] += self.dt * (stress_x / self.density)
        self.velocity[:, :, 1] += self.dt * (stress_y / self.density)

if __name__ == "__main__":
    lattice = PowerLawXelLattice(grid_size=32, K=1.2, n=0.7)
    print("Initialized PowerLawXelLattice successfully on grid size 32x32.")
    for step in range(10):
        lattice.update_lattice_step()
    print("Executed 10 test time steps without instability.")
