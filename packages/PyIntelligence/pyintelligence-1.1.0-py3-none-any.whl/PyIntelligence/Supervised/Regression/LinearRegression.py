import numpy as np
import os
import time

class LinearRegression:
    def __init__(self):
        self.b = None
        self.w = None

    def predict(self, x):
        return x @ self.w + self.b

    def fit(self, x, y):   
        xTx = x.T @ x
        self.w = np.linalg.solve(xTx, x.T @ y) if np.linalg.cond(xTx) < 1e10 else np.linalg.pinv(x) @ y       
        self.b = np.mean(y - x @ self.w)
        self.mse = np.mean((y - x @ self.w - self.b) ** 2)        
        
    def save(self, filename='linear.npz'):
        np.savez(filename, b=self.b, w=self.w)
        print("Saved as ", filename)

    def load(self, filename='linear.npz'):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"{filename} does not exist.")
        params = np.load(filename)
        self.b = params['b']
        self.w = params['w']
