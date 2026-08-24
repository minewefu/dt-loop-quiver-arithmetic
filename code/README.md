# Code accompanying "Arithmetic of Donaldson-Thomas invariants of loop quivers"

All computations are exact (integer/polynomial arithmetic; FLINT via python-flint,
or plain Python big integers). Python 3.14, `pip install python-flint`.

## Files

- `dt_core.py` — first-principles CoHA engine: computes refined DT invariants
  Omega~_n(z) of the m-loop quiver from the Kontsevich-Soibelman/Efimov
  plethystic factorization of the CoHA Poincare series. Truncation soundness
  via the gauge trick (all operations move q-support upward only).
  `python dt_core.py` runs anchor validation (m=0,1 collapse; Efimov positivity).
- `produce.py` — production runs (m=2..6), writes `data/omega_m{m}.json`.
- `scan_refined.py` — conversion to Reineke's normalization DT_n(q) (dictionary
  verified against published tables), Efimov sanity checks, improved-integrality
  valuation scan, mod-Phi_p congruence scan, root-of-unity tables.
- `test_master.py` — verification of the master identities:
  (M1) barQ_n = PLog(A) + doubling correction (Theorem: exact necklace formula);
  (M2) P_d = q^{-(m-1)C(d,2)} * qbinom(md-1, d-1);
  (M3) R_n = n*barQ_n at n-th roots of unity (with doubling correction);
  (M4) derivative theorem: (q^n - 1) | Laurent-derivative of R_n.
- `test_exact_mobius.py` — admissible (ballot) polynomials A_n(q) by enumeration;
  earlier exploratory test (historical; superseded by test_master.py).
- `test_towers.py` — stress tests of the tower inequalities (T1),(T2),(T3)
  behind Theorem A (m<=10, p in {2,3,5,7}) and the main valuation theorem
  directly from Reineke's formula (m<=10, n<=120, p<=13), incl. sharpness.
- `test_framing.py`, `framed.py`, `refined_framed.py`, `w_world.py`, `mine.py` —
  exploratory scripts from the discovery phase (framed/unframed relation,
  numerical congruence mining); kept for reproducibility of the search.
- `cleanroom/` — independent clean-room implementation of the cyclic-word
  model (written by a separate agent from the definitions only).

## Data

- `../data/omega_m{2..6}.json` — refined invariants Omega~_n(z) as
  {n: [[z-exponent, coeff], ...]}; dictionary to Reineke's DT_n(q):
  DT_n(q) = (-1)^{(m-1)n} sum c * q^{(-e-(m-1)n)/2}.
- `../data/wordmodel_dt.json` — word-model results (DT_n(q) coefficient lists,
  independent enumeration; see wordmodel.py).
- `../data/scan_output.txt` — full scan logs.

## Lean formalization

`../lean/dtformal/Dtformal.lean` — Lean 4 + Mathlib formalization of the
arithmetic core. Builds with `lake build Dtformal` (toolchain
leanprover/lean4:v4.33.0, mathlib v4.33.0); no `sorry`; all theorems depend
only on Lean's standard axioms (see AxiomCheck.lean). Unconditional:
choose_mul_left, S_collapse, sharpness at n = 2, 3, orbit_sum_zero.
Conditional on the Kazandzidis congruences (KazOdd/Kaz2, stated as explicit
hypotheses = Thm 2.2 / Prop 2.3 of the paper): tower_odd, tower_two,
main_bound, improved_integrality_{ge5,three,two}, dt_valuation_ge5.
