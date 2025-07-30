import numpy as np

class ElasticNet:
    def __init__(self, lambda1=0.1, lambda2=0.1):
        self.lambda1 = lambda1
        self.lambda2 = lambda2
        self.coef_ = None
        self.intercept = None

    def predict(self, x):
        return x @ self.coef_ + self.intercept
    
    def fit(self, x, y, max_iter=1000, tol=1e-10):
        n_samples, n_features = x.shape
        beta = np.zeros(n_features)
        z = beta.copy()
        t = 1.0
        L = (np.linalg.norm(X, ord=2) ** 2) / n_samples + self.lambda2
        step = self.lambda1 / L

        for i in range(max_iter):
            beta_old = beta.copy()
            grad = -(1 / n_samples) * x.T @ (y - x @ z) + self.lambda2 * z
            z_temp = z - grad / L
            beta = np.sign(z_temp) * np.maximum(np.abs(z_temp) - step, 0.0)
            t_new = (1 + np.sqrt(1 + 4 * t ** 2)) / 2
            z = beta + ((t - 1) / t_new) * (beta - beta_old)
            t = t_new
            if np.linalg.norm(beta - beta_old, 2) < tol:
                break
        self.coef_ = beta
        self.intercept = np.mean(y - x @ self.coef_)
        self.mse = 0.5 * np.mean((y - x @ self.coef_ - self.intercept) ** 2)
        l1 = self.lambda1 * np.sum(np.abs(self.coef_))
        l2 = 0.5 * self.lambda2 * np.sum(self.coef_ ** 2)
        self.loss = self.mse + l1 + l2

    def save(self, filename='elastic_net.npz'):
        np.savez(filename, intercept=self.intercept, coef_=self.coef_)
        print("Saved as ", filename)

    def load(self, filename='elastic_net.npz'):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"{filename} does not exist.")
        params = np.load(filename)
        self.intercept = params['intercept']
        self.coef_ = params['coef_']
