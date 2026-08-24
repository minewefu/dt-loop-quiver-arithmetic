/-
# Arithmetic of Donaldson–Thomas invariants of loop quivers: Lean formalization

Formalizes the arithmetic core of the paper "Arithmetic of Donaldson–Thomas
invariants of loop quivers: improved integrality and exact q-analogues".

For the m-loop quiver, Reineke's formula gives `n² · DT_n = ± S m n` where

  `S m n = ∑_{d ∣ n} μ(n/d) · a m d`,   `a m e = (-1)^((m-1)(e-1)) · C(me-1, e-1)`.

UNCONDITIONAL results:
* `choose_mul_left` : the identity `C(me, e) = m · C(me-1, e-1)`;
* `S_collapse`     : the Möbius collapse of `S` at a prime power;
* `S_two_eval`, `two_mul_S_three`, `four_dvd_S_two`, `nine_dvd_S_three`,
  `sharp_two`, `sharp_three` : evaluations and sharpness at `n = 2, 3`;
* `orbit_sum_zero` : the orbit-sum identity behind the paper's derivative
  theorem (Lemma 3.3 of the paper).

CONDITIONAL on the classical Jacobsthal–Kazandzidis congruences, stated as
explicit hypotheses (`KazOdd p κ`: Kazandzidis 1968 / Robert–Zuber 1995, with
κ = 3 for p ≥ 5 and κ = 2 for p = 3; `Kaz2`: the signed p = 2 form proved in
Appendix B of the paper):
* `tower_odd`, `tower_two` : the tower congruences (Lemma 6.1), including the
  exact p = 2 sign cancellation;
* `main_bound`, `improved_integrality_ge5/three/two`, `dt_valuation_ge5` :
  the valuation bounds of Theorem 1.2 in the normalization `n² DT_n = ± S`.
-/

import Mathlib

open Finset ArithmeticFunction

namespace DTLoop

/-! ## Definitions -/

/-- The signed binomial sequence `a m e = (-1)^((m-1)(e-1)) C(me-1, e-1)`. -/
def a (m e : ℕ) : ℤ :=
  (-1) ^ ((m - 1) * (e - 1)) * ((m * e - 1).choose (e - 1) : ℤ)

/-- The Möbius–binomial sum: `n² DT_n^{(m)} = (-1)^{(m-1)(n-1)} S m n`. -/
def S (m n : ℕ) : ℤ :=
  ∑ d ∈ n.divisors, (moebius (n / d) : ℤ) * a m d

/-- Jacobsthal–Kazandzidis congruence for an odd prime with strength `κ`. -/
def KazOdd (p κ : ℕ) : Prop :=
  ∀ N K : ℕ, 1 ≤ K → K ≤ N →
    (p : ℤ) ^ (κ + padicValNat p (N * K * (N - K) * N.choose K)) ∣
      (((p * N).choose (p * K) : ℤ) - (N.choose K : ℤ))

/-- Signed Kazandzidis congruence at `p = 2` (Appendix B of the paper). -/
def Kaz2 : Prop :=
  ∀ N K : ℕ, 1 ≤ K → K ≤ N →
    (2 : ℤ) ^ (1 + padicValNat 2 (N * K * (N - K) * N.choose K)) ∣
      (((2 * N).choose (2 * K) : ℤ) - (-1) ^ (K * (N - K)) * (N.choose K : ℤ))

/-! ## Elementary helpers -/

/-- `(-1)^A = (-1)^B` whenever `A ≡ B (mod 2)`. -/
lemma neg_one_pow_congr {A B : ℕ} (h : A % 2 = B % 2) :
    ((-1 : ℤ)) ^ A = (-1) ^ B := by
  conv_lhs => rw [← Nat.div_add_mod A 2, pow_add, pow_mul]
  conv_rhs => rw [← Nat.div_add_mod B 2, pow_add, pow_mul]
  norm_num [h]

