import numpy as np
import polars as pl
from scipy.integrate import solve_ivp

from .case import TransientCase


def rhs_transient(t, p, lamT, muT, ls_max):
    """
    RHS of the CKEs
    rhs_transient(t,p,coef) implements the right hand sides of the CKE at time t and state vector p[]
    """
    i = 0
    pdot = np.zeros(ls_max + 1)

    cT = 1

    pdot[0] = muT * p[1] - lamT * p[0]
    for i in range(1, cT):
        pdot[i] = (
            (i + 1) * muT * p[i + 1]
            + lamT * p[i - 1]
            - (i * muT + lamT) * p[i]
        )
    for i in range(cT, ls_max):
        pdot[i] = (
            cT * muT * p[i + 1] + lamT * p[i - 1] - (cT * muT + lamT) * p[i]
        )
    pdot[ls_max] = lamT * p[ls_max - 1] - cT * muT * p[ls_max]

    return pdot


def solve_transient(case_config: TransientCase) -> pl.DataFrame:
    ls_max = case_config.ls_max
    time_step = case_config.time_step

    rows = []

    pT = np.zeros(ls_max + 1)
    pT[case_config.L_0] = 1
    t = 0.0
    while True:
        last_pT = pT.copy()
        if t > 0:
            solver = solve_ivp(
                fun=rhs_transient,
                args=(
                    case_config.λ,
                    case_config.μ,
                    ls_max,
                ),
                method="RK45",
                y0=pT,
                t_span=[t, t + time_step],
                rtol=1e-8,
            )

            pT = solver.y[:, -1]
            if np.sum(pT) != 1:
                pT = pT / np.sum(pT)

        new_rows = [
            dict(t=t, l_s=l_s, p=p)
            for l_s, p in zip(np.arange(0, ls_max + 1), pT)
        ]
        rows.extend(new_rows)
        if np.allclose(last_pT, pT, atol=1e-8) and t > 100:
            break
        t += time_step
    return pl.DataFrame(rows)
