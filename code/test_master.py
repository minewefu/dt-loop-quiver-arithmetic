"""Verify the master identities:

 (M1) barQ_n(q) = [t^n] PLog(A(q,t)) + [m even, n=2 mod 4] psi_2([t^{n/2}] PLog(A)),
      A(q,t) = sum_n A_n(q) t^n, A_n = admissible (ballot) polynomials.
      (barQ_n = [n]_q q^{1-n} DT_n(q) from the engine.)

 (M2) R_n(q) := sum_{d|n} mu(n/d) P_d(q^{n/d})  with
      P_d(q) = sum_{a in U_d} q^{wt(a)}  (ALL sequences; balanced Laurent),
      equals sum over primitive a of q^{wt(a)}  -- check via direct enumeration
      for small n; and P_d(q) = q^{-(m-1)C(d,2)} qbinom(md-1, d-1)_q.

 (M3) R_n(zeta) = n * barQ_n(zeta) for all zeta^n = 1  (checked as
      polynomial congruence  R_n = n*barQ_n mod q^n - 1).

 (M4) NEW THEOREM CANDIDATE: (q^n - 1) | R_n'(q).
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dt_core import moebius, divisors
from scan_refined import load_DT
from test_exact_mobius import admissible_poly, barQ_from_DT, scale_exp, padd, pscal
from mine import poly_trim, poly_sub, poly_divmod_monic
from refined_framed import qbinom


def plog_coeffs(A, D):
    """A: dict n -> poly list (n=1..D); returns dict n -> [t^n] PLog(1 + sum A_n t^n)
    as Laurent-free polys (all integer polys in q). Plethysm: psi_r(q)=q^r."""
    # G_n = n [t^n] log(A-series); series has constant term 1
    F = {0: [1]}
    for n_ in range(1, D + 1):
        F[n_] = A[n_]
    Finv = {0: [1]}
    for n_ in range(1, D + 1):
        s = []
        for j in range(1, n_ + 1):
            s = padd(s, pmul(F[j], Finv[n_ - j]))
        Finv[n_] = pscal(s, -1)
    G = {}
    for n_ in range(1, D + 1):
        s = []
        for j in range(1, n_ + 1):
            s = padd(s, pscal(pmul(F[j], Finv[n_ - j]), j))
        G[n_] = poly_trim(s)
    out = {}
    for n_ in range(1, D + 1):
        s = []
        for r in divisors(n_):
            mu = moebius(r)
            if mu:
                s = padd(s, pscal(scale_exp(G[n_ // r], r), mu))
        # divide by n exactly
        q, rem = [x // n_ for x in s], [x % n_ for x in s]
        assert all(v == 0 for v in rem), f"PLog not integral at n={n_}"
        out[n_] = poly_trim(q)
    return out


def pmul(a, b):
    if not a or not b:
        return []
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    out[i + j] += x * y
    return out


def full_P_poly(m, d):
    """P_d(q) = q^{-(m-1)C(d,2)} qbinom(md-1,d-1)_q as (offset, list)."""
    qb = qbinom(m * d - 1, d - 1)
    off = (m - 1) * d * (d - 1) // 2
    return off, qb


def enumerate_P(m, d):
    """Direct enumeration of P_d over ALL of U_d; returns (offset, list)."""
    from itertools import product
    N = (m - 1) * d
    vals = {}

    def rec(i, remaining, wt):
        if i == d:
            vals[wt] = vals.get(wt, 0) + 1
            return
        for a in range(remaining + 1):
            rec(i + 1, remaining - a, wt + (d - i) * (m - 1 - a))

    rec(1, N, 0)
    lo = min(vals)
    arr = [0] * (max(vals) - lo + 1)
    for w, c in vals.items():
        arr[w - lo] = c
    return -lo, arr


def main():
    for m in (2, 3, 4):
        print(f"=== m = {m} ===")
        DT = load_DT(m)
        D = 10 if m == 2 else 8
        A = {d: admissible_poly(m, d) for d in range(1, D + 1)}
        PL = plog_coeffs(A, D)
        # (M1)
        ok1 = True
        for n in range(1, D + 1):
            T = list(PL[n])
            if m % 2 == 0 and n % 4 == 2:
                T = padd(T, scale_exp(PL[n // 2], 2))
            T = poly_trim(T)
            B = barQ_from_DT(m, DT, n)
            if T != B:
                ok1 = False
                print(f"  (M1) n={n} MISMATCH:")
                print(f"     PLog(A)+corr: {T[:16]}")
                print(f"     barQ        : {B[:16]}")
        print(f"  (M1) barQ = PLog(A) + doubling correction: {ok1}")
        # (M2): P via qbinom vs enumeration
        ok2 = True
        for d in range(1, min(D, 7) + 1):
            o1, p1 = full_P_poly(m, d)
            o2, p2 = enumerate_P(m, d)
            if o1 != o2 or poly_trim(list(p1)) != poly_trim(list(p2)):
                ok2 = False
                print(f"  (M2) P_{d}: qbinom form vs enumeration MISMATCH"
                      f" off {o1} vs {o2}")
        print(f"  (M2) P_d = q^{{-(m-1)C(d,2)}} qbinom(md-1,d-1): {ok2}")
        # (M3),(M4): R_n checks (clear denominators: multiply by q^{big})
        ok3 = True
        ok4 = True
        for n in range(1, D + 1):
            # R_n as Laurent: collect with common offset
            terms = []
            maxoff = 0
            for d in divisors(n):
                mu = moebius(n // d)
                if mu:
                    off, arr = full_P_poly(m, d)
                    s = n // d
                    terms.append((mu, off * s, scale_exp(arr, s)))
                    maxoff = max(maxoff, off * s)
            R = []
            for mu, off, arr in terms:
                R = padd(R, pscal([0] * (maxoff - off) + arr, mu))
            R = poly_trim(R)
            # (M3): R = n * q^{maxoff} * (barQ shifted?) mod q^n - 1
            # barQ_n(q): R(zeta) = n q_shift... barQ picks up zeta^{-maxoff}:
            # check R - n * (q^{maxoff mod n-ish} barQ) mod q^n-1 == 0 properly:
            B = barQ_from_DT(m, DT, n)
            modp = [-1] + [0] * (n - 1) + [1]  # q^n - 1
            sh = maxoff % n
            Bsh = [0] * sh + list(B)
            diff = poly_sub(R, pscal(Bsh, n))
            _, rem = poly_divmod_monic(diff, modp)
            if poly_trim(rem):
                ok3 = False
                print(f"  (M3) n={n}: R != n*q^s*barQ mod q^n-1  (rem {rem[:8]})")
            # (M4): derivative of Laurent R_n: d/dq (q^{-maxoff} R(q)):
            # = q^{-maxoff-1}(q R'(q) - maxoff R(q)) -- test divisibility of
            # the polynomial  q R'(q) - maxoff*R(q)  by q^n - 1.
            Rp = [i * c for i, c in enumerate(R)][1:] if len(R) > 1 else []
            qRp = [0] + Rp  # q * R'
            qRp = padd(qRp, [])
            cand = poly_sub([c * 1 for c in qRp], pscal(R, maxoff))
            _, rem2 = poly_divmod_monic(poly_trim(cand), modp)
            if poly_trim(rem2):
                ok4 = False
                print(f"  (M4) n={n}: (q^n-1) does NOT divide Laurent-derivative"
                      f" of R_n (rem {poly_trim(rem2)[:8]})")
        print(f"  (M3) R_n = n*barQ_n at all n-th roots of unity: {ok3}")
        print(f"  (M4) (q^n-1) | (Laurent derivative of R_n): {ok4}")


if __name__ == "__main__":
    main()
