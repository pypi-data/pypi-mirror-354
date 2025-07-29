from sklearn.datasets import load_breast_cancer as load
from sklearn.model_selection import train_test_split as split
from sklearn.tree import DecisionTreeClassifier as DT, plot_tree
from sklearn.metrics import accuracy_score as acc
import matplotlib.pyplot as plt
X, y = load(return_X_y=True)
Xtr, Xte, ytr, yte = split(X, y, test_size=0.2, random_state=42)
clf = DT(random_state=42).fit(Xtr, ytr)
print(f"Accuracy: {acc(yte, clf.predict(Xte)) * 100:.2f}%")
print(f"Predicted: {['Malignant','Benign'][clf.predict([Xte[0]])[0]]}")
plt.figure(figsize=(12,8))
plot_tree(clf, filled=True, feature_names=load().feature_names, class_names=load().target_names)
plt.title("Decision Tree - Breast Cancer")
plt.show()