"""Find the refined (q-deformed) framing relation empirically.

Candidate framed refined series: q-Fuss-Catalan polynomials
    qFC_d(m; q) = (1/[(m-1)d+1]_q) * qbinom(md, d)_q   (integer polynomial)
possibly with a normalization twist q^{alpha(d)}.

We compute  M_d(q) := sum_{r|d} mu(r) psi_r(G_{d/r}),  G_n := n [x^n] log B_q,
so that [x^d] PLog(B_q) = M_d / d, and compare against the known refined DT
invariants Omega~_d(z) (z^2 = q) of the m-loop quiver, looking for the kernel
K_d(q) with  M_d / d = (Omega-transform) * K_d.

All arithmetic exact over Z[q] (dense integer lists).
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dt_core import moebius, divisors, DATA_DIR


# ---------------- dense Z[q] helpers ----------------

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


def padd(a, b):
    n = max(len(a), len(b))
    return [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
            for i in range(n)]


def pscal(a, c):
    return [c * x for x in a]


def ptrim(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def pdiv_exact(a, b):
    """Exact division a/b over Z (b monic-leading or divides exactly)."""
    a = ptrim(a)
    b = ptrim(b)
    if not a:
        return []
    q = [0] * (len(a) - len(b) + 1)
    r = list(a)
    lead = b[-1]
    for i in range(len(a) - len(b), -1, -1):
        c = r[i + len(b) - 1]
        if c % lead != 0:
            raise ArithmeticError("non-exact poly division")
        c //= lead
        q[i] = c
        if c:
            for j in range(len(b)):
                r[i + j] -= c * b[j]
    if ptrim(r):
        raise ArithmeticError("nonzero remainder")
    return q


def qint(n):
    """[n]_q = 1 + q + ... + q^{n-1}."""
    return [1] * n


def qbinom(n, k):
    """Gaussian binomial [n choose k]_q, exact."""
    if k < 0 or k > n:
        return []
    num = [1]
    den = [1]
    for i in range(1, k + 1):
        num = pmul(num, qint(n - k + i))
        den = pmul(den, qint(i))
    return pdiv_exact(num, den)


def ppsi(a, r):
    out = [0] * ((len(a) - 1) * r + 1) if a else []
    for i, c in enumerate(a):
        if c:
            out[i * r] = c
    return out


# ---------------- q-Fuss-Catalan and log ----------------

def qFC(m, d):
    if d == 0:
        return [1]
    return pdiv_exact(qbinom(m * d, d), qint((m - 1) * d + 1))


def log_gammas_poly(B, D):
    """G_n = n [x^n] log B for B a list of Z[q] polys (B[0] = [1])."""
    Binv = [None] * (D + 1)
    Binv[0] = [1]
    for d in range(1, D + 1):
        s = []
        for j in range(1, d + 1):
            s = padd(s, pmul(B[j], Binv[d - j]))
        Binv[d] = pscal(s, -1)
    G = [None] * (D + 1)
    for n in range(1, D + 1):
        s = []
        for j in range(1, n + 1):
            s = padd(s, pscal(pmul(B[j], Binv[n - j]), j))
        G[n] = ptrim(s)
    return G


def load_omega(m):
    path = os.path.join(DATA_DIR, f"omega_m{m}.json")
    with open(path) as f:
        raw = json.load(f)
    return {int(d): [(e, c) for e, c in items] for d, items in raw.items()}


def poly_str(a, var="q", maxterms=14):
    it = [(i, c) for i, c in enumerate(a) if c]
    if not it:
        return "0"
    s = " + ".join(f"{c}{'' if i==0 else f'*{var}^{i}'}" for i, c in it[:maxterms])
    if len(it) > maxterms:
        s += f" ... ({len(it)} terms)"
    return s


def main():
    for m in (2, 3):
        print("=" * 76)
        print(f"m = {m}")
        Om = load_omega(m)
        D = 8
        B = [qFC(m, d) for d in range(D + 1)]
        print("qFC_1..4:")
        for d in range(1, 5):
            print(f"  d={d}: {poly_str(B[d])}")
        G = log_gammas_poly(B, D)
        for d in range(1, D + 1):
            M = []
            for r in divisors(d):
                mu = moebius(r)
                if mu == 0:
                    continue
                M = padd(M, pscal(ppsi(G[d // r], r), mu))
            M = ptrim(M)
            # M = d * [x^d] PLog(B_q)
            print(f"d={d}:")
            print(f"  M_d(q)   = {poly_str(M)}")
            items = Om[d]
            print(f"  Omega~_d(z) = "
                  + " + ".join(f"{c}*z^{e}" for e, c in items[:10])
                  + (" ..." if len(items) > 10 else ""))
        print()


if __name__ == "__main__":
    main()
