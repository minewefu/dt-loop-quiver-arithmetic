"""Direct verification of Theorem qsuper:
  (a) for every ODD prime p | n:  Phi_p(q)^2 | R_n(q)  (as Laurent polys);
  (b) for p=2, m even, n = 2 mod 4:  R_n(-1) = -n * barQprim_{n/2}(1),
      R_n'(-1) = 0;
  (c) for p=2 with (m odd or 4 | n):  Phi_2^2 | R_n.
Also descend to prime powers p^j | n (odd p): Phi_{p^j}^2 | R_n.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dt_core import moebius, divisors
from mine import poly_trim, poly_divmod_monic
from test_master import full_P_poly, scale_exp, padd, pscal
import math


def cyclotomic(n):
    """Phi_n(q) for n = p^j (p prime): Phi_{p^j} = sum_{i<p} q^{i p^{j-1}}."""
    # factor n as p^j
    p = None
    for cand in (2, 3, 5, 7, 11, 13, 17):
        if n % cand == 0:
            p = cand
            break
    j = 0
    t = n
    while t % p == 0:
        t //= p
        j += 1
    assert t == 1, "cyclotomic() only for prime powers here"
    step = p ** (j - 1)
    out = [0] * ((p - 1) * step + 1)
    for i in range(p):
        out[i * step] = 1
    return out


def R_hat(m, n):
    """Monomial-cleared R_n: returns (shift, poly list) with R_n = q^{-shift}*poly."""
    terms = []
    maxoff = 0
    for d in divisors(n):
        mu = moebius(n // d)
        if mu:
            off, arr = full_P_poly(m, d)
            s = n // d
            terms.append((mu, off * s, scale_exp(list(arr), s)))
            maxoff = max(maxoff, off * s)
    R = []
    for mu, off, arr in terms:
        R = padd(R, pscal([0] * (maxoff - off) + arr, mu))
    return maxoff, poly_trim(R)


def barQprim1(m, k):
    """barQprim_k(1) = number of primitive classes = (1/k) sum mu(k/d) binom(md-1,d-1)."""
    s = sum(moebius(k // d) * math.comb(m * d - 1, d - 1) for d in divisors(k))
    assert s % k == 0
    return s // k


def divides(mod, poly):
    _, r = poly_divmod_monic(list(poly), mod)
    return not poly_trim(r)


def main():
    fails = []
    for m in (2, 3, 4, 5):
        for n in range(2, 19):
            sh, R = R_hat(m, n)
            for pj in divisors(n):
                if pj == 1:
                    continue
                # prime powers only
                ps = [p for p in (2, 3, 5, 7, 11, 13, 17) if pj % p == 0]
                if len(ps) != 1:
                    continue
                p = ps[0]
                t = pj
                while t % p == 0:
                    t //= p
                if t != 1:
                    continue
                phi = cyclotomic(pj)
                phi2 = poly_trim([sum(phi[i] * phi[k - i] for i in range(max(0, k - len(phi) + 1), min(k + 1, len(phi))))
                                  for k in range(2 * len(phi) - 1)])
                if p != 2:
                    ok = divides(phi2, R)
                    if not ok:
                        fails.append((m, n, pj, "odd-p Phi^2"))
                else:
                    if m % 2 == 1 or n % 4 == 0:
                        if pj == 2:
                            ok = divides(phi2, R)
                            if not ok:
                                fails.append((m, n, pj, "p=2 clean Phi^2"))
                    elif n % 4 == 2 and pj == 2:
                        # R(-1) = -n*barQprim_{n/2}(1); R'(-1)=0
                        Rm1 = sum(c * (-1) ** i for i, c in enumerate(R))
                        Rpm1 = sum(i * c * (-1) ** ((i - 1) % 2) for i, c in enumerate(R) if i >= 1)
                        # Laurent: R_n = q^{-sh} * poly: value at -1: (-1)^{-sh}*poly(-1)
                        val = (-1) ** sh * Rm1
                        # derivative of q^{-sh}f: q^{-sh-1}(qf' - sh f); at -1:
                        dval = (-1) ** (sh + 1) * ((-1) * Rpm1 - sh * Rm1) * (-1)
                        # simpler: d/dq [q^{-sh} f] (-1) = (-sh)(-1)^{-sh-1}f(-1)+(-1)^{-sh}f'(-1)
                        dval = (-sh) * ((-1) ** (sh + 1)) * Rm1 + ((-1) ** sh) * Rpm1
                        expect = -n * barQprim1(m, n // 2)
                        if val != expect:
                            fails.append((m, n, 2, f"R(-1)={val} expect {expect}"))
                        if dval != 0:
                            fails.append((m, n, 2, f"R'(-1)={dval} nonzero"))
    if fails:
        print("FAILURES:", fails)
    else:
        print("Theorem qsuper verified end-to-end: Phi_{p^j}^2 | R_n for odd prime powers"
              " p^j | n; p=2 clean cases; and exact p=2 defect R_n(-1) = -n*barQprim_{n/2}(1),"
              " R_n'(-1)=0, for m<=5, n<=18.")


if __name__ == "__main__":
    main()
