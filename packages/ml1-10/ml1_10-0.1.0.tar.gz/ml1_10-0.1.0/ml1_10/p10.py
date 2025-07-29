import numpy as np, pandas as pd, matplotlib.pyplot as plt, seaborn as sns
from sklearn.datasets import load_breast_cancer
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import confusion_matrix, classification_report
d = load_breast_cancer()
X = StandardScaler().fit_transform(d.data)
y = d.target
k = KMeans(n_clusters=2, random_state=42).fit(X)
p = k.predict(X)
print("Confusion Matrix:\n", confusion_matrix(y, p))
print("\nClassification Report:\n", classification_report(y, p))
pca = PCA(2)
Xp = pca.fit_transform(X)
cent = pca.transform(k.cluster_centers_)
df = pd.DataFrame(Xp, columns=['PC1', 'PC2']); df['C'], df['T'] = p, y
def plot(h, title, pal, center=False):
 sns.scatterplot(data=df, x='PC1', y='PC2', hue=h, palette=pal, s=60, edgecolor='k')
 if center: plt.scatter(*cent.T, c='r', s=150, marker='X', label='Centroids')
 plt.title(title); plt.xlabel('PC1'); plt.ylabel('PC2'); plt.legend(); plt.show()
plot('C', 'K-Means Clustering', 'Set1')
plot('T', 'True Labels', 'coolwarm')
plot('C', 'K-Means with Centroids', 'Set1', center=True)