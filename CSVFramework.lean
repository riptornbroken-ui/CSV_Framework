import Mathlib

namespace CSV.Framework

/-- Lattice density with a hard ceiling.
  rho_base : base mass density (kg m^-3)
  norm_G   : norm of the shear rate tensor (s^-1)
  kappa_G  : shear resistance rate (s^-1)
  delta_x  : displacement scale (m)
  ell_xel  : xel edge length (m)
  rho_ceil : ceiling (kg m^-3) -/
def lattice_density (rho_base norm_G kappa_G delta_x ell_xel rho_ceil : ℝ) : ℝ :=
  min (rho_base * (1 + (norm_G / kappa_G) * (delta_x / ell_xel))) rho_ceil

/-- The V2.5 saturating form, with ceiling parameter T. -/
def old_saturating (T b : ℝ) : ℝ := b / (1 + (b / T) ^ 2)

/-- The correction factor is nonnegative when its inputs are. -/
theorem factor_nonneg (norm_G kappa_G delta_x ell_xel : ℝ)
    (hG : 0 ≤ norm_G) (hk : 0 < kappa_G) (hd : 0 ≤ delta_x) (hl : 0 < ell_xel) :
    0 ≤ 1 + (norm_G / kappa_G) * (delta_x / ell_xel) := by
  have h1 : 0 ≤ norm_G / kappa_G := div_nonneg hG hk.le
  have h2 : 0 ≤ delta_x / ell_xel := div_nonneg hd hl.le
  have := mul_nonneg h1 h2
  linarith

/-- The density never exceeds the ceiling. -/
theorem lattice_le_ceiling (rho_base norm_G kappa_G delta_x ell_xel rho_ceil : ℝ) :
    lattice_density rho_base norm_G kappa_G delta_x ell_xel rho_ceil ≤ rho_ceil := by
  unfold lattice_density
  exact min_le_right _ _

/-- The density is nonnegative for nonnegative base density and a positive ceiling. -/
theorem lattice_nonneg (rho_base norm_G kappa_G delta_x ell_xel rho_ceil : ℝ)
    (hb : 0 ≤ rho_base) (hG : 0 ≤ norm_G) (hk : 0 < kappa_G)
    (hd : 0 ≤ delta_x) (hl : 0 < ell_xel) (hc : 0 < rho_ceil) :
    0 ≤ lattice_density rho_base norm_G kappa_G delta_x ell_xel rho_ceil := by
  unfold lattice_density
  have h3 := factor_nonneg norm_G kappa_G delta_x ell_xel hG hk hd hl
  exact le_min (mul_nonneg hb h3) hc.le

/-- The density is nondecreasing in the base density. -/
theorem lattice_monotone_in_base (norm_G kappa_G delta_x ell_xel rho_ceil b1 b2 : ℝ)
    (hG : 0 ≤ norm_G) (hk : 0 < kappa_G) (hd : 0 ≤ delta_x) (hl : 0 < ell_xel)
    (h12 : b1 ≤ b2) :
    lattice_density b1 norm_G kappa_G delta_x ell_xel rho_ceil ≤
      lattice_density b2 norm_G kappa_G delta_x ell_xel rho_ceil := by
  unfold lattice_density
  have h3 := factor_nonneg norm_G kappa_G delta_x ell_xel hG hk hd hl
  refine min_le_min ?_ le_rfl
  exact mul_le_mul_of_nonneg_right h12 h3

/-- The V2.5 form is not monotone: it falls as base density grows past the ceiling. -/
theorem old_not_monotone :
    ¬ (∀ a b : ℝ, 0 ≤ a → a ≤ b → old_saturating 1 a ≤ old_saturating 1 b) := by
  intro h
  have key := h 1 10 (by norm_num) (by norm_num)
  have h1 : old_saturating 1 1 = 1 / 2 := by
    unfold old_saturating
    norm_num
  have h10 : old_saturating 1 10 = 10 / 101 := by
    unfold old_saturating
    norm_num
  rw [h1, h10] at key
  norm_num at key

end CSV.Framework
