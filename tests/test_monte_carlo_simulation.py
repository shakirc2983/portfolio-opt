import unittest
from unittest.mock import patch
import pandas as pd
from portfolio_opt.monte_carlo_simulation import MonteCarloSimulation
class TestMCS(unittest.TestCase):




    def test_get_args(self):
        tickers = ['AAPL']
        mcs_object = MonteCarloSimulation(5000,tickers)
        # Make a mock object to shut up yfinance.download

        print(mcs_object)
        print(mcs_object.max_sharpe())

    @patch('yfinance.download')  # Mocking yfinance.download
    def test_get_historical_returns(self, mock_download): pass

