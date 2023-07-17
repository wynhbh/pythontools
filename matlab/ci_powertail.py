import numpy as np
from scipy.stats import binom
import matplotlib.pyplot as plt

def powerfit(x, y):
    x = x[y != 0]
    y = y[y != 0]
    p = np.polyfit(np.log(x), np.log(y), 1)
    COEFF = np.exp(p[1])
    POWER = p[0]
    return POWER, COEFF

def ci_powertail(data, alpha, tail, clt=True, plotflag=False):
    if len(data.shape) > 1:
        data = data.flatten()

    if len(data) == 0:
        raise ValueError("Input data is empty.")

    if len(data) < 2:
        raise ValueError("Input data must contain at least 2 elements.")

    if tail[0] >= tail[1]:
        raise ValueError("The first element of 'tail' should be smaller than the second element.")

    if plotflag:
        plt.figure()

    if clt:
        plotflag = False  # Skip plotting in intermediate steps for CLT
    else:
        clt = False  # Skip non-CLT section if it's not required

    n = len(data)
    k = np.ceil(tail[0] * n)
    s = np.ceil(tail[1] * n)

    # Compute edf
    y, x = np.histogram(data, bins='auto', density=True)
    y = np.cumsum(y)
    y -= 1 / (2 * n)

    # Fit a power law to the tail of the edf
    power, coeff = powerfit(x[-k:-s], 1 - y[-k:-s])
    powertail = coeff * x[-k:] ** power

    if clt:  # Asymptotic, Gaussian CI
        CI_lo = np.maximum(0, powertail - np.sqrt(powertail * (1 - powertail) / n) * norminv(1 - alpha / 2))
        CI_hi = powertail + np.sqrt(powertail * (1 - powertail) / n) * norminv(1 - alpha / 2)
    else:  # Exact, binomial law based CI
        CI_lo = np.maximum(0, binom.ppf(alpha / 2, n, powertail) / n)
        CI_hi = binom.ppf(1 - alpha / 2, n, powertail) / n

    # Plot the results
    if plotflag:
        plt.loglog(x, 1 - y, '.')
        plt.loglog(x[-k:], powertail, 'r')
        plt.loglog(x[-k:], CI_lo, 'r--')
        plt.loglog(x[-k:], CI_hi, 'r--')
        plt.legend(['Data', f"{coeff:.2f}x^{power:.2f}", f"{(1 - alpha) * 100:.2f}% CI"])
        plt.show()

    return CI_lo, CI_hi