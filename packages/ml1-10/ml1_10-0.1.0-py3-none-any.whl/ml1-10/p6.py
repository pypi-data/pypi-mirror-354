import numpy as np, matplotlib.pyplot as plt
def lwr(x, X, y, tau):
 W = np.exp(-np.sum((X - x)**2, axis=1) / (2 * tau**2))
 W = np.diag(W)
 return x @ np.linalg.pinv(X.T @ W @ X) @ X.T @ W @ y
np.random.seed(42)
X = np.linspace(0, 2*np.pi, 100)
y = np.sin(X) + 0.1*np.random.randn(100)
Xb = np.c_[np.ones_like(X), X]
Xt = np.linspace(0, 2*np.pi, 200)
Xtb = np.c_[np.ones_like(Xt), Xt]
tau = 0.5
yp = np.array([lwr(xi, Xb, y, tau) for xi in Xtb])
plt.scatter(X, y, c='r', label='Training Data', alpha=0.7)
plt.plot(Xt, yp, c='b', label=f'LWR Fit (tau={tau})')
plt.title('Locally Weighted Regression'), plt.xlabel('X'), plt.ylabel('y')
plt.legend(), plt.grid(alpha=0.3)
plt.show() 