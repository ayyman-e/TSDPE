# Time Series Data Processing Engine (TSDPE)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
  - [Dataset Fusion](#dataset-fusion)
  - [Order Domain Normalization (ODN)](#order-domain-normalization-odn)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Code Formatting and Linting](#code-formatting-and-linting)
- [CI/CD](#ci/cd)
- [Acknowledgments](#acknowledgments)

## Overview

Time Series Data Processing Engine (TSDPE) is a Python library that offers advanced functionalities for time series data processing and analysis.

## Features

### Dataset Fusion

Dataset Fusion is a feature that allows you to combine multiple datasets into a single unified dataset. This is particularly useful when dealing with different sources of time-series data that need to be synchronized and resampled to achieve a common timestamp.

#### How it works

1. **Data Loading**: Load multiple datasets with differing timestamps.
2. **Synchronization**: Align the datasets to have a common timestamp.
3. **Resampling**: Interpolate or decimate data points to conform to a user-defined sampling rate.

### Order Domain Normalization (ODN)

Order Domain Normalization (ODN) is designed to normalize and process time-series data in the frequency domain with a focus on the harmonic analysis.

#### How it works

1. **Fourier Transformation**: Convert the time-domain data into frequency-domain data.
2. **Normalization**: Normalize the frequency data based on a reference.
3. **Inverse Fourier Transformation**: Convert the normalized frequency-domain data back into time-domain.

## Getting Started

### Prerequisites

- Python 3.9+
- Pipenv

### Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/yourusername/TSDPE.git
cd TSDPE
```

Install dependencies using Pipenv:

```bash
pipenv install --dev
```

### Usage

1. To use Dataset Fusion, import and call the relevant function:

   ```python
   from tsdpe import dataset_fusion
   ```

2. For ODN, use:

   ```python
   from tsdpe import order_domain_normalization
   ```


## Testing

Run the tests to ensure everything is set up correctly:

```bash
pytest
```

## Code Formatting and Linting

- This project uses `Black` for code formatting and `pylint` for linting.

    ```bash
    black .
    pylint tsdpe/
    ```

## CI/CD

GitHub Actions is set up for Continuous Integration. It automatically runs tests and linters on every push to the repository.

## Acknowledgments

- Thanks to the Brunel AI Center for providing support and inspiration, and have helped to improve this project.
