import numpy as np
from portfolio import Portfolio


class MonteCarloSimulation:
    def __init__(self, simulations, tickers):
        self.simulations = simulations
        self.tickers = tickers
        self.portfolios = []
        self.id = id(self)

        self._initialize_object()

    def __str__(self):
        return f"""
        Monte Carlo Simulation: {self.id}
        Simulations: {self.simulations}
        Stocks: {self.tickers}
        Portfolio Size: {len(self.tickers)}
        """

    def __repr__(self):
        return f"MonteCarloSimulation(simulations={self.simulations}, tickers={self.tickers})"

    def __len__(self):
        return self.simulations

    def _initialize_object(self):

        self._generate_portfolios()

    def _generate_portfolios(self):
        for simulation_no in range(self.simulations):
            print(f"Simulation: {simulation_no}")
            print("Generating Portfolio")
            weights = self._randomise_weights()
            portfolio = Portfolio(weights, len(self.tickers))
            self.portfolios.append(portfolio)

    def _randomise_weights(self):
        weights = np.array(np.random.random(len(self.tickers)))
        weights = weights / np.sum(weights)
        return weights

    def get_portfolios(self):
        return self.portfolios

    def set_returns(self):
        pass

    # Pull from yfinance
    # Get returns data for self.tickers
    # Pandas DataFrame

    def calculate_sharpe_ratios(self):
        pass

    def min_volatility(self):
        pass

    def max_volatility(self):
        pass

    def max_sharpe(self):
        pass

    def min_sharpe(self):
        pass

    def run(self):
        pass
