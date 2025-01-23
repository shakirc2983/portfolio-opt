from portfolio_opt.monte_carlo_simulation import MonteCarloSimulation


if __name__ == "__main__":
    ## TODO: When using 'SQ' stock, got error ['SQ'] OperationalError('database is locked')
    ##       Look into error handling in yfinance.

    mcs = MonteCarloSimulation(10000, ["AAPL", "MSFT", "AMZN"])
    print(mcs)
    portfolios = mcs.get_portfolios()

    print(mcs.overview())
