# %%

import sys
import os

# Add the project root directory to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from common import *

from sklearn.cluster import KMeans,DBSCAN,kmeans_plusplus
import fastdtw
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster



#rul_FD001_training = rul_FD001_training.drop(columns='1')
print(rul_FD001_training.columns)
# Assuming '1.1' is the time column
time_column = '1.1'
features = rul_FD001_training.columns.tolist()
features.remove(time_column)

# Standard scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(rul_FD001_training[features])
X_scaled_df = pd.DataFrame(X_scaled, columns=features)

def calculate_dtw_matrix(data):
    num_series = data.shape[1]
    dtw_matrix = np.zeros((num_series, num_series))

    for i in range(num_series):
        for j in range(i + 1, num_series):
            distance, _ = fastdtw(data.iloc[:, i], data.iloc[:, j])
            dtw_matrix[i, j] = distance
            dtw_matrix[j, i] = distance
    
    return dtw_matrix

dtw_matrix = calculate_dtw_matrix(X_scaled_df)
dtw_matrix_condensed = squareform(dtw_matrix)

linkage_matrix = linkage(dtw_matrix_condensed, method='complete')

# Cluster the time series into 2 clusters
num_clusters = 2
clusters = fcluster(linkage_matrix, num_clusters, criterion='maxclust')

# Print cluster assignments
for i, cluster in enumerate(clusters):
    print(f"Time series {X_scaled_df.columns[i]} is in cluster {cluster}")

# Plot the time series with cluster colors
colors = ['r', 'g', 'b', 'c', 'm']
plt.figure(figsize=(10, 6))

for i, col in enumerate(X_scaled_df.columns):
    plt.plot(rul_FD001_training[time_column], rul_FD001_training[col], color=colors[clusters[i] - 1], label=f'{col} (Cluster {clusters[i]})')

plt.title('Time Series Clustering with DTW')
plt.xlabel('Time')
plt.ylabel('Value')
plt.legend()
plt.show()

'''
def kmeans_cluster_explore(data: pd.DataFrame,clusters: int):

    inertias = []
    
    for i in range(1,clusters):
        kmeans = kmeans_plusplus(data, n_clusters=i, random_state=42)
        inertias.append(kmeans.inertia_)
#dbscan = DBSCAN(eps=2.0, min_samples=5).fit(X)
#rul_FD001_training['db_scan_cluster'] = dbscan.labels_

#predictions = dbscan.labels_
#print(np.unique(predictions))
# Plot the clusters
subset_features = ['1.1','9050.17','8125.55','47.20','521.72']  # Select any subset of features
'''

'''
#sns.pairplot(rul_FD001_training, vars=subset_features, hue='db_scan_cluster', palette='viridis')
#plt.show()


inertias = []

for i in range(1, 21):
    kmeans = KMeans(n_clusters=i, random_state=42)
    kmeans.fit(X)
    inertias.append(kmeans.inertia_)

print(inertias)

def plotstuff(list_of_inertias):
    plt.plot(list(range(1, 21)), list_of_inertias, '--o')
    plt.xticks(list(range(1, 21)), list(range(1, 21)))
    plt.title('Inertia Score by n cluster centers')
    plt.show()

plotstuff(inertias)

# Calculate percentage differential
percent_diff = [0] + [100 * (inertias[i - 1] - inertias[i]) / inertias[i - 1] for i in range(1, len(inertias))]

# Plot inertia and percentage differential
fig, ax1 = plt.subplots()

color = 'tab:blue'
ax1.set_xlabel('Number of clusters (k)')
ax1.set_ylabel('Inertia', color=color)
ax1.plot(range(1, 21), inertias, 'o-', color=color, label='Inertia')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Percent Differential', color=color)
ax2.plot(range(1, 21), percent_diff, 's--', color=color, label='Percent Differential')
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
plt.title('Inertia and Percent Differential by Number of Clusters')
plt.show()


kmeans = KMeans(n_clusters=8, n_init=100, max_iter=300, random_state=42)
kmeans.fit(X)

# Add cluster labels to the DataFrame
rul_FD001_training['kmeans_cluster'] = kmeans.labels_

# Create a 3D scatter plot using Plotly
fig = px.scatter_3d(rul_FD001_training, 
                    x='1.1', 
                    y='9050.17', 
                    z='8125.55', 
                    color='kmeans_cluster',
                    title='K-Means Clustering with k=8 (3D Plot)',
                    labels={'1.1': 'Feature 1.1', '9050.17': 'Feature 9050.17', '8125.55': 'Feature 8125.55'},
                    opacity=0.7)

# Show the plot
fig.show()
'''