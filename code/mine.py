"""Mine the DT invariant data for arithmetic patterns.

Part 1: numerical supercongruences  v_p( c_{pd}(m) - c_d(m) ).
Part 2: refined q-congruences: max k with Phi_p(q)^k | Omega~_{pd}(q) - Omega~_d(q^{p^2})
        (bottom-aligned; purity makes both polynomials in q = z^2 after shift).
Part 3: level-raising (Jacobsthal towers): v_p( c_{p^2 d} - c_{p d} ).
"""

import json
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dt_core import DATA_DIR

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23]


def load(m):
    path = os.path.join(DATA_DIR, f"omega_m{m}.json")
    with open(path) as f:
        raw = json.load(f)
    return {int(d): [(e, c) for e, c in items] for d, items in raw.items()}


def numerical_signed(items):
    return sum(c for _, c in items)


def numerical_abs(items):
    s = sum(((-1) ** (e % 2)) * c for e, c in items)
    return abs(s)


def vp(n, p):
    if n == 0:
        return None  # infinity
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


# ---------------------------------------------------------------------------
# polynomial helpers over Z (dense lists, index = exponent)
# ---------------------------------------------------------------------------

def cyclotomic_p(p):
    """Phi_p(w) = 1 + w + ... + w^{p-1} for prime p."""
    return [1] * p


def poly_sub(a, b):
    n = max(len(a), len(b))
    return [(a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)
            for i in range(n)]


def poly_trim(a):
    while a and a[-1] == 0:
        a.pop()
    return a


def poly_divmod_monic(a, b):
    """Divide a by monic b over Z; returns (quot, rem)."""
    a = list(a)
    db = len(b) - 1
    if len(a) - 1 < db:
        return [], a
    quot = [0] * (len(a) - db)
    for i in range(len(a) - 1 - db, -1, -1):
        c = a[i + db]
        if c:
            quot[i] = c
            for j in range(db + 1):
                a[i + j] -= c * b[j]
    poly_trim(a)
    return quot, a


def max_cyclotomic_power(diff, p, kmax=8):
    """Largest k <= kmax with Phi_p^k | diff (over Z[w])."""
    diff = poly_trim(list(diff))
    if not diff:
        return None  # identically zero: infinite
    phi = cyclotomic_p(p)
    k = 0
    while k < kmax:
        q, r = poly_divmod_monic(diff, phi)
        if poly_trim(r):
            break
        diff = q
        k += 1
        if not poly_trim(list(diff)):
            break
    return k


def items_to_qpoly_bottom(items):
    """Given Omega~ items (z-exponents, single parity), return (bot_z, list in w=z^2).

    All exponents share one parity; shift by the minimum exponent, then halve.
    """
    if not items:
        return 0, []
    exps = [e for e, _ in items]
    par = {e % 2 for e in exps}
    assert len(par) == 1, "purity violated"
    bot = min(exps)
    arr = [0] * ((max(exps) - bot) // 2 + 1)
    for e, c in items:
        assert (e - bot) % 2 == 0
        arr[(e - bot) // 2] = c
    return bot, arr


def scale_exponents(arr, s):
    """w -> w^s on a dense poly list."""
    out = [0] * ((len(arr) - 1) * s + 1) if arr else []
    for i, c in enumerate(arr):
        if c:
            out[i * s] = c
    return out


# ---------------------------------------------------------------------------

def part1_numerical(data):
    print("=" * 78)
    print("PART 1: v_p( c_{pd} - c_d )   [c_d = |Omega_d(1)|, positive normalization]")
    print("=" * 78)
    for m, Om in data.items():
        D = max(Om)
        c = {d: numerical_abs(Om[d]) for d in Om}
        print(f"--- m = {m} (D={D}) ---")
        for p in PRIMES:
            rows = []
            d = 1
            while p * d <= D:
                val = c[p * d] - c[d]
                rows.append((d, vp(val, p)))
                d += 1
            if rows:
                print(f"  p={p:>2}: " + "  ".join(
                    f"v_p(c_{{{p}*{d}}}-c_{d})={v if v is not None else 'inf'}"
                    for d, v in rows))
        print()


def part3_towers(data):
    print("=" * 78)
    print("PART 3: towers v_p( c_{p^2 d} - c_{p d} )")
    print("=" * 78)
    for m, Om in data.items():
        D = max(Om)
        c = {d: numerical_abs(Om[d]) for d in Om}
        for p in PRIMES:
            d = 1
            rows = []
            while p * p * d <= D:
                val = c[p * p * d] - c[p * d]
                rows.append((d, vp(val, p)))
                d += 1
            if rows:
                print(f"  m={m} p={p}: " + "  ".join(
                    f"v_p(c_{{{p*p}*{d}}}-c_{{{p}*{d}}})={v if v is not None else 'inf'}"
                    for d, v in rows))
    print()


def part2_refined(data):
    print("=" * 78)
    print("PART 2: max k with Phi_p(q)^k | Omega~_{pd}(q) - Omega~_d(q^{p^2})")
    print("        (z-polys bottom-aligned, w = z^2; 'inf' = identical)")
    print("=" * 78)
    for m, Om in data.items():
        D = max(Om)
        print(f"--- m = {m} (D={D}) ---")
        for p in [2, 3, 5, 7, 11, 13]:
            rows = []
            d = 1
            while p * d <= D:
                botA, A = items_to_qpoly_bottom(Om[p * d])
                botB0, B0 = items_to_qpoly_bottom(Om[d])
                B = scale_exponents(B0, p * p)
                botB = botB0 * p * p
                if botA != botB:
                    rows.append((d, f"BOTMISMATCH({botA},{botB})"))
                    d += 1
                    continue
                diff = poly_sub(A, B)
                k = max_cyclotomic_power(diff, p)
                rows.append((d, "inf" if k is None else k))
                d += 1
            if rows:
                print(f"  p={p:>2}: " + "  ".join(f"d={d}:k={k}" for d, k in rows))
        print()


def main():
    data = {m: load(m) for m in (2, 3, 4, 5, 6)}
    part1_numerical(data)
    part2_refined(data)
    part3_towers(data)


if __name__ == "__main__":
    main()
