from portfolio_opt.monte_carlo_simulation import MonteCarloSimulation


if __name__ == "__main__":
    mcs = MonteCarloSimulation(1000, ["AAPL", "CSCO","IBM", "AMZN"], "2020-01-04", "2022-01-08")
    print(mcs)


    portfolio = mcs.max_sharpe()

    mcs.plot_mcs()
    mcs.plot_allocations(portfolio)

    print(portfolio)
