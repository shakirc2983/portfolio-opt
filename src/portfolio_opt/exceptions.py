class TickerDownloadError(Exception):
    """Exception raised when there's an error downloading tickers."""

    def __init__(self, tickers_error):
        super().__init__(f"Can't download specific tickers: {tickers_error}")
        self.tickers_error = tickers_error


class TickerDateOutOfRange(Exception):
    """Exception raised when the date is out of range, ie. asking for a stock date in the future"""

    def __init__(self, tickers_error):
        super().__init__(f"Date given not valid: {tickers_error}")
        self.rationale = "Date given not valid"
        self.tickers_error = tickers_error
