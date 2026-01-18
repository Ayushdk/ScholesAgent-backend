import numpy as np
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..price_market import get_latest_price, get_historical_prices
from ..volatility import calculate_annual_volatility as calculate_volatility
from ..black_schole import black_scholes_price


# ==================================================
# SYMBOLS API
# ==================================================
@api_view(["GET"])
def symbols_api(request):
    return Response([
        {"symbol": "AAPL", "name": "Apple"},
        {"symbol": "MSFT", "name": "Microsoft"},
        {"symbol": "GOOGL", "name": "Google"},
        {"symbol": "AMZN", "name": "Amazon"},
        {"symbol": "TSLA", "name": "Tesla"},
        {"symbol": "NVDA", "name": "NVIDIA"},
        {"symbol": "META", "name": "Meta"},
    ])


# ==================================================
# OPTION CALCULATOR API
# ==================================================
@api_view(["POST"])
def calculate_option_api(request):
    try:
        symbol = request.data["symbol"]
        strike = float(request.data["strike"])
        maturity = float(request.data["maturity"])
        rate = float(request.data["rate"]) / 100

        S = get_latest_price(symbol)
        prices = get_historical_prices(symbol)

        sigma = calculate_volatility(prices)

        call, put = black_scholes_price(S, strike, maturity, rate, sigma)

        return Response({
            "symbol": symbol,
            "stock_price": round(S, 2),
            "volatility": round(sigma, 4),
            "call_price": round(max(call, 0), 2),
            "put_price": round(max(put, 0), 2),
        })

    except Exception as e:
        return Response({"error": str(e)}, status=400)


# ==================================================
# GRAPH DATA API
# ==================================================
@api_view(["POST"])
def graph_data_api(request):
    try:
        symbol = request.data["symbol"]
        strike = float(request.data["strike"])
        maturity = float(request.data["maturity"])
        rate = float(request.data["rate"]) / 100

        # ---------- Market Data ----------
        S = get_latest_price(symbol)
        prices = get_historical_prices(symbol).dropna()

        sigma = calculate_volatility(prices)

        # ---------- Price History ----------
        price_dates = prices.index.strftime("%Y-%m-%d").tolist()
        price_values = prices.values.tolist()

        # ---------- Daily Returns ----------
        returns = prices.pct_change().dropna()

        return_dates = returns.index.strftime("%Y-%m-%d").tolist()
        return_values = returns.values.tolist()

        # ---------- Rolling Volatility ----------
        rolling_vol = returns.rolling(30).std() * np.sqrt(252)
        rolling_vol = rolling_vol.replace([np.inf, -np.inf], np.nan).dropna()

        vol_dates = rolling_vol.index.strftime("%Y-%m-%d").tolist()
        vol_values = rolling_vol.values.tolist()

        # ==================================================
        # OPTION PRICE vs STRIKE (ITM / ATM / OTM)
        # ==================================================
        strike_curve = []

        min_strike = int(S * 0.7)
        max_strike = int(S * 1.3)

        for K in range(min_strike, max_strike + 1, 5):
            call, put = black_scholes_price(S, K, maturity, rate, sigma)

            strike_curve.append({
                "strike": K,
                "call": round(max(call, 0), 3),
                "put": round(max(put, 0), 3),
            })

        # ==================================================
        # OPTION PRICE vs TIME (THETA DECAY)
        # ==================================================
        time_curve = []
        atm_strike = S  # important for interpretation

        for months in range(1, 25):
            T = months / 12

            call, put = black_scholes_price(S, atm_strike, T, rate, sigma)

            time_curve.append({
                "months": months,
                "call": round(max(call, 0), 3),
                "put": round(max(put, 0), 3),
            })

        # ==================================================
        # FINAL RESPONSE
        # ==================================================
        return Response({
            "price_history": {
                "dates": price_dates,
                "values": price_values
            },
            "daily_returns": {
                "dates": return_dates,
                "values": return_values
            },
            "rolling_volatility": {
                "dates": vol_dates,
                "values": vol_values
            },
            "strike_curve": strike_curve,
            "time_curve": time_curve,
            "meta": {
                "spot_price": round(S, 2),
                "volatility": round(sigma, 4)
            }
        })

    except Exception as e:
        return Response({"error": str(e)}, status=400)


# ==================================================
# ABOUT API
# ==================================================
@api_view(["GET"])
def about_api(request):
    return Response({
        "model": "Black–Scholes Option Pricing Model",
        "formula": "C = S N(d1) − K e^{−rT} N(d2)",
        "variables": {
            "S": "Current stock price",
            "K": "Strike price",
            "T": "Time to maturity",
            "r": "Risk-free interest rate",
            "σ": "Volatility"
        },
        "assumptions": [
            "European options",
            "No dividends",
            "Constant volatility",
            "Efficient markets",
            "No arbitrage"
        ]
    })
