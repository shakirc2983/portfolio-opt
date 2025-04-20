from portfolio_opt.monte_carlo_simulation import MonteCarloSimulation


if __name__ == "__main__":
    mcs = MonteCarloSimulation(10000, ["AAPL", "MSFT"], "2020-01-04", "2022-01-08")
    print(mcs)


    portfolio = mcs.max_sharpe()

    mcs.plot_allocations(portfolio)

    print(portfolio)
