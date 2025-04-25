import unittest
import yfinance as yf
from yfinance.exceptions import YFTickerMissingError
from portfolio_opt.monte_carlo_simulation import MonteCarloSimulation
from portfolio_opt.exceptions import TickerDateOutOfRange
import numpy as np


class TestMCS(unittest.TestCase):

    def test_validate_date(self):
        start_date = "2023-12-07"
        end_date = "2024-01"
        tickers = ["AAPL", "MSFT"]
        with self.assertRaises(ValueError) as context:
            MonteCarloSimulation(100, tickers, start_date, end_date)

        self.assertEqual(
            str(context.exception), "Incorrect date format, should be YYYY-MM-DD"
        )

    def test_date_incorrect_range(self):
        start_date = "2023-01-02"
        end_date = "2022-01-02"
        tickers = ["AAPL", "MSFT"]

        with self.assertRaises(TickerDateOutOfRange) as context:
            MonteCarloSimulation(100, tickers, start_date, end_date)

        self.assertEqual(
            str(context.exception),
            f"Date given not valid: Portfolio start date {start_date} "
            f"greater than portfolio end date {end_date}",
        )

    def test_validate_tickers(self):
        start_date = "2024-01-05"
        end_date = "2024-01-09"

        tickers = ["AAPL", "MSFT", "foo"]

        with self.assertRaises(YFTickerMissingError) as context:
            MonteCarloSimulation(100, tickers, start_date, end_date)

        expected_ticker = "foo"
        expected_rationale = "Couldn't find ticker in yfinance"

        self.assertEqual(context.exception.ticker, expected_ticker)
        self.assertEqual(context.exception.rationale, expected_rationale)

    def test_returns_and_volatility(self):

        start_date = "2022-01-04"
        end_date = "2022-01-08"

        tickers = ["AAPL", "MSFT"]
        data = yf.download(tickers=tickers, start=start_date, end=end_date)

        if data is None or data.empty or "Close" not in data:
            raise ValueError("Failed to fetch valid data from Yahoo Finance.")

        close_data = data["Close"]
        mcs_object = MonteCarloSimulation(100, tickers, start_date, end_date)
        portfolio = mcs_object.get_random_portfolio()

        log_return = np.log(close_data / close_data.shift(1)).dropna()
        weights = np.array([0.5, 0.5])

        # Manual Implementation
        # mean_returns = log_return.mean()
        # expected_return = np.dot(log_return.mean(), weights) * 252
        # cov_matrix = log_return.cov() * 252
        # expected_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

        expected_return = mcs_object._calculate_expected_return(weights, log_return)
        expected_volatility = mcs_object._calculate_expected_volatility(
            weights, log_return
        )

        constant_expected_return = -3.7537
        constant_expected_volatility = 0.2705

        tolerance = 0.0001

        assert (
            abs(expected_return - constant_expected_return) < tolerance
        ), f"Expected return is incorrect: {expected_return:.4f} != {constant_expected_return:.4f}"
        assert (
            abs(expected_volatility - constant_expected_volatility) < tolerance
        ), f"Expected volatility is incorrect: {expected_volatility:.4f} != {constant_expected_volatility:.4f}"
        assert isinstance(expected_return, float), "Expected return should be a float"

        assert isinstance(
            expected_volatility, float
        ), "Expected volatility should be a float"
        assert expected_volatility >= 0, "Volatility should not be negative"
        print(f"Expected Return: {expected_return:.4f}")
        print(f"Expected Volatility: {expected_volatility:.4f}")
