import pandas as pd

# Replace 'your_binary_file.csv' with the actual path to your binary file
data = pd.read_csv('Umfrage_Ergebnis.csv')

binary_data = data.values.tolist()

import numpy as np
from kmodes.kmodes import KModes

# Assuming binary_data is your list of lists
binary_data = np.array(binary_data)

# Define the number of clusters
n_clusters = 3

# Create the K-Modes model
km = KModes(n_clusters=n_clusters, init='Huang', n_init=5, verbose=1)

# Fit the model to your data
clusters = km.fit_predict(binary_data)

# Add the cluster assignments to your original DataFrame
data['Cluster'] = clusters

# Display the cluster assignments
print(data[['Cluster']])

print(km.cluster_centroids_)