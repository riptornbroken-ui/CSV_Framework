import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import os

class TelemetryPowerLawLattice:
    def __init__(self, grid_size=64, K=1.2, n=0.7, dt=0.01, db_name="csv_telemetry.db"):
        self.N = grid_size
        self.K = K
        self.n = n
        self.dt = dt
        self.db_name = db_name
        
        # Initialize velocity and telemetry database
        self.velocity = np.zeros((grid_size, grid_size, 2))
        self.density = np.ones((grid_size, grid_size))
        
        # Inject a localized velocity disturbance to drive shear
        center = grid_size // 2
        self.velocity[center-4:center+4, center-4:center+4, 0] = 2.0
        
        self._init_db()

    def _init_db(self):
        """Initializes SQLite telemetry logging database."""
        if os.path.exists(self.db_name):
            os.remove(self.db_name)
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS lattice_telemetry (
                step INTEGER PRIMARY KEY,
                max_shear_rate REAL,
                mean_viscosity REAL,
                max_velocity REAL
            )
        ''')
        self.conn.commit()

    def compute_shear_rate_tensor(self):
        du_dx = np.gradient(self.velocity[:, :, 0], axis=1)
        du_dy = np.gradient(self.velocity[:, :, 0], axis=0)
        dv_dx = np.gradient(self.velocity[:, :, 1], axis=1)
        dv_dy = np.gradient(self.velocity[:, :, 1], axis=0)
        
        s_xx = du_dx
        s_yy = dv_dy
        s_xy = 0.5 * (du_dy + dv_dx)
        
        gamma_dot = np.sqrt(2.0 * (s_xx**2 + s_yy**2 + 2.0 * s_xy**2))
        return gamma_dot, s_xx, s_yy, s_xy

    def step(self, step_idx):
        gamma_dot, s_xx, s_yy, s_xy = self.compute_shear_rate_tensor()
        gamma_dot = np.maximum(gamma_dot, 1e-6)
        
        # Ostwald-de Waele effective viscosity
        eta_eff = self.K * (gamma_dot ** (self.n - 1.0))
        
        stress_x = np.gradient(2.0 * eta_eff * s_xx, axis=1) + np.gradient(2.0 * eta_eff * s_xy, axis=0)
        stress_y = np.gradient(2.0 * eta_eff * s_xy, axis=1) + np.gradient(2.0 * eta_eff * s_yy, axis=0)
        
        self.velocity[:, :, 0] += self.dt * (stress_x / self.density)
        self.velocity[:, :, 1] += self.dt * (stress_y / self.density)
        
        # Log telemetry
        max_sr = float(np.max(gamma_dot))
        mean_vis = float(np.mean(eta_eff))
        max_vel = float(np.max(np.linalg.norm(self.velocity, axis=2)))
        
        self.cursor.execute(
            "INSERT INTO lattice_telemetry (step, max_shear_rate, mean_viscosity, max_velocity) VALUES (?, ?, ?, ?)",
            (step_idx, max_sr, mean_vis, max_vel)
        )
        self.conn.commit()
        return eta_eff

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    lattice = TelemetryPowerLawLattice(grid_size=64, K=1.2, n=0.7)
    print("Running 50 simulation steps with telemetry logging...")
    
    final_eta = None
    for s in range(50):
        final_eta = lattice.step(s)
    
    lattice.close()
    print("Telemetry successfully saved to csv_telemetry.db")
    
    # Plot 2D Viscosity Heatmap
    plt.figure(figsize=(7, 6))
    plt.imshow(final_eta, cmap='plasma', origin='lower')
    plt.colorbar(label='Effective Viscosity $\\eta_{\\text{eff}}$ [Pa·s]')
    plt.title("Xel Lattice Effective Viscosity Field (n = 0.7)", fontsize=11, fontweight='bold')
    plt.xlabel("Xel Grid X", fontsize=10)
    plt.ylabel("Xel Grid Y", fontsize=10)
    plt.tight_layout()
    plt.savefig("power_law_viscosity_heatmap.png", dpi=300)
    print("Generated: power_law_viscosity_heatmap.png")
