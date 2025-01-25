class TickerDownloadError(Exception):
    """Exception raised when there's an error downloading tickers."""
    def __init__(self, tickers_error):
        super().__init__(f"Can't download specific tickers: {tickers_error}")
        self.tickers_error = tickers_error