/-- Cancel a factor coprime to `p` from a power-of-`p` divisibility over `ℤ`. -/
lemma pow_dvd_of_dvd_mul {p : ℕ} (hp : p.Prime) {c : ℤ} {T : ℕ}
    (hc : ¬ (p : ℤ) ∣ c) : ∀ {y : ℤ}, (p : ℤ) ^ T ∣ c * y → (p : ℤ) ^ T ∣ y := by
  induction T with
  | zero => exact fun _ => one_dvd _
  | succ t ih =>
    intro y h
    have hpZ : Prime (p : ℤ) := Nat.prime_iff_prime_int.mp hp
    have h1 : (p : ℤ) ∣ c * y := (dvd_pow_self (p : ℤ) t.succ_ne_zero).trans h
    rcases hpZ.dvd_mul.mp h1 with hc' | hy
    · exact absurd hc' hc
    · obtain ⟨y', rfl⟩ := hy
      have hne : (p : ℤ) ≠ 0 := by exact_mod_cast hp.ne_zero
      have h2 : (p : ℤ) ^ (t + 1) ∣ (p : ℤ) * (c * y') := by
        rw [show (p : ℤ) * (c * y') = c * ((p : ℤ) * y') by ring]; exact h
      rw [pow_succ'] at h2
      have h3 : (p : ℤ) ^ t ∣ c * y' := (mul_dvd_mul_iff_left hne).mp h2
      rw [pow_succ']
      exact mul_dvd_mul_left _ (ih h3)

/-- The key identity `C(me, e) = m · C(me-1, e-1)` for `m, e ≥ 1`. -/
lemma choose_mul_left {m e : ℕ} (hm : 1 ≤ m) (he : 1 ≤ e) :
    (m * e).choose e = m * ((m * e - 1).choose (e - 1)) := by
  have hme : 1 ≤ m * e := Nat.one_le_iff_ne_zero.mpr (Nat.mul_ne_zero (by omega) (by omega))
  have h := Nat.add_one_mul_choose_eq (m * e - 1) (e - 1)
  rw [Nat.sub_add_cancel hme, Nat.sub_add_cancel he] at h
  -- h : m * e * ((m*e-1).choose (e-1)) = (m*e).choose e * e
  have h2 : (m * ((m * e - 1).choose (e - 1))) * e = ((m * e).choose e) * e := by
    calc (m * ((m * e - 1).choose (e - 1))) * e
        = m * e * ((m * e - 1).choose (e - 1)) := by ring
      _ = (m * e).choose e * e := h
  exact (Nat.eq_of_mul_eq_mul_right he h2).symm

lemma a_one (m : ℕ) : a m 1 = 1 := by simp [a]

/-! ## The tower congruences -/

section Tower

/-- Common core: from the Kazandzidis divisibility at `(N,K) = (me, e)` with a
sign `ε` on the second term, deduce the bound for the `C(·-1, ·-1)` difference. -/
lemma tower_core (p : ℕ) (hp : p.Prime) (κ : ℕ)
    (m e : ℕ) (hm : 2 ≤ m) (he : 1 ≤ e) (ε : ℤ)
    (h : (p : ℤ) ^ (κ + padicValNat p ((m * e) * e * (m * e - e) * (m * e).choose e)) ∣
      ((m * (p * e)).choose (p * e) : ℤ) - ε * ((m * e).choose e : ℤ)) :
    (p : ℤ) ^ (κ + 3 * padicValNat p e + padicValNat p (m * (m - 1))) ∣
      (((m * (p * e) - 1).choose (p * e - 1) : ℤ) -
        ε * (((m * e - 1).choose (e - 1)) : ℤ)) := by
  have : Fact p.Prime := ⟨hp⟩
  have hm1 : 1 ≤ m := by omega
  have he0 : e ≠ 0 := by omega
  have hpe : 1 ≤ p * e := Nat.one_le_iff_ne_zero.mpr (Nat.mul_ne_zero hp.pos.ne' he0)
  have hC' : 0 < (m * e - 1).choose (e - 1) :=
    Nat.choose_pos (Nat.sub_le_sub_right (Nat.le_mul_of_pos_left e (by omega)) 1)
  -- rewrite both big binomials
  have e1 : (m * (p * e)).choose (p * e) = m * ((m * (p * e) - 1).choose (p * e - 1)) :=
    choose_mul_left hm1 hpe
  have e2 : (m * e).choose e = m * ((m * e - 1).choose (e - 1)) :=
    choose_mul_left hm1 he
  have hY : ((m * (p * e)).choose (p * e) : ℤ) - ε * ((m * e).choose e : ℤ)
      = (m : ℤ) * ((((m * (p * e) - 1).choose (p * e - 1) : ℕ) : ℤ) -
          ε * (((m * e - 1).choose (e - 1) : ℕ) : ℤ)) := by
    rw [e1, e2]; push_cast; ring
  rw [hY] at h
  -- valuation of the modulus
  have hsub : m * e - e = (m - 1) * e := (Nat.sub_one_mul m e).symm
  have hval : padicValNat p ((m * e) * e * (m * e - e) * (m * e).choose e)
      = 2 * padicValNat p m + 3 * padicValNat p e + padicValNat p (m - 1)
        + padicValNat p ((m * e - 1).choose (e - 1)) := by
    rw [hsub, e2]
    have v1 : padicValNat p ((m * e) * e * ((m - 1) * e) * (m * ((m * e - 1).choose (e - 1))))
        = padicValNat p ((m * e) * e * ((m - 1) * e))
          + padicValNat p (m * ((m * e - 1).choose (e - 1))) :=
      padicValNat.mul (Nat.mul_ne_zero (Nat.mul_ne_zero (Nat.mul_ne_zero (by omega) he0) he0)
        (Nat.mul_ne_zero (by omega) he0)) (Nat.mul_ne_zero (by omega) hC'.ne')
    have v2 : padicValNat p ((m * e) * e * ((m - 1) * e))
        = padicValNat p ((m * e) * e) + padicValNat p ((m - 1) * e) :=
      padicValNat.mul (Nat.mul_ne_zero (Nat.mul_ne_zero (by omega) he0) he0)
        (Nat.mul_ne_zero (by omega) he0)
    have v3 : padicValNat p ((m * e) * e)
        = padicValNat p (m * e) + padicValNat p e :=
      padicValNat.mul (Nat.mul_ne_zero (by omega) he0) he0
    have v4 : padicValNat p (m * e) = padicValNat p m + padicValNat p e :=
      padicValNat.mul (by omega) he0
    have v5 : padicValNat p ((m - 1) * e) = padicValNat p (m - 1) + padicValNat p e :=
      padicValNat.mul (by omega) he0
    have v6 : padicValNat p (m * ((m * e - 1).choose (e - 1)))
        = padicValNat p m + padicValNat p ((m * e - 1).choose (e - 1)) :=
      padicValNat.mul (by omega) hC'.ne'
    omega
  have hvm : padicValNat p (m * (m - 1))
      = padicValNat p m + padicValNat p (m - 1) :=
    padicValNat.mul (by omega) (by omega)
  have hexp : κ + padicValNat p ((m * e) * e * (m * e - e) * (m * e).choose e)
      = ((κ + 3 * padicValNat p e + padicValNat p (m * (m - 1)))
          + padicValNat p ((m * e - 1).choose (e - 1))) + padicValNat p m := by
    rw [hval, hvm]; ring
  rw [hexp] at h
  set T := κ + 3 * padicValNat p e + padicValNat p (m * (m - 1)) with hT
  have h' : (p : ℤ) ^ (T + padicValNat p m) ∣
      (m : ℤ) * ((((m * (p * e) - 1).choose (p * e - 1) : ℕ) : ℤ) -
        ε * (((m * e - 1).choose (e - 1) : ℕ) : ℤ)) :=
    (pow_dvd_pow _ (by omega)).trans h
  -- decompose m = p^{v_p m} * m₀ with p ∤ m₀
  have hproj : p ^ (m.factorization p) * (m / p ^ (m.factorization p)) = m :=
    Nat.ordProj_mul_ordCompl_eq_self m p
  have hfac : m.factorization p = padicValNat p m := Nat.factorization_def m hp
  have hm0 : ¬ p ∣ (m / p ^ (m.factorization p)) :=
    Nat.not_dvd_ordCompl hp (by omega)
  have hmz : (m : ℤ) = (p : ℤ) ^ (padicValNat p m) * ((m / p ^ (m.factorization p) : ℕ) : ℤ) := by
    rw [← hfac]
    exact_mod_cast hproj.symm
  rw [hmz, mul_assoc, pow_add] at h'
  have hne : ((p : ℤ) ^ (padicValNat p m)) ≠ 0 :=
    pow_ne_zero _ (by exact_mod_cast hp.ne_zero)
  rw [mul_comm ((p : ℤ) ^ T) ((p : ℤ) ^ (padicValNat p m))] at h'
  have h'' := (mul_dvd_mul_iff_left hne).mp h'
  refine pow_dvd_of_dvd_mul hp ?_ h''
  intro hd
  exact hm0 (by exact_mod_cast hd)

/-- Tower congruence at odd primes (identical signs). -/
theorem tower_odd {p : ℕ} (hp : p.Prime) (hodd : p % 2 = 1) {κ : ℕ}
    (hK : KazOdd p κ) (m e : ℕ) (hm : 2 ≤ m) (he : 1 ≤ e) :
    (p : ℤ) ^ (κ + 3 * padicValNat p e + padicValNat p (m * (m - 1))) ∣
      a m (p * e) - a m e := by
  have hm1 : 1 ≤ m := by omega
  have hKa := hK (m * e) e he (Nat.le_mul_of_pos_left e hm1)
  rw [show p * (m * e) = m * (p * e) by ring] at hKa
  have hcore := tower_core p hp κ m e hm he 1 (by simpa using hKa)
  have hpe : 1 ≤ p * e := Nat.one_le_iff_ne_zero.mpr
    (Nat.mul_ne_zero hp.pos.ne' (by omega))
  have hpar : ((m - 1) * (p * e - 1)) % 2 = ((m - 1) * (e - 1)) % 2 := by
    have h1 : (p * e) % 2 = e % 2 := by
      rw [Nat.mul_mod, hodd, one_mul]
      omega
    have h2 : (p * e - 1) % 2 = (e - 1) % 2 := by omega
    rw [Nat.mul_mod, h2, ← Nat.mul_mod]
  have hkey : a m (p * e) - a m e
      = (-1 : ℤ) ^ ((m - 1) * (e - 1)) *
        ((((m * (p * e) - 1).choose (p * e - 1) : ℕ) : ℤ) -
          1 * (((m * e - 1).choose (e - 1) : ℕ) : ℤ)) := by
    unfold a
    rw [neg_one_pow_congr hpar]
    ring
  rw [hkey]
  exact hcore.mul_left _

/-- Tower congruence at `p = 2`: the Kazandzidis sign `(-1)^{K(N-K)}` cancels
exactly against the motivic sign twist. -/
theorem tower_two (hK : Kaz2) (m e : ℕ) (hm : 2 ≤ m) (he : 1 ≤ e) :
    (2 : ℤ) ^ (1 + 3 * padicValNat 2 e + padicValNat 2 (m * (m - 1))) ∣
      a m (2 * e) - a m e := by
  have hm1 : 1 ≤ m := by omega
  have hKa := hK (m * e) e he (Nat.le_mul_of_pos_left e hm1)
  rw [show 2 * (m * e) = m * (2 * e) by ring] at hKa
  have hsub : m * e - e = (m - 1) * e := (Nat.sub_one_mul m e).symm
  have hsgn : ((-1 : ℤ)) ^ (e * (m * e - e)) = (-1) ^ ((m - 1) * e) := by
    apply neg_one_pow_congr
    rw [hsub]
    rcases Nat.mod_two_eq_zero_or_one e with hy | hy <;>
      rcases Nat.mod_two_eq_zero_or_one (m - 1) with hx | hx <;>
      · rw [Nat.mul_mod e ((m - 1) * e), Nat.mul_mod (m - 1) e, hx, hy]
  rw [hsgn] at hKa
  have hcore := tower_core 2 Nat.prime_two 1 m e hm he ((-1 : ℤ) ^ ((m - 1) * e)) hKa
  have hpar1 : ((m - 1) * (2 * e - 1)) % 2 = (m - 1) % 2 := by
    have h2 : (2 * e - 1) % 2 = 1 := by omega
    rw [Nat.mul_mod, h2, mul_one]
    omega
  have hpar2 : ((m - 1) + (m - 1) * e) % 2 = ((m - 1) * (e - 1)) % 2 := by
    have h1 : (m - 1) + (m - 1) * e = (m - 1) * (e + 1) := by ring
    have h4 : (e + 1) % 2 = (e - 1) % 2 := by omega
    rw [h1, Nat.mul_mod, h4, ← Nat.mul_mod]
  have hkey : a m (2 * e) - a m e
      = (-1 : ℤ) ^ (m - 1) *
        ((((m * (2 * e) - 1).choose (2 * e - 1) : ℕ) : ℤ) -
          (-1 : ℤ) ^ ((m - 1) * e) * (((m * e - 1).choose (e - 1) : ℕ) : ℤ)) := by
    unfold a
    rw [show ((-1 : ℤ)) ^ ((m - 1) * (2 * e - 1)) = (-1) ^ (m - 1) from by
      have := neg_one_pow_congr (A := (m - 1) * (2 * e - 1)) (B := m - 1)
        (by rw [hpar1])
      exact this]
    rw [show ((-1 : ℤ)) ^ ((m - 1) * (e - 1)) = (-1) ^ ((m - 1) + (m - 1) * e) from
      (neg_one_pow_congr hpar2).symm]
    rw [pow_add]
    ring
  rw [hkey]
  exact hcore.mul_left _

end Tower

/-! ## The Möbius collapse -/

/-- Collapse of `S m (p^v u)` (with `p ∤ u`, `v ≥ 1`) to consecutive-level
differences of the sequence `a`. -/
lemma S_collapse {p : ℕ} (hp : p.Prime) (m v u : ℕ) (hv : 1 ≤ v) (hu : u ≠ 0)
    (hpu : ¬ p ∣ u) :
    S m (p ^ v * u) = ∑ f ∈ u.divisors,
      (moebius (u / f) : ℤ) * (a m (p ^ v * f) - a m (p ^ (v - 1) * f)) := by
  classical
  have hppos : 0 < p := hp.pos
  have hn0 : p ^ v * u ≠ 0 := by positivity
  have hstep : S m (p ^ v * u)
      = ∑ x ∈ (Finset.range (v + 1)) ×ˢ u.divisors,
          (moebius ((p ^ v * u) / (p ^ x.1 * x.2)) : ℤ) * a m (p ^ x.1 * x.2) := by
    rw [S]
    apply Finset.sum_nbij' (i := fun d => (d.factorization p, d / p ^ (d.factorization p)))
      (j := fun x => p ^ x.1 * x.2)
    · -- forward membership
      intro d hd
      rw [Nat.mem_divisors] at hd
      obtain ⟨hdvd, _⟩ := hd
      have hd0 : d ≠ 0 := by
        rintro rfl
        exact hn0 (Nat.zero_dvd.mp hdvd)
      simp only [Finset.mem_product, Finset.mem_range, Nat.mem_divisors]
      refine ⟨?_, ?_, hu⟩
      · have hle : d.factorization ≤ (p ^ v * u).factorization :=
          (Nat.factorization_le_iff_dvd hd0 hn0).mpr hdvd
        have h2 : (p ^ v * u).factorization p = v := by
          rw [Nat.factorization_mul (by positivity) hu]
          simp [Nat.factorization_pow, hp.factorization, Nat.factorization_eq_zero_of_not_dvd hpu]
        have h3 := Finsupp.le_def.mp hle p
        omega
      · have h1 : (d / p ^ (d.factorization p)) ∣ d := Nat.ordCompl_dvd d p
        have h2 : (d / p ^ (d.factorization p)) ∣ p ^ v * u := h1.trans hdvd
        have h3 : ¬ p ∣ (d / p ^ (d.factorization p)) :=
          Nat.not_dvd_ordCompl hp hd0
        have hcop : Nat.Coprime (d / p ^ (d.factorization p)) (p ^ v) :=
          (((Nat.Prime.coprime_iff_not_dvd hp).mpr h3).symm).pow_right v
        exact hcop.dvd_of_dvd_mul_left h2
    · -- backward membership
      intro x hx
      simp only [Finset.mem_product, Finset.mem_range, Nat.mem_divisors] at hx
      rw [Nat.mem_divisors]
      exact ⟨mul_dvd_mul (pow_dvd_pow p (by omega)) hx.2.1, hn0⟩
    · -- left inverse
      intro d hd
      exact Nat.ordProj_mul_ordCompl_eq_self d p
    · -- right inverse
      intro x hx
      simp only [Finset.mem_product, Finset.mem_range, Nat.mem_divisors] at hx
      have hf0 : x.2 ≠ 0 := fun h => hu (Nat.eq_zero_of_zero_dvd (h ▸ hx.2.1))
      have hpf : ¬ p ∣ x.2 := fun h => hpu (h.trans hx.2.1)
      have h1 : (p ^ x.1 * x.2).factorization p = x.1 := by
        rw [Nat.factorization_mul (by positivity) hf0]
        simp [Nat.factorization_pow, hp.factorization, Nat.factorization_eq_zero_of_not_dvd hpf]
      refine Prod.ext ?_ ?_
      · exact h1
      · simp only [h1]
        exact Nat.mul_div_cancel_left _ (by positivity : 0 < p ^ x.1)
    · -- values agree
      intro d hd
      conv_lhs => rw [← Nat.ordProj_mul_ordCompl_eq_self d p]
  rw [hstep, Finset.sum_product]
  have hterm : ∀ j ∈ Finset.range (v + 1), ∀ f ∈ u.divisors,
      (moebius ((p ^ v * u) / (p ^ j * f)) : ℤ)
        = (moebius (p ^ (v - j)) * moebius (u / f) : ℤ) := by
    intro j hj f hf
    rw [Finset.mem_range] at hj
    rw [Nat.mem_divisors] at hf
    have hdiv : (p ^ v * u) / (p ^ j * f) = p ^ (v - j) * (u / f) := by
      rw [← Nat.div_mul_div_comm (pow_dvd_pow p (by omega : j ≤ v)) hf.1,
        Nat.pow_div (by omega) hppos]
    rw [hdiv]
    have hcop : Nat.Coprime (p ^ (v - j)) (u / f) := by
      apply Nat.Coprime.pow_left
      rw [Nat.Prime.coprime_iff_not_dvd hp]
      exact fun h => hpu (h.trans (Nat.div_dvd_of_dvd hf.1))
    rw [isMultiplicative_moebius.map_mul_of_coprime hcop]
  have hsum : ∀ j ∈ Finset.range (v + 1),
      (∑ f ∈ u.divisors, (moebius ((p ^ v * u) / (p ^ j * f)) : ℤ) * a m (p ^ j * f))
      = (moebius (p ^ (v - j)) : ℤ) *
          ∑ f ∈ u.divisors, (moebius (u / f) : ℤ) * a m (p ^ j * f) := by
    intro j hj
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro f hf
    rw [hterm j hj f hf]
    push_cast
    ring
  rw [Finset.sum_congr rfl hsum]
  have hv1 : v + 1 = (v - 1) + 1 + 1 := by omega
  rw [hv1, Finset.sum_range_succ, Finset.sum_range_succ]
  have hmid : v - 1 + 1 = v := by omega
  rw [hmid]
  have hzero : ∀ j ∈ Finset.range (v - 1),
      (moebius (p ^ (v - j)) : ℤ) *
        (∑ f ∈ u.divisors, (moebius (u / f) : ℤ) * a m (p ^ j * f)) = 0 := by
    intro j hj
    rw [Finset.mem_range] at hj
    have h2 : v - j ≠ 1 := by omega
    have h0 : v - j ≠ 0 := by omega
    rw [moebius_apply_prime_pow hp h0, if_neg h2]
    simp
  rw [Finset.sum_eq_zero hzero, zero_add]
  have hμv : (moebius (p ^ (v - v)) : ℤ) = 1 := by
    simp
  have hμv1 : (moebius (p ^ (v - (v - 1))) : ℤ) = -1 := by
    rw [show v - (v - 1) = 1 by omega, pow_one, moebius_apply_prime hp]
  rw [hμv, hμv1]
  rw [Finset.mul_sum, Finset.mul_sum, ← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro f hf
  push_cast
  ring

/-! ## Main valuation bounds -/

/-- Main bound, parameterized form: from the tower congruence at `p`, the
valuation bound on `S m (p^v u)`. -/
theorem main_bound {p : ℕ} (hp : p.Prime) {κ w : ℕ} (m : ℕ)
    (hT : ∀ e : ℕ, 1 ≤ e →
      (p : ℤ) ^ (κ + 3 * padicValNat p e + w) ∣ a m (p * e) - a m e)
    (v u : ℕ) (hv : 1 ≤ v) (hu : u ≠ 0) (hpu : ¬ p ∣ u) :
    (p : ℤ) ^ (κ + 3 * (v - 1) + w) ∣ S m (p ^ v * u) := by
  have : Fact p.Prime := ⟨hp⟩
  rw [S_collapse hp m v u hv hu hpu]
  apply Finset.dvd_sum
  intro f hf
  rw [Nat.mem_divisors] at hf
  have hf0 : f ≠ 0 := fun h => hu (Nat.eq_zero_of_zero_dvd (h ▸ hf.1))
  have hpf : ¬ p ∣ f := fun h => hpu (h.trans hf.1)
  have he : 1 ≤ p ^ (v - 1) * f :=
    Nat.one_le_iff_ne_zero.mpr (Nat.mul_ne_zero (pow_ne_zero _ hp.pos.ne') hf0)
  have hp' : p * p ^ (v - 1) = p ^ v := by
    rw [← pow_succ', Nat.sub_add_cancel hv]
  have hrw : p ^ v * f = p * (p ^ (v - 1) * f) := by
    rw [← mul_assoc, hp']
  have hval : padicValNat p (p ^ (v - 1) * f) = v - 1 := by
    rw [padicValNat.mul (pow_ne_zero _ hp.pos.ne') hf0,
      padicValNat.prime_pow, padicValNat.eq_zero_of_not_dvd hpf, add_zero]
  have hT' := hT (p ^ (v - 1) * f) he
  rw [hval] at hT'
  rw [hrw]
  exact hT'.mul_left _

/-- Improved integrality, `p ≥ 5`: `p^{3 v} ∣ S m (p^v u)`.  (Theorem 1.2(1) in
the normalization `n² DT_n = ± S m n`.)  Conditional on Kazandzidis. -/
theorem improved_integrality_ge5 {p : ℕ} (hp : p.Prime) (h5 : 5 ≤ p)
    (hK : KazOdd p 3) (m : ℕ) (hm : 2 ≤ m)
    (v u : ℕ) (hv : 1 ≤ v) (hu : u ≠ 0) (hpu : ¬ p ∣ u) :
    (p : ℤ) ^ (3 * v) ∣ S m (p ^ v * u) := by
  have hodd : p % 2 = 1 := by
    rcases hp.eq_two_or_odd with h | h
    · omega
    · exact h
  have hmain := main_bound hp m
    (fun e he => tower_odd hp hodd hK m e hm he) v u hv hu hpu
  exact (pow_dvd_pow _ (by omega)).trans hmain

/-- Improved integrality at `p = 3`: `3^{3v - 1 + v_3(m(m-1))} ∣ S`. -/
theorem improved_integrality_three (hK : KazOdd 3 2) (m : ℕ) (hm : 2 ≤ m)
    (v u : ℕ) (hv : 1 ≤ v) (hu : u ≠ 0) (hpu : ¬ (3 : ℕ) ∣ u) :
    (3 : ℤ) ^ (3 * v - 1 + padicValNat 3 (m * (m - 1))) ∣ S m (3 ^ v * u) := by
  have hmain := main_bound Nat.prime_three m
    (fun e he => tower_odd Nat.prime_three (by norm_num) hK m e hm he) v u hv hu hpu
  exact (pow_dvd_pow _ (by omega)).trans hmain

/-- Improved integrality at `p = 2`: `2^{3v - 2 + v_2(m(m-1))} ∣ S`. -/
theorem improved_integrality_two (hK : Kaz2) (m : ℕ) (hm : 2 ≤ m)
    (v u : ℕ) (hv : 1 ≤ v) (hu : u ≠ 0) (hpu : ¬ (2 : ℕ) ∣ u) :
    (2 : ℤ) ^ (3 * v - 2 + padicValNat 2 (m * (m - 1))) ∣ S m (2 ^ v * u) := by
  have hmain := main_bound Nat.prime_two m
    (fun e he => tower_two hK m e hm he) v u hv hu hpu
  exact (pow_dvd_pow _ (by omega)).trans hmain

/-- DT-level valuation, `p ≥ 5`: if `S m n = n² D` (Reineke's integrality of
`DT_n`), then `p^{v_p(n)} ∣ D`.  This is Theorem 1.2(1) of the paper. -/
theorem dt_valuation_ge5 {p : ℕ} (hp : p.Prime) (h5 : 5 ≤ p)
    (hK : KazOdd p 3) (m : ℕ) (hm : 2 ≤ m)
    (v u : ℕ) (hv : 1 ≤ v) (hu : u ≠ 0) (hpu : ¬ p ∣ u)
    (D : ℤ) (hD : S m (p ^ v * u) = ((p ^ v * u : ℕ) : ℤ) ^ 2 * D) :
    (p : ℤ) ^ v ∣ D := by
  have h3v := improved_integrality_ge5 hp h5 hK m hm v u hv hu hpu
  rw [hD] at h3v
  have hcast : ((p ^ v * u : ℕ) : ℤ) ^ 2 = (p : ℤ) ^ (2 * v) * ((u : ℤ) * u) := by
    push_cast
    ring
  rw [hcast, mul_assoc, show 3 * v = 2 * v + v by ring, pow_add] at h3v
  have hne : ((p : ℤ) ^ (2 * v)) ≠ 0 := pow_ne_zero _ (by exact_mod_cast hp.ne_zero)
  have h2 := (mul_dvd_mul_iff_left hne).mp h3v
  have hpu' : ¬ (p : ℤ) ∣ ((u : ℤ) * u) := by
    intro hcon
    have hpZ : Prime (p : ℤ) := Nat.prime_iff_prime_int.mp hp
    rcases hpZ.dvd_mul.mp hcon with h | h <;>
      exact hpu (by exact_mod_cast h)
  exact pow_dvd_of_dvd_mul hp hpu' h2

/-! ## Sharpness at n = 2 and n = 3 -/

lemma divisors_two : (2 : ℕ).divisors = {1, 2} := Nat.prime_two.divisors

lemma divisors_three : (3 : ℕ).divisors = {1, 3} := Nat.prime_three.divisors

lemma S_two_eval (m : ℕ) (hm : 2 ≤ m) :
    S m 2 = (-1 : ℤ) ^ (m - 1) * (2 * (m : ℤ) - 1) - 1 := by
  rw [S, divisors_two]
  rw [Finset.sum_insert (by decide), Finset.sum_singleton]
  norm_num
  have hμ2 : (moebius 2 : ℤ) = -1 := by
    rw [moebius_apply_prime Nat.prime_two]
  rw [hμ2, a_one]
  have ha2 : a m 2 = (-1 : ℤ) ^ (m - 1) * (2 * (m : ℤ) - 1) := by
    unfold a
    rw [show (2 : ℕ) - 1 = 1 from rfl, mul_one, Nat.choose_one_right]
    congr 1
    push_cast [Nat.cast_sub (by omega : 1 ≤ m * 2)]
    ring
  rw [ha2]
  ring

/-- `4 ∣ S m 2` (unconditional part of integrality at `n = 2`). -/
lemma four_dvd_S_two (m : ℕ) (hm : 2 ≤ m) : (4 : ℤ) ∣ S m 2 := by
  rw [S_two_eval m hm]
  rcases Nat.even_or_odd (m - 1) with he | ho
  · rw [he.neg_one_pow, one_mul]
    have hodd : (m : ℤ) % 2 = 1 := by
      have h0 : (m - 1) % 2 = 0 := Nat.even_iff.mp he
      omega
    obtain ⟨k, hk⟩ : ∃ k : ℤ, (m : ℤ) = 2 * k + 1 := ⟨(m : ℤ) / 2, by omega⟩
    rw [hk]
    exact ⟨k, by ring⟩
  · rw [ho.neg_one_pow]
    have heven : (m : ℤ) % 2 = 0 := by
      have h1 : (m - 1) % 2 = 1 := Nat.odd_iff.mp ho
      omega
    obtain ⟨k, hk⟩ : ∃ k : ℤ, (m : ℤ) = 2 * k := ⟨(m : ℤ) / 2, by omega⟩
    rw [hk]
    exact ⟨-k, by ring⟩

/-- Sharpness at `p = 2`: for `m ≡ 2, 3 (mod 4)`, `8 ∤ S m 2`.  Together with
`4 · DT_2 = ± S m 2` this shows the defect `ε_2 = 1` is attained. -/
theorem sharp_two (m : ℕ) (hm : 2 ≤ m) (hmod : m % 4 = 2 ∨ m % 4 = 3) :
    ¬ (8 : ℤ) ∣ S m 2 := by
  rw [S_two_eval m hm]
  rcases hmod with h | h
  · have hodd : (m - 1) % 2 = 1 := by omega
    rw [(Nat.odd_iff.mpr hodd).neg_one_pow]
    obtain ⟨k, hk⟩ : ∃ k : ℕ, m = 4 * k + 2 := ⟨m / 4, by omega⟩
    subst hk
    rintro ⟨c, hc⟩
    push_cast at hc
    omega
  · have heven : (m - 1) % 2 = 0 := by omega
    rw [(Nat.even_iff.mpr heven).neg_one_pow, one_mul]
    obtain ⟨k, hk⟩ : ∃ k : ℕ, m = 4 * k + 3 := ⟨m / 4, by omega⟩
    subst hk
    rintro ⟨c, hc⟩
    push_cast at hc
    omega

lemma S_three_eval (m : ℕ) (hm : 2 ≤ m) :
    S m 3 = ((3 * m - 1).choose 2 : ℤ) - 1 := by
  rw [S, divisors_three]
  rw [Finset.sum_insert (by decide), Finset.sum_singleton]
  norm_num
  have hμ3 : (moebius 3 : ℤ) = -1 := by
    rw [moebius_apply_prime Nat.prime_three]
  rw [hμ3, a_one]
  have ha3 : a m 3 = ((3 * m - 1).choose 2 : ℤ) := by
    unfold a
    have hpar : ((m - 1) * (3 - 1)) % 2 = 0 % 2 := by
      omega
    rw [neg_one_pow_congr hpar, pow_zero, one_mul]
    congr 2
    ring_nf
  rw [ha3]
  ring

/-- The exact identity `2 · S m 3 = 9 m (m-1)` (in `ℤ`). -/
lemma two_mul_S_three (m : ℕ) (hm : 2 ≤ m) :
    2 * S m 3 = 9 * ((m : ℤ) * ((m : ℤ) - 1)) := by
  rw [S_three_eval m hm]
  have hdvd : 2 ∣ (3 * m - 1) * (3 * m - 2) := by
    have h := Nat.even_mul_succ_self (3 * m - 2)
    rw [show 3 * m - 2 + 1 = 3 * m - 1 by omega] at h
    rw [mul_comm]
    exact h.two_dvd
  have hchoose : ((3 * m - 1).choose 2) * 2 = (3 * m - 1) * (3 * m - 2) := by
    rw [Nat.choose_two_right, show (3 * m - 1) - 1 = 3 * m - 2 by omega]
    exact Nat.div_mul_cancel hdvd
  have hcast : ((3 * m - 1).choose 2 : ℤ) * 2
      = ((3 * m - 1 : ℕ) : ℤ) * ((3 * m - 2 : ℕ) : ℤ) := by
    exact_mod_cast hchoose
  have h1 : ((3 * m - 1 : ℕ) : ℤ) = 3 * (m : ℤ) - 1 := by
    push_cast [Nat.cast_sub (by omega : 1 ≤ 3 * m)]; ring
  have h2 : ((3 * m - 2 : ℕ) : ℤ) = 3 * (m : ℤ) - 2 := by
    push_cast [Nat.cast_sub (by omega : 2 ≤ 3 * m)]; ring
  rw [h1, h2] at hcast
  linear_combination hcast

/-- `9 ∣ S m 3` (unconditional part of integrality at `n = 3`). -/
lemma nine_dvd_S_three (m : ℕ) (hm : 2 ≤ m) : (9 : ℤ) ∣ S m 3 := by
  have h := two_mul_S_three m hm
  have h9 : (9 : ℤ) ∣ 2 * S m 3 := by
    rw [h]; exact dvd_mul_right 9 _
  have hcop : IsCoprime (9 : ℤ) 2 := by
    rw [Int.isCoprime_iff_gcd_eq_one]
    decide
  exact hcop.dvd_of_dvd_mul_left h9

/-- Sharpness at `p = 3`: for `m ≡ 2 (mod 3)`, `27 ∤ S m 3`.  Together with
`9 · DT_3 = ± S m 3` this shows the defect `ε_3 = 1` is attained. -/
theorem sharp_three (m : ℕ) (hm : 2 ≤ m) (hmod : m % 3 = 2) :
    ¬ (27 : ℤ) ∣ S m 3 := by
  intro hdvd
  have h := two_mul_S_three m hm
  have h27 : (27 : ℤ) ∣ 9 * ((m : ℤ) * ((m : ℤ) - 1)) := by
    rw [← h]
    exact hdvd.mul_left 2
  have h3 : (3 : ℤ) ∣ (m : ℤ) * ((m : ℤ) - 1) := by
    obtain ⟨c, hc⟩ := h27
    exact ⟨c, by linarith⟩
  have hp3 : Prime (3 : ℤ) := Int.prime_three
  have hmz : (m : ℤ) % 3 = 2 := by omega
  rcases hp3.dvd_mul.mp h3 with h | h
  · obtain ⟨c, hc⟩ := h
    omega
  · obtain ⟨c, hc⟩ := h
    omega

/-! ## The orbit-sum identity (unconditional; Lemma 3.3 of the paper) -/

/-- The weight statistic of the cyclic-word model, in `ℤ`-form. -/
def wt (m n : ℕ) (x : Fin n → ℕ) : ℤ :=
  ∑ i : Fin n, ((n : ℤ) - 1 - (i : ℕ)) * ((m : ℤ) - 1 - (x i : ℕ))

/-- **Orbit-sum identity**: for `x` with `∑ x i = (m-1) n` (in `ℤ`-form), the
sum of the weights of all `n` cyclic rotations of `x` vanishes.  This is the
engine of the paper's derivative theorem. -/
theorem orbit_sum_zero (m n : ℕ) (hn : n ≠ 0) (x : Fin n → ℕ)
    (hx : ∑ i : Fin n, ((x i : ℕ) : ℤ) = ((m : ℤ) - 1) * n) :
    ∑ k : Fin n, wt m n (fun i => x (i + k)) = 0 := by
  obtain ⟨N, rfl⟩ := Nat.exists_eq_succ_of_ne_zero hn
  simp only [wt]
  rw [Finset.sum_comm]
  apply Finset.sum_eq_zero
  intro i _
  have hshift : ∑ k : Fin (N + 1), ((x (i + k) : ℕ) : ℤ)
      = ∑ j : Fin (N + 1), ((x j : ℕ) : ℤ) :=
    Fintype.sum_bijective _ (Equiv.addLeft i).bijective _ _ (fun k => rfl)
  rw [← Finset.mul_sum]
  have h0 : (∑ k : Fin (N + 1), ((m : ℤ) - 1 - ((x (i + k) : ℕ) : ℤ))) = 0 := by
    rw [Finset.sum_sub_distrib, Finset.sum_const, Finset.card_univ, Fintype.card_fin,
      nsmul_eq_mul, hshift, hx]
    push_cast
    ring
  rw [h0, mul_zero]

end DTLoop
