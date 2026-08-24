"""Test the EXACT q-Mobius conjecture:

  barQ_n(q) = sum_{d|n} mu(n/d) A_d(q^{n/d})
              + [m even, n = 2 mod 4] * sum_{d | n/2} mu(n/(2d)) A_d(q^{n/d}),

where A_d(q) = sum over ADMISSIBLE a in U_d of q^{wt(a)}:
  U_d = {a in N^d : sum a_i = (m-1)d},  admissible: sum_{j<=i} a_j <= (m-1)i,
  wt(a) = sum_i (d-i)(m-1-a_i),
and barQ_n(q) = [n]_q * q^{1-n} * DT_n(q)  (from the engine data).

Also compare A_d(q) with the framed series coefficients (NC Hilbert scheme
Poincare polynomials, Reineke's F(q,t)) computed from H(q,t)/H(q,q^{-1}t).
"""

import json
import os
import sys
from itertools import product as iproduct

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dt_core import DATA_DIR, moebius, divisors
from scan_refined import load_DT
from mine import poly_trim, poly_sub


def admissible_poly(m, d):
    """A_d(q) by direct enumeration (compositions of (m-1)d into d parts,
    ballot condition), as dense list."""
    N = (m - 1) * d
    out = {}

    def rec(i, remaining, partials_ok, wt):
        # a_i chosen for positions 1..i-1; wt accumulated
        if i == d:
            a_d = remaining
            w = wt + (d - i) * (m - 1 - a_d)  # (d-i)=0, no contribution
            out[w] = out.get(w, 0) + 1
            return
        # position i (1-based), can take a_i = 0..min(remaining, (m-1)i - used)
        # partial sum condition: sum_{j<=i} a_j <= (m-1) i
        used = N - remaining
        for a in range(0, min(remaining, (m - 1) * i - used) + 1):
            rec(i + 1, remaining - a, True, wt + (d - i) * (m - 1 - a))

    rec(1, N, True, 0)
    deg = max(out) if out else 0
    arr = [0] * (deg + 1)
    for w, c in out.items():
        arr[w] = c
    return arr


def scale_exp(arr, s):
    out = [0] * ((len(arr) - 1) * s + 1) if arr else []
    for i, c in enumerate(arr):
        if c:
            out[i * s] = c
    return out


def padd(a, b):
    n = max(len(a), len(b))
    return [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
            for i in range(n)]


def pscal(a, c):
    return [c * x for x in a]


def barQ_from_DT(m, DT, n):
    """barQ_n = [n]_q q^{1-n} DT_n: DT_n is divisible by q^{n-1}."""
    arr = DT[n]
    assert all(c == 0 for c in arr[: n - 1]), "q^{n-1} | DT_n fails?"
    shifted = arr[n - 1:]
    out = [0] * (len(shifted) + n - 1)
    for i, c in enumerate(shifted):
        if c:
            for j in range(n):
                out[i + j] += c
    return poly_trim(out)


def main():
    for m in (2, 3, 4):
        print(f"=== m = {m} ===")
        DT = load_DT(m)
        Dmax = 9 if m == 2 else 8
        A = {d: admissible_poly(m, d) for d in range(1, Dmax + 1)}
        print(f"  A_1..A_4: {[A[d] for d in range(1, 5)]}")
        print(f"  A_d(1) (should be Fuss-Catalan binom(md,d)/((m-1)d+1)):"
              f" {[sum(A[d]) for d in range(1, Dmax + 1)]}")
        allok = True
        for n in range(1, Dmax + 1):
            T = []
            for d in divisors(n):
                mu = moebius(n // d)
                if mu:
                    T = padd(T, pscal(scale_exp(A[d], n // d), mu))
            if m % 2 == 0 and n % 4 == 2:
                for d in divisors(n // 2):
                    mu = moebius(n // (2 * d))
                    if mu:
                        T = padd(T, pscal(scale_exp(A[d], n // d), mu))
            T = poly_trim(T)
            B = barQ_from_DT(m, DT, n)
            if T == B:
                print(f"  n={n}: EXACT MATCH  (barQ_n = Mobius(A) formula)")
            else:
                allok = False
                print(f"  n={n}: MISMATCH")
                print(f"    Mobius(A): {T[:18]}")
                print(f"    barQ_n   : {B[:18]}")
        print(f"  all exact: {allok}")


if __name__ == "__main__":
    main()
