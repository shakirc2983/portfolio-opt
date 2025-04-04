from portfolio_opt.monte_carlo_simulation import MonteCarloSimulation


if __name__ == "__main__":
    mcs = MonteCarloSimulation(10000, ["AAPL", "MSFT"], "2019-05-02", "2022-05-07")
    print(mcs)

    print(mcs._get_historical_returns())
    portfolios = mcs.get_portfolios()

    print(mcs.overview())
