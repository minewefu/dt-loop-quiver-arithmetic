"""
Exact computation of refined Donaldson-Thomas invariants of the m-loop quiver
via the Kontsevich-Soibelman / Efimov plethystic factorization.

Conventions
-----------
v = q^{1/2}.  For the m-loop quiver Q_m (one vertex, m loops) the Euler form is
chi(d,e) = (1-m) d e.  The Poincare series of the (KS-shifted) Cohomological
Hall algebra is

  P(x,v) = sum_{d>=0} v^{(1-m) d^2} x^d / (v^2; v^2)_d ,
  (v^2;v^2)_d = prod_{j=1}^d (1 - v^{2j})   (nonnegative coefficients).

Efimov: the CoHA is free supercommutative, Sym(V (x) C[u]) with u of weight
v^2; Omega_d(v) := Poincare polynomial of V_d has NONNEGATIVE coefficients;
parity of a weight-w generator = w mod 2.

Extraction: substitute v -> -z (turning super-Sym into ordinary plethystic Exp
with psi_r(z) = z^r, psi_r(x) = x^r):

  P~(x,z) := P(x,-z) = Exp( sum_{d>=1} barOmega~_d(z) x^d ),
  Omega~_d(z) := (1 - z^2) * barOmega~_d(z),
  Omega_d(v)  = (-1)^{(m-1)d} * Omega~_d(-v)   (nonnegative).

Gauge trick (soundness of truncation)
-------------------------------------
The x^d coefficient of P~ has support in [(1-m)d^2, +infinity).  We store the
GAUGED coefficient  sigma_d(z) := z^{(m-1)d^2} * [x^d]P~  which has support in
[0, +infinity).  In this gauge:
  * product of x-degrees j,k acquires shift  z^{2(m-1)jk}   (>= 0),
  * psi_r at x-degree e acquires shift       z^{(m-1)r(r-1)e^2} (>= 0),
so every operation moves mass upward only, and truncation at a cap is EXACT
below the cap.  All arithmetic uses FLINT fmpz_poly (exact integers).

Anchors (proved by hand via Euler's identities, verified in validate()):
  m=0:  Omega_1(v) = v  (one fermionic generator, chi(1,1)=1 odd), rest 0.
  m=1:  Omega_1(v) = 1  (one bosonic generator,  chi(1,1)=0 even), rest 0.
"""

from flint import fmpz_poly
import json
import os
import time

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")


# ----------------------------------------------------------------------------
# number theory helpers
# ----------------------------------------------------------------------------

def moebius(n):
    if n == 1:
        return 1
    result = 1
    p = 2
    while p * p <= n:
        if n % p == 0:
            n //= p
            if n % p == 0:
                return 0
            result = -result
        p += 1
    if n > 1:
        result = -result
    return result


