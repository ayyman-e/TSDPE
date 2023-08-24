"""
TSDPE (Time-Series Data Processing Engine)
==========================================

This package provides classes and functions for processing and analyzing time-series data.

Main Features
-------------
- Order Domain Normalisation
- Dataset Fusion
- Resampling utilities
- Period batching

Usage Example
-------------

.. code-block:: python

    from TSDPE import OrderDomainNormalisation, dataset_fusion
    
    # Your code here

Dependencies
------------
- NumPy
- SciPy
- scikit-learn

Authors
-------
Ayman Elhalwagy

License
-------
MIT

For more information, please see the full documentation at: http://github.com/your_username/TSDPE
"""

from .order_domain_normalisation import OrderDomainNormalisation
from .dataset_fusion import dataset_fusion
