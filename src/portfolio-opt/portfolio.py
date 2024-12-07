class Portfolio:
    def __init__(self, weights, size, expected_returns, expected_volatility):
        self.id = id(self)
        self.weights = weights
        self.size = size
        self.sharpe_ratio = None
        self.simulation_no = None
        self.expected_returns = expected_returns
        self.expected_volatility = expected_volatility

    def __str__(self):
        return f"""
        --- Portfolio ---
        Object ID: {self.id}
        {self._print_simulation_no()}
        Weights: {self.weights}
        Size: {self.size}
        {self._print_sharpe_ratio()}
        """

    def _print_sharpe_ratio(self):
        return (
            f"Sharpe Ratio: {self.sharpe_ratio}"
            if hasattr(self, "sharpe_ratio")
            else "Empty"
        )

    def _print_simulation_no(self):
        return (
            f"Simulation Number: {self.simulation_no}"
            if hasattr(self, "simulation_no")
            else "Empty"
        )

    def set_sharpe_ratio(self, sharpe_ratio):
        self.sharpe_ratio = sharpe_ratio

    def set_simulation_no(self, simulation_no):
        self.simulation_no = simulation_no

    def get_sharpe_ratio(self):
        return self.sharpe_ratio
