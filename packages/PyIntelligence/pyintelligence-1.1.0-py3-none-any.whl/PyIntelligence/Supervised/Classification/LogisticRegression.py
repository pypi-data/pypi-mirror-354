import numpy as np
import os

class LogisticRegression:
    def __init__(self):
        self.intercept = None
        self.coef_ = None
    
    def predict(self, x, threshold=None):
        z = x @ self.coef_ + self.intercept
        if threshold == None:
            return 1 / (1 + np.exp(-z))
        elif threshold == 0:
            return 1
        elif threshold == 1:
            return 0
        else:
            return z >= -np.log(1 / threshold + 1)
    
    def fit(self, x, y):
        if not np.all(np.isin(y, [0, 1])):
            raise ValueError("Input data is not binary. Logistic regression requires binary target values.")        
        xTx = x.T @ x
        logits = 20 * y - 10
        self.coef_ = np.linalg.solve(xTx, x.T @ logits) if np.linalg.cond(xTx) < 1e10 else np.linalg.pinv(x) @ logits
        self.intercept = np.mean(y - x @ self.coef_)
        self.mse = np.mean((y - x @ self.coef_ - self.intercept) ** 2)

    def save(self, filename='logistic.npz'):
        np.savez(filename, b=self.b, w=self.w)

    def load(self, filename='logistic.npz'):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"{filename} does not exist.")
        params = np.load(filename)
        self.intercept = params['intercept']
        self.coef_ = params['coef_']
