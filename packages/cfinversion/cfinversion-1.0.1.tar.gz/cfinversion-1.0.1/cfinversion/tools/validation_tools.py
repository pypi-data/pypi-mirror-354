import numpy as np
import scipy as sp
from typing import Callable
def lre(v_true: np.ndarray, v: np.ndarray) -> np.ndarray:
    """
     Log Relative Error gives an approximation
     for the number of correct digits in predicted value (v).
     If the error is 10^(−𝑘), the logarithm tells the 𝑘.

    :param v_true: true value
    :param v: predicted value
    :return: log relative error
    """
    rel_errors, nlre = np.zeros_like(v_true), np.zeros_like(v_true)
    rel_errors[v_true != 0] = np.abs((v_true[v_true != 0] - v[v_true != 0]) / v_true[v_true != 0])
    nlre[rel_errors != 0] = -np.log10(rel_errors[rel_errors != 0])
    nlre[rel_errors == 0] = np.nan
    return nlre

def l0_err(f: Callable, tol_diff:float = 1e-3) -> float:
    return 1 - sp.integrate.quad(f, -np.inf, np.inf, epsabs = tol_diff)[0]
