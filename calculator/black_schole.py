import math
from typing import Tuple
from scipy.stats import norm


class PricingError(ValueError):
    """Raised when invalid inputs are provided to the pricing model."""
    pass


def black_scholes_price(
    S: float,
    K: float,
    T: float,
    r: float,
    sigma: float
) -> Tuple[float, float]:
    """
    Calculate European Call and Put option prices using the Black–Scholes model.

    Parameters
    ----------
    S : float
        Current stock price
    K : float
        Strike price
    T : float
        Time to maturity (in years)
    r : float
        Risk-free interest rate (annual, decimal)
    sigma : float
        Volatility (annualized, decimal)

    Returns
    -------
    (call_price, put_price) : Tuple[float, float]

    Raises
    ------
    PricingError
        If inputs are invalid
    """

    # ---- Input validation (production-safe) ----
    if S <= 0:
        raise PricingError("Stock price (S) must be positive")
    if K <= 0:
        raise PricingError("Strike price (K) must be positive")
    if T <= 0:
        raise PricingError("Time to maturity (T) must be positive")
    if sigma <= 0:
        raise PricingError("Volatility (sigma) must be positive")
    if r < 0:
        raise PricingError("Risk-free rate (r) cannot be negative")

    # ---- Core Black–Scholes calculations ----
    sqrt_T = math.sqrt(T)

    d1 = (
        math.log(S / K)
        + (r + 0.5 * sigma ** 2) * T
    ) / (sigma * sqrt_T)

    d2 = d1 - sigma * sqrt_T

    call_price = (
        S * norm.cdf(d1)
        - K * math.exp(-r * T) * norm.cdf(d2)
    )

    put_price = (
        K * math.exp(-r * T) * norm.cdf(-d2)
        - S * norm.cdf(-d1)
    )

    return float(call_price), float(put_price)
