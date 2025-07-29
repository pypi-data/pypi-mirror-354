import pandas as pd, matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing as fch
from sklearn.model_selection import train_test_split as split
from sklearn.linear_model import LinearRegression as LR
from sklearn.pipeline import make_pipeline as pipe
from sklearn.preprocessing import PolynomialFeatures as PF, StandardScaler as SS
from sklearn.metrics import mean_squared_error as mse, r2_score as r2
def plot_score(Xt, yt, yp, xlbl, ylbl, title):
 plt.scatter(Xt, yt, c='b', label='Actual')
 plt.plot(Xt, yp, 'r.' if yp.ndim == 1 else 'ro', label='Predicted')
 plt.xlabel(xlbl); plt.ylabel(ylbl); plt.title(title)
 plt.legend(); plt.show()
 print(f"{title}\nMSE: {mse(yt, yp):.4f}\nR2: {r2(yt, yp):.4f}\n")
def linear():
 X, y = fch(as_frame=True, return_X_y=True)
 Xt, Xv, yt, yv = split(X[["AveRooms"]], y, test_size=0.2, random_state=42)
 yp = LR().fit(Xt, yt).predict(Xv)
 plot_score(Xv, yv, yp, "AveRooms", "Value ($100k)", "Linear - California")
def poly():
 url = "https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data"
 cols = ["mpg","cyl","disp","hp","wt","acc","yr","origin"]
 df = pd.read_csv(url, sep=r'\s+', names=cols, na_values="?").dropna()
 Xt, Xv, yt, yv = split(df[["disp"]], df["mpg"], test_size=0.2, random_state=42)
 yp = pipe(PF(2), SS(), LR()).fit(Xt, yt).predict(Xv)
 plot_score(Xv, yv, yp, "Displacement", "MPG", "Poly - Auto MPG")
linear(); poly()