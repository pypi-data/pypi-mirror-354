import numpy as np, matplotlib.pyplot as plt
from sklearn.datasets import fetch_olivetti_faces
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
a, b = fetch_olivetti_faces(return_X_y=True, shuffle=True, random_state=42)
at, av, bt, bv = train_test_split(a, b, test_size=0.3, random_state=42)
clf = GaussianNB().fit(at, bt); bp = clf.predict(av)
print("Accuracy:", round(accuracy_score(bv, bp)*100, 2), "%")
print(classification_report(bv, bp, zero_division=1))
print(confusion_matrix(bv, bp))
print("CV Accuracy:", round(cross_val_score(clf, a, b, cv=5).mean()*100, 2), "%")
fig, ax = plt.subplots(3, 5, figsize=(12, 8))
for i, img, t, p in zip(ax.ravel(), av, bv, bp):
 i.imshow(img.reshape(64, 64), cmap='gray')
 i.set_title(f"T:{t}, P:{p}"); i.axis('off')