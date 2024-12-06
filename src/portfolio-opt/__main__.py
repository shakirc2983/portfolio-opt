from MonteCarloSimulation import MonteCarloSimulation


if __name__ == "__main__":
    mcs = MonteCarloSimulation(10, ["APPL", "GOOGL"])
    print(mcs)
    print(mcs.portfolios[0])

    
