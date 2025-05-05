import pandas as pd # KMeans clustering with PCA (2D)
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

input_file = 'SourceCode/problem-1/results.csv'
output_file = 'SourceCode/problem-3/KMeans_clustering.png'

df = pd.read_csv(input_file, encoding='utf-8')
numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns

# Data preprocessing
x = df[numeric_columns]
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)
pca = PCA(n_components=2)
x_pca = pca.fit_transform(x_scaled)

# KMeans clustering
k_means = KMeans(n_clusters=3, random_state=42, n_init=10)
df["Cluster"] = k_means.fit_predict(x_scaled)

# Visualization setup
plt.figure(figsize=(10, 6))
x_min, x_max = x_pca[:, 0].min() - 1, x_pca[:, 0].max() + 1
y_min, y_max = x_pca[:, 1].min() - 1, x_pca[:, 1].max() + 1
xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100), np.linspace(y_min, y_max, 100))

# Predict clusters
z = k_means.predict(pca.inverse_transform(np.c_[xx.ravel(), yy.ravel()]))
z = z.reshape(xx.shape)
plt.contourf(xx, yy, z, alpha=0.2, cmap="viridis")
scatter = plt.scatter(x_pca[:, 0], x_pca[:, 1], c=df["Cluster"], cmap="viridis", s=75)

# Plot cluster centroids
centers = k_means.cluster_centers_
centers_pca = pca.transform(centers)
plt.scatter(centers_pca[:, 0], centers_pca[:, 1], c='red', s=80, marker='o', label="Centroids")

# Add plot labels
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.title("KMeans clustering with PCA (2D)")
plt.grid(True, linestyle='--', alpha=0.3)

# Save and show
plt.savefig(output_file, dpi=300, bbox_inches='tight')
plt.show()