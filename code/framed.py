"""Test the framed <-> unframed (DT) relation empirically.

Fuss-Catalan numbers FC_d(m) = binom(md, d) / ((m-1)d + 1) are the Euler
characteristics of noncommutative Hilbert schemes Hilb^{(m)}_{d,1} (framed
representations of the free algebra on m generators).

If the numerical framing/product formula holds in the form
    B(x) = sum_d FC_d(m) x^d = prod_{d>=1} (1 - eps^d x^d)^{-d * s_d * c_d}
for signs eps, s_d in {+-1}, then the exponents b_d extracted by Mobius
inversion of log B should reproduce d * c_d up to sign.

We extract  gamma_n := n [x^n] log B  (integers), then
    b_d = (1/d) sum_{e|d} mu(d/e) gamma_e,
and compare b_d with +- d * c_d.
"""

import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dt_core import moebius, divisors, DATA_DIR


def fuss_catalan(m, d):
    return math.comb(m * d, d) // ((m - 1) * d + 1)


def series_log_gammas(coeffs, D):
    """gamma_n = n [x^n] log B for B given by integer coeffs list (B[0]=1)."""
    B = coeffs
    Binv = [0] * (D + 1)
    Binv[0] = 1
    for d in range(1, D + 1):
        Binv[d] = -sum(B[j] * Binv[d - j] for j in range(1, d + 1))
    gam = [0] * (D + 1)
    for n in range(1, D + 1):
        gam[n] = sum(j * B[j] * Binv[n - j] for j in range(1, n + 1))
    return gam


def load_c(m):
    path = os.path.join(DATA_DIR, f"omega_m{m}.json")
    with open(path) as f:
        raw = json.load(f)
    c = {}
    for dstr, items in raw.items():
        d = int(dstr)
        s = sum(((-1) ** (e % 2)) * cc for e, cc in items)
        c[d] = abs(s)
    return c


def main():
    for m in (2, 3, 4, 5, 6):
        c = load_c(m)
        D = min(max(c), 60)
        B = [fuss_catalan(m, d) for d in range(D + 1)]
        gam = series_log_gammas(B, D)
        print(f"--- m = {m} ---")
        print(f"  FC: {B[:8]}")
        print(f"  gamma: {gam[1:9]}")
        ok_all = True
        for d in range(1, D + 1):
            tot = sum(moebius(d // e) * gam[e] for e in divisors(d))
            if tot % d != 0:
                print(f"  d={d}: Mobius sum not divisible by d! {tot}")
                ok_all = False
                continue
            b = tot // d
            # compare with +- d c_d
            target = d * c.get(d)
            status = None
            if b == target:
                status = "+"
            elif b == -target:
                status = "-"
            if status is None:
                ok_all = False
                if d <= 12:
                    print(f"  d={d}: b_d={b} vs d*c_d={target}  MISMATCH")
            else:
                if d <= 12:
                    print(f"  d={d}: b_d={b} = {status}d*c_d   OK")
        print(f"  all matched (up to sign): {ok_all}")
        # record sign pattern
        signs = []
        for d in range(1, min(D, 16) + 1):
            tot = sum(moebius(d // e) * gam[e] for e in divisors(d))
            b = tot // d
            t = d * c.get(d)
            signs.append('+' if b == t else ('-' if b == -t else '?'))
        print(f"  sign pattern (d=1..): {''.join(signs)}")
        print()


if __name__ == "__main__":
    main()
