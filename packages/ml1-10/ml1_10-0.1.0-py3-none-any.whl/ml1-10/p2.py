import pandas as pd,numpy as np,seaborn as sns,matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing
df=fetch_california_housing(as_frame=True).frame
sns.heatmap(df.corr(),annot=True,cmap='coolwarm',fmt='.2f')
plt.title("coorelation matrix");plt.show()
sns.pairplot(df)
plt.suptitle("pairplot",y=1.02);plt.show()