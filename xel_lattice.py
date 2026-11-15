#!/usr/bin/env python3
"""
Chromatic Spacetime Viscosity (CSV) Framework
Sub-Planckian Xel Lattice: Spatial Boundary Layer Mapping
"""

import numpy as np

class XelLatticeSimulator:
    def __init__(self, grid_size=33):
        self.grid_size = grid_size
        self.center = (grid_size // 2, grid_size // 2, grid_size // 2)
        self.density = np.zeros((grid_size, grid_size, grid_size), dtype=np.float64)
        
        self.XEL_EDGE = 1e-40                  # meters
        self.XEL_VOL = 1e-120                  # m^3
        self.MAX_DENSITY = 2.17643e112         # kg/m^3 (Sub-Planckian Ceiling)
        self.BASE_VISCOSITY = 1.8734           # kg/(m*s)

    def inject_mass_vortex(self, mass_amount):
        cx, cy, cz = self.center
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                for z in range(self.grid_size):
                    dist_sq = (x - cx)**2 + (y - cy)**2 + (z - cz)**2
                    if dist_sq == 0:
                        self.density[x, y, z] += mass_amount
                    else:
                        # Gradated inverse-square drop-off across the lattice
                        self.density[x, y, z] += mass_amount / (dist_sq * 5.0)

    def evaluate_and_map(self):
        total_nodes = self.grid_size ** 3
        
        # Apply Causal Pinch-Off (clamp density at sub-Planckian ceiling)
        saturation_mask = self.density >= self.MAX_DENSITY
        saturated_nodes = np.sum(saturation_mask)
        self.density[saturation_mask] = self.MAX_DENSITY
        
        # Calculate gradients and shear stress tensor
        grad_x, grad_y, grad_z = np.gradient(self.density)
        shear_magnitude = np.sqrt(grad_x**2 + grad_y**2 + grad_z**2)
        
        # Map concentric shell boundary layers outward from the center
        cx, cy, cz = self.center
        shells = {}
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                for z in range(self.grid_size):
                    r = int(np.round(np.sqrt((x - cx)**2 + (y - cy)**2 + (z - cz)**2)))
                    if r not in shells:
                        shells[r] = []
                    shells[r].append(self.density[x, y, z])
                    
        shell_profile = {r: np.mean(vals) for r, vals in sorted(shells.items())}
        
        return {
            "total_nodes": total_nodes,
            "saturated_nodes": saturated_nodes,
            "max_shear": np.max(shear_magnitude),
            "mean_density": np.mean(self.density),
            "shell_profile": shell_profile
        }

if __name__ == "__main__":
    sim = XelLatticeSimulator(grid_size=33)
    print("--- Initializing CSV Large-Grid Simulation (33x33x33) ---")
    print(f"Total Grid Nodes: {sim.grid_size**3:,} xels | Density Ceiling: {sim.MAX_DENSITY:.2e} kg/m^3")
    
    # Inject high-intensity mass to expand the core
    sim.inject_mass_vortex(mass_amount=8.0e113)
    results = sim.evaluate_and_map()
    
    print("\n--- Core Saturation Results ---")
    print(f"Saturated Core Nodes (Pinch-Off Active): {results['saturated_nodes']}")
    print(f"Max Shear Stress (G_alpha_beta): {results['max_shear']:.4e}")
    print(f"Mean Lattice Density: {results['mean_density']:.4e} kg/m^3")
    
    print("\n--- Spatial Boundary Layer (Radial Shell Profile) ---")
    print(f"{'Radius (Xels)':<15} | {'Mean Shell Density (kg/m^3)':<25} | {'Status'}")
    print("-" * 65)
    for r, dens in list(results['shell_profile'].items())[:10]: # Print first 10 radii
        status = "SATURATED CORE" if dens >= sim.MAX_DENSITY else ("Boundary Transition" if dens > 1e105 else "Vacuum Baseline")
        print(f"{r:<15} | {dens:<25.4e} | {status}")
