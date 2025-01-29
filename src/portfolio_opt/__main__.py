from portfolio_opt.monte_carlo_simulation import MonteCarloSimulation


if __name__ == "__main__":
    mcs = MonteCarloSimulation(10000, ["AAPL", "MSFT", "foo"], "2024-09-07", "2024-10-07")
    print(mcs)
    portfolios = mcs.get_portfolios()

    print(mcs.overview())
