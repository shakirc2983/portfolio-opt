from portfolio_opt.monte_carlo_simulation import MonteCarloSimulation


if __name__ == "__main__":
    mcs = MonteCarloSimulation(10000, ["AAPL", "MSFT", "AMZN",'foo'])
    print(mcs)
    portfolios = mcs.get_portfolios()

    print(mcs.overview())
