# Literature dossier: arithmetic (super)congruences for Donaldson–Thomas / BPS invariants, and the binomial & q-binomial supercongruence toolkit

*Compiled 2026-07-31. Sources: arXiv (incl. full-text extraction of key PDFs), arXiv API abstract searches, journals, general web. All theorem transcriptions below were taken from the actual papers (PDF text extracted) unless explicitly flagged otherwise.*

---

## Executive summary

- **No paper exists** (as of 2026-07-31) proving congruences or supercongruences *for Donaldson–Thomas invariants of quivers* (or of Hilbert schemes / curve counting), in the sense of `c_{pd} ≡ c_d mod p^k` or q-analogues mod `Φ_p(q)^k`. Systematic arXiv abstract searches for {Donaldson–Thomas, cohomological Hall, Kac polynomial, quiver} × {congruence, supercongruence, divisibility, Wolstenholme, mod p} return **zero** relevant hits.
- **However, the *statement* of the numerical supercongruence for loop-quiver DT invariants is essentially anticipated as a conjecture** in the physics/knot-theory literature: Garoufalidis–Kucharski–Sułkowski's **"Improved Integrality" Conjecture 1.3** (2015, attributed to Kontsevich) for extremal BPS invariants of knots — and the extremal BPS invariants of twist/torus knots are literally Möbius/necklace transforms of `binom(me-1, e-1)`, i.e. (signed) m-loop quiver DT invariants. This conjecture is **still open** in print; nobody appears to have noticed that Jacobsthal–Ljunggren proves it for these families.
- A second adjacent cluster is the **2-functions / s-functions** literature (Schwarz–Vologodsky–Walcher; Müller 2021), which proves `mod p^{2r}` and `mod p^{3r}` congruences (`a_{mp^r} ≡ Frob a_{mp^{r-1}}`) for coefficients of open-string/BPS-type generating functions — but only for *rational* generating functions, not the algebraic ones arising from quivers.
- On the toolkit side, everything needed exists and is collected below with exact statements: Wolstenholme / Ljunggren / Jacobsthal–Kazandzidis (incl. p = 2, 3), Straub's q-Ljunggren mod `Φ_p(q)^3` (exact statement with the `(p²−1)/24` correction), Andrews' and Clark's q-analogues, the q-Lucas theorem, Zudilin's mod `Φ_n(q)^4` refinements and q-factorial-ratio congruences, Gorodetsky's **q-Gauss congruences** (the q-analogue of the necklace/Witt congruence — exactly the formalism needed for a "q-necklace" approach to refined DT), and the classical Gauss/Dold/Dieudonné–Dwork/Witt machinery.
- Novelty verdicts (details at the end): **(i)** theorem new, statement partially anticipated (must cite GKS Conj. 1.3, Kontsevich, Müller, SVW); **(ii)** entirely new — would be the first q-supercongruence for refined DT/BPS invariants; **(iii)** new as a theorem; adjacent folklore (λ-rings/Witt vectors, KS admissibility, Habiro-ring Frobenius gluing) must be cited but no published statement exists.

---

# PART A — Novelty scan

## A.0 Queries run and raw outcomes

Web searches (Google-backed) and arXiv API abstract searches (`export.arxiv.org/api`), July 2026:

| Query | Outcome |
|---|---|
| "congruences Donaldson-Thomas invariants" (+quiver) | Only irrelevant hits (modular congruence *subgroups* in Pioline–Schimannek arXiv:2510.23722; DT surveys) |
| "supercongruence Donaldson-Thomas" | Nothing relevant |
| arXiv `abs:"Donaldson-Thomas" AND abs:"divisibility"` | **0 results** |
| arXiv `abs:"Kac polynomial" AND abs:"congruence"` | **0 results** |
| arXiv `all:"supercongruence" AND all:"quiver"` | **0 results** |
| arXiv `abs:"cohomological Hall" AND abs:"congruence"` | **0 results** |
| arXiv `abs:"Wolstenholme" AND (abs:"quiver" OR abs:"Donaldson-Thomas" OR abs:"BPS" OR abs:"knot")` | **0 results** |
| "p-adic Donaldson-Thomas congruence divisibility" | Nothing relevant |
| "arithmetic properties BPS invariants congruence prime" | → Bryan's multiple-cover notes (see A.4); Grünberg–Moree (see A.4) |
| "plethystic exponential congruence", "necklace congruence BPS" | Nothing (plethystic program literature is purely geometric/counting) |
| MathOverflow scans ("congruence Donaldson-Thomas", "Wolstenholme DT") | No relevant threads found |
| "Fuss-Catalan supercongruence mod p^3" | No dedicated paper (see B.5) |

Conclusion of the raw scan: the specific subject "congruences/supercongruences of DT invariants" is **unoccupied territory** in the published record. The genuinely relevant prior art is indirect and is catalogued in A.1–A.6 below.

---

## A.1 THE closest prior art: "Improved Integrality" for extremal BPS invariants (= loop-quiver DT invariants in disguise)

**S. Garoufalidis, P. Kucharski, P. Sułkowski, "Knots, BPS states, and algebraic curves"**, Commun. Math. Phys. **346** (2016) 75–113; arXiv:**1504.06327** [hep-th].

They compute *extremal* (top/bottom row) LMOV/BPS degeneracies `b±_r` of knots from algebraic curves ("extremal A-polynomials"). Exact transcriptions from the paper:

**Proposition 1.2 (GKS).** The extremal BPS invariants of twist knots `K_p` are
```latex
b^-_{K_p,r} = -\frac{1}{r^2}\sum_{d|r}\mu\!\Big(\frac rd\Big)\binom{3d-1}{d-1},\qquad
b^+_{K_p,r} = \frac{1}{r^2}\sum_{d|r}\mu\!\Big(\frac rd\Big)\binom{(2|p|+1)d-1}{d-1}\qquad (p\le -1),
```
```latex
b^-_{K_p,r} = \frac{1}{r^2}\sum_{d|r}\mu\!\Big(\frac rd\Big)(-1)^{d+1}\binom{2d-1}{d-1},\qquad
b^+_{K_p,r} = \frac{1}{r^2}\sum_{d|r}\mu\!\Big(\frac rd\Big)(-1)^{d}\binom{(2p+2)d-1}{d-1}\qquad (p\ge 2).
```
Integrality of `b±_r` (LMOV) already forces the divisor sums to be divisible by `r²`. Then:

> **Conjecture 1.3 (Improved Integrality).** *Given a knot there exist nonzero integers γ± such that for any r ∈ ℕ:* `\frac{1}{r\,\gamma^{\pm}} b^{\pm}_r \in \mathbb{Z}`.

Quote: *"we experimentally discover an Improved Integrality for the BPS invariants, observed by Kontsevich for algebraic curves satisfying the K2 condition [Kon]"* (Kontsevich, Arbeitstagung Bonn 2011 talk). They verified it for twist knots, torus knots, and knots up to 10 crossings; e.g. `γ± = 2` for the figure-eight knot `4₁` (their Table 2 lists `b^-_r` and `2b^-_r/r` as integers). **Status: still an open conjecture** — checked against 2016–2026 literature: the follow-up integrality papers (Luo–Zhu arXiv:1611.06506, "Integrality structures in topological strings I: framed unknot"; W. Wang–Zhu, "BPS invariants from framed links", arXiv:2502.16609 (2025); survey arXiv:2505.02059 (2025)) prove only *plain* integrality, never the improved (r·γ) divisibility.

