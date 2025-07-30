# Outliers Detect

A Python library for outlier detection in embeddings using multiple statistical and machine learning methods.

## Features

- 🎯 **5 different methods** for outlier detection
- 📊 **Automatic visualization** of results
- 🐼 **Simple interface** with pandas DataFrames
- 📈 **Detailed metrics** for each observation
- 📚 **Demo notebook** included

## Installation

```bash
pip install outliers-detect
```

For development:

```bash
git clone https://github.com/your-username/outliers-detect
cd outliers-detect
pip install -e ".[dev]"
```

## Basic Usage

```python
import pandas as pd
from outliers_detect import outliers_detect_df

# Creating a DataFrame with embeddings
df = pd.DataFrame({
    'id': [1, 2, 3, 4],
    'embedding': [
        '[0.1, 0.2, 0.3]',
        '[0.2, 0.3, 0.4]',
        '[0.15, 0.25, 0.35]',
        '[5.0, 5.1, 5.2]'  # This is an outlier
    ]
})

# Detecting outliers using the percentile method
result = outliers_detect_df(
    df,
    metodo='percentil',
    threshold_percentil=95,
    plotar=True
)

# Viewing the results
print(result[['id', 'eh_outlier', 'score']])

# Filtering only outliers
outliers = result[result['eh_outlier']]
print(f"Found {len(outliers)} outliers")
```

## Available Methods

### 1. **Percentile**
Detects outliers based on a specific percentile of distances.

```python
result = outliers_detect_df(
    df,
    metodo='percentil',
    threshold_percentil=95  # Considers top 5% as outliers
)
```

### 2. **Z-Score**
Uses standard deviation to identify outliers.

```python
result = outliers_detect_df(
    df,
    metodo='zscore',
    threshold_z=2.0  # Points with z-score > 2.0 are outliers
)
```

### 3. **IQR (Interquartile Range)**
Uses the Interquartile Range method.

```python
result = outliers_detect_df(
    df,
    metodo='iqr'  # Uses standard IQR criteria
)
```

### 4. **Cosine Distance**
Based on cosine distance to the centroid of embeddings.

```python
result = outliers_detect_df(
    df,
    metodo='cosine',
    threshold_cosine=0.10  # Distances > 0.10 are outliers
)
```

### 5. **PCA Reconstruction**
Uses PCA reconstruction error to detect outliers.

```python
result = outliers_detect_df(
    df,
    metodo='pca_reconstruction',
    n_components=2  # Number of principal components
)
```

## Function Parameters

### `outliers_detect_df(df, metodo, **kwargs)`

**Required parameters:**
- `df`: DataFrame with 'embedding' column containing list strings
- `metodo`: Detection method ('percentil', 'zscore', 'iqr', 'cosine', 'pca_reconstruction')

**Optional parameters:**
- `threshold_percentil`: Percentile for 'percentil' method (default: 95)
- `threshold_z`: Z-score threshold for 'zscore' method (default: 2.0)
- `threshold_cosine`: Cosine distance threshold for 'cosine' method (default: 0.10)
- `n_components`: PCA components for 'pca_reconstruction' (default: 2)
- `plotar`: Whether to plot graphs (default: False)

**Returns:**
DataFrame with additional columns:
- `eh_outlier`: Boolean indicating if it's an outlier
- `score`: Score/metric from the used method
- `distancia`: Calculated distance (when applicable)

## Examples and Demonstrations

### Demo Notebook

A complete Jupyter notebook is available at `exemplos/outliers_detect_demo.ipynb` with:

- 📊 Creation of synthetic data with known outliers
- 🎨 3D visualizations of embeddings
- 🔍 Testing of all available methods
- 📈 Comparison between different methods
- ⚙️ Parameter tuning and their effects

To run the notebook:

```bash
# Install additional dependencies if needed
pip install jupyter matplotlib

# Run the notebook
jupyter notebook exemplos/outliers_detect_demo.ipynb
```

### Advanced Example

```python
import numpy as np
import pandas as pd
from outliers_detect import outliers_detect_df

# Creating more realistic data
np.random.seed(42)

# Normal embeddings
normal_data = np.random.normal(0, 1, (100, 5))
# Outliers
outlier_data = np.random.normal(4, 0.5, (5, 5))

# Combining data
all_embeddings = np.vstack([normal_data, outlier_data])

# Creating DataFrame
df = pd.DataFrame({
    'id': range(len(all_embeddings)),
    'embedding': [str(emb.tolist()) for emb in all_embeddings],
    'category': ['normal'] * 100 + ['outlier'] * 5
})

# Testing different methods
methods = ['percentil', 'zscore', 'iqr', 'cosine', 'pca_reconstruction']

for method in methods:
    print(f"\n=== Method: {method} ===")
    result = outliers_detect_df(df, metodo=method, plotar=True)
    
    detected_outliers = result['eh_outlier'].sum()
    print(f"Detected outliers: {detected_outliers}")
    
    # Calculating precision (if you know the true outliers)
    true_outliers = df['category'] == 'outlier'
    precision = (result['eh_outlier'] & true_outliers).sum() / detected_outliers
    print(f"Precision: {precision:.2%}")
```

## Development

### Environment Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/outliers-detect
cd outliers-detect
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - **Windows**: `venv\Scripts\activate`
   - **Unix/MacOS**: `source venv/bin/activate`

4. Install development dependencies:
```bash
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=outliers_detect

# Run specific tests
pytest tests/test_outliers_detect.py::test_percentil_method
```

### Project Structure

```
outliers-detect/
├── outliers_detect/
│   ├── __init__.py
│   └── outliers_detect.py
├── tests/
│   └── test_outliers_detect.py
├── exemplos/
│   └── outliers_detect_demo.ipynb
├── pyproject.toml
├── setup.py
├── README.md
└── requirements.txt
```

## Contributing

Contributions are welcome! Please:

1. Fork the project
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Changelog

### v0.1.0
- ✨ Initial implementation with 5 detection methods
- 📊 Support for automatic visualizations
- 📚 Demo notebook included
- 🧪 Complete unit test suite 