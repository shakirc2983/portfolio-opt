from monte_carlo_simulation import MonteCarloSimulation


if __name__ == "__main__":
    mcs = MonteCarloSimulation(10000, ["AAPL", "MSFT", "SQ", "AMZN"])
    print(mcs)
    portfolios = mcs.get_portfolios()

    print(mcs.overview())
