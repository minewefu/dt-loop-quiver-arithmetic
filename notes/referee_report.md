# Referee Report

**Manuscript:** "Arithmetic of Donaldson–Thomas invariants of loop quivers: improved integrality and exact q-analogues" (paper.tex, dated July 31, 2026)

**Recommendation: MAJOR REVISION — in the binary terms requested: FAIL** (two major defects, both excisable; the core mathematics is correct and the general-m theorem and q-identities appear genuinely new).

---

## 1. Summary of the manuscript

The paper studies the numerical DT invariants DT_n^{(m)} of the m-loop quiver (Reineke's formula, eq. (1.4)) and their quantized refinements DT_n^{(m)}(q). Main claims:

- **Theorem 1.2** (improved integrality, sharp form): v_p(DT_n) >= v_p(n) for p >= 5; v_3(DT_n) >= v_3(n) − ε_3(m) with ε_3 = 1 iff m ≡ 2 (mod 3); v_2(DT_n) >= v_2(n) − ε_2(m) with ε_2 = 1 iff m ≡ 2,3 (mod 4); the constant γ(m) = 2^{ε_2}3^{ε_3} is optimal. Proof via Jacobsthal–Kazandzidis supercongruences (Robert–Zuber for p >= 5 and p = 3; a self-contained signed p = 2 version proved in Appendix B), with the tower congruences of Lemma 6.1.
- **Corollary 1.3**: the GKS Improved Integrality conjecture (GKS Conj. 1.3) for extremal BPS invariants of twist knots and (2,2p+1) torus knots, with optimal γ± = γ(m).
- **Theorem 1.4** (q-identities): P_n(q) = q^{−(m−1)C(n,2)} [mn−1 choose n−1]_q; Möbius formula for the primitive part R_n; the **derivative theorem** (P_n' and R_n' vanish at all n-th roots of unity; equivalently ζB'(ζ) = (m−1)C(n,2)·B(ζ) for B = [mn−1, n−1]_q); the **q-supercongruence** R_n ≡ 0 (mod Φ_p²) for odd p | n, with exact p = 2 defect R_n(−1) = −n·barQ^prim_{n/2}(1), R_n'(−1) = 0.
- **Theorem 1.5** (exact necklace formula): barQ_n = [t^n] PLog A(q,t) (+ ψ₂-correction in the doubling case), A(q,t) the co-area q-Fuss–Catalan (ballot) series.
- **Proposition 5.6**: algebraicity of A(ζ, t) at roots of unity; Section 7: mod-Φ_p phenomenology (Table 1) and conjectures; Appendix B: elementary proof of the signed Kazandzidis congruence at p = 2.

---

## 2. Correctness (Task A)

I checked every definition, lemma, proposition and theorem line by line, recomputed all embedded small examples by hand, and independently verified the computational claims (Section 3 below). **I found no mathematical error in any proof.** Details:

### 2.1 Section 3 (weight-statistic lemmas)
Lemma 3.1 (rotation), Lemma 3.2 (repetition), Lemma 3.3 (orbit-sum) were re-derived by hand; all steps check, including the normalization identities (2.1)/(eq:wtnorm), the induction for wt(ρ^k a), the period-d refinement, and the admissible = orbit-max characterization. (Verified additionally on 3000 random instances.) Note: the rotation and repetition formulas are *not* new — they are literally in Reineke [Rei1102, Lemma 6.5], as the paper itself admits at the end of Section 3; only the orbit-sum identity appears new (see Defect 5).

### 2.2 Section 4 (exact identities)
- Prop. 4.1: the composition-to-partition bijection, the box-partition generating function, palindromy, and the degree computation deg = 2(m−1)C(n,2) are all correct.
- Prop. 4.2: period decomposition, Möbius inversion, and the root-of-unity collapse are correct (orbit weights congruent mod n makes ζ^{wt(C)} well-defined).
- Theorem 4.3 (derivative theorem): the orbit-grouping argument is correct and complete, including non-free orbits for P_n (via the period-d orbit-sum remark) and the Laurent-vs-polynomial normalization. I re-verified the equivalent B-form by hand for (m,n) = (2,2) and (2,3) at all roots, and computationally far beyond (Section 3).
- Theorem 4.4: correct. The p odd case, the clean p = 2 cases, and the doubling case (with the descent to n/2 odd where no further doubling can occur, and Φ_p | [n/2]_q since p | n/2) are all handled; conjugation gives vanishing at all primitive p-th roots, hence Φ_p² | R_n over Z[q^{±1}]. The prime-power extension in the following Remark is also correct (checked: Φ_9, Φ_25, Φ_27, Φ_8, Φ_16 cases computationally).

### 2.3 Section 5 (necklace formula)
- Lemma 5.2 (first-return factorization, weight additivity): correct; the additivity computation only needs S_j(u) = (m−1)j for the left factor, which holds for blocks and their concatenations.
- Lemma 5.3 (classes vs. aperiodic necklaces): correct in both directions; the aperiodicity transfer (a sequence-period forces a necklace-period and conversely) is argued correctly via the weight-maximality characterization of returns.
- Theorem 1.5 proof: the Chen–Fox–Lyndon argument over the graded (countable, degreewise-finite) alphabet is correct; local finiteness holds; Exp multiplicativity is standard; the doubling correction ψ₂(barQ^prim_{n/2}) is computed correctly via Lemma 3.2 (rotations of bb are doubles of rotations of b, so class-max doubles). The structural inputs (doubling exactly when m even, n ≡ 2 mod 4; [n]_q | barQ_n) are correctly attributed to Reineke Thm. 5.11/§6 and Thm. 6.7 — I checked these against Reineke's actual text (see 4.2).
- Prop. 5.6 (algebraicity): the strategy (finite polynomial system for G_j(t) = F(ζ, ζ^j t), Jacobian ≡ identity mod t, Hensel/isolated-point, then arithmetic-progression sections with the periodic twist ζ^{(m−1)C(n,2)}) is sound. However the displayed system is garbled: it prints G_j = 1 + ζ^{−j}·(ζ^j t)·Π G_{j+k} "i.e." G_j = 1 + t·ζ^j ζ^{−j} Π G_{j+k} (= 1 + tΠG_{j+k}), whereas the correct system from substituting t → ζ^j t is G_j = 1 + ζ^j t Π_k G_{j+k}. The spurious ζ^{−j} does not affect the argument (the Jacobian is the identity mod t either way), but the display as printed is wrong. (Defect 4, minor.)

### 2.4 Section 6 (arithmetic proof)
- (6.1)/(eq:reineke2) sign bookkeeping: correct ((−1)^{(m−1)(n−d)} = (−1)^{(m−1)(n−1)}(−1)^{(m−1)(d−1)}).
- Lemma 6.1 (tower congruences): correct. The Kazandzidis modulus valuation is computed exactly; the lower bound v_p(binom(me,e)) >= v_p(m) via binom(me,e) = m·binom(me−1,e−1) is right, and dividing the congruence by m costs exactly v_p(m), which the modulus repays — this is the key uniformity-in-m mechanism and it is airtight. The p = 2 sign computation ((−1)^{(m−1)+(m−1)e+(m−1)(e−1)} = +1) is correct; I re-derived it independently.
- Proof of Theorem 1.2: the Möbius collapse to consecutive-level differences (only j ∈ {v−1, v} survive), the application of Lemma 6.1 with e = p^{v−1}f, and the case analysis at p = 2, 3 are all correct. The v = 0 cases reduce to Reineke's integrality (cited). Optimality: DT_2 = floor(m/2) and DT_3 = C(m,2) are correct (I re-derived both from (1.4) by hand; they also match Reineke's own Theorem 3.2 examples), and the parity/3-divisibility analysis is right.
- Corollary 6.3 (towers): immediate from Lemma 6.1; consistent with (1.5)/(eq:tower).

### 2.5 Appendix B (signed Kazandzidis at p = 2)
Checked line by line; correct and complete:
- Step 1: (2n)! = 2^n n! (2n−1)!! and the reduction to v(Q − ε) >= 1 + v(NKM) — correct (the k = n edge case M = 0 makes the ideal zero and the congruence an identity 1 = 1, consistent with the Proposition's "n >= k >= 1").
- Step 2: the mod-4 sign split and the floor-parity identity (checked in both cases) — correct; (eq:square) v(Q−ε) = v(Q²−1) − 1 is right since v(Q+ε) = 1 exactly.
- Step 3 (interpolation lemma): the Faulhaber/Bernoulli construction converges (v(h_r) = r+1−v(r) → ∞, von Staudt–Clausen v(B_{2s}) >= −1); the Strassmann argument for oddness is valid (coefficients tend to 0, so Strassmann applies; the backwards iteration uses the interpolated difference equation, which itself follows by the same Strassmann argument — this could be spelled out in one more sentence but is correct). The three coefficient bounds: r = i−1 term has v = i − v(i−1) >= 2 (using v(i−1) <= log2(i−1) <= i−2 for odd i >= 3); r = i term has v = i >= 3; r > i terms have v >= r − v(r) >= 2 for even r >= 4. All correct.
- Step 4: the divisibility of (K+M)^i − K^i − M^i by KM(K+M) in Z[K,M] for odd i, and the ultrametric assembly, are correct. Sharpness at (N,K) = (2,1) checks: 6 − (−1)·2 = 8, modulus 2·2·1·1·2 = 8.
- I verified the Proposition computationally for all 2 <= N <= 120, 1 <= K < N: no violations, minimum slack 0 attained at (2,1) (matching the authors' claimed N <= 300 run), and I confirmed the *unsigned* version genuinely fails (190 failures for N < 40), so the sign is essential, as the paper emphasizes.

### 2.6 Edge cases hunted
n = 1 (all statements trivially consistent), k = n in Kazandzidis (trivial), m even doubling cases at n ≡ 2 mod 4 (verified extensively, including the exact defect), p | m and p | m−1 in Lemma 6.1 (the v_p(m(m−1)) bookkeeping is exactly right), prime powers Φ_{p^j}. No circularity found: Theorem 4.4 uses only Reineke's Thm 6.7 ([n]_q | barQ_n) as external input; Theorem 1.5 uses Reineke's Thm 5.11/§6 doubling structure; Theorem 1.2 uses Robert–Zuber + Appendix B + Reineke's integrality for the trivial v_p(n) = 0 case. The erratum (Remark 2.2) does not enter any proof.

---

## 3. Independent computation (Task B)

I wrote my own scripts from scratch (no code shared with the authors' implementations; word model + a plethystic product engine in a different gauge (x = q^{−1}, t = x^K u) + flint polynomial arithmetic). Results:

1. **Reineke formula / Appendix A Table 1**: all 50 entries (m = 2..6, n <= 10) reproduced exactly. The γ(m) table (App. A Table 2) matches the ε-formula, and the *empirical minimal* γ over n <= 200 equals γ(m) for every m = 2..13.
2. **Theorem 1.2**: verified for m = 2..16, n <= 200, all p | n — no violations; defects attained exactly on the predicted residue classes (v_2(DT_2) = 0 whenever m ≡ 2,3 mod 4; v_3(DT_3) = 0 whenever m ≡ 2 mod 3), including the un-emphasized range m = 11, 12, 13 (e.g. m = 11: v_2(DT_{2^k}) = k−1 and v_3(DT_{3^k}) = k−1 exactly; m = 12, 13: no defect anywhere).
3. **Lemma 6.1 towers**: verified m <= 13, p ∈ {2,3,5,7,11}, e <= 60, including sharpness (bound attained at e = 1 for all small m, p).
4. **Kazandzidis**: Thm 2.2 verified for p ∈ {3,5,7}, n <= 40 with the exact stated moduli; Prop 2.3 for n <= 120 (min slack 0 at (2,1)).
5. **Word model** (m = 2: n <= 12; m = 3: n <= 9; m = 4: n <= 7; m = 5, 6: n <= 6): Prop 4.1, Prop 4.2(1), Theorem 4.3 (all three equivalent forms), Theorem 4.4 including the exact p = 2 defect, [n]_q | barQ_n, and barQ_n(1) = n·DT_n — all verified against brute-force enumeration.
6. **Large-range stress test of Theorems 4.3/4.4** far beyond the authors' stated verification (via the now-verified Gaussian-binomial formula): 23 cases up to (m,n) = (12,36), including Φ_{p^j}^2 for p^j ∈ {4, 8, 9, 16, 25, 27} and seven doubling-defect cases — all pass.
7. **Product definition (eq. 1.2) engine**: computed DT_n^{(2)}(q) for n <= 30, DT^{(3)} n <= 9, DT^{(4)} n <= 7 from first principles. Efimov constraints (monic, degree (m−1)C(n,2), q^{n−1} | DT_n, nonnegativity) hold; q = 1 values match Reineke's formula; **the word formula (1.7) with prefactor q^{n−1} reproduces the product-definition invariants in every case, and the printed q^{1−n} version fails in every case with n > 1** — the manuscript's erratum claim is correct in its own conventions (and see 4.2 for Reineke's text).
8. **Table 1 (mod Φ_5, m = 2)**: all 30 rows verified exactly, including V_11 = V_16 = V_21 = 0, V_6 = V_26 = [−1,0,0,−1], the multiplier sequences (1,1,3,9), (1,2,6,17), and c_k = 1, 2, 4, 12, 41, 138 for n = 5k <= 30.
9. **Theorem 1.5**: verified as a polynomial identity for m = 2 (n <= 10), m = 3 (n <= 8), m = 4 (n <= 6), m = 5 (n <= 5), plus the Fuss–Catalan specialization A_n(1).
10. **Authors' data**: omega_m{2..6}.json match my engine (m = 2 checked coefficientwise to n = 30; q = 1 values checked at the maximal claimed n for every m: n = 50, 36, 27, 22, 14 — exactly the ranges claimed in the abstract and §8). The claimed verification statements in §8 are honest as far as I could probe them.

**One discrepancy found** (internal typo, not affecting any result): Remark 2.2 states "barQ_2 = q" for m = 2. Under the paper's own definitions barQ_2 = 1 + q (the primitive class {(2,0),(0,2)} has wt(C) = 1 and the doubling class (1,1) has weight 0); barQ^prim_2 = q. Both computations displayed in the Remark (q^{n−1}barQ_2/[2]_q = q and q^{1−n}barQ_2/[2]_q = q^{−1}) are consistent with 1 + q and inconsistent with q, so this is a pure typo. Note also [2]_q ∤ q, so Reineke's Thm 6.7 itself forces barQ_2 = 1 + q.

---

## 4. Novelty and attribution (Task C)

I verified the following against the actual sources (GKS = arXiv:1504.06327 published CMP 346 (2016); Reineke = arXiv:1102.3978 = Doc. Math. 17 (2012); Robert–Zuber via NUMDAM; PSS = arXiv:1802.04573; Müller = arXiv:2104.10754; Kucharski–Sułkowski = arXiv:1608.06600; Gorodetsky = arXiv:1805.01254; Straub = arXiv:1103.3258; Mestrović = arXiv:1111.3057).

### 4.1 Accurate citations (verified verbatim)
- **GKS Conjecture 1.3** is stated as quoted (nonzero integers γ± with γ±b±_r/r ∈ Z); **Prop. 1.2** formulas for twist knots (both the p <= −1 and p >= 2 rows, with signs (−1)^{d+1}, (−1)^d) are transcribed exactly; **Table 2** indeed tabulates 2b−_r/r ∈ Z for 4_1 (I checked the printed values against DT^{(3)}: they agree through r = 15); GKS state γ± = 2 for 4_1 and γ− = 6, γ+ = 2 for 5_2 = K_2 — the latter matches the manuscript's γ(2) = 6, γ(6) = 2. In fact the manuscript's γ(m) formula reproduces **every** twist-knot row of GKS Table 1 (all twelve period-6 classes K_{p±6k}); the paper could say so — it is striking confirmation.
- **Robert–Zuber (1995)**: the abstract displays exactly the two congruences of the manuscript's Theorem 2.2 — binom(np,kp) ≡ binom(n,k) mod p³·n·k·(n−k)·binom(n,k)·Z_p for p >= 5, and mod 3²·n·k·(n−k)·binom(n,k)·Z_3 for p = 3. The claim "exactly as printed" is correct.
- **Reineke [Rei1102]**: Thm 3.2 (formula + the DT_2, DT_3 closed forms), Thm 5.11 (Exp-form; doubling exactly for m even, n = 2·odd), Lemma 6.5 (rotation/repetition/max-at-admissible), Lemma 6.6 (congruence mod q^n − 1), Thm 6.7 ([n] | barQ_n), Cor 2.2(1) (grafting q-difference equation) — all as cited. **The erratum claim is correct**: Reineke's Theorem 6.8(1) is printed with prefactor q^{1−n}; this contradicts his own Thm 5.11 + Conjecture 3.3 Exp-forms (whose termwise comparison forces q^{n−1}, exactly as the manuscript's Remark 2.2 argues), contradicts Thm 6.8's own assertion that the result is a polynomial (q^{1−n}barQ_2/[2] = q^{−1} for m = 2), and fails against the product definition computationally. **Kucharski–Sułkowski (B.4)** indeed reproduces the q^{1−r} form, as stated.
- **Müller [2104.10754]**: his Theorem 1.1 covers framings of *rational* 2-functions; his introduction explicitly notes that the twist-knot improved integrality of GKS concerns solutions of extremal A-polynomials (algebraic, not rational). The manuscript's characterization is fair.
- **Gorodetsky Thm 2.6**: evaluates ω·d/dq[an,bn]_q(ω) = ord(ω)²·binom(an/ord, bn/ord)·b(a−b)n²/2 — generically nonzero, a different family (both entries multiples of n), as the manuscript's Remark says. **Straub's Remark 6** is indeed an open problem about a q-analogue of Jacobsthal. Mestrović's survey confirms the Kazandzidis bibliography and that the original sources are hard to access, consistent with Appendix B's rationale.
- Reineke's 2024 survey (arXiv:2410.03219) contains the formula (Ex. 2.4) and no arithmetic/divisibility results, and a 2025 knots-quivers survey (arXiv:2505.02059) does not mention improved integrality — consistent with the general-m problem being open in the quiver literature.

### 4.2 MAJOR NOVELTY DEFECT: uncited prior proof of the m = 3 case
**Basor–Conrey–Morrison, "Knots and ones", arXiv:1703.00990 (March 2017)** — not cited — proves, for exactly the m = 3 sums n_r = r^{−2}Σ_{d|r} μ(r/d)binom(3d−1, d−1) (= DT_r^{(3)}, the figure-eight extremal BPS invariants):
- **Theorem 1 (BCM)**: 2n_r/r ∈ Z for all r ("one case of the same authors' 'Improved Integrality' conjecture [GKS, Conjecture 1.3]", in their words), **and** an exact characterization of when n_r/r ∈ Z (r odd, or via the binary "well-spaced" criterion).

BCM's Theorem 1 is precisely the m = 3 case of the manuscript's Theorem 1.2 (equivalent to v_p(DT_n^{(3)}) >= v_p(n) for p odd and v_2 >= v_2(n) − 1), and at p = 2 their per-r characterization is strictly finer than the manuscript's uniform bound. Consequently:
- the claim "the improved divisibility by r has remained open" (§1.2) is **false**;
- the Related-work claim "Congruences for DT-type invariants seem not to have been studied before: systematic searches locate no prior results" is **false**;
- the figure-eight highlight of Corollary 1.3 and of the abstract ("recovers the value γ = 2 observed by GKS") is **prior art** (2017), as is the m = 3 instance of Theorem 1.2.

What remains novel (my searches found nothing else): the general-m theorem with the sharp defect classification ε_2(m), ε_3(m) and optimal γ(m); the uniform Kazandzidis-based method (including p | m); the tower/supercongruence layer (Lemma 6.1, Cor. 6.3); and all q-refinements. This is still a substantial contribution, but the paper's novelty claims must be rewritten and BCM must be cited and compared honestly (including that BCM's p = 2 analysis for m = 3 goes beyond Theorem 1.2 in one direction).

### 4.3 MAJOR CORRECTNESS/OVERCLAIM DEFECT: the torus-knot part of Corollary 1.3
The abstract ("Via the identification of extremal BPS invariants of twist knots and (2,2p+1) torus knots with loop-quiver DT invariants...") and Corollary 1.3 ("Conjecture 1.1 holds for the extremal BPS invariants of ... all (2,2p+1) torus knots, with the explicit optimal constants γ± = γ(m)") assert that the extremal BPS invariants of (2,2p+1) torus knots are (±) loop-quiver DT invariants, attributing the identification to PSS. This is **not correct**:
- GKS themselves (Table 1) list γ−(T_{2,2p+1}) = 2p+3 and γ+(T_{2,2p+1}) = 2p−1, "growing linearly with p" — e.g. γ− = 5 for the trefoil. A value of 5 is impossible for loop-quiver invariants, whose optimal γ(m) ∈ {1, 2, 3, 6} by the manuscript's own Theorem 1.2. Concretely, GKS's trefoil values b−_r = −2, 2, −3, 8, −26, 90, ... (their Table 7) have b−_1 = −2, which already rules out ±DT^{(m)}_r for every m (DT_1 = 1 always), and b−_5 = −26 forces 5 | γ−.
- PSS (arXiv:1802.04573) do **not** identify extremal invariants of (2,2p+1) torus knots with loop quivers. Their quivers for the (2,2p+1) family are (p+1)-vertex quivers (their eq. (4.13)–(4.14): C(2,3) = [[7,5],[5,5]] etc.), and the corresponding extremal BPS numbers are lattice-path/Bizley counts under the line of slope 2/(2p+1) (their eq. (4.25)–(4.26) and Table 1: (2,3) row = 2, 10, 111, 1572, ...). Only the (f,1) "torus knots" (framed unknots) reduce to the f-loop quiver (their §4.1) — and those are exactly the twist-knot/loop-quiver cases already covered.

So the torus-knot claim is false as stated (and in the weaker reading "extremal DT invariants of the torus-knot quiver" it is not what GKS Conjecture 1.3 is about, and no such statement is in PSS either). The twist-knot part of Corollary 1.3 is fully correct and well-supported. The fix is to delete the torus-knot claims from the abstract, §1.2 and Corollary 1.3 (or replace them by a correctly-scoped remark about single-vertex sub-quiver contributions, if the authors can actually source one).

### 4.4 Other novelty notes
- The derivative theorem (Thm 4.3) and the Φ_p² q-supercongruence (Thm 4.4) appear to be new; they sit adjacent to Gorodetsky's q-Gauss-congruence framework (his Cor. 8.2 evaluates derivatives of arbitrary Gaussian binomials at roots of unity, so an expert could likely re-derive Thm 4.3 from it), and to the recent necklace/q-Gauss work of Gossow (arXiv:2410.05678), which contains neither derivatives nor Φ_p² statements. The manuscript's hedged claim ("appears to be new even as a statement about Gaussian binomial coefficients") is reasonable; citing Gossow would improve the scholarship.
- Theorem 1.5 is close in spirit to Reineke's exact Exp-identity (Thm 5.11) and his Hilbert-series factorization (Cor. 2.2(4)); I checked numerically that the naive combination of those two (the area-statistic analogue) does **not** reproduce the identity, so the specific co-area gauge in which the exact plethystic/ballot formula holds is genuine content of the manuscript. A sentence delimiting Theorem 1.5 from Reineke's Thm 5.11 would nonetheless help.
- The signed p = 2 Kazandzidis congruence: the statement is attributed to the Kazandzidis tradition and only the (nice, correct) proof is claimed, with the honest remark that no accessible published proof was located; Mestrović's survey corroborates the inaccessibility of the originals. Fine.
- Attribution nuance: GKS credit the improved-integrality observation to Kontsevich via "[Kon] private communication"; their "2011 Arbeitstagung talk" citation is attached to their Theorem 1.1 (algebraicity), not to the integrality observation. The manuscript's "(Arbeitstagung Bonn, 2011)" parenthetical conflates the two slightly.

---

## 5. Significance and presentation (Task D)

If revised as indicated, this is a good paper for a solid journal: a sharp, uniform arithmetic theorem for a natural family of DT invariants; a clean new mechanism (the m-division cost repaid by the Kazandzidis modulus; the p = 2 sign matching the motivic sign twist — a genuinely elegant observation, verified); new exact q-identities with complete elementary proofs; a correct and useful erratum to a published theorem of Reineke (verified three independent ways); an honest and unusually thorough verification apparatus (I probed it adversarially and found only the one typo). The writing is generally precise; theorem statements are clean; the phenomenology section is clearly separated from the theorems. The two major defects are quarantined: deleting the torus-knot claim and rewriting the novelty claims around BCM costs two paragraphs and one corollary clause, and no proof elsewhere depends on either.

---

## 6. Itemized defects

**MAJOR**
1. **Torus-knot overclaim (false claim in a main corollary).** Locations: Abstract (sentence "Via the identification of extremal BPS invariants of twist knots and (2,2p+1) torus knots with loop-quiver DT invariants ..."); §1.2, sentence "Panfil–Stošić–Sułkowski [PSS] identified the extremal DT invariants of (2,2p+1) torus knots with m-loop quiver invariants as well"; Corollary 1.3 statement ("... and all (2,2p+1) torus knots, with the explicit optimal constants γ± = γ(m)") and its proof ("by [PSS] the extremal DT invariants of (2,2p+1) torus knots are again loop-quiver invariants"). The extremal BPS invariants of genuine (2,2p+1) torus knots are Bizley lattice-path counts attached to (p+1)-vertex quivers (PSS §4.3), not loop-quiver invariants; GKS's own Table 1 gives γ± = 2p+3, 2p−1 for this family (γ− = 5 for the trefoil), which no γ(m) ∈ {1,2,3,6} can match. The claim is contradicted by both cited sources. Fix: remove or correctly re-scope all torus-knot claims.
2. **Missing directly-relevant prior work; false novelty claims.** Basor–Conrey–Morrison, "Knots and ones", arXiv:1703.00990 (2017), proves the m = 3 case of improved integrality (2n_r/r ∈ Z for all r, presented explicitly as a case of GKS Conjecture 1.3) plus an exact characterization of when n_r/r ∈ Z. Locations affected: §1.2 "the improved divisibility by r has remained open"; Related work, "Congruences for DT-type invariants seem not to have been studied before: systematic searches locate no prior results"; Corollary 1.3 and abstract insofar as the figure-eight γ = 2 is presented as new. Fix: cite BCM, restate what is new (general m; sharp p-adic form; optimal γ(m); towers; all q-results), and note that for m = 3, p = 2 BCM's per-r characterization refines Theorem 1.2.

**MINOR**
3. Remark 2.2 (rem:erratum): "barQ_2 = q" should be "barQ_2 = 1 + q" (or "barQ^prim_2 = q"); as printed it contradicts the two computations in the same parenthesis and Reineke's Thm 6.7. The erratum's conclusion is unaffected (and correct).
4. Proposition 5.6 proof: the displayed specialized system "G_j = 1 + ζ^{−j}·(ζ^j t)Π_k G_{j+k}, i.e. G_j(t) = 1 + tζ^j ζ^{−j}Π_k G_{j+k}(t)" is garbled; the correct system is G_j(t) = 1 + ζ^j t Π_{k=0}^{m−1} G_{j+k}(t). The Jacobian argument is unaffected.
5. §1.3, "three elementary but apparently unnoticed identities": the rotation and repetition formulas are stated and proved in [Rei1102, Lemma 6.5] (the rotation formula appears there verbatim); only the orbit-sum identity is new. Rephrase (the paper's own end-of-§3 acknowledgment is accurate; the intro should match it).
6. Kontsevich attribution: per GKS, the observation is credited to Kontsevich as private communication ([Kon]); "Arbeitstagung Bonn 2011" is GKS's citation for their Theorem 1.1. Adjust the parenthetical in the abstract and §1.2 (or cite GKS's phrasing directly).
7. Scholarship suggestions (no obligation): compare Theorem 1.5 with Reineke's Thm 5.11 + Cor. 2.2(4) explicitly; mention Gossow, arXiv:2410.05678 (necklace-model q-Gauss congruences and cyclic sieving) near Theorems 4.3–4.4; consider noting that the manuscript's γ(m) formula reproduces all twelve twist-knot rows of GKS Table 1.
8. Code/README nit: README.md refers to ../data/cleanroom_dt.json; the shipped file is wordmodel_dt.json.
9. Appendix B, Step 3(1): the backwards iteration g(−n) = −Σ h(−j) tacitly uses the interpolated difference equation at negative arguments; add half a sentence (Strassmann applied to g(y+1) − g(y) − h(y), as done for oddness).

---

## 7. Verdict

The proofs of Theorem 1.2, Theorem 1.4 (= Props 4.1–4.2 + Thms 4.3–4.4), Theorem 1.5, Proposition 5.6 and Appendix B are correct — I could not break any of them, by hand or by machine, including at the edge cases the proofs must survive (p | m, doubling classes, prime powers, n = 1, k = n). The verification claims are honest. But the manuscript as it stands contains a false headline claim (torus knots) contradicted by its own cited sources, and misstates the state of the art by omitting a 2017 paper that already settled its most advertised special case (figure-eight, γ = 2, m = 3). Under the binary standard requested ("correct, novel, and good enough as it stands"):

**VERDICT: FAIL** — with the explicit assessment that both major defects are excisable, the remaining mathematics is correct, and the general-m theorem plus the q-analogue package would, after revision, merit publication in a good journal.

---

# Second round (revision of July 31, 2026)

I re-refereed the revised manuscript under the same standard. Every changed passage was checked against the sources and, where it makes a mathematical claim, re-verified independently by computation. The unchanged mathematical core is identical to the first-round text (verified section by section) and stands as previously assessed.

## Verification of the fixes

**MAJOR 1 (torus knots) — FIXED.** All torus-knot claims are removed from the abstract, §1.2 and Corollary 1.3 (grep confirms the only remaining occurrences are the new scoping parenthetical and the PSS bibliography title). The replacement parenthetical in §1.2 is factually accurate on both counts I could check: PSS attach multi-vertex quivers and Bizley-type lattice-path counts to genuine (2,2p+1) torus knots (PSS §4.2–4.3, eqs. (4.13)–(4.14), (4.25)–(4.26)), and GKS Table 1's torus-knot constants 2p+3, 2p−1 grow linearly in p (GKS's own wording). The corollary and its proof now concern twist knots only.

**MAJOR 2 (BCM prior art) — FIXED.** [BCM17] arXiv:1703.00990 is cited; §1.2 states their theorem correctly and completely (2n_r/r ∈ Z for all r for the figure-eight sums, explicitly as an instance of GKS Conj. 1.3 with γ = 2, plus the exact characterization of when n_r/r ∈ Z); the abstract credits BCM as "the one previously proved case"; "For all other m the problem has remained open" is consistent with my literature search; the Related-work opener is corrected; and the new Remark 1.4 fairly states that BCM's p = 2 analysis for m = 3 is finer than Theorem 1.2 in one direction (their well-spaced criterion determines exactly when r | DT_r^{(3)}). The positioning is accurate and fair.

**New content in Corollary 1.3 (twelve GKS values) — VERIFIED TRUE.** The two new claims check out: (i) γ(m) depends only on m mod 12 (ε₂, ε₃ depend on m mod 4, m mod 3; numerically re-confirmed for m ≤ 48), so the families m = 2|p|+1, 2p+2 give values depending only on p mod 6; (ii) I re-checked all twelve twist-knot rows of the printed GKS Table 1 (both the γ− and γ+ columns, i.e. all 24 entries) against γ(m): K_{−1−6k}, …, K_{−6−6k} predict (2, γ(3+12k')…) = (2,2), (2,3), (2,2), (2,1), (2,6), (2,1) and K_{2+6k}, …, K_{7+6k} predict (6,2), (6,3), (6,2), (6,1), (6,6), (6,1) — perfect match with the table. (Copy-editing: the apposition "(twelve values, periodic in p of period 6)" would be clearer as "twelve rows/value-pairs"; the table has 24 numbers in 12 rows, and the operative claim "every twist-knot entry" is true for all 24.)

**MINOR 3 (barQ_2) — FIXED**, now with the correct class-by-class computation (primitive class contributes q, doubling class contributes 1), matching my enumeration.

**MINOR 4 (Prop. 5.6 display) — FIXED, with one residual echo.** The displayed system is now the correct G_j(t) = 1 + ζ^j t ∏_{k=0}^{m−1} G_{j+k}(t). However, the following sentence still defines Ψ_j := G_j − 1 − t∏_k G_{j+k}, omitting the ζ^j — a leftover shorthand inconsistent with the (correct) display. This is an inert notational slip: "the system" plainly refers to the display, and the Jacobian-identity-mod-t claim and the Hensel/isolated-point argument hold verbatim for the correct Ψ_j. It does not affect the validity of the proof, but should be fixed in proof (write Ψ_j := G_j − 1 − ζ^j t ∏_k G_{j+k}).

**MINOR 5 (attribution of the three lemmas) — FIXED** ("essentially in [Rei1102, Lem. 6.5] and which we reprove for completeness"; novelty claimed only for the orbit-sum identity). Accurate.

**MINOR 6 (Kontsevich attribution) — FIXED** ("who credit the observation to Kontsevich"; "private communication; for algebraic curves satisfying the K2 condition"). Matches GKS's actual text; Arbeitstagung removed from the integrality attribution.

**MINOR 7 (related work) — FIXED.** Gossow [arXiv:2410.05678] and the Gorodetsky Cor. 8.2 pointer are added. The new delimiting sentence after Theorem 1.6's (thm:master's) proof makes a checkable claim: "the naive area-statistic analogue of Theorem [thm:master] is false (we checked that it fails already at n = 3)". **Verified true, and sharp**: replacing the co-area series A by the area-statistic series F (F_n = Σ_adm q^{(m−1)C(n,2)−wt}) and forming the same formula, I find [t^1]PLog F = barQ^prim_1 and [t^2]PLog F = barQ^prim_2 (so with the ψ₂-correction the analogue still holds at n = 2), while at n = 3 the analogue fails for every m ∈ {2,3,4,5} tested (e.g. m = 2: [t^3]PLog F = q² · 2 + q³ vs barQ_3 = q + q² + q³). (Copy-editing: "produces barQ_n on the nose" in that sentence is shorthand — strictly [t^n]PLog A = barQ^prim_n, with the ψ₂-correction giving barQ_n, exactly as the theorem states.)

**MINOR 8 (README) — FIXED** (now references wordmodel_dt.json, which exists).

**MINOR 9 (Appendix B backwards iteration) — FIXED** exactly as suggested: the difference equation is first upgraded to an identity on Z_2 by Strassmann (the difference of convergent series vanishes on Z_{≥0}, hence identically), then iterated backwards. Correct.

## Scan for newly-introduced errors

The changed passages introduce three new mathematical assertions (mod-12 periodicity; twelve-value agreement with GKS Table 1; n = 3 failure of the area analogue) — all three verified true above. The rewritten abstract and §1.2 sentences are accurate (including "the one previously proved case of the conjecture": BCM is the only published proof of a case of GKS Conj. 1.3 that I could locate). Remark 1.4's statements about BCM and about sharpness at r = 2 (v_2(DT_2^{(3)}) = 0) are correct. No other text changed (verified against my first-round reading section by section); the bibliography additions are correctly formatted.

## Remaining copy-editing items (non-blocking; none affects validity)

a. Prop. 5.6 proof: Ψ_j := G_j − 1 − ζ^j t ∏_k G_{j+k} (restore the ζ^j in the shorthand; the display above it is correct).
b. Corollary 1.3: "(twelve values …)" → "(twelve rows/value-pairs …)" for precision.
c. §1.2: BCM's proof analyzes all primes (their §2 treats odd p, §3 treats p = 2); "by a direct 2-adic analysis" would be better as "by a direct p-adic analysis".
d. Remark after thm:master's proof: "produces barQ_n on the nose" → "produces barQ^prim_n (hence barQ_n via the ψ₂-correction) on the nose".

## Second-round verdict

Both major defects are fully and accurately repaired; all minor defects are repaired (one repair leaves the inert Ψ_j echo noted in (a)); the newly added claims are correct — including the two I could verify only against the primary sources (the twelve GKS Table 1 entries) and by fresh computation (the n = 3 failure). The mathematics of every theorem and proof is correct as established in round 1 and unchanged; the novelty claims are now accurate and appropriately scoped; the scholarly apparatus is in order. The residual items (a)–(d) are proof-stage copy-editing, of the kind routinely handled after acceptance, and none makes any proof or claim incorrect.

**VERDICT: PASS**
