import pandas as pd # Elbow Method to Find the Optimal K
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

input_file = 'SourceCode/problem-1/results.csv'
output_file = 'SourceCode/problem-3/Find_the_optimal_k.png'

df = pd.read_csv(input_file)

features = df.select_dtypes(include=[np.number])
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

inertia = []
k = range(1, 11)
for i in k:
    k_means = KMeans(n_clusters=i, n_init=10, random_state=42)
    k_means.fit(scaled_features)
    inertia.append(k_means.inertia_)

plt.plot(k, inertia, 'bo-')
plt.xlabel('Number of clusters')
plt.ylabel('Deviation within the group')
plt.title('Elbow Method to Find the Optimal K')
plt.grid(True, linestyle='--', alpha=0.3)

plt.savefig(output_file, dpi=300, bbox_inches='tight')
plt.show()