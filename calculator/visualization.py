import os
import numpy as np
import matplotlib.pyplot as plt
from django.conf import settings

from .price_market import get_historical_prices
from .black_schole import black_scholes_price


def plot_stock_price_history(symbol, period="6mo"):
    prices = get_historical_prices(symbol, period)

    plt.figure()
    plt.plot(prices.index, prices.values)
    plt.title(f"{symbol} Stock Price History")
    plt.xlabel("Date")
    plt.ylabel("Price")

    filename = "price_history.png"
    filepath = os.path.join(settings.MEDIA_ROOT, filename)

    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()

    return filename


def plot_daily_returns(symbol, period="6mo"):
    prices = get_historical_prices(symbol, period)
    returns = prices.pct_change().dropna()

    plt.figure()
    plt.plot(returns.index, returns.values)
    plt.title(f"{symbol} Daily Returns")
    plt.xlabel("Date")
    plt.ylabel("Returns")

    filename = "daily_returns.png"
    filepath = os.path.join(settings.MEDIA_ROOT, filename)

    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()

    return filename


def plot_rolling_volatility(symbol, window=30):
    prices = get_historical_prices(symbol)
    returns = prices.pct_change()

    rolling_vol = returns.rolling(window).std() * (252 ** 0.5)

    plt.figure()
    plt.plot(rolling_vol.index, rolling_vol.values)
    plt.title(f"{symbol} Rolling Volatility ({window} days)")
    plt.xlabel("Date")
    plt.ylabel("Volatility")

    filename = "rolling_volatility.png"
    filepath = os.path.join(settings.MEDIA_ROOT, filename)

    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()

    return filename


def plot_option_price_vs_strike(S, T, r, sigma):
    strikes = np.linspace(0.5 * S, 1.5 * S, 50)

    prices = []
    for K in strikes:
        call_price, _ = black_scholes_price(S, K, T, r, sigma)
        prices.append(call_price)

    plt.figure()
    plt.plot(strikes, prices)
    plt.axvline(S, linestyle="--", alpha=0.7)

    plt.title("Call Option Price vs Strike Price")
    plt.xlabel("Strike Price")
    plt.ylabel("Call Option Price")

    filename = "option_vs_strike.png"
    filepath = os.path.join(settings.MEDIA_ROOT, filename)

    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()

    return filename


def plot_option_price_vs_time(S, K, r, sigma):
    times = np.linspace(0.01, 1, 50)

    prices = []
    for T in times:
        call_price, _ = black_scholes_price(S, K, T, r, sigma)
        prices.append(call_price)

    plt.figure()
    plt.plot(times, prices)
    plt.title("Option Price vs Time to Maturity (Theta Decay)")
    plt.xlabel("Time (Years)")
    plt.ylabel("Option Price")

    filename = "option_vs_time.png"
    filepath = os.path.join(settings.MEDIA_ROOT, filename)

    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()

    return filename
