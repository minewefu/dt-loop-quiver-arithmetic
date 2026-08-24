"""Definitive arithmetic scan in Reineke's normalization.

Dictionary (verified against Reineke's tables):
    DT_n(q) = (-1)^{(m-1)n} * sum_{(e,c) in Omega~_n} c * q^{(-e-n)/2}.

Checks:
  0. Efimov Cor 4.2 sanity: DT_n monic of degree (m-1) n(n-1)/2, divisible by
     q^{n-1}, nonnegative coefficients.
  1. Improved integrality: v_p(DT_n) >= v_p(n) for p >= 5; exact defects at 2,3.
  2. Refined congruences: for p | n, compare DT_n(q) mod Phi_p(q)^k against
     candidates +- q^j * DT_{n/p}(q^{p^2}), +- q^j * DT_{n/p}(q^p), j=0..p-1,
     for k = 1, 2, 3.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dt_core import DATA_DIR
from mine import poly_divmod_monic, poly_sub, poly_trim, cyclotomic_p, vp

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]


def load_DT(m):
    with open(os.path.join(DATA_DIR, f"omega_m{m}.json")) as f:
        raw = json.load(f)
    DT = {}
    for dstr, items in raw.items():
        n = int(dstr)
        sign = (-1) ** ((m - 1) * n)
        coeffs = {}
        for e, c in items:
            j2 = -e - (m - 1) * n
            assert j2 % 2 == 0
            j = j2 // 2
            assert j >= 0
            coeffs[j] = sign * c
        deg = max(coeffs)
        arr = [0] * (deg + 1)
        for j, c in coeffs.items():
            arr[j] = c
        DT[n] = arr
    return DT


def sanity(m, DT):
    ok = True
    for n, arr in DT.items():
        deg = len(arr) - 1
        exp_deg = (m - 1) * n * (n - 1) // 2
        low = next(i for i, c in enumerate(arr) if c)
        if deg != exp_deg or arr[deg] != 1 or low < n - 1 or any(c < 0 for c in arr):
            print(f"  SANITY FAIL m={m} n={n}: deg={deg} (exp {exp_deg}), "
                  f"top={arr[deg]}, low={low}, minc={min(arr)}")
            ok = False
    print(f"  [m={m}] Efimov sanity (monic, deg, q^(n-1) | DT, >=0): {ok}")
    return ok


def improved_integrality(m, DT):
    print(f"  [m={m}] improved integrality  v_p(DT_n) - v_p(n):")
    defects = {}
    for n in sorted(DT):
        val = sum(DT[n])  # DT_n(1) = numerical
        for p in PRIMES:
            vn = vp(n, p) if n % p == 0 else 0
            if vn == 0:
                continue
            vd = vp(val, p)
            d = (vd if vd is not None else 99) - vn
            if d < 0:
                defects.setdefault(p, []).append((n, d))
    for p in PRIMES:
        if p in defects:
            print(f"    p={p}: DEFECTS (v_p(DT_n) < v_p(n)) at: {defects[p]}")
        elif any(n % p == 0 for n in DT):
            print(f"    p={p}: OK for all n <= {max(DT)} with p | n")
    return defects


def scale_poly(arr, s):
    out = [0] * ((len(arr) - 1) * s + 1) if arr else []
    for i, c in enumerate(arr):
        if c:
            out[i * s] = c
    return out


def shift_poly(arr, j):
    return [0] * j + list(arr)


def phi_power(p, k):
    out = [1]
    phi = cyclotomic_p(p)
    for _ in range(k):
        new = [0] * (len(out) + len(phi) - 1)
        for i, a in enumerate(out):
            if a:
                for jj, b in enumerate(phi):
                    new[i + jj] += a * b
        out = new
    return out


def reduce_mod(arr, modpoly):
    _, r = poly_divmod_monic(list(arr), modpoly)
    return poly_trim(r)


def refined_scan(m, DT):
    print(f"  [m={m}] refined congruence scan (p | n):")
    Dmax = max(DT)
    for p in [2, 3, 5, 7, 11, 13]:
        results = []
        n = p
        while n <= Dmax:
            if n // p in DT and n in DT:
                d = n // p
                best = None
                for k in (3, 2, 1):
                    mod = phi_power(p, k)
                    A = reduce_mod(DT[n], mod)
                    found = None
                    for scale in (p * p, p):
                        B0 = scale_poly(DT[d], scale)
                        for j in range(p):
                            for sgn in (1, -1):
                                B = [sgn * c for c in shift_poly(B0, j)]
                                if poly_trim(poly_sub(A, reduce_mod(B, mod))) == []:
                                    found = (k, scale, j, sgn)
                                    break
                            if found:
                                break
                        if found:
                            break
                    if found:
                        best = found
                        break
                results.append((n, best))
            n += p
        if results:
            desc = []
            for n, b in results:
                if b is None:
                    desc.append(f"n={n}:none")
                else:
                    k, sc, j, sg = b
                    desc.append(f"n={n}:k={k},q^{{{'p^2' if sc==p*p else 'p'}}},"
                                f"j={j},s={sg:+d}")
            print(f"    p={p}: " + "  ".join(desc))


def root_of_unity_dive(m, DT):
    """Print the NORMALIZED value  V_n := q^{1-n} DT_n(q) = barQ_n/[n]  mod
    Phi_p as coefficient vectors (multiply by q^k, k = (1-n) mod p, since
    q^p = 1 mod Phi_p)."""
    print(f"  [m={m}] normalized values V_n = q^(1-n) DT_n mod Phi_p:")
    for p in (2, 3, 5, 7):
        phi = cyclotomic_p(p)
        rows = []
        for n in sorted(DT):
            if n > (16 if p < 5 else (30 if p == 5 else 28)):
                continue
            k = (1 - n) % p
            r = reduce_mod(shift_poly(DT[n], k), phi)
            r = r + [0] * ((p - 1) - len(r))
            rows.append((n, r, sum(DT[n])))
        print(f"    p={p}:")
        for n, r, num in rows:
            print(f"      n={n:>2}: V_n mod Phi_{p} = {r}"
                  + (f"   V(1)={num}" if n <= 10 else ""))


def main():
    for m in (2, 3, 4, 5, 6):
        print("=" * 78)
        DT = load_DT(m)
        sanity(m, DT)
        improved_integrality(m, DT)
        refined_scan(m, DT)
        root_of_unity_dive(m, DT)


if __name__ == "__main__":
    main()
