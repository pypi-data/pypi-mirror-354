import numpy as np
import os

class LassoRegression:
    def __init__(self, lambda1=0.1):
        self.intercept = None
        self.coef_ = None
        self.lamb = lambda1

    def predict(self, x):
        pred = x @ self.coef_ + self.intercept
        return pred

    def instant_fit(self, x, y):
        batch_size, num_samples = x.shape
        xTx = x.T @ x 
        inv = np.linalg.inv(xTx) if np.linalg.cond(xTx) < 1e10 else np.linalg.pinv(xTx)
        xTy = x.T @ y
        ols = inv @ xTy
        l1 = self.lamb * num_samples * inv @ np.ones(num_samples)
        soft_coef_ = np.sign(ols) * np.maximum(np.abs(ols) - l1, 0)
        #soft_coef_ = np.sign(xTy) * np.maximum(np.abs(xTy) - self.lamb * num_samples, 0)
        #soft_coef_ = inv @ soft_coef_
        '''
        grad = xTy - xTx @ soft_coef_
        grad /= num_samples * self.lamb
        grad = grad * (soft_coef_ == 0.0) + np.sign(soft_coef_) * (soft_coef_ != 0.0)
        self.coef_ = ols - self.lamb * num_samples * inv @ grad
        '''
        self.coef_ = soft_coef_       
        self.intercept = np.mean(y - x @ self.coef_) 
        self.mse = 0.5 * np.mean((y - x @ self.coef_ - self.intercept) ** 2)
        self.loss = self.mse + self.lamb * np.sum(np.abs(self.coef_))
        
    def fit(self, x, y, max_iter=1000, tol=1e-6):
        n_samples, n_features = x.shape
        beta = np.zeros(n_features)
        z = beta.copy()
        t = 1
        L = np.linalg.norm(X, ord=2) ** 2 / n_samples
        step = self.lamb / L
        for i in range(max_iter):
            beta_old = beta.copy()
            grad = -(1 / n_samples) * x.T @ (y - x @ z)
            z_temp = z - grad / L
            beta = np.sign(z_temp) * np.maximum(np.abs(z_temp) - step, 0)
            t_new = (1 + np.sqrt(1 + 4 * t ** 2)) / 2
            z = beta + (t - 1) * (beta - beta_old) / t_new
            t = t_new
            if np.linalg.norm(beta - beta_old) < tol:
                break
        beta[beta == 0] = 0.0
        self.coef_ = beta
        self.intercept = np.mean(y - x @ self.coef_) 
        self.mse = 0.5 * np.mean((y - x @ self.coef_ - self.intercept) ** 2)
        self.loss = self.mse + self.lamb * np.sum(np.abs(self.coef_))
        
    def save(self, filename='lasso.npz'):
        np.savez(filename, intercept=self.intercept, coef_=self.coef_)
        print("Saved as ", filename)

    def load(self, filename='lasso.npz'):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"{filename} does not exist.")
        params = np.load(filename)
        self.intercept = params['intercept']
        self.coef_ = params['coef_']
