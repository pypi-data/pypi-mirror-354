# Celline - Single Cell RNA-seq Analysis Pipeline

Celline is a comprehensive, interactive pipeline for single-cell RNA sequencing (scRNA-seq) analysis, designed to streamline the workflow from raw data to biological insights.

## Features

- **Automated Data Processing**: From raw fastq files to expression matrices
- **Quality Control**: Built-in QC metrics and filtering
- **Dimensionality Reduction**: PCA, t-SNE, and UMAP implementations
- **Clustering Analysis**: Multiple clustering algorithms
- **Cell Type Prediction**: Automated cell type annotation
- **Batch Effect Correction**: Multiple methods for data integration
- **Interactive Visualization**: Web-based interface for data exploration
- **Reproducible Workflows**: Containerized environments and version control

## Installation

Install Celline using pip:

```bash
pip install celline
```

## Quick Start

After installation, you can use the `celline` command globally:

```bash
# Initialize a new project
celline init

# List available functions
celline list

# Run preprocessing
celline run preprocess

# Launch interactive interface
celline interactive
```

## Documentation

For detailed documentation, please refer to the user guide and API reference.

## License

This project is licensed under the MIT License.