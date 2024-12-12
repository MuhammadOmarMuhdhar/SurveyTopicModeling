from hdbscan import HDBSCAN
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.metrics import silhouette_score
from itertools import product
import pandas as pd
import numpy as np

def optimize_hdbscan_parameters(distance_matrix, param_grid):
    """
    Optimizes HDBSCAN parameters to maximize silhouette score.
    """
    best_score = -1
    best_params = None

    # Iterate over all parameter combinations
    for min_cluster_size, min_samples in product(param_grid['min_cluster_size'], param_grid['min_samples']):
        hdbscan_model = HDBSCAN(
            min_cluster_size=min_cluster_size,
            min_samples=min_samples,
            metric='precomputed',
            cluster_selection_method='eom'
        )
        labels = hdbscan_model.fit_predict(distance_matrix)

        # # Exclude noise and calculate silhouette score
        # if len(set(labels) - {-1}) > 1:  # Ensure more than one cluster excluding noise
        #     valid_labels = labels[labels != -1]
        #     valid_distances = distance_matrix[labels != -1][:, labels != -1]
        #     score = silhouette_score(distance_matrix, labels, metric='precomputed')
        #     if score > best_score:
        #         best_score = score
        #         best_params = {'min_cluster_size': min_cluster_size, 'min_samples': min_samples}

        if len(set(labels) - {-1}) > 1:  # Ensure more than one cluster excluding noise
            score = silhouette_score(distance_matrix, labels, metric='precomputed')
            if score > best_score:
                best_score = score
                best_params = {'min_cluster_size': min_cluster_size, 'min_samples': min_samples}

    return best_params


def create_clusters(df_with_embeddings, granularity='default'):
    """
    Creates clusters using HDBSCAN with optional optimization for hyperparameter selection.
    """
    if granularity not in ['default', 'broad']:
        raise ValueError("Granularity must be 'default' or 'broad'.")

    if df_with_embeddings.empty:
        raise ValueError("The DataFrame is empty. Clustering cannot be performed.")

    num_rows = len(df_with_embeddings)

    # Compute distance matrix
    distance_matrix = pairwise_distances(df_with_embeddings[['Umap_1', 'Umap_2']], metric='cosine').astype('float64')
    np.fill_diagonal(distance_matrix, 0)

    # Define parameter grids for each granularity
    
    default_param_grid = {
        'min_cluster_size': [
            # max(5, int(num_rows * 0.005)),  # 0.5% of the data or 5
            # max(7, int(num_rows * 0.0075)), # 0.75% of the data or 7
            # max(10, int(num_rows * 0.01)),  # 1% of the data or 10
            # max(12, int(num_rows * 0.0125)), # 1.25% of the data or 12
            # max(15, int(num_rows * 0.015)),  # 1.5% of the data or 15
            max(17, int(num_rows * 0.0175)), # 1.75% of the data or 17
            max(20, int(num_rows * 0.02)),   # 2% of the data or 20
            max(22, int(num_rows * 0.0225)), # 2.25% of the data or 22
            max(25, int(num_rows * 0.025)),  # 2.5% of the data or 25
            max(27, int(num_rows * 0.0275)), # 2.75% of the data or 27
            max(30, int(num_rows * 0.03)),   # 3% of the data or 30
            max(32, int(num_rows * 0.0325)), # 3.25% of the data or 32
            max(35, int(num_rows * 0.035)), # 3.5% of the data or 35
            # max(37, int(num_rows * 0.0375)) # 3.75% of the data or 37
            # max(40, int(num_rows * 0.04))   # 4% of the data or 40
            # max(42, int(num_rows * 0.0425)) # 4.25% of the data or 42
            # max(45, int(num_rows * 0.045))  # 4.5% of the data or 45
        ],
        'min_samples': [
            max(5, int(num_rows * 0.005)),  # 0.5% of the data or 5
            max(6, int(num_rows * 0.0075)), # 0.75% of the data or 6
            max(7, int(num_rows * 0.01)),   # 1% of the data or 7
            max(8, int(num_rows * 0.0125))  # 1.25% of the data or 8
        ]
        }

    broad_param_grid = {
        'min_cluster_size': [
            max(50, int(num_rows * 0.04)),  # 4% of the data or 50
            max(50, int(num_rows * 0.045)), # 4.5% of the data or 50
            max(50, int(num_rows * 0.05)),  # 5% of the data or 50
            max(60, int(num_rows * 0.055))  # 5.5% of the data or 60
        ],
        'min_samples': [
            max(10, int(num_rows * 0.008)), # 0.8% of the data or 10
            max(10, int(num_rows * 0.009)), # 0.9% of the data or 10
            max(10, int(num_rows * 0.01)),  # 1% of the data or 10
            max(15, int(num_rows * 0.012))  # 1.2% of the data or 15
        ]
    }

    # Predefined fallback parameters
    fallback_params = {'min_cluster_size': 10, 'min_samples': 5}

    # Select the appropriate parameter grid
    param_grid = default_param_grid if granularity == 'default' else broad_param_grid

    # Optimize parameters
    best_params = optimize_hdbscan_parameters(distance_matrix, param_grid)
    if best_params:
        min_cluster_size = best_params['min_cluster_size']
        min_samples = best_params['min_samples']
    else:
        min_cluster_size = fallback_params['min_cluster_size']
        min_samples = fallback_params['min_samples']


    # Instantiate and fit HDBSCAN
    hdbscan_model = HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=min_samples,
        metric='precomputed',
        cluster_selection_method='eom'
    )
    labels = hdbscan_model.fit_predict(distance_matrix)

    return labels
