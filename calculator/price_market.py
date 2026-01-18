import yfinance as yf


def get_historical_prices(symbol, period="1y"):
    """
    Fetch historical adjusted prices for a stock.
    Handles yfinance MultiIndex columns safely.
    """

    data = yf.download(
        symbol,
        period=period,
        auto_adjust=True,
        progress=False
    )

    if data.empty:
        raise ValueError("No data found for the given symbol")


    if isinstance(data.columns, type(data.columns)) and hasattr(data.columns, "levels"):
        prices = data["Close"][symbol]
    else:
        prices = data["Close"]

    return prices


def get_latest_price(symbol):
    """
    Fetch the latest available adjusted close price.
    """

    prices = get_historical_prices(symbol, period="5d")
    return float(prices.iloc[-1])