**Why this is the same thing as (i):** Compare with the numerical DT invariants of the m-loop quiver (Reineke; stated in Reineke's survey arXiv:2410.03219, Example 2.4(5)):
```latex
\widetilde{DT}^{(m)}_d(1) \;=\; \frac{1}{d^2}\sum_{e\mid d}\mu\!\Big(\frac de\Big)\,(-1)^{(m-1)(d-e)}\binom{me-1}{e-1}.
```
So (up to sign conventions) `b^-` of negative twist knots is exactly the 3-loop-quiver DT invariant, `b^-` of positive twist knots the 2-loop one, `b^+` the `(2|p|+1)`- resp. `(2p+2)`-loop one. The knots–quivers correspondence (Kucharski–Reineke–Stošić–Sułkowski, arXiv:1707.02991 [Phys. Rev. D 96 (2017) 121902] and arXiv:1707.04017 [ATMP 23 (2019) 1849–1902]) and Panfil–Stošić–Sułkowski, *"Donaldson-Thomas invariants, torus knots, and lattice paths"*, Phys. Rev. D **98** (2018) 026022, arXiv:1802.04573, make this identification structural (extremal invariants of (2,2p+1) torus knots ↔ m-loop quiver DT invariants ↔ lattice-path/Fuss–Catalan combinatorics).

**Translation to supercongruence form.** By the Almkvist–Zudilin equivalence (Part B.6, Prop. AZ below), for any fixed prime p and `a_e := (-1)^{(m-1)e}\binom{me-1}{e-1}`:
`\sum_{e|d}\mu(d/e)a_e ≡ 0 \bmod d^3` for all d ⟺ `a_{p^k e} ≡ a_{p^{k-1}e} \bmod p^{3k}` for all p, k, e. So GKS Conjecture 1.3 (with γ absorbing p = 2,3 anomalies) is *equivalent* to the order-3 Gauss/necklace supercongruence for the numerators `d^2·DT_d`, which is exactly the arithmetic content of planned result (i). Nobody appears to have observed in print that Jacobsthal–Ljunggren (`\binom{mpe}{pe} ≡ \binom{me}{e} \bmod p^3`, and `\binom{me-1}{e-1} = \frac1m\binom{me}{e}`) yields this for loop quivers.

## A.2 The 2-functions / s-realizable sequences cluster (mod p² and mod p³ congruences for BPS-type series)

- **A. Schwarz, V. Vologodsky, J. Walcher, "Integrality of framing and geometric origin of 2-functions"**, arXiv:**1702.07135**. Defines *2-functions*: power series `V(z)=\sum a_n z^n` (coefficients in a number field K) whose coefficients satisfy the mod-p² Frobenius congruence (in the ℚ-case: `a_{np} ≡ a_n \bmod p^2` in the appropriate Lambert normalization). **Main theorem: the framing operation preserves 2-functions** ("Integrality of Framing"). Geometric origin: q-expansions of truncated normal functions of algebraic cycles on degenerating CY 3-folds; building blocks of open-string/genus-0 BPS generating functions.
- **L. F. Müller, "Wolstenholme type congruences and framing of rational 2-functions"**, arXiv:**2104.10754** (2021). Uses the terminology *s-sequence / s-realizable* (attributed to Almkvist–Zudilin [AZ06]): `a_{mp^r} ≡ a_{mp^{r-1}} \bmod p^{sr}` (with Frobenius twist over K):
  ```latex
  \mathrm{Frob}_{\mathfrak p}\big(a_{p^{r-1}m}\big) - a_{p^r m} \equiv 0 \pmod{p^{sr}\mathcal O_{\mathfrak p}}.
  ```
  **Theorem 1.1 (Müller).** Framings of *rational* 2-functions integrate to **3-sequences**: for primes `p ≥ 5` unramified with `p ∤ N` (N = period), `Frob_p(a^+_{mp^{r-1}}) − a^+_{mp^r} ≡ 0 \bmod p^{3r}\mathcal O_p`, with explicitly quantified corrections at p = 2, 3 (via `γ_p`; `γ_p = 1` for p = 3, `γ_p = 1+ord₂(N+1)` for p = 2). Proved via a new **generalization of Wolstenholme's theorem for weighted harmonic sums** (his Theorem 1.2: for a periodic sequence `(a_k)` of period N, `\sum_{k=1,\,p\nmid k}^{n} \frac{a_{n-k}a_k}{k^2} ≡ 0 \bmod p^{\max\{0,\mathrm{ord}_p(n)-\varepsilon_{p,N}\}}`, with explicit `ε_{p,N}`). Müller *explicitly cites* the GKS twist-knot observation ("improved integrality") as motivation but his hypotheses (rational generating function) **exclude** the algebraic (quiver / knot) cases. He also cites Panfil–Stošić–Sułkowski's DT paper.
- **M. Kontsevich, A. Schwarz, V. Vologodsky, "Integrality of instanton numbers and p-adic B-model"**, Phys. Lett. B **637** (2006) 97–101, hep-th/**0603106** (see also Vologodsky's and Schwarz–Vologodsky's follow-ups, e.g. hep-th/0606151). Proves p-adic integrality statements for genus-0 Gopakumar–Vafa ("instanton") numbers of the quintic via Frobenius on p-adic cohomology (reported caveat: integrality after multiplying by 12, i.e. p ≥ 5 clean). The mirror-symmetry statement "Yukawa coupling coefficients are 3-realizable ⟺ instanton numbers are integers" is the template for the necklace-transform view of (i).

**Assessment:** this cluster proves *exactly the shape* of congruence in (i) (a_{pd} ≡ a_d mod p², p³ with Frobenius), for adjacent-but-different generating functions (rational 2-functions, quintic periods). None of it covers quiver DT invariants; the algebraic/hypergeometric case relevant to loop quivers is explicitly left open (GKS Conj. 1.3).

## A.3 Congruence skein relations for colored HOMFLY-PT / LMOV (arithmetic of BPS invariants of knots)

**Q. Chen, K. Liu, P. Peng, S. Zhu, "Congruent skein relations for colored HOMFLY-PT invariants and colored Jones polynomials"** arXiv:**1402.3571**; published as *"Congruence skein relations for colored HOMFLY-PT invariants"*, Commun. Math. Phys. **400** (2023) 683–729. Motivated by LMOV integrality, they prove *congruence* skein relations for reformulated colored HOMFLY-PT invariants (congruences modulo powers of `[p]` / p in suitable rings, prime p), verified in many cases. This is the main published body of work on "congruences of BPS-type invariants" — but the congruences relate *different knots/colors* (skein-type), not `d ↦ pd` scaling of DT/BPS invariants of a fixed object. Also relevant: S. Zhu's and Luo–Zhu's integrality papers (arXiv:1611.06506) which reprove LMOV integrality for the framed unknot via number theory.

## A.4 Enumerative-geometry congruence culture (weaker, mod p flavor)

- **J. Bryan, R. Pandharipande**, "BPS states of curves in Calabi–Yau 3-folds" (and Bryan's RIMS lecture notes "Multiple cover formulas for GW invariants and BPS states"): GV/BPS **integrality of multiple-cover formulas ⟹ conjectural congruence properties of Hurwitz numbers**, some proven. These are order-1 (necklace/Gauss, mod p) congruences from Möbius inversion — the standard weaker cousin of (i).
- **D. Grünberg, P. Moree (appendix D. Zagier), "Sequences of enumerative geometry: congruences and asymptotics"**, Exp. Math. 17 (2008) 409–426, arXiv:math/0610286: congruences for classical enumerative sequences (lines in hypersurfaces, rational plane curves, quintic instanton numbers). Closest classical-geometry precedent for "congruences of enumerative invariants"; no DT, no supercongruences of Gauss type.
- **I. Itenberg, V. Kharlamov, E. Shustin**, arXiv:1108.3369: Welschinger ≡ genus-0 GW **mod 4** (real vs. complex counts); cf. also "BPS polynomials and Welschinger invariants" arXiv:2506.02770 (2025) which proves *equalities* at q = −1, not congruences.
- **Partition-function congruence culture around Hilbert schemes**: Euler characteristics of `Hilb^n(ℂ²)` are `p(n)` (Ramanujan congruences mod 5,7,11); **N. Gillman, X. Gonzalez, K. Ono, L. Rolen, M. Schoenbauer, "From partitions to Hodge numbers of Hilbert schemes of surfaces"**, Phil. Trans. R. Soc. A 378 (2020) 20180435, arXiv:1902.05421 (equidistribution of Hodge numbers via partition congruences). MacMahon-related congruence papers (k-elongated plane partition diamonds: Andrews–Paule XI; Banerjee–Smoot mod 5^k; arXiv:2508.09723 mod 7^k) concern partition-analysis functions, **not** the MacMahon function `M(q) = \prod (1-q^n)^{-n}` itself, i.e. not `DT(ℂ³)`. No paper states congruences for DT invariants of `Hilb^n(ℂ³)`.

## A.5 Quiver arithmetic (Kac polynomials, counting over 𝔽_q)

- arXiv `abs:"Kac polynomial" AND abs:"congruence"`: **0 results**. The Kac-polynomial literature (Hua's formula; Hausel–Letellier–Rodriguez-Villegas; Davison; Bozec–Schiffmann asymptotics arXiv:2003.06929; refined Kac polynomials arXiv:2207.09839; "Counting representations of quivers with multiplicities" arXiv:2405.14914) concerns positivity, integrality, cohomological interpretations and asymptotics — **no congruence results** for `A_d(q)` values or coefficients.
- **S. Mozgovoy, "Motivic Donaldson–Thomas invariants and Kac conjecture"** arXiv:1103.2100 links quiver DT invariants to Kac polynomials — useful bridge, no arithmetic.
- Background integrality/positivity chain for symmetric quivers: **Kontsevich–Soibelman** arXiv:1006.2706 (COHA; admissible series; integrality of `Ω_d(q)` via λ-ring formalism), **Efimov** arXiv:1103.2736 (positivity: `\widetilde{DT}_d(q) ∈ ℕ[-q^{1/2}]`, quoted as Theorem 2.3 in Reineke's survey arXiv:2410.03219), **Reineke** arXiv:0903.0261 (integrality for loop quivers via functional equations; Compos. Math. 147 (2011) 943–964) and arXiv:1102.3978 (explicit combinatorial formula for *quantized* m-loop DT invariants via degenerate COHA and noncommutative Hilbert schemes, Theorem 6.8 there, in terms of cyclic classes of integer sequences), **Davison–Meinhardt** (integrality via vanishing cycles). None state congruences.

## A.6 Habiro-ring / roots-of-unity arithmetic of DT-type series (2024–26, important for positioning (ii)–(iii))

**S. Garoufalidis, P. Scholze, C. Wheeler, D. Zagier, "The Habiro ring of a number field"**, arXiv:**2412.04241** (Dec 2024). Constructs rings of "collections of power series at each complex root of unity that arithmetically glue with each other after applying a Frobenius endomorphism", graded by `K₃(K)`, with per-prime divisibility structures; inputs from perturbative Chern–Simons theory and **"expansions of the admissible series of Kontsevich–Soibelman"**. Abstract: *"This link suggests that some Donaldson-Thomas invariants have arithmetic meaning and that some elements of the Habiro ring of a number field have enumerative meaning."* This is the most serious recent statement that DT-type q-series carry root-of-unity/Frobenius congruence structure — but it is a *structural/ring-theoretic* framework (quantum dilogarithm / 3-manifold DT flavor), with **no supercongruences for quiver DT invariants** and nothing like `Ω_{pd}(q) ≡ Ω_d(q^{p^2}) mod Φ_p^3`. Classical Habiro ring: `\widehat{\mathbb{Z}[q]} = \varprojlim_n \mathbb{Z}[q]/((q;q)_n)` (Habiro 2004) — the natural home for congruences modulo products of cyclotomics.

Also in this orbit: physics "arithmetic of gauge theories over 𝔽_p" (Y.-H. He, "On fields over fields", arXiv:1003.2986) — zeta functions/point counts, no congruences of BPS numbers.

---

# PART B — Proof tools: exact statements

Conventions: `[n]_q = 1+q+\cdots+q^{n-1} = \frac{q^n-1}{q-1}`, `[n]_q! = [n]_q[n-1]_q\cdots[1]_q`, `\binom{n}{k}_q = \frac{[n]_q!}{[k]_q![n-k]_q!} \in \mathbb{Z}[q]` (Gaussian binomial), `Φ_n(q)` = n-th cyclotomic polynomial. For prime p: `[p]_q = Φ_p(q)`, and `Φ_{p^k}(q) = [p]_{q^{p^{k-1}}}`, `[p^k]_q = \prod_{j=1}^{k}Φ_{p^j}(q)`. Congruences of polynomials mod a monic polynomial mean divisibility of the difference in `\mathbb{Z}[q]` (Gauss's lemma). `v_p` = p-adic valuation.

## B.1 Classical: Babbage, Wolstenholme, Glaisher, Ljunggren, Jacobsthal–Kazandzidis

Primary sources: Wolstenholme (1862); Granville, *"Arithmetic properties of binomial coefficients I"*, CMS Conf. Proc. 20 (1997) 253–275; **R. Meštrović's survey arXiv:1111.3057** ("Wolstenholme's theorem … (1862–2012)"), from which the numbered statements below were extracted verbatim (his equation numbers kept).

- **Babbage (1819).** For primes `p ≥ 3`: `\binom{2p-1}{p-1} \equiv 1 \pmod{p^2}`.
- **Wolstenholme (1862).** For primes `p ≥ 5`:
  ```latex
  \sum_{i=1}^{p-1}\frac 1i \equiv 0 \pmod{p^2},\qquad \sum_{i=1}^{p-1}\frac 1{i^2} \equiv 0 \pmod p,\qquad
  \binom{2p-1}{p-1} \equiv 1 \pmod{p^3}\ \Big(\Longleftrightarrow \binom{2p}{p}\equiv 2 \pmod{p^3}\Big).
  ```
  (Fails for p = 2, 3: `\binom 31 = 3 \equiv 1 \bmod 2` only; `\binom 52 = 10 \equiv 1 \bmod 3^2` only.)
- **Glaisher (1900).** Case b = 1 of Ljunggren; refined form: `\binom{np}{p} \equiv n \pmod{p^3}` for `p ≥ 5`, and (Helou–Terjanian form, survey (44) with m = 1) `\binom{np}{p}\big/ n \equiv 1 - \frac13 n(n-1)p^3 B_{p-3} \pmod{p^4}`.
- **Ljunggren (1952)** [survey (36); also Stanley EC1, Problem 1.6(d)]. For primes `p ≥ 5`, `n ≥ m ≥ 0`:
  ```latex
  \binom{np}{mp} \equiv \binom{n}{m} \pmod{p^3}.
  ```
  Original reference: V. Brun, J. O. Stubban, J. E. Fjeldstad, R. Tambs Lyche, K. E. Aubert, W. Ljunggren, E. Jacobsthal, *"On the divisibility of the difference between two binomial coefficients"*, Den 11te Skandinaviske Matematikerkongress, Trondheim 1949 (publ. 1952), 42–54.
- **Jacobsthal(–Kazandzidis)** [survey (37)]: For `p ≥ 5`, `n ≥ m ≥ 1`:
  ```latex
  \binom{np}{mp} \equiv \binom{n}{m} \pmod{p^t},\qquad t = v_p\big(p^3\, n\, m\, (n-m)\big),
  ```
  "this exponent t can only be increased if p divides `B_{p-3}`" (Wolstenholme primes). Rediscovered by Kazandzidis (Bull. Soc. Math. Grèce 9 (1968) 1–12; 10 (1969) 35–40) and Trakhtman (1974); p-adic proofs by Kazandzidis and by **A. Robert, M. Zuber, "The Kazandzidis supercongruences. A simple proof and an application"**, Rend. Sem. Mat. Univ. Padova **94** (1995) 235–243 (via the Morita p-adic Γ-function); textbook treatment: A. Robert, *A Course in p-adic Analysis*, GTM 198, §VII.1.6.
- **Strong (Z_p-module) form incl. p = 2, 3** (Kazandzidis; Robert–Zuber; Robert GTM 198 — *statement below reconstructed from these sources' framework and verified numerically here for all `2 ≤ n ≤ 35`, `1 ≤ k < n`, `p ∈ {2,3,5,7}`; the exponents 3, 2, 1 are sharp, attained at (n,k) = (2,1)*):
  ```latex
  p\ge 5:\quad \binom{pn}{pk} \equiv \binom nk \pmod{p^3\,nk(n-k)\binom nk\,\mathbb{Z}_p},
  ```
  ```latex
  p= 3:\quad \binom{3n}{3k} \equiv \binom nk \pmod{3^2\,nk(n-k)\binom nk\,\mathbb{Z}_3},
  ```
  ```latex
  p= 2:\quad \binom{2n}{2k} \equiv (-1)^{k(n-k)}\binom nk \pmod{2\,nk(n-k)\binom nk\,\mathbb{Z}_2}.
  ```
  (Without the sign, the p = 2 congruence fails badly.)
- **Helou–Terjanian** (J. Number Theory 128 (2008) 475–499) [survey (41)+(43)]: modulus improvable to `p^s`, `s = v_p(p^3 m(n-m)\binom nm)` (and even `v_p(p^3 mn(n-m)\binom nm)` p-adically); Bernoulli-explicit version:
  ```latex
  \binom{np}{mp}\Big/\binom nm \equiv 1 - \tfrac13\,mn(n-m)\,p^3 B_{p-3} \pmod{p^4}\qquad (p\ge5).
  ```
- **Zhao's mod p⁵ refinement** [survey (42)]: for `p ≥ 7`, with `w_p ≡ (\sum_{k=1}^{p-1} 1/k)/p^2 \pmod{p^2}`:
  `\binom{np}{mp}/\binom nm \equiv 1 + w_p\, nm(n-m)\, p^3 \pmod{p^5}`.
- **Prime-power versions** [survey (38),(39); Robert–Zuber]: for `p ≥ 5`,
  ```latex
  \binom{np^a}{mp^b} \equiv \binom{np^{a-c}}{mp^{b-c}} \pmod{p^{3+a+2b-3c}}\quad (c\le b\le a),\qquad
  \binom{np^a}{mp^a} \equiv \binom{np^{a-1}}{mp^{a-1}} \pmod{p^{3a}}.
  ```
  For `p ≥ 3` (Sun–Davis, survey Rem. 17): `\binom{np}{mp} \equiv \binom nm \bmod p^s`, `s = v_p(p^2 n^2)`.
- **Composite-modulus curiosity** (McIntosh 1995, survey (53)): for the modified binomial `\binom{2n-1}{n-1}' = \prod_{(k,n)=1,\,k\le n}\frac{2n-k}{k}`: `\binom{2n-1}{n-1}' \equiv 1 + n^2\varepsilon_n \pmod{n^3}` with explicit `ε_n ≠ 0` exactly for `n` a power of 2 or divisible by 3 — a clean quantification of the p = 2, 3 anomalies.

## B.2 Straub's q-analogue of Ljunggren (exact, from the paper's PDF)

**A. Straub, "A q-analog of Ljunggren's binomial congruence"**, DMTCS Proc. FPSAC 2011, 897–902; arXiv:**1103.3258**.

> **Theorem 1 (Straub).** For primes `p ⩾ 5` and nonnegative integers `a, b`,
> ```latex
> \binom{ap}{bp}_q \;\equiv\; \binom{a}{b}_{q^{p^2}} \;-\; \binom{a}{b+1}\binom{b+1}{2}\,\frac{p^2-1}{12}\,(q^p-1)^2 \pmod{[p]_q^3}. \tag{2}
> ```
> "The congruence (2) … [is] understood over the ring of polynomials in q with integer coefficients. We remark that p²−1 is divisible by 12 for all primes p ⩾ 5."

Since `\binom{a}{b+1}\binom{b+1}{2} = \binom ab\,\frac{b(a-b)}{2}`, the correction term equals `-\binom ab\, b(a-b)\,\frac{p^2-1}{24}(q^p-1)^2` — this is the "(p²−1)/24" form (used e.g. by Zudilin and Gorodetsky):
```latex
\binom{ap}{bp}_q \equiv \binom{a}{b}_{q^{p^2}} - \binom ab\, b(a-b)\,\frac{p^2-1}{24}\,(q^p-1)^2 \pmod{\Phi_p(q)^3}.
```
Note `[p]_q = Φ_p(q)` for prime p, and `q → 1` recovers Ljunggren. Straub's Example 2 (p = 13, a = 2, b = 1): `\binom{26}{13}_q = 1 + q^{169} - 14(q^{13}-1)^2 + [13]_q^3 f(q)`.

Key intermediate steps (transcribed):
- Via the q-Chu–Vandermonde identity (his Theorem 4) one gets Clark's q-Babbage [W. E. Clark, IJMMS 18 (1995) 197–200]:
  ```latex
  \binom{ap}{bp}_q \equiv \binom ab_{q^{p^2}} \pmod{[p]_q^2}, \tag{7}
  ```
  and the reduction identity
  ```latex
  \binom{ap}{bp}_q \equiv \binom ab_{q^{p^2}} + \binom{a}{b+1}\binom{b+1}{2}\Big(\binom{2p}{p}_q - [2]_{q^{p^2}}\Big) \pmod{[p]_q^3}, \tag{11}
  ```
  reducing everything to the case a = 2, b = 1.
- **Lemma 5 (q-Wolstenholme).** For primes `p ⩾ 5`:
  ```latex
  \binom{2p}{p}_q \equiv [2]_{q^{p^2}} - \frac{p^2-1}{12}(q^p-1)^2 \pmod{[p]_q^3}.
  ```
- **Shi–Pan q-harmonic congruences** [L.-L. Shi, H. Pan, Amer. Math. Monthly 114 (2007) 529–531], quoted as Theorem 3: for `p ⩾ 5`,
  ```latex
  \sum_{i=1}^{p-1}\frac{1}{[i]_q} \equiv -\frac{p-1}{2}(q-1) + \frac{p^2-1}{24}(q-1)^2[p]_q \pmod{[p]_q^2},\qquad
  \sum_{i=1}^{p-1}\frac{1}{[i]_q^2} \equiv -\frac{(p-1)(p-5)}{12}(q-1)^2 \pmod{[p]_q},
  ```
  whence `\sum_{1\le i<j\le p-1}\frac{1}{[i]_q[j]_q} \equiv \frac{(p-1)(p-2)}{6}(q-1)^2 \pmod{[p]_q}` (his (13)).
- **Remark 6 (Jacobsthal in q-context).** "Jacobsthal … generalized (1) to hold modulo `p^{3+r}` where r is the p-adic valuation of `ab(a-b)\binom ab = 2a\binom{a}{b+1}\binom{b+1}{2}`. It would be interesting to see if this generalization has a nice analog in the q-world." — *i.e. a q-Jacobsthal is explicitly posed as an open problem (2011); still open as far as this scan found. Directly relevant to (ii).*

**General n (composite) version.** **A. Straub, "Supercongruences for polynomial analogs of the Apéry numbers"**, Proc. AMS **147** (2019) 1023–1036, arXiv:**1803.07146**, Theorem 2.2 (as quoted in both Zudilin arXiv:1901.07843 and Gorodetsky arXiv:1805.01254, eq. (2.13)):
```latex
\binom{am}{bm}_q \equiv \binom ab_{q^{m^2}} - \binom ab\, b(a-b)\,\frac{m^2-1}{24}\,(q^m-1)^2 \pmod{\Phi_m(q)^3}
```
for all `m ≥ 1` with `(m,6)=1` (Gorodetsky's precise quotation; note `24 \mid m^2-1` then). Substituting `m = p^k` gives `\binom{ap^k}{bp^k} \equiv \binom ab \bmod p^3` — but see B.7 for the stronger `p^{3k}` statement. In the same paper Straub proves the q-Apéry supercongruence
`A_{nm}(q) \equiv A_n(q^{m^2}) - (q^m-1)^2\frac{m^2-1}{12}n^2 A_n(1) \pmod{Φ_m(q)^3}` (his Cor. 1.1, quoted by Gorodetsky as (2.18)).

**Follow-up:** B. Ning, *"An inductive proof of Straub's q-analogue of Ljunggren's congruence"*, arXiv:1301.2986 (2013). Variants for a = 2, b = 1: Cai & García-Pulgarín (2001), per Gorodetsky §2.3.

## B.3 The q-Lucas theorem (Olive; Désarménien)

Standard statement (see e.g. Désarménien, *"Un analogue des congruences de Kummer pour les q-nombres d'Euler"*, European J. Combin. 3 (1982) 19–28; G. Olive, *"Generalized powers"*, Amer. Math. Monthly 72 (1965) 619–627; modern quotations in Straub arXiv:1802.02684 and Adamczewski–Bell–Delaygue–Jouhet):

> **q-Lucas theorem.** Let `n ≥ 1`, and write `m = an + b`, `k = rn + s` with `0 ≤ b, s ≤ n−1`. Then
> ```latex
> \binom{m}{k}_q \;\equiv\; \binom{a}{r}\,\binom{b}{s}_q \pmod{\Phi_n(q)}.
> ```
> Equivalently, at any primitive n-th root of unity ω: `\binom mk_\omega = \binom ar \binom bs_\omega`.

Special case (`n = p` prime, q → 1) recovers Lucas' theorem digit-by-digit. Zudilin's paper (B.4) records the "trivial (q-Lucas) congruence" as `\binom{an}{bn}_q \equiv \binom ab = \binom{a-1}{b} + \binom{a-1}{a-b} \pmod{Φ_n(q)}`. Sagan, *"Congruence properties of q-analogs"*, Adv. Math. 95 (1992) 127–143, develops systematic consequences (q-Catalan etc.).

## B.4 Andrews' q-Babbage/Wolstenholme/Glaisher, Pan's extension, and Zudilin's mod Φ⁴ refinements

**G. E. Andrews, "q-analogs of the binomial coefficient congruences of Babbage, Wolstenholme and Glaisher"**, Discrete Math. **204** (1999) 15–25. Main statement (quoted exactly in Gorodetsky arXiv:1805.01254 §2.3 as [And99, Thm. 3]): for odd primes p,
```latex
\binom{ap}{bp}_q \;\equiv\; q^{(a-b)b\binom p2}\,\binom ab_{q^p} \pmod{[p]_q^2}.
```
Andrews also shows (complementary result, ibid.) that the full classical mod-p³ congruence (1) can be *derived* from this q-analogue — i.e. the q-analog "sees" one power of p more than its naive q → 1 limit. (Compare Clark's variant (7) above, with `q^{p^2}` and no q-power prefactor.)

**Zudilin's synthesis and refinements** — **W. Zudilin, "Congruences for q-binomial coefficients"**, Ann. Comb. **23** (2019) 1123–1135, arXiv:**1901.07843** (full text extracted; notation `σ_n = (−1)^{n−1}`):
- Andrews' congruence in general-n form, eq. (4): `\binom{an}{bn}_q \equiv σ_n^{b(a-b)}\, q^{b(a-b)\binom n2}\, \binom ab_{q^n} \pmod{Φ_n(q)^2}` for any n > 1 (Andrews: n = p > 3).
- **Hao Pan's mod Φ³ extension** [H. Pan, *"Factors of some lacunary q-binomial sums"*, Monatsh. Math. 172 (2013) 387–398], eq. (5):
  ```latex
  \binom{an}{bn}_q \equiv σ_n^{b(a-b)} q^{b(a-b)\binom n2}\binom ab_{q^n} + ab(a-b)\binom ab\,\frac{n^2-1}{24}(q^n-1)^2 \pmod{Φ_n(q)^3}.
  ```
- Zudilin's own (3): `\binom{an}{bn}_q σ_n^b q^{\binom{bn}2} \equiv \binom{a-1}b + \binom{a-1}{a-b} σ_n^a q^{\binom{an}2} \pmod{Φ_n(q)^2}`.
- **Theorem 1 (Zudilin, mod Φ⁴).** For any n > 1:
  ```latex
  \binom{an}{bn}_q \equiv \binom ab_{q^{n^2}} - b(a-b)\binom ab (q^n-1)\Big( a\sum_{k=1}^{n-1}\frac{q^k}{1-q^k} + \frac{a(n-1)}2 + \frac{(a+1)(n^2-1)}{24}(q^n-1) + \frac{(b(a-b)n-a-2)(n^2-1)}{48}(q^n-1)^2 \Big) \pmod{Φ_n(q)^4}.
  ```
- **Theorem 2 (Zudilin, mod Φ⁴).** For any n > 1:
  ```latex
  \binom{an}{bn}_q \equiv σ_n^{b(a-b)} q^{b(a-b)\binom n2}\binom ab_{q^n} - ab(a-b)\binom ab(q^n-1)\Big( \sum_{k=1}^{n-1}\frac{q^k}{1-q^k} + \frac{n-1}2 - \frac{(b(a-b)n-1)(n^2-1)}{48}(q^n-1)^2 \Big) \pmod{Φ_n(q)^4}.
  ```
  Both are q-analogues of `\binom{ap}{bp} \equiv \binom ab + ab(a-b)\binom ab\, p\sum_{k=1}^{p-1}\frac1k \pmod{p^4}` (p > 3).
- Useful q-harmonic expansions proved en route:
  ```latex
  \sum_{k=1}^{n-1}\frac{q^k}{1-q^k} \equiv -\frac{n-1}2 - \frac{n^2-1}{24}(q^n-1) + \frac{(n-1)(n^2-1)}{48n}(q^n-1)^2 + \frac{(q^n-1)^2}{2n^2}\sum_{k=1}^{n-1}\frac{kq^k((k+1)q^k+k-1)}{(1-q^k)^3} \pmod{Φ_n(q)^3}.
  ```
- **Theorem 3 (q-factorial ratios — directly relevant to quiver DT series!).** For `\mathbf a, \mathbf b` with `\sum a_i = \sum b_j` and the Landau condition, set `D_n(q) = \frac{[a_1n]!\cdots[a_rn]!}{[b_1n]!\cdots[b_sn]!}` and `c_i = \sum_j\binom{a_j}i - \sum_j\binom{b_j}i` (i = 2,3). Then for any n ≥ 1:
  ```latex
  D_n(q) \equiv D_1(q^{n^2}) - D_1(1)\,c_2\,\frac{n^2-1}{24}(q^n-1)^2 \pmod{Φ_n(q)^3},
  ```
  ```latex
  D_n(q) \equiv σ_n^{c_2} q^{c_2\binom n2} D_1(q^n) + D_1(1)\,(c_2+c_3)\,\frac{n^2-1}{12}(q^n-1)^2 \pmod{Φ_n(q)^3},
  ```
  valid even for the *rational functions* `D_n(q)` assuming only the balancing `\sum a_i = \sum b_j`. Zudilin explicitly suggests "the polynomials D_n(q) satisfy q-Gauss relations from [Gorodetsky]" as an open direction. Related Lucas-type congruences for `D_n(q)`: **Adamczewski–Bell–Delaygue–Jouhet**, *"Congruences modulo cyclotomic polynomials and algebraic independence for q-series"*, Sém. Lothar. Combin. 78B (2017), #54.

## B.5 p-adic valuations: Kummer's theorem, `binom(mp^k, p^k)`, Fuss–Catalan

- **Kummer (1852).** `v_p\binom{n}{m}` = number of carries when adding m and n−m in base p.
- Consequence for the quantities relevant to loop quivers: adding `p^k` and `(m-1)p^k` in base p has the same carries as adding 1 and m−1 (shift by k digits), so
  ```latex
  v_p\binom{mp^k}{p^k} = \#\{\text{carries adding } 1,\ m-1 \text{ in base } p\} = v_p\binom m1 \text{-independent of } k;\quad \text{in particular } =0 \text{ if } m \le p.
  ```
  Combined with B.1: `\binom{mp^k}{p^k} \equiv \binom{mp^{k-1}}{p^{k-1}} \pmod{p^{3k}}` (p ≥ 5).
- **Fuss–Catalan numbers** `C^{(m)}_d = \frac{1}{(m-1)d+1}\binom{md}{d} = \frac1{md+1}\binom{md+1}{d}` (Fuss 1791). Note the loop-quiver binomial is `\binom{md-1}{d-1} = \frac1m\binom{md}{d} = \frac{(m-1)d+1}{m}\,C^{(m)}_d`.
- Dedicated literature on p-adic valuations of Fuss–Catalan numbers: **sparse — no single canonical paper found** (arXiv scan). The Catalan case (m = 2) is classical: **R. Alter, K. K. Kubota, "Prime and prime power divisibility of Catalan numbers"**, J. Combin. Theory Ser. A 15 (1973) 243–256; **E. Deutsch, B. Sagan, "Congruences for Catalan and Motzkin numbers and related sequences"**, J. Number Theory 117 (2006) 191–215, arXiv:math/0407326 (Lucas-type and 2-adic results); Eu–Liu–Yeh (Catalan/Motzkin mod 4, 8); Pomerance's notes on Catalan divisibility; Aebi–Cairns (Catalan `C_p ≡ 2 mod p` etc.). For (i)-type arguments the working tool is simply Kummer + Jacobsthal: e.g. for `p ∤ (m-1)d+1` and `p ∤ (m-1)pd+1`-type side conditions, Ljunggren transfers directly to Fuss–Catalan quotients:
  ```latex
  C^{(m)}_{pd} \equiv \frac{(m-1)d+1}{(m-1)pd+1}\,C^{(m)}_{d}\ \cdot\ u \pmod{p^3\text{-corrections}},
  ```
  best handled through `\binom{md-1}{d-1}` (no rational prefactor) as in GKS/Reineke's formulas.
- q-side: q-Catalan `\frac{1}{[n+1]_q}\binom{2n}{n}_q ∈ ℕ[q]`; congruence framework in Sagan (Adv. Math. 1992); "q-rious positivity" for q-factorial ratios: Warnaar–Zudilin, Aequat. Math. 81 (2011) 177–183 (conjecture that every integral factorial ratio has `D_n(q) ∈ ℕ[q]`; partial results known — verify current status before citing any full proof).

## B.6 Gauss/Dold/necklace congruences, Witt vectors, Dieudonné–Dwork

**Definition (Gauss congruences).** `(a_n)_{n≥1} ⊂ ℤ` satisfies the Gauss congruences if `\sum_{d|n}\mu(d)a_{n/d} \equiv 0 \pmod n` for all n. Other names: Gauss sequence, generalized Fermat sequence, **Dold sequence**, *realizable* sequence. Key classical references: Gauss (`a^n`); A. Dold, *"Fixed point indices of iterated maps"*, Invent. Math. 74 (1983) 419–435; A. V. Zarelua, *"On congruences for the traces of powers of some matrices"*, Proc. Steklov Inst. Math. 263 (2008) 78–98 (survey + proofs; `a_n = \mathrm{Tr}(A^n)`, A integer matrix); R. Minton, *"Linear recurrence sequences satisfying congruence conditions"*, Proc. AMS 142 (2014) 2337–2352; Steinlein (2017 survey); **F. Beukers, M. Houben, A. Straub, "Gauss congruences for rational functions in several variables"**, Indag. Math. 29 (2018) 1259–1274, arXiv:**1710.00423**.

**Equivalences** (as compiled in Gorodetsky arXiv:1805.01254, Prop. 3.1, citing Stanley EC1 Ch. 5 Ex. 5.2(a)):
> For `(a_n) ⊂ ℤ` TFAE:
> 1. Gauss congruences: `\sum_{d|n}\mu(d)a_{n/d} \equiv 0 \bmod n` for all n;
> 2. `a_{p^k n} \equiv a_{p^{k-1} n} \pmod{p^k}` for all primes p and all n, k ≥ 1;
> 3. `\exp\big(\sum_{n\ge1} a_n x^n/n\big) \in \mathbb{Z}[[x]]`.

Equivalently (necklace form): `F(x) = \prod_{d\ge1}(1-x^d)^{-M_d}` with all necklace-transform exponents `M_d = \frac1d\sum_{e|d}\mu(d/e)a_e \in \mathbb{Z}` — this is precisely the DT-integrality shape (Euler-product/plethystic-exponential factorization with integer exponents). The Witt-vector formulation: `(a_n)` is in the image of the ghost map of the big Witt vectors `W(\mathbb{Z}) \to \mathbb{Z}^{\mathbb N}` iff the Gauss congruences hold (Hazewinkel, *Witt vectors, Part 1*, arXiv:0804.3888; over `ℤ_p`: `(a_n)` is a ghost vector iff `a_{p^k m} ≡ a_{p^{k-1}m} \bmod p^k`). Cyclotomic identity & necklace algebra: Metropolis–Rota, *"Witt vectors and the algebra of necklaces"*, Adv. Math. 50 (1983) 95–125; Dress–Siebeneicher, Adv. Math. 70 (1988).

**Higher-order Gauss congruences — the exact tool for (i)** (Gorodetsky Prop. 3.2 = **Almkvist–Zudilin, "Differential equations, mirror maps and zeta values"**, AMS/IP Stud. Adv. Math. 38 (2006) 481–515, **Proposition 11**):
> For `(a_n) ⊂ ℤ` and `m ≥ 1` TFAE:
> 1. `\sum_{d|n}\mu(n/d)\,a_d \equiv 0 \pmod{n^m}` for all n ≥ 1;
> 2. `a_{p^k n} \equiv a_{p^{k-1} n} \pmod{p^{km}}` for all primes p and n, k ≥ 1.

(AZ06 also coined *s-realizable*; m = 2, 3 are the "2-/3-function" conditions of A.2. This proposition is the dictionary between "improved integrality" divisor-sum divisibility and supercongruences `c_{pd} ≡ c_d`.)

**Dieudonné–Dwork lemma** (Gorodetsky Prop. 3.4, citing **A. Robert, GTM 198, §VII.2.3**; also Koblitz, *p-adic Numbers…*, Ch. on Dwork's lemma; original: B. Dwork, *"Norm residue symbol in local number fields"*, Abh. Math. Sem. Univ. Hamburg 22 (1958) 503–516):
> Fix a prime p, `F(x) = \exp\big(\sum_{n\ge1} a_n x^n/n\big) \in \mathbb{Q}[[x]]`. TFAE:
> 1. `a_{p^k n} \equiv a_{p^{k-1}n} \pmod{p^k \mathbb{Z}_p}` for all n, k (Gauss congruences w.r.t. {p});
> 2. `F(x) \in \mathbb{Z}_p[[x]]`;
> 3. `F(x^p)/F(x)^p \in 1 + p\,x\,\mathbb{Z}_p[[x]]`.
>
> (Frobenius-twisted version over unramified extensions: `F^{\sigma}(x^p)/F(x)^p \in 1+px\mathcal O[[x]]` with σ the Frobenius lift.) The Artin–Hasse exponential `\exp(\sum_{k\ge0} x^{p^k}/p^k) \in \mathbb{Z}_{(p)}[[x]]` is the standard first application. Multivariable/Hasse–Witt matrix generalizations ("Dwork-type congruences", `\frac{F(x)}{F^{\sigma}(x^p)} \bmod p^s` for period-like series): Mellit–Vlasenko; **A. Varchenko, W. Zudilin, "Congruences for Hasse–Witt matrices and solutions of p-adic KZ equations"**, arXiv:2108.12679.

**In DT language:** for a symmetric quiver, `\log` of the (specialized) partition function has coefficients `g_d = d\,[x^d]\log F`; DT integrality is the statement that the necklace transform of `(g_d)` is integral, i.e. `(g_d)` satisfies Gauss congruences — the m = 1 case. Planned result (iii) = upgrading this from folklore to a stated theorem with Frobenius/Adams structure (`ψ^p ≡ (\cdot)^p \bmod p` in λ-rings — Wilkerson's criterion; cf. Kontsevich–Soibelman's λ-ring "admissibility" in arXiv:1006.2706 §6); planned (i) = the m = 3 (order-3) case for loop quivers.

## B.7 q-analogues of the necklace/Gauss congruence — **Gorodetsky's q-Gauss framework** (the key modern tool for (ii))

**O. Gorodetsky, "q-congruences, with applications to supercongruences and the cyclic sieving phenomenon"**, Int. J. Number Theory 15 (2019), arXiv:**1805.01254** (full text extracted).

> **Definition 1.1 (q-Gauss congruences).** `\{a_n(q)\}_{n\ge1} \subset \mathbb{Z}[q]` satisfies the q-Gauss congruences if for all n ≥ 1:
> ```latex
> \sum_{d\mid n}\mu(d)\,a_{n/d}(q^d) \;\equiv\; 0 \pmod{[n]_q}.
> ```
> **Lemma 2.2.** This implies, for all primes p and n, k ≥ 1: `a_{p^k n}(q) \equiv a_{p^{k-1}n}(q^p) \pmod{[p^k]_q}`. (k = 1 is a special case of q-Lucas congruences; q = 1 recovers the classical Gauss congruences. "There is no implication in the reverse direction.")
> **Corollary 2.3 (root-of-unity criterion).** q-Gauss ⟺ `a_n(\omega) = a_{n/\mathrm{ord}(\omega)}(1)` for all n and all `ω ∈ μ_n` ⟺ `a_n(q) \equiv a_{n/d}(1) \pmod{Φ_d(q)}` for all `d | n`.

Examples proved there: `\binom{an}{bn}_q`, `\binom{an-1}{bn}_q`, `[t^{bn}]\prod_{i=0}^{n-1}(1-tq^i)^a`, q-central trinomials `\sum_i q^{i(i+b)}\binom ni_q\binom{n-i}i_q`, q-Lucas numbers `\mathrm{Tr}(A(q^{n-1})\cdots A(1))`. Earlier isolated q-example: **H. Pan, "A q-analogue of Gauss' divisibility theorem"**, arXiv:0804.0834 (`a_n(q) = \prod_{i=1}^n[a]_{q^i}`, congruence mod `[n]_{q^{\gcd(n,a)}}`).

> **Definition 1.7 / 2.6 (q-Gauss congruences of order r).** q-Gauss holds and additionally for `1 ≤ j ≤ r−1` the functions `ω \mapsto ω^j a_n^{(j)}(ω)` on `μ_n` depend only on `\mathrm{ord}(ω)`.
> **Theorem 2.4 (consequences).** If `(a_n(q))` satisfies q-Gauss of order r, then for primes `p ≥ r+1` and all n, k: `a_{np^k}(1) \equiv a_{np^{k-1}}(1) \pmod{p^{rk}}`; more precisely the first `1+\min\{p-2, r-1\}` "`[n]_q`-digits" of `a_{mn}(q)` are given by an explicit recursion, and
> ```latex
> \sum_{d\mid n}\mu\big(\tfrac nd\big)\,a_{md}(1) \;\equiv\; 0 \pmod{n^{1+\min\{p-2,\,r-1\}}}\qquad (p = \text{smallest prime factor of } n).
> ```
> **Corollary 2.5** gives the explicit base-`[n]_q` digits `f_0, f_1, f_2` for order 3 when `(n,6)=1`: `a_{nm}(q) \equiv f_0(q) + f_1(q)[n]_q + f_2(q)[n]_q^2 \pmod{[n]_q^3}`.
> **Theorem 2.6 (q-binomials have order 3).** For `a_n(q)=\binom{an}{bn}_q`, all n and `ω ∈ μ_n`:
> ```latex
> a_n(\omega)=a_{\frac{n}{\mathrm{ord}\,\omega}}(1),\qquad
> \omega\,a_n'(\omega)=\mathrm{ord}(\omega)^2\binom{an/\mathrm{ord}\,\omega}{bn/\mathrm{ord}\,\omega}\frac{b(a-b)n^2}{2},
> ```
> ```latex
> \omega^2 a_n''(\omega)=\binom{an/\mathrm{ord}\,\omega}{bn/\mathrm{ord}\,\omega} b(a-b)n^2\Big(\frac{b(a-b)n^2}{4}+\frac{an\cdot\mathrm{ord}(\omega)-5}{12}\Big),
> ```
> whence the first q-analogue of **Jacobsthal–Ljunggren at prime powers**: `\binom{ap^k}{bp^k} \equiv \binom{ap^{k-1}}{bp^{k-1}} \pmod{p^{3k}}` (p ≥ 5), with a full q-congruence mod `[p^k]_q^3`. For n = p ≥ 5, m = 1 the explicit digit expansion reads (his (2.12); OCR-checked)
> ```latex
> \binom{ap}{bp}_q \equiv \binom ab + \binom ab\frac{b(a-b)p}{2}(q^p-1) + \binom ab\frac{b(a-b)}{2}\Big(\frac{b(a-b)}{4}p^2 + \frac{ap^2-5}{12} - \frac{p-1}{2}\Big)(q^p-1)^2 \pmod{[p]_q^3}.
> ```
> Analogous order-3 results for q-Apéry numbers (Thm 2.7 ⟹ Beukers–Coster supercongruence `g_{np^k} ≡ g_{np^{k-1}} \bmod p^{3k}`) and for the Almkvist–Zudilin ζ-sequence (Thm 2.8 — new supercongruence).

**Other q-necklace-adjacent items:** T. Hyde, *"Cyclotomic factors of necklace polynomials"*, arXiv:1811.08601 (vanishing/factorization of `M_d(q) = \frac1d\sum_{e|d}\mu(e)q^{d/e}` at roots of unity); V. J. W. Guo, *"Dwork-type q-congruences through the q-Lucas theorem"*, arXiv:2310.15207 (2023). **No q-analogue of the necklace congruence has ever been applied to plethystic exponentials / DT products** — the combination "q-Gauss congruences + quantum dilogarithm products `(q^{1/2+k}x; …)`" is unclaimed territory (Zudilin's Theorem 3 on q-factorial ratios and his closing remark are the nearest approach).

---

# PART C — The q-supercongruence landscape (positioning paragraph)

Since 2018 the field of q-supercongruences has exploded around **Guo–Zudilin's "creative q-microscoping"**: *"A q-microscope for supercongruences"*, Adv. Math. **346** (2019) 329–358, arXiv:**1803.01830**, which proves Ramanujan/van-Hamme-type supercongruences by establishing q-analogues modulo `Φ_n(q)^2` or `Φ_n(q)^3` (often with an auxiliary parameter a and the radial/root-of-unity asymptotic method), then specializing `q → 1`. The surrounding corpus includes: Guo, *"q-Analogues of Dwork-type supercongruences"* (arXiv:1910.07551), Guo–Zudilin, *"Dwork-type supercongruences through a creative q-microscope"*, J. Combin. Theory Ser. A **178** (2021) 105362 (arXiv:2001.02311), Guo–Schlosser (q-hypergeometric transformation methods), Gorodetsky's derivative/q-Gauss method (arXiv:1805.01254), Straub's polynomial-Apéry supercongruences (arXiv:1803.07146), Zudilin's mod-`Φ⁴` binomial congruences (arXiv:1901.07843), and Adamczewski–Bell–Delaygue–Jouhet's Lucas-type `Φ_n`-congruences for q-factorial ratios. The philosophy uniformly is: *q-congruences modulo powers of `Φ_p(q)` are strictly finer invariants than p-adic congruences, and the q-world supplies extra leverage (roots of unity, derivatives, parameter deformation)*. A paper proving q-supercongruences for **refined DT invariants of quivers** would connect this active number-theory industry to geometric representation theory / BPS counting for the first time — the natural bridging objects being exactly the q-factorial-ratio congruences (Zudilin Thm 3), the q-Gauss formalism (Gorodetsky), and the Habiro-ring/root-of-unity arithmetic of KS admissible series (Garoufalidis–Scholze–Wheeler–Zagier).

---

# Bibliography (with arXiv IDs where they exist)

**Arithmetic of BPS/DT-adjacent invariants (Part A):**
1. S. Garoufalidis, P. Kucharski, P. Sułkowski, *Knots, BPS states, and algebraic curves*, Commun. Math. Phys. 346 (2016) 75–113. arXiv:1504.06327. [Improved Integrality Conj. 1.3; extremal BPS = necklace transforms of `binom(me-1,e-1)`.]
2. P. Kucharski, M. Reineke, M. Stošić, P. Sułkowski, *BPS states, knots and quivers*, Phys. Rev. D 96 (2017) 121902. arXiv:1707.02991; *Knots-quivers correspondence*, Adv. Theor. Math. Phys. 23 (2019) 1849–1902. arXiv:1707.04017.
3. M. Panfil, M. Stošić, P. Sułkowski, *Donaldson–Thomas invariants, torus knots, and lattice paths*, Phys. Rev. D 98 (2018) 026022. arXiv:1802.04573.
4. A. Schwarz, V. Vologodsky, J. Walcher, *Integrality of framing and geometric origin of 2-functions*, arXiv:1702.07135.
5. L. F. Müller, *Wolstenholme type congruences and framing of rational 2-functions*, arXiv:2104.10754; L. F. Müller, *Rational 2-functions are abelian*, arXiv:2006.06388.
6. M. Kontsevich, A. Schwarz, V. Vologodsky, *Integrality of instanton numbers and p-adic B-model*, Phys. Lett. B 637 (2006) 97–101. hep-th/0603106; A. Schwarz, V. Vologodsky, *Frobenius transformation, mirror map and instanton numbers*, hep-th/0606151.
7. Q. Chen, K. Liu, P. Peng, S. Zhu, *Congruence skein relations for colored HOMFLY-PT invariants*, Commun. Math. Phys. 400 (2023) 683–729. arXiv:1402.3571.
8. W. Luo, S. Zhu, *Integrality structures in topological strings I: framed unknot*, arXiv:1611.06506; W. Wang, S. Zhu, *BPS invariants from framed links*, arXiv:2502.16609.
9. S. Garoufalidis, P. Scholze, C. Wheeler, D. Zagier, *The Habiro ring of a number field*, arXiv:2412.04241.
10. M. Reineke, *Donaldson–Thomas invariants of symmetric quivers* (survey), arXiv:2410.03219. [Contains `\widetilde{DT}^{(m)}_d(1)` formula, Efimov's positivity as Thm 2.3.]
11. M. Reineke, *Cohomology of quiver moduli, functional equations, and integrality of Donaldson–Thomas type invariants*, Compos. Math. 147 (2011) 943–964. arXiv:0903.0261.
12. M. Reineke, *Degenerate Cohomological Hall algebra and quantized Donaldson–Thomas invariants for m-loop quivers*, Doc. Math. 17 (2012) 1–22. arXiv:1102.3978. [Thm 6.8: combinatorial formula for quantized m-loop DT invariants.]
13. M. Kontsevich, Y. Soibelman, *Cohomological Hall algebra, exponential Hodge structures and motivic DT-invariants*, Commun. Number Theory Phys. 5 (2011) 231–352. arXiv:1006.2706.
14. A. I. Efimov, *Cohomological Hall algebra of a symmetric quiver*, Compos. Math. 148 (2012) 1133–1146. arXiv:1103.2736.
15. S. Mozgovoy, *Motivic Donaldson–Thomas invariants and Kac conjecture*, arXiv:1103.2100.
16. J. Bryan, R. Pandharipande, *BPS states of curves in Calabi–Yau 3-folds*, Geom. Topol. 5 (2001); J. Bryan, *Multiple cover formulas for GW invariants and BPS states*, RIMS Kokyuroku 1232 (2001).
17. D. Grünberg, P. Moree (app. D. Zagier), *Sequences of enumerative geometry: congruences and asymptotics*, Exp. Math. 17 (2008) 409–426. arXiv:math/0610286.
18. N. Gillman, X. Gonzalez, K. Ono, L. Rolen, M. Schoenbauer, *From partitions to Hodge numbers of Hilbert schemes of surfaces*, Phil. Trans. R. Soc. A 378 (2020). arXiv:1902.05421.
19. I. Itenberg, V. Kharlamov, E. Shustin, *Welschinger invariants of real del Pezzo surfaces of degree ≥ 3*, arXiv:1108.3369. [Welschinger ≡ GW mod 4.]

**Toolkit (Part B):**
20. R. Meštrović, *Wolstenholme's theorem: its generalizations and extensions in the last hundred and fifty years (1862–2012)*, arXiv:1111.3057.
21. A. Granville, *Arithmetic properties of binomial coefficients I: binomial coefficients modulo prime powers*, CMS Conf. Proc. 20 (1997) 253–275.
22. Brun–Stubban–Fjeldstad–Tambs Lyche–Aubert–Ljunggren–Jacobsthal, *On the divisibility of the difference between two binomial coefficients*, 11th Skand. Mat. Kongress Trondheim 1949, 42–54.
23. G. S. Kazandzidis, Bull. Soc. Math. Grèce 9 (1968) 1–12 and 10 (1969) 35–40.
24. A. Robert, M. Zuber, *The Kazandzidis supercongruences. A simple proof and an application*, Rend. Sem. Mat. Univ. Padova 94 (1995) 235–243; A. Robert, *A Course in p-adic Analysis*, GTM 198, Springer 2000 (§VII.1.6 Kazandzidis; §VII.2.3 Dieudonné–Dwork).
25. C. Helou, G. Terjanian, *On Wolstenholme's theorem and its converse*, J. Number Theory 128 (2008) 475–499.
26. J. Zhao, *Bernoulli numbers, Wolstenholme's theorem, and p⁵ variations of Lucas' theorem*, J. Number Theory 123 (2007); arXiv:math/0303332.
27. L. Long, R. Ramakrishna, *Some supercongruences occurring in truncated hypergeometric series*, Adv. Math. 290 (2016) 773–808. arXiv:1403.5232. [Uses Kazandzidis + Robert–Zuber `\binom{p^rn}{p^rm} \equiv \binom{p^{r-1}n}{p^{r-1}m} \bmod p^{3r}`.]
28. A. Straub, *A q-analog of Ljunggren's binomial congruence*, FPSAC 2011, DMTCS Proc., 897–902. arXiv:1103.3258.
29. A. Straub, *Supercongruences for polynomial analogs of the Apéry numbers*, Proc. AMS 147 (2019) 1023–1036. arXiv:1803.07146. [Thm 2.2: general-n q-Ljunggren, (n,6)=1.]
30. W. Zudilin, *Congruences for q-binomial coefficients*, Ann. Comb. 23 (2019) 1123–1135. arXiv:1901.07843.
31. O. Gorodetsky, *q-congruences, with applications to supercongruences and the cyclic sieving phenomenon*, Int. J. Number Theory 15 (2019). arXiv:1805.01254. [q-Gauss congruences; order-r theory.]
32. G. E. Andrews, *q-analogs of the binomial coefficient congruences of Babbage, Wolstenholme and Glaisher*, Discrete Math. 204 (1999) 15–25.
33. W. E. Clark, *q-analogue of a binomial coefficient congruence*, Int. J. Math. Math. Sci. 18 (1995) 197–200.
34. L.-L. Shi, H. Pan, *A q-analogue of Wolstenholme's harmonic series congruence*, Amer. Math. Monthly 114 (2007) 529–531.
35. H. Pan, *Factors of some lacunary q-binomial sums*, Monatsh. Math. 172 (2013) 387–398; H. Pan, *A q-analogue of Gauss' divisibility theorem*, arXiv:0804.0834.
36. G. Olive, *Generalized powers*, Amer. Math. Monthly 72 (1965) 619–627; J. Désarménien, *Un analogue des congruences de Kummer pour les q-nombres d'Euler*, European J. Combin. 3 (1982) 19–28. [q-Lucas]
37. B. Sagan, *Congruence properties of q-analogs*, Adv. Math. 95 (1992) 127–143.
38. B. Adamczewski, J. P. Bell, É. Delaygue, F. Jouhet, *Congruences modulo cyclotomic polynomials and algebraic independence for q-series*, Sém. Lothar. Combin. 78B (2017) #54.
39. G. Almkvist, W. Zudilin, *Differential equations, mirror maps and zeta values*, AMS/IP Stud. Adv. Math. 38 (2006) 481–515. [Prop. 11: order-m Gauss ⟺ `a_{p^kn} ≡ a_{p^{k-1}n} mod p^{km}`; "s-realizable".]
40. F. Beukers, M. Houben, A. Straub, *Gauss congruences for rational functions in several variables*, Indag. Math. 29 (2018) 1259–1274. arXiv:1710.00423.
41. A. V. Zarelua, Proc. Steklov Inst. Math. 263 (2008) 78–98; A. Dold, Invent. Math. 74 (1983) 419–435; R. Minton, Proc. AMS 142 (2014) 2337–2352.
42. N. Metropolis, G.-C. Rota, *Witt vectors and the algebra of necklaces*, Adv. Math. 50 (1983) 95–125; A. Dress, C. Siebeneicher, Adv. Math. 70 (1988); M. Hazewinkel, *Witt vectors, Part 1*, arXiv:0804.3888.
43. B. Dwork, *Norm residue symbol in local number fields*, Abh. Math. Sem. Univ. Hamburg 22 (1958) 503–516; N. Koblitz, *p-adic Numbers, p-adic Analysis, and Zeta-Functions*, GTM 58.
44. T. Hyde, *Cyclotomic factors of necklace polynomials*, arXiv:1811.08601.
45. R. Alter, K. K. Kubota, J. Combin. Theory Ser. A 15 (1973) 243–256; E. Deutsch, B. Sagan, J. Number Theory 117 (2006) 191–215, arXiv:math/0407326. [Catalan valuations/congruences]
46. A. Varchenko, W. Zudilin, *Congruences for Hasse–Witt matrices and solutions of p-adic KZ equations*, arXiv:2108.12679.

**q-supercongruence industry (Part C):**
47. V. J. W. Guo, W. Zudilin, *A q-microscope for supercongruences*, Adv. Math. 346 (2019) 329–358. arXiv:1803.01830.
48. V. J. W. Guo, *q-Analogues of Dwork-type supercongruences*, J. Math. Anal. Appl. (2020). arXiv:1910.07551.
49. V. J. W. Guo, W. Zudilin, *Dwork-type supercongruences through a creative q-microscope*, J. Combin. Theory Ser. A 178 (2021) 105362. arXiv:2001.02311.
50. V. J. W. Guo, *Dwork-type q-congruences through the q-Lucas theorem*, arXiv:2310.15207.
51. S. O. Warnaar, W. Zudilin, *A q-rious positivity*, Aequat. Math. 81 (2011) 177–183.

---

# Final novelty verdict

## (i) Supercongruences `c_{pd} ≡ c_d (mod p³)` for numerical DT invariants of m-loop quivers

**Verdict: the theorem would be new; the statement is partially anticipated as an open conjecture.** No proof exists in the literature. However:
- The *statement*, in necklace-transform form, is precisely **Kontsevich's "improved integrality"** observation (Arbeitstagung 2011, unpublished) and **GKS Conjecture 1.3** (arXiv:1504.06327) for extremal BPS invariants — and for twist/torus knots those extremal invariants *are* (±) m-loop quiver DT invariants (identification made structural by Kucharski–Reineke–Stošić–Sułkowski arXiv:1707.02991/1707.04017 and Panfil–Stošić–Sułkowski arXiv:1802.04573). Via Almkvist–Zudilin Prop. 11 the two formulations (divisor-sum mod d³ vs. `c_{pd} ≡ c_d mod p³`) are equivalent up to bookkeeping of the `1/d²` normalization and p = 2, 3 anomalies (the GKS `γ±`).
- **Müller arXiv:2104.10754** proves the analogous mod-`p^{3r}` theorem for framings of *rational* 2-functions and explicitly flags the (algebraic) twist-knot/BPS case as open motivation. Schwarz–Vologodsky–Walcher prove the mod-p² (2-function) layer.
- The proof route (Jacobsthal–Ljunggren `\binom{mpe-1}{pe-1} ≡ \binom{me-1}{e-1} \bmod p^{3+\dots}` + Möbius bookkeeping) is available since 1952 but appears never to have been applied to these invariants. A paper proving (i) should present itself as *proving cases of GKS Conjecture 1.3 / Kontsevich's improved integrality* and determining the invariants γ± (p = 2, 3 corrections via Kazandzidis) — that is a genuine, citable contribution, not a rediscovery.

**Closest prior art:** GKS 1504.06327 (Conj. 1.3 + Prop. 1.2 formulas); Kontsevich (unpublished, as cited by GKS); Müller 2104.10754; Schwarz–Vologodsky–Walcher 1702.07135; Kontsevich–Schwarz–Vologodsky hep-th/0603106; Almkvist–Zudilin AZ06 Prop. 11; Reineke 0903.0261/1102.3978 (formulas + integrality).

## (ii) q-supercongruences `Ω_{pd}(q) ≡ Ω_d(q^{p²}) mod Φ_p(q)^k` for refined DT invariants of loop quivers

**Verdict: new — no prior art whatsoever in the DT/BPS context.** All searches for congruences of refined/motivic/quantized DT invariants modulo cyclotomic polynomials return nothing. The enabling machinery exists entirely on the number-theory side (Straub 1103.3258 & 1803.07146; Zudilin 1901.07843 — esp. his Theorem 3 on q-factorial ratios, which is the "shape" of quiver DT series; Gorodetsky's q-Gauss congruences of order r; q-Lucas; Andrews/Pan). A `q^{p²}`-Frobenius-twisted supercongruence for `Ω_d(q)` would be the *first* q-supercongruence theorem for any flavor of DT invariant, and simultaneously the first "geometric" application of the Straub/Zudilin/Gorodetsky circle of results. The only conceptually adjacent works are: Straub's Remark 6 (2011) posing the q-Jacobsthal problem; Zudilin's closing remark suggesting q-Gauss relations for factorial ratios; Chen–Liu–Peng–Zhu's congruence skein relations (different scaling direction); and the Habiro-ring Frobenius-gluing philosophy of Garoufalidis–Scholze–Wheeler–Zagier 2412.04241 (structural, no supercongruences). Cite all four as context.

## (iii) General mod-p congruence for DT invariants of arbitrary symmetric quivers via Witt vectors / Adams operations

**Verdict: new as a stated and proved theorem; adjacent folklore exists and must be handled carefully.** Zero literature hits for congruences in COHA/symmetric-quiver DT theory. What exists nearby: (a) the *integrality* theorems (Kontsevich–Soibelman 1006.2706 via λ-ring admissibility; Efimov 1103.2736; Davison–Meinhardt), whose λ-ring formalism is exactly Witt-flavored — a referee may regard a mod-p congruence `Ω_{pd} ≡ ψ^p Ω_d`-type statement as the "expected Witt shadow" of admissibility, so the paper should be explicit about what is genuinely stronger (order of the congruence, uniformity in the quiver, refined vs. numerical level); (b) the classical Gauss/Dold/Dwork equivalences (B.6) which give the order-1 statement for any Euler-product-integral series essentially for free — the content of (iii) must therefore exceed the trivial necklace layer (e.g. Frobenius twist at refined level, or order ≥ 2 phenomena, or exactness/sharpness); (c) Garoufalidis–Scholze–Wheeler–Zagier's Habiro ring of a number field (Frobenius-glued congruences for KS admissible series — the closest published *structure*, though aimed at Chern–Simons/3-manifold DT series, with no quiver statement). No one has published even the order-1 mod-p congruence *stated for* symmetric-quiver DT invariants, so priority is available, but the introduction should credit the folklore honestly.

**Overall:** the planned trio (i)–(iii) occupies a genuinely empty niche ("arithmetic of quiver DT invariants"), with (ii) the most unambiguously novel, (i) the most valuable to position correctly (it resolves cases of a named open conjecture), and (iii) requiring the most careful delimitation against λ-ring folklore.
