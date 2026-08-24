"""Production runs: compute refined DT invariants of m-loop quivers and save
to data/omega_m{m}.json as {d: [[exponent, coeff], ...]} (Omega~_d(z) items,
true exponents, z-convention)."""

import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dt_core import dt_invariants, omega_true, numerical, DATA_DIR

RUNS = {
    2: 50,
    3: 36,
    4: 27,
    5: 22,
    6: 14,
}


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    for m, D in RUNS.items():
        t0 = time.time()
        Om = dt_invariants(m, D, progress=True)
        path = os.path.join(DATA_DIR, f"omega_m{m}.json")
        with open(path, "w") as f:
            json.dump({str(d): [[e, c] for e, c in Om[d]] for d in Om}, f)
        nums = {d: numerical(omega_true(Om[d])) for d in Om}
        print(f"m={m}, D={D}: saved in {time.time()-t0:.1f}s")
        print(f"  numerical c_d: {[nums[d] for d in sorted(nums)][:16]} ...")
    print("done")


if __name__ == "__main__":
    main()
