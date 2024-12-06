class Portfolio:
    def __init__(self, weights, size):
        self.weights = weights
        self.size = size

    def __str__(self):
        return f"""
        Weights: {self.weights}
        Size: {self.size}
        """
