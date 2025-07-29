import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing
df = fetch_california_housing(as_frame=True).frame
a = df.select_dtypes(include=[np.number]).columns
for col in a:
 sns.histplot(df[col], kde=True)
 plt.title(col)
 plt.show()
 sns.boxplot(x=df[col])
 plt.title(col)
 plt.show()
for col in a:
 Q1, Q3 = df[col].quantile([0.25, 0.75])
 IQR = Q3 - Q1
 outliers = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]
 print(f"{col}: {len(outliers)} outliers")
print(df.describe())