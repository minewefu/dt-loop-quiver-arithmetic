"""Independent verification of DT_n(q) via direct enumeration of the
cyclic-word model (Reineke), implemented from the definitions:

  U_n = {a in N^n : sum a_i = (m-1)n},  wt(a) = sum_i (n-i)(m-1-a_i),
  classes = C_n-orbits;  primitive = free orbit;  wt(C) = max over orbit;
  U^{prim,+}: add doubles b.b of primitive b in U_{n/2} iff m even, n=2 mod 4;
  barQ_n = sum_C q^{wt(C)};  DT_n(q) = q^{n-1} barQ_n / [n]_q  (exact division).

Algorithm differs from the CoHA engine entirely: canonical-rotation
enumeration, direct max-weight over orbits.  Compares against the engine data.
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dt_core import DATA_DIR
from scan_refined import load_DT


def gen_compositions(total, parts):
    """Yield tuples of `parts` nonnegative ints summing to `total`."""
    a = [0] * parts
    def rec(i, rem):
        if i == parts - 1:
            a[i] = rem
            yield tuple(a)
            return
        for v in range(rem + 1):
            a[i] = v
            yield from rec(i + 1, rem - v)
    yield from rec(0, total)


def weight(a, m, n):
    return sum((n - i - 1) * (m - 1 - a[i]) for i in range(n))


def barQ(m, n):
    """barQ_n(q) as dict exponent -> count."""
    out = {}
    seen_rot = set()
    N = (m - 1) * n
    for a in gen_compositions(N, n):
        # canonical representative: lexicographically minimal rotation
        rots = [a[k:] + a[:k] for k in range(n)]
        mn = min(rots)
        if a != mn:
            continue
        period = rots.index(mn, 1) if mn in rots[1:] else n
        # period = smallest k >= 1 with rot_k == a; recompute properly:
        period = n
        for k in range(1, n):
            if rots[k] == a:
                period = k
                break
        if period != n:
            continue  # not primitive
        w = max(weight(r, m, n) for r in rots)
        out[w] = out.get(w, 0) + 1
    if m % 2 == 0 and n % 4 == 2:
        # doubles of primitive classes of U_{n/2}
        h = n // 2
        Nh = (m - 1) * h
        for b in gen_compositions(Nh, h):
            rots = [b[k:] + b[:k] for k in range(h)]
            if b != min(rots):
                continue
            if any(rots[k] == b for k in range(1, h)):
                continue
            w = 2 * max(weight(r, m, h) for r in rots)
            out[w] = out.get(w, 0) + 1
    return out


def dt_from_barQ(bq, n):
    """DT_n(q) = q^{n-1} barQ / [n]_q; exact polynomial division."""
    deg = max(bq)
    arr = [0] * (deg + 1)
    for w, c in bq.items():
        arr[w] = c
    # divide by [n]_q = 1 + q + ... + q^{n-1}: synthetic division
    # arr = quot * [n]; quot[i] = arr[i] - sum_{j=1}^{n-1} quot[i-j]
    quot = [0] * (len(arr) - n + 1) if len(arr) >= n else []
    rem = list(arr)
    for i in range(len(arr) - n, -1, -1):
        c = rem[i + n - 1]
        quot[i] = c
        if c:
            for j in range(n):
                rem[i + j] -= c
    assert not any(rem), f"[n]_q does not divide barQ (n={n})"
    # multiply by q^{n-1}
    return [0] * (n - 1) + quot


def main():
    grid = {2: 12, 3: 9, 4: 7, 5: 6, 6: 6}
    results = {}
    allok = True
    for m, D in grid.items():
        DT_engine = load_DT(m)
        res = {}
        for n in range(1, D + 1):
            t0 = time.time()
            bq = barQ(m, n)
            dt = dt_from_barQ(bq, n)
            res[str(n)] = dt
            eng = DT_engine.get(n)
            match = (eng is not None and [int(x) for x in dt] == [int(x) for x in eng])
            if not match:
                allok = False
                print(f"  m={m} n={n}: MISMATCH vs engine!")
                print(f"    word : {dt[:12]}")
                print(f"    engine: {eng[:12] if eng else None}")
            else:
                print(f"  m={m} n={n}: OK ({time.time()-t0:.1f}s, "
                      f"{sum(bq.values())} classes)")
        results[f"m{m}"] = res
    with open(os.path.join(DATA_DIR, "wordmodel_dt.json"), "w") as f:
        json.dump(results, f)
    print(f"ALL MATCH: {allok}")


if __name__ == "__main__":
    main()
