"""Stress-test the tower inequalities used in the proof of Theorem A.

a_e := (-1)^{(m-1)(e-1)} binom(me-1, e-1).

(T1) p >= 5:  v_p(a_{pe} - a_e) >= 3 + 3 v_p(e) + v_p(m(m-1))
(T2) p = 3:   v_3(a_{3e} - a_e) >= 2 + 3 v_3(e) + v_3(m(m-1))
(T3) p = 2:   v_2(a_{2e} - a_e) >= 1 + 3 v_2(e) + v_2(m(m-1))

(These follow from Kazandzidis; here we verify them directly.)

Also the derived main statement, from the actual DT formula:
  DT_n = (1/n^2) |sum_{d|n} mu(n/d) (-1)^{(m-1)(n-d)} binom(md-1,d-1)|
  v_p(DT_n) >= v_p(n)            for p >= 5
  v_3(DT_n) >= v_3(n) - [m == 2 mod 3]
  v_2(DT_n) >= v_2(n) - [m in {2,3} mod 4]
for a larger grid than the engine reached: m <= 10, n <= 120.
"""

import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dt_core import moebius, divisors
from mine import vp


def a_seq(m, e):
    return (-1) ** ((m - 1) * (e - 1)) * math.comb(m * e - 1, e - 1)


def check_towers():
    fails = []
    for m in range(2, 11):
        vm = {p: vp(m * (m - 1), p) for p in (2, 3, 5, 7)}
        for p, base in ((5, 3), (7, 3), (3, 2), (2, 1)):
            for e in [1, 2, 3, 4, 5, 6, 8, 9, 12, 16, 18, 25, 27, 32, 49, 50]:
                diff = a_seq(m, p * e) - a_seq(m, e)
                lhs = vp(diff, p)
                need = base + 3 * vp(e, p) + vm[p]
                if lhs is not None and lhs < need:
                    fails.append((m, p, e, lhs, need))
    if fails:
        print("TOWER FAILURES:", fails[:20])
    else:
        print("All tower inequalities (T1),(T2),(T3) verified"
              " (m<=10, p in {2,3,5,7}, e up to 50 incl. high p-valuations)")


def dt_num(m, n):
    s = sum(moebius(n // d) * (-1) ** ((m - 1) * (n - d)) * math.comb(m * d - 1, d - 1)
            for d in divisors(n))
    assert s % (n * n) == 0, (m, n, s)
    return abs(s // (n * n))


def check_main():
    fails = []
    sharp2 = set()
    sharp3 = set()
    for m in range(2, 11):
        e2 = 1 if m % 4 in (2, 3) else 0
        e3 = 1 if m % 3 == 2 else 0
        for n in range(2, 121):
            c = dt_num(m, n)
            for p in (2, 3, 5, 7, 11, 13):
                v = vp(n, p)
                if v == 0:
                    continue
                need = v - (e2 if p == 2 else (e3 if p == 3 else 0))
                got = vp(c, p)
                if got is not None and got < need:
                    fails.append((m, n, p, got, need))
                if p == 2 and e2 and got == v - 1:
                    sharp2.add(m)
                if p == 3 and e3 and got == v - 1:
                    sharp3.add(m)
    if fails:
        print("MAIN THEOREM FAILURES:", fails[:20])
    else:
        print("Main valuation theorem verified for m<=10, n<=120, p<=13")
        print(f"  sharpness attained (defect exactly -1) at p=2 for m in {sorted(sharp2)}")
        print(f"  sharpness attained (defect exactly -1) at p=3 for m in {sorted(sharp3)}")


if __name__ == "__main__":
    check_towers()
    check_main()
