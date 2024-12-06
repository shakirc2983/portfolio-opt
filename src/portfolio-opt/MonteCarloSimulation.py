class MonteCarloSimulation:
    def __init__(self, simulations, tickers):
        self.simulations = simulations
        self.tickers = tickers
        self.portfolio_size = len(tickers)
        self.id = id(self)

    def __str__(self):
        return f"""
        Monte Carlo Simulation: {self.id}
        Simulations: {self.simulations}
        Stocks: {self.tickers}
        Portfolio Size: {self.portfolio_size}
        """

    def _randomise_weights(self):
        pass

    # Randomise weights for self.portfolio_size

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
