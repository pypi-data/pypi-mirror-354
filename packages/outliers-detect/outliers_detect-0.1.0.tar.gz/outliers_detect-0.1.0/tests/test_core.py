"""
Tests for the main functions
"""

import pytest
import numpy as np
import pandas as pd
from outliers_detect import outliers_detect_df

@pytest.fixture
def sample_df():
    # Creating sample data with embeddings
    np.random.seed(42)
    n_samples = 100
    embedding_dim = 3
    
    # Creating normal embeddings
    normal_embeddings = np.random.normal(0, 1, (n_samples, embedding_dim))
    
    # Creating some outliers
    outlier_embeddings = np.random.normal(5, 1, (5, embedding_dim))
    
    # Combining the data
    all_embeddings = np.vstack([normal_embeddings, outlier_embeddings])
    
    # Creating DataFrame
    df = pd.DataFrame({
        'id': range(len(all_embeddings)),
        'embedding': [str(emb.tolist()) for emb in all_embeddings]
    })
    
    return df

def test_outliers_detect_df_percentile(sample_df):
    result = outliers_detect_df(
        sample_df,
        method='percentile',
        percentile_threshold=95,
        plot=False
    )
    
    # Verify if outliers column was created
    assert 'is_outlier' in result.columns
    # Verify if distance column was created
    assert 'centroid_distance' in result.columns
    # Verify if some outliers were found
    assert result['is_outlier'].sum() > 0

def test_outliers_detect_df_zscore(sample_df):
    result = outliers_detect_df(
        sample_df,
        method='zscore',
        z_threshold=2.0,
        plot=False
    )
    
    assert 'is_outlier' in result.columns
    assert 'z_score' in result.columns
    assert result['is_outlier'].sum() > 0

def test_outliers_detect_df_iqr(sample_df):
    result = outliers_detect_df(
        sample_df,
        method='iqr',
        plot=False
    )
    
    assert 'is_outlier' in result.columns
    assert result['is_outlier'].sum() > 0

def test_outliers_detect_df_cosine(sample_df):
    result = outliers_detect_df(
        sample_df,
        method='cosine',
        cosine_threshold=0.10,
        plot=False
    )
    
    assert 'is_outlier' in result.columns
    assert result['is_outlier'].sum() > 0

def test_outliers_detect_df_pca(sample_df):
    result = outliers_detect_df(
        sample_df,
        method='pca_reconstruction',
        percentile_threshold=95,
        plot=False
    )
    
    assert 'is_outlier' in result.columns
    assert 'reconstruction_error' in result.columns
    assert result['is_outlier'].sum() > 0

def test_outliers_detect_df_return_outliers_only(sample_df):
    result = outliers_detect_df(
        sample_df,
        method='percentile',
        percentile_threshold=95,
        plot=False,
        return_outliers_only=True
    )
    
    # Verify if only outliers were returned
    assert len(result) == result['is_outlier'].sum()
    assert len(result) < len(sample_df)

def test_outliers_detect_df_invalid_method(sample_df):
    with pytest.raises(ValueError):
        outliers_detect_df(
            sample_df,
            method='invalid_method',
            plot=False
        )