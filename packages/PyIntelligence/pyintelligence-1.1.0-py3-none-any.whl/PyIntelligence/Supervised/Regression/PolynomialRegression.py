import numpy as np
from itertools import combinations_with_replacement
import os

class PolynomialRegression:
    def __init__(self):
        self.coef_ = None

    def get_polynomial_features(self, x:np.ndarray, degree):
        n_features = x.shape[1]
        powers = []
        for d in range(degree + 1):
            combos = combinations_with_replacement(range(n_features), d)
            for comb in combos:
                counts = np.bincount(comb, minlength=n_features)
                powers.append(counts)
        powers = np.array(powers)
        exp = x[:, :, None] ** powers.T[None, :, :]
        poly = np.prod(exp, axis=1)
        return poly

    def predict(self, x):
        x = self.get_polynomial_features(x, self.degree)
        pred = x @ self.coef_
        return pred

    def fit(self, x, y, degree=1):
        self.degree = degree
        x = self.get_polynomial_features(x, self.degree)
        xTx = x.T @ x
        self.coef_ = np.linalg.solve(xTx, x.T @ y) if np.linalg.cond(xTx) < 1e10 else np.linalg.pinv(x) @ y

    def save(self, filename='polynomial.npz'):
        np.savez(filename, self.coef_)

    def load(self, filename='polynomial.npz'):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"{filename} does not exist.")
        self.coef_ = np.load(filename)