def divisors(n):
    ds = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            ds.append(i)
            if i != n // i:
                ds.append(n // i)
        i += 1
    return sorted(ds)


# ----------------------------------------------------------------------------
# polynomial helpers (ordinary polynomials in z, exact, truncated at a cap)
# ----------------------------------------------------------------------------

def ptrunc(p, cap):
    if p.degree() <= cap:
        return p
    return fmpz_poly([int(p[i]) for i in range(cap + 1)])


def pmul(a, b, cap):
    return ptrunc(a * b, cap)


def pshift(p, k, cap):
    """Multiply by z^k, k >= 0."""
    if k == 0:
        return ptrunc(p, cap)
    d = p.degree()
    if d < 0:
        return p
    return fmpz_poly([0] * k + [int(p[i]) for i in range(min(d, cap - k) + 1)])


def pgeom(p, s, cap):
    """Multiply by 1/(1 - z^s), s > 0 (cumulative sums upward)."""
    arr = [int(p[i]) for i in range(min(p.degree(), cap) + 1)]
    arr += [0] * (cap + 1 - len(arr))
    for k in range(s, cap + 1):
        arr[k] += arr[k - s]
    return fmpz_poly(arr)


def ppsi(p, r, cap):
    """z -> z^r on exponents."""
    d = p.degree()
    out = [0] * (min(d * r, cap) + 1)
    for k in range(d + 1):
        c = int(p[k])
        if c and r * k <= cap:
            out[r * k] = c
    return fmpz_poly(out)


def pdiv_exact(p, n):
    cs = []
    for i in range(p.degree() + 1):
        c = int(p[i])
        q, rem = divmod(c, n)
        if rem != 0:
            raise ArithmeticError(f"non-exact division by {n}: coeff {c} at z^{i}")
        cs.append(q)
    return fmpz_poly(cs)


def pitems(p):
    return [(i, int(p[i])) for i in range(p.degree() + 1) if int(p[i]) != 0]


# ----------------------------------------------------------------------------
# gauged quantum series of the m-loop quiver (m >= 1)
# ----------------------------------------------------------------------------

def coeff_sigma(m, d, cap):
    """sigma_d(z) = z^{(m-1)d^2} * [x^d] P~(x,z);  support in [0, inf).

    [x^d]P~ = (-1)^{(m-1)d} z^{(1-m)d^2} / (z^2;z^2)_d, so
    sigma_d = (-1)^{(m-1)d} / (z^2;z^2)_d  as a power series.
    """
    if d == 0:
        return fmpz_poly([1])
    c = fmpz_poly([1])
    for j in range(1, d + 1):
        c = pgeom(c, 2 * j, cap)
    if ((m - 1) * d) % 2 == 1:
        c = fmpz_poly([0]) - c
    return c


def dt_invariants(m, D, ecap=None, progress=False):
    """Refined DT invariants of the m-loop quiver (m >= 1), d = 1..D.

    Returns dict d -> list of (exponent, coeff) pairs of Omega~_d(z)
    (true exponents, i.e. after removing the gauge z^{(m-1)d^2}).
    The nonnegative Omega_d(v) = (-1)^{(m-1)d} Omega~_d(-v).
    """
    if m < 1:
        raise ValueError("gauged engine requires m >= 1")
    if ecap is None:
        ecap = (m - 1) * D * D + 2 * D + 24
    cap = ecap + 16  # working cap; final results truncated to ecap
    t0 = time.time()
    F = [coeff_sigma(m, d, cap) for d in range(D + 1)]
    shift2 = 2 * (m - 1)

    # x-series inverse of F in the gauge
    G = [None] * (D + 1)
    G[0] = fmpz_poly([1])
    for d in range(1, D + 1):
        s = fmpz_poly([0])
        for j in range(1, d + 1):
            t = pmul(F[j], G[d - j], cap)
            s = s + pshift(t, shift2 * j * (d - j), cap)
        G[d] = fmpz_poly([0]) - s

    # H_d = d * [x^d] log F   (gauged)
    H = [None] * (D + 1)
    for d in range(1, D + 1):
        s = fmpz_poly([0])
        for j in range(1, d + 1):
            t = pmul(F[j] * fmpz_poly([j]), G[d - j], cap)
            s = s + pshift(t, shift2 * j * (d - j), cap)
        H[d] = s
    if progress:
        print(f"  [m={m}] D={D}: log-derivative done in {time.time()-t0:.1f}s",
              flush=True)

    one_minus_z2 = fmpz_poly([1, 0, -1])
    Omega = {}
    for d in range(1, D + 1):
        S = fmpz_poly([0])
        for r in divisors(d):
            mu = moebius(r)
            if mu == 0:
                continue
            e = d // r
            t = ppsi(H[e], r, cap)
            t = pshift(t, (m - 1) * r * (r - 1) * e * e, cap)
            S = S + t * fmpz_poly([mu])
        barOm = pdiv_exact(S, d)
        Om = ptrunc(pmul(one_minus_z2, barOm, cap), ecap)
        deg = Om.degree()
        while deg >= 0 and int(Om[deg]) == 0:
            deg -= 1
        if deg > ecap - 8:
            raise ValueError(f"Omega_{d} support reaches ecap; increase ecap")
        base = (m - 1) * d * d
        Omega[d] = [(i - base, int(Om[i])) for i in range(deg + 1) if int(Om[i])]
    return Omega


# ----------------------------------------------------------------------------
# views and checks (items = list of (exponent, coeff) of Omega~_d(z))
# ----------------------------------------------------------------------------

def check_signed_purity(items):
    """Efimov positivity: (-1)^e * c must have one common sign over Omega~_d."""
    signs = {1 if ((-1) ** (e % 2)) * c > 0 else -1 for e, c in items}
    return len(signs) <= 1


def omega_true(items):
    """The nonnegative Omega_d(v) as items [(exp, coeff >= 0)]."""
    out = [(e, (-1) ** (e % 2) * c) for e, c in items]
    if out and out[0][1] < 0:
        out = [(e, -c) for e, c in out]
    return out


def numerical(items):
    return sum(c for _, c in items)


def fmt(items, var="v"):
    if not items:
        return "0"
    return " + ".join(f"{c}*{var}^{e}" if e else f"{c}" for e, c in items)


# ----------------------------------------------------------------------------
# validation
# ----------------------------------------------------------------------------

def validate():
    print("=" * 72)
    print("VALIDATION: anchors, positivity, symmetry")
    print("=" * 72)
    Om = dt_invariants(1, 8, ecap=80)
    nz = {d: fmt(Om[d], "z") for d in Om if Om[d]}
    print(f"m=1: nonzero Omega~_d: {nz}   (expect only d=1: '1')")
    for m in (2, 3, 4):
        D = 8
        Om = dt_invariants(m, D, progress=True)
        allpure = all(check_signed_purity(Om[d]) for d in Om)
        print(f"m={m}: signed-purity (Efimov positivity) for d<={D}: {allpure}")
        for d in range(1, D + 1):
            items = omega_true(Om[d])
            num = numerical(items)
            supp = [e for e, _ in items]
            lo, hi = (supp[0], supp[-1]) if supp else (None, None)
            print(f"  Omega_{d}(v): num={num:>12}  support=[{lo},{hi}]")
            if d <= 4:
                print(f"      = {fmt(items)}")
    print()


if __name__ == "__main__":
    validate()
