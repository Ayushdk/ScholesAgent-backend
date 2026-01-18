import numpy as np

def calculate_annual_volatility(prices,trading_days = 252):
    """
    Calculate the annualized volatility of a stock given its historical prices.
    
    Parameters:
    prices (pd.Series): Series of historical adjusted closing prices.
    trading_days (int): Number of trading days in a year. Default is 252.
    
    Returns:
    float: Annualized volatility as a decimal.
    """
    # calculating daily log return and dropping NaN values:
    # R = ln(Pt / Pt-1)
    log_returns = np.log(prices / prices.shift(1)).dropna()
    
    # calculating standard deviation of daily log returns
    # σ_daily​=std(Rt​)
    daily_volatility = log_returns.std()

    # calculating annualized volatility
    # σ_annual​=σ_daily​ * sqrt(N)   
    annual_volatility = daily_volatility * np.sqrt(trading_days)

    return float(annual_volatility)