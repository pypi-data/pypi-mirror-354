import numpy as np, pandas as pd, matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
iris = load_iris()
data, labels = iris.data, iris.target
pca = PCA(n_components=2).fit_transform(data)
df = pd.DataFrame(pca, columns=['PC1', 'PC2'])
df['Label'] = labels
colors = ['r', 'g', 'b']
for i, color in zip(np.unique(labels), colors):
 plt.scatter(df[df.Label==i]['PC1'], df[df.Label==i]['PC2'], color=color,
label=iris.target_names[i])
plt.title('PCA - Iris'); plt.xlabel('PC1'); plt.ylabel('PC2')
plt.legend(); plt.grid(); plt.show()