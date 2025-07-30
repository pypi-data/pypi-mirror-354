import numpy as np
import opt_einsum as oe
import os

class RidgeRegression:
    def __init__(self, lambda2=1.0):
        self.b = None
        self.w = None
        self.lamb = lambda2

    def predict(self, x):
        pred = x @ self.w + self.b
        return pred

    def fit(self, x, y):
        x = np.c_[np.ones((x.shape[0], 1)), x]
        i = np.eye(x.shape[1])
        i[0, 0] = 0
        need_inv = x.T @ x + self.lamb * i
        inv = np.linalg.inv(need_inv) if np.linalg.cond(need_inv) < 1e10 else np.linalg.pinv(need_inv)
        params = oe.contract('jk,ik,i->j', inv, x, y)
        
        self.b = params[0]
        self.w = params[1:]
        self.mse = np.mean((y - (x @ self.w + self.b)) ** 2)

    def save(self, filename='ridge.npz'):
        np.savez(filename, b=self.b, w=self.w)
        print("Saved as ", filename)

    def load(self, filename='ridge.npz'):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"{filename} does not exist.")
        params = np.load(filename)
        self.b = params['b']
        self.w = params['w']
        
