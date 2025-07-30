"""
Main implementation of outlier detection
"""

import numpy as np
import pandas as pd
from typing import List, Union, Tuple
from scipy.spatial.distance import cosine
from scipy.stats import zscore
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import ast

def outliers_detect_df(
    df: pd.DataFrame,
    method: str = 'percentile',
    percentile_threshold: float = 95,
    z_threshold: float = 2.0,
    cosine_threshold: float = 0.10,
    plot: bool = False,
    return_outliers_only: bool = False
) -> pd.DataFrame:
    """
    Detects outliers in a DataFrame containing embeddings.

    Args:
        df: DataFrame with 'embedding' column containing the embeddings
        method: Detection method ('percentile', 'zscore', 'iqr', 'cosine', 'pca_reconstruction')
        percentile_threshold: Percentile threshold for detection (default: 95)
        z_threshold: Z-score threshold (default: 2.0)
        cosine_threshold: Cosine distance threshold (default: 0.10)
        plot: If True, plots the results
        return_outliers_only: If True, returns only the outliers

    Returns:
        DataFrame with additional 'is_outlier' column
    """
    # Convert embeddings from string to numpy array
    embeddings = np.array([eval(emb) for emb in df['embedding']])
    
    # Calculate centroid
    centroid = np.mean(embeddings, axis=0)
    
    # Calculate distances to centroid
    distances = np.array([np.linalg.norm(emb - centroid) for emb in embeddings])
    
    # Initialize outliers column
    df['is_outlier'] = False
    
    if method == 'percentile':
        threshold = np.percentile(distances, percentile_threshold)
        df['is_outlier'] = distances > threshold
        df['centroid_distance'] = distances
        
    elif method == 'zscore':
        z_scores = (distances - np.mean(distances)) / np.std(distances)
        df['is_outlier'] = np.abs(z_scores) > z_threshold
        df['z_score'] = z_scores
        
    elif method == 'iqr':
        q1 = np.percentile(distances, 25)
        q3 = np.percentile(distances, 75)
        iqr = q3 - q1
        df['is_outlier'] = (distances < (q1 - 1.5 * iqr)) | (distances > (q3 + 1.5 * iqr))
        
    elif method == 'cosine':
        cosine_distances = np.array([cosine(emb, centroid) for emb in embeddings])
        df['is_outlier'] = cosine_distances > cosine_threshold
        df['cosine_distance'] = cosine_distances
        
    elif method == 'pca_reconstruction':
        # Reduce to 2 dimensions
        pca = PCA(n_components=2)
        reduced = pca.fit_transform(embeddings)
        reconstructed = pca.inverse_transform(reduced)
        
        # Calculate reconstruction error
        reconstruction_error = np.mean((embeddings - reconstructed) ** 2, axis=1)
        threshold = np.percentile(reconstruction_error, percentile_threshold)
        df['is_outlier'] = reconstruction_error > threshold
        df['reconstruction_error'] = reconstruction_error
        
    else:
        raise ValueError(f"Method '{method}' not recognized")
    
    if plot:
        plt.figure(figsize=(10, 6))
        if method in ['percentile', 'zscore', 'iqr']:
            plt.scatter(range(len(distances)), distances, c=df['is_outlier'], cmap='viridis')
            plt.axhline(y=threshold if method == 'percentile' else np.mean(distances) + z_threshold * np.std(distances), 
                       color='r', linestyle='--')
        elif method == 'cosine':
            plt.scatter(range(len(cosine_distances)), cosine_distances, c=df['is_outlier'], cmap='viridis')
            plt.axhline(y=cosine_threshold, color='r', linestyle='--')
        elif method == 'pca_reconstruction':
            plt.scatter(range(len(reconstruction_error)), reconstruction_error, c=df['is_outlier'], cmap='viridis')
            plt.axhline(y=threshold, color='r', linestyle='--')
        plt.title(f'Outlier Detection - Method: {method}')
        plt.show()
    
    if return_outliers_only:
        return df[df['is_outlier']]
    
    return df