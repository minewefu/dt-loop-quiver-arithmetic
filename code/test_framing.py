"""Empirically pin down the refined framing identity:

    Z(x) := P(z^a x) / P(x)   (in the CoHA z-convention series P~),

testing for which shift a the coefficients Z_d match the q-Fuss-Catalan
polynomials qFC_d(m; q=z^2) up to a per-degree monomial +-z^{tau(d)}.

Gauge arithmetic: sigma_d = z^{(m-1)d^2} [x^d]P~; multiplying x by z^a
multiplies sigma_d by z^{ad} (a >= 0 keeps everything polynomial).
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dt_core import coeff_sigma, ptrunc, pmul, pshift, pitems
from flint import fmpz_poly
from refined_framed import qFC, ptrim


def series_ratio_gauge(m, D, cap, a, sign_x=False):
    """Coefficients (gauged) of P~(z^a x)/P~(x); returns list of fmpz_poly.

    Gauge: entry d equals z^{(m-1)d^2} * [x^d] ratio.
    """
    F = [coeff_sigma(m, d, cap) for d in range(D + 1)]
    Fa = [pshift(F[d], a * d, cap) for d in range(D + 1)]  # P~(z^a x), gauged
    if sign_x:
        Fa = [Fa[d] if d % 2 == 0 else fmpz_poly([0]) - Fa[d] for d in range(D + 1)]
    # inverse of F in gauge
    G = [None] * (D + 1)
    G[0] = fmpz_poly([1])
    sh = 2 * (m - 1)
    for d in range(1, D + 1):
        s = fmpz_poly([0])
        for j in range(1, d + 1):
            t = pmul(F[j], G[d - j], cap)
            s = s + pshift(t, sh * j * (d - j), cap)
        G[d] = fmpz_poly([0]) - s
    # product Fa * G
    Z = [None] * (D + 1)
    for d in range(D + 1):
        s = fmpz_poly([0])
        for j in range(0, d + 1):
            t = pmul(Fa[j], G[d - j], cap)
            s = s + pshift(t, sh * j * (d - j), cap)
        Z[d] = s
    return Z


def as_list(p):
    return [int(p[i]) for i in range(p.degree() + 1)]


def monomial_ratio(zpoly, qpoly_q):
    """Check zpoly(z) == +- z^t * qpoly(q=z^2); return (sign, t) or None."""
    A = ptrim(as_list(zpoly))
    B = [0] * (2 * len(qpoly_q) - 1) if qpoly_q else []
    for i, c in enumerate(qpoly_q):
        B[2 * i] = c
    B = ptrim(B)
    if not A or not B:
        return None
    # strip leading zeros (lowest exponents)
    la = next(i for i, c in enumerate(A) if c)
    lb = next(i for i, c in enumerate(B) if c)
    A2, B2 = A[la:], B[lb:]
    if len(A2) != len(B2):
        return None
    if A2 == B2:
        return (1, la - lb)
    if A2 == [-c for c in B2]:
        return (-1, la - lb)
    return None


def main():
    for m in (2, 3):
        print("=" * 70)
        print(f"m = {m}")
        D = 6
        cap = (m - 1) * D * D + 8 * D + 60
        qfc = [qFC(m, d) for d in range(D + 1)]
        for sign_x in (False, True):
            for a in range(0, 7):
                Z = series_ratio_gauge(m, D, cap, a, sign_x)
                ok = True
                taus = []
                for d in range(1, D + 1):
                    r = monomial_ratio(Z[d], qfc[d])
                    if r is None:
                        ok = False
                        break
                    taus.append((d, r))
                if ok:
                    print(f"  MATCH: a={a} sign_x={sign_x}: (sign, tau(d)) = {taus}")
        # show first coefficients for manual inspection at a=2
        Z = series_ratio_gauge(m, 4, cap, 2, False)
        for d in range(1, 4):
            print(f"  [a=2] Z_{d} (gauged, low terms): {pitems(ptrunc(Z[d], 24))[:12]}")
            print(f"        qFC_{d} = {qfc[d]}")


if __name__ == "__main__":
    main()
