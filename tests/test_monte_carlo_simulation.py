import unittest
from unittest.mock import patch
import pandas as pd
from yfinance.exceptions import YFTickerMissingError
from portfolio_opt.monte_carlo_simulation import MonteCarloSimulation
class TestMCS(unittest.TestCase):
    
    def test_validate_date(self):
        start_date = "2024-01-07"
        end_date = "2024-01"
        tickers = ['AAPL','MSFT']
        with self.assertRaises(ValueError) as context:
            mcs_object = MonteCarloSimulation(100,tickers,start_date, end_date)
        
        self.assertEqual(str(context.exception), "Incorrect date format, should be YYYY-MM-DD")
    def test_validate_tickers(self):
        ## TODO: Need to fix this.
        start_date = "2024-01-05"
        end_date = "2024-01-09"

        tickers = ['AAPL', 'MSFT', 'foo']

        with self.assertRaises(YFTickerMissingError) as context:
            mcs_object = MonteCarloSimulation(100,tickers,start_date,end_date)

        self.assertEqual(str(context.exception), "Couldn't find ticker in yfinance")
    #def test_get_args(self):
    #   tickers = ['AAPL']
    #    mcs_object = MonteCarloSimulation(5000,tickers)
        # Make a mock object to shut up yfinance.download

     #   print(mcs_object)
    #def test_get_historical_returns(self, mock_download):
    #    tickers = ['AAPL']
        
