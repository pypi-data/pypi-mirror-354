import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# Generate random data
data = np.random.rand(100)
train, test = data[:50], data[50:]
labels = np.array(["Class1" if x <= 0.5 else "Class2" for x in train])

# k-NN function
def knn(x, k):
    distances = np.abs(train - x)  # Compute distances
    sorted_indices = np.argsort(distances)  # Sort indices based on distance
    nearest_labels = labels[sorted_indices[:k]]  # Get k nearest labels
    return Counter(nearest_labels).most_common(1)[0][0]

# Visualization
for k in [1, 3, 5, 20, 30]:
    print(f"\n--- k = {k} ---")
    preds = np.array([knn(x, k) for x in test])

    for i, (x, p) in enumerate(zip(test, preds), 51):
        print(f"x{i} (value: {x:.4f}) -> {p}")

    plt.scatter(train, np.zeros_like(train), c=["blue" if l == "Class1" else "red" for l in labels], label="Train", marker="o", alpha=0.6)
    plt.scatter(test, np.ones_like(test), c=["blue" if p == "Class1" else "red" for p in preds], label="Test", marker="x", alpha=0.6)
    plt.title(f"k-NN Results (k={k})")
    plt.yticks([0, 1], ["Train", "Test"])
    plt.grid(True)
    plt.legend()
    plt.show()