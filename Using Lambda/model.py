class LinearRegression:
    def __init__(self):
        self.intercept = 0.0
        self.slope = 0.0

    def fit(self, X, y):
        n = len(X)

        x_mean = sum(X) / n
        y_mean = sum(y) / n

        numerator = sum(
            (x - x_mean) * (target - y_mean)
            for x, target in zip(X, y)
        )

        denominator = sum(
            (x - x_mean) ** 2
            for x in X
        )

        self.slope = numerator / denominator
        self.intercept = y_mean - self.slope * x_mean

    def predict(self, X):
        return [
            self.intercept + self.slope * x
            for x in X
        ]
