# Arithmetic of Donaldson–Thomas invariants of loop quivers

**Improved integrality and exact q-analogues** — paper, verification code, and
partial Lean formalization.

**[📄 paper/paper.pdf](paper/paper.pdf)** (19 pp., LaTeX source included)

## Main results

Let $\mathrm{DT}^{(m)}_n$ be the numerical Donaldson–Thomas invariants of the
$m$-loop quiver ($m \ge 2$), in the sense of Kontsevich–Soibelman / Efimov /
Reineke.

**Theorem 1 (improved integrality, sharp form).** For every prime $p \ge 5$:
$v_p(\mathrm{DT}^{(m)}_n) \ge v_p(n)$ for all $n \ge 1$; moreover
$v_3 \ge v_3(n) - \varepsilon_3(m)$ and $v_2 \ge v_2(n) - \varepsilon_2(m)$,
where $\varepsilon_3(m) = 1$ iff $m \equiv 2 \pmod 3$ and
$\varepsilon_2(m) = 1$ iff $m \equiv 2, 3 \pmod 4$. The bounds are attained,
so the optimal constant with $n \mid \gamma(m)\,\mathrm{DT}^{(m)}_n$ is exactly
$\gamma(m) = 2^{\varepsilon_2}3^{\varepsilon_3}$.

Via the identification of twist-knot extremal BPS invariants with loop-quiver
DT invariants (Garoufalidis–Kucharski–Sułkowski, Prop. 1.2 of
[arXiv:1504.06327](https://arxiv.org/abs/1504.06327)), this **proves the
Improved Integrality Conjecture 1.3 of that paper (an observation they credit
to Kontsevich) for all twist knots, with optimal constants** — reproducing,
now with proof, all twelve $\gamma^{\pm}$ values they tabulated empirically.
The figure-eight case ($m = 3$, $\gamma = 2$) was previously proved by
Basor–Conrey–Morrison ([arXiv:1703.00990](https://arxiv.org/abs/1703.00990));
all other $m$ were open. The torus-knot case (multi-vertex quivers) remains
open and is not claimed.

**Theorem 2 (exact q-identities, all new).** A derivative theorem for Gaussian
binomials at roots of unity ($\zeta B'(\zeta) = (m-1)\binom n2 B(\zeta)$ for
$B = \binom{mn-1}{n-1}_q$, all $\zeta^n = 1$), proved via an orbit-sum
identity for the cyclic-word weight statistic; the first q-supercongruence for
DT invariants ($\Phi_p(q)^2 \mid R_n$ for odd $p \mid n$, with the exact
$p = 2$ defect); and an exact plethystic (necklace) formula for the quantized
invariants through ballot/q-Fuss–Catalan polynomials, sharpening Reineke's
congruence mod $q^n - 1$ to an identity.

**Appendix B.** A self-contained elementary proof of the signed Kazandzidis
supercongruence at $p = 2$:
$\binom{2n}{2k} \equiv (-1)^{k(n-k)}\binom nk \pmod{2\,nk(n-k)\binom nk\,\mathbb{Z}_2}$.

The paper also documents a (verified) erratum to the prefactor in Reineke's
Theorem 6.8 (arXiv:1102.3978).

## Verification

- **Two structurally independent implementations** (first-principles CoHA
  plethystic engine vs. direct cyclic-word enumeration) agree on every
  computed invariant; see [code/README.md](code/README.md).
- Theorem 1 checked numerically for $m \le 10$, $n \le 120$ (and
  independently to $m \le 16$, $n \le 200$ during refereeing); the
  Kazandzidis inputs checked to $n = 300$ with sharpness.
- **Lean 4 formalization** ([lean/dtformal/Dtformal.lean](lean/dtformal/Dtformal.lean)):
  builds against Mathlib with **zero `sorry`**; every theorem passes the axiom
  audit (only `propext`, `Classical.choice`, `Quot.sound`). Machine-checked
  unconditionally: the Möbius collapse, the $n = 2, 3$ sharpness (optimality
  of $\gamma(m)$), and the orbit-sum identity. Machine-checked conditionally
  on the classical Kazandzidis congruences (stated as explicit hypotheses):
  the full reduction to Theorem 1, including the exact $p = 2$ sign
  cancellation. See the paper's §8(e) for the precise scope.
- The manuscript passed a two-round adversarial referee process performed by
  an independent AI agent (report in
  [notes/referee_report.md](notes/referee_report.md)), which verified every
  proof by hand and by fresh computation, checked all citations against the
  primary sources, and identified the prior work and scoping issues fixed in
  revision.

## Provenance

The mathematics in this repository — the conjecture identification, the
theorems, the proofs, both implementations, and the Lean formalization — was
produced by **Claude Fable 5 (Anthropic)** working autonomously under human
direction, in a single supervised session on 2026-07-31 (Lean formalization
2026-08-12). It has **not yet been peer-reviewed by human mathematicians**;
scrutiny, corrections, and issues are very welcome.

## Layout

```
paper/   paper.pdf, paper.tex
code/    exact-arithmetic implementations and verification scripts (Python)
lean/    Lean 4 + Mathlib formalization (lake project)
data/    computed refined DT invariants, verification outputs
notes/   literature dossiers, referee report, source-verification notes
```

License: paper text CC BY 4.0; code MIT.
