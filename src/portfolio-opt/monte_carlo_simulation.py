import numpy as np
import yfinance as yf
from portfolio import Portfolio


class MonteCarloSimulation:
    def __init__(self, simulations, tickers):
        self.id = id(self)
        self.simulations = simulations
        self.tickers = tickers
        self.portfolios = []

        self._initialize_object()

    def __str__(self):
        return f"""
        --- Monte Carlo Simulation ---
        Object ID: {self.id}
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

    def _get_historical_returns(self):
        start_date = "2024-09-07"
        end_date = "2024-10-07"

        data = yf.download(self.tickers, start=start_date, end=end_date)

        price_df = data["Close"]

        return price_df

    def _calculate_expected_return(self, weights, log_return):
        exp_ret = np.sum((log_return.mean() * weights) * 252)
        return exp_ret

    def _calculate_expected_volatility(self, weights, log_return):
        expected_volatility = np.sqrt(
            np.dot(weights.T, np.dot(log_return.cov() * 252, weights))
        )

        return expected_volatility

    def _calculate_sharpe_ratio(self, expected_returns, expected_volatility):
        if expected_volatility == 0:
            return 0
        return expected_returns / expected_volatility

    def _generate_portfolios(self):
        price_df = self._get_historical_returns()
        for simulation_no in range(1, self.simulations + 1):
            weights = self._randomise_weights()
            log_return = np.log(1 + price_df.pct_change())
            expected_returns = self._calculate_expected_return(weights, log_return)
            expected_volatility = self._calculate_expected_volatility(
                weights, log_return
            )
            sharpe_ratio = self._calculate_sharpe_ratio(
                expected_returns, expected_volatility
            )
            portfolio = Portfolio(
                weights, len(self.tickers), expected_returns, expected_volatility
            )
            portfolio.set_sharpe_ratio(sharpe_ratio)
            portfolio.set_simulation_no(simulation_no)
            self.portfolios.append(portfolio)

    def _randomise_weights(self):
        weights = np.array(np.random.random(len(self.tickers)))
        weights = weights / np.sum(weights)
        return weights

    def get_portfolios(self):
        return self.portfolios

    def min_volatility(self):
        return min(self.portfolios, key=lambda p: p.expected_volatility)

    def max_volatility(self):
        return max(
            self.portfolios, key=lambda p: p.expected_volatility
        ).expected_volatility

    def max_sharpe(self):
        return max(self.portfolios, key=lambda p: p.sharpe_ratio)

    def min_sharpe(self):
        return min(self.portfolios, key=lambda p: p.sharpe_ratio)

    def min_volatility_value(self):
        return min(
            self.portfolios, key=lambda p: p.expected_volatility
        ).expected_volatility

    def max_volatility_value(self):
        return max(
            self.portfolios, key=lambda p: p.expected_volatility
        ).expected_volatility

    def max_sharpe_value(self):
        return max(self.portfolios, key=lambda p: p.sharpe_ratio).sharpe_ratio

    def min_sharpe_value(self):
        return min(self.portfolios, key=lambda p: p.sharpe_ratio).sharpe_ratio

    def overview(self):
        return f"""
        --- Overview ---
        Number of Portfolios: {self.simulations}
        Volatility (Min): {self.min_volatility_value()}
        Volatility (Max): {self.max_volatility_value()}
        Sharpe Ratio (Max): {self.max_sharpe_value()}
        Sharpe Ratio (Min): {self.min_sharpe_value()}
        """
