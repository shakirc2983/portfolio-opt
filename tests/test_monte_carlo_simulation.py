import unittest
from unittest.mock import patch
import pandas as pd
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
            mcs_object = MonteCarloSimulation(100, tickers, start_date, end_date)

        self.assertEqual(
            str(context.exception), "Incorrect date format, should be YYYY-MM-DD"
        )

    def test_date_incorrect_range(self):
        start_date = "2023-01-02"
        end_date = "2022-01-02"
        tickers = ["AAPL", "MSFT"]

        with self.assertRaises(TickerDateOutOfRange) as context:
            mcs_object = MonteCarloSimulation(100, tickers, start_date, end_date)

        self.assertEqual(str(context.exception), f"Date given not valid: Portfolio start date {start_date} greater than portfolio end date {end_date}")

    def test_validate_tickers(self):
        start_date = "2024-01-05"
        end_date = "2024-01-09"

        tickers = ["AAPL", "MSFT", "foo"]

        with self.assertRaises(YFTickerMissingError) as context:
            mcs_object = MonteCarloSimulation(100, tickers, start_date, end_date)

        expected_ticker = "foo"
        expected_rationale = "Couldn't find ticker in yfinance"

        self.assertEqual(context.exception.ticker, expected_ticker)
        self.assertEqual(context.exception.rationale, expected_rationale)

    # TODO: // Create test cases for trying to see if the results of get_expected_returns and get_volatility is the right one produced
    #       // Run functions and see if results produced is the same


