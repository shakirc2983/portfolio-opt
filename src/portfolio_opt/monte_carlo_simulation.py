import datetime
import random
import requests
import yfinance as yf
import numpy as np
import pandas as pd
from yfinance import shared
from yfinance.exceptions import YFTickerMissingError
from matplotlib import pyplot as plt

from portfolio_opt.portfolio import Portfolio
from portfolio_opt.exceptions import TickerDateOutOfRange, TickerDownloadError


class MonteCarloSimulation:
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments
    def __init__(self, simulations, tickers, start_date, end_date):

        self.id_ = id(self)
        self.simulations = simulations
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.portfolios = []
        self.object_index = {}
        self.exit_flag = False
        self._initialize_object()

    def __str__(self):
        return f"""
        --- Monte Carlo Simulation ---
        Object ID: {self.id_}
        Simulations: {self.simulations}
        Stocks: {self.tickers}
        Portfolio Size: {len(self.tickers)}
        """

    def __repr__(self):
        return f"MonteCarloSimulation(simulations={self.simulations}, tickers={self.tickers})"

    def __len__(self):
        return self.simulations

    def _validate_date(self, date_text):
        try:
            past = datetime.date.fromisoformat(date_text)
            present = datetime.date.today()
            if past >= present:
                self.exit_flag = True
                raise TickerDateOutOfRange(
                    tickers_error=f"Past: {past} greater than "
                        f"or equal to Present: {present} for {self.tickers}"
                )
            if self.start_date >= self.end_date:
                self.exit_flag = True
                raise TickerDateOutOfRange(
                    tickers_error=f"Portfolio start date {self.start_date} "
                    f"greater than or equal to portfolio end date {self.end_date}"
                )
        except ValueError as e:
            self.exit_flag = True
            raise ValueError("Incorrect date format, should be YYYY-MM-DD") from e

    def _validate_tickers(self, tickers):
        for ticker_text in tickers:
            ticker = yf.Ticker(ticker_text)
            try:
                ticker.info["forwardPE"]
            except requests.exceptions.HTTPError as e:
                print(f"HTTP error: {e.args[0]}")
                self.exit_flag = True
            except KeyError as e:
                print(f"Key error: {e}")
                self.exit_flag = True
                raise YFTickerMissingError(
                    ticker=ticker_text, rationale="Couldn't find ticker in yfinance"
                ) from e

    def _initialize_object(self):
        self._validate_tickers(self.tickers)
        self._validate_date(self.start_date)
        self._validate_date(self.end_date)

        if self.exit_flag:
            return

        self._generate_portfolios()
        self._setup_object_index()

    def _get_historical_returns(self):
        start_date = self.start_date
        end_date = self.end_date
        data = pd.DataFrame()
        try:
            data = yf.download(self.tickers, start=start_date, end=end_date)

            if data is None or data.empty:
                raise ValueError(
                    "No data returned by yfinance. Please check the tickers or date range."
                )

            if "Close" not in data.columns:
                raise KeyError("'Close' column not found in the returned data.")

            # pylint: disable=protected-access
            if shared._ERRORS:
                tickers_error = list(shared._ERRORS.keys())
                raise TickerDownloadError(
                    f"Can't download specific tickers {tickers_error}"
                )
            # pylint: enable=protected-access
            return data["Close"]

        except (ValueError, KeyError, TickerDownloadError) as e:
            print(f"[ERROR]: {e}")
            self.exit_flag = True
            return pd.DataFrame()

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

        if self.exit_flag:
            return

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
                simulation_no,
                weights,
                len(self.tickers),
                expected_returns,
                expected_volatility,
            )
            portfolio.set_sharpe_ratio(sharpe_ratio)
            portfolio.set_simulation_no(simulation_no)
            self.portfolios.append(portfolio)

    def _randomise_weights(self):
        weights = np.array(np.random.random(len(self.tickers)))
        weights = weights / np.sum(weights)
        return weights

    def _setup_object_index(self):
        self.object_index = {
            portfolio.id: index for index, portfolio in enumerate(self.portfolios)
        }

    def get_portfolios(self):
        return self.portfolios

    def get_portfolio(self, id_):
        print(self.object_index)
        index = self.object_index[id_]
        return self.portfolios[index]

    def get_random_portfolio(self):
        return random.choice(self.portfolios)

    def min_volatility(self):
        return min(self.portfolios, key=lambda p: p.expected_volatility)

    def max_volatility(self):
        return max(self.portfolios, key=lambda p: p.expected_volatility)

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
        if self.exit_flag:
            return f"""
        --- Overview ---
        Number of Portfolios: {self.simulations if hasattr(self, 'simulations') else 'NA'}
        Volatility (Min): 0.0
        Volatility (Max): 0.0
        Sharpe Ratio (Max): 0.0
        Sharpe Ratio (Min): 0.0
        """

        return f"""
        --- Overview ---
        Number of Portfolios: {self.simulations}
        Volatility (Min): {self.min_volatility_value()}
        Volatility (Max): {self.max_volatility_value()}
        Sharpe Ratio (Max): {self.max_sharpe_value()}
        Sharpe Ratio (Min): {self.min_sharpe_value()}
        """

    def plot_allocations(self, portfolio):
        tickers = self.tickers
        weights = portfolio.weights
        sizes = np.multiply(weights, 10)

        _, axis = plt.subplots()
        graph = axis.pie(sizes, labels=tickers, autopct="%1.1f%%")
        plt.show()
        return graph

    def plot_mcs(self):
        plt.figure(figsize=(12, 8))
        vol_arr, ret_arr, sharpe_arr = zip(
            *[
                (p.expected_volatility, p.expected_returns, p.sharpe_ratio)
                for p in self.portfolios
            ]
        )
        plt.scatter(vol_arr, ret_arr, c=sharpe_arr)
        plt.colorbar(label="Sharpe Ratio")
        plt.xlabel("Volatility")
        plt.ylabel("Return")

        max_sharpe_port = self.max_sharpe()
        plt.scatter(
            max_sharpe_port.expected_volatility,
            max_sharpe_port.expected_returns,
            c="red",
            s=50,
            edgecolors="black",
        )

        min_volatility_port = self.min_volatility()
        plt.scatter(
            min_volatility_port.expected_volatility,
            min_volatility_port.expected_returns,
            c="lawngreen",
            s=50,
            edgecolors="black",
        )
        plt.show()
