class OrdinaryLeastSquares:
    def __init__(self):
        self.b = None
        self.m = None

    def fit(self, X_train, y_train):
        num = 0
        den = 0
        n = X_train.shape[0]
        X_mean = X_train.mean()
        y_mean = y_train.mean()

        for i in range(n):
            num += (X_train[i] - X_mean) * (y_train[i] - y_mean)
            den += (X_train[i] - X_mean) ** 2

        self.m = num / den
        self.b = y_mean - (self.m * X_mean)

    def predict(self, X_test):
        return self.m * X_test + self.b
