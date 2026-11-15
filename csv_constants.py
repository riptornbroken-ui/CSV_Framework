#!/usr/bin/env python3
"""
Chromatic Spacetime Viscosity (CSV) Framework v2.5
Centralized Physical Constants & Lattice Parameters
"""

# Spatial & Temporal Discretization Units
XEL_EDGE_METERS = 1.0e-40                  # Xel edge length (\ell_xel)
XEL_VOLUME_M3 = 1.0e-120                   # Xel volume ($V_x$)
CAUSAL_TICK_SECONDS = 3.3333e-49           # Causal tick step (\tau_step)

# Density & Shear Ceilings
MAX_SUB_PLANCK_DENSITY = 2.17643e112       # Sub-Planckian Density Ceiling (\rho_sub-Planck) in kg/m^3
BASE_VISCOSITY_KAPPA = 1.8734              # Baseline fluid viscosity tensor constant (\kappa_G)

# Grid & Simulation Defaults
DEFAULT_GRID_SIZE = 33
DEFAULT_VORTEX_MASS = 8.0e113
