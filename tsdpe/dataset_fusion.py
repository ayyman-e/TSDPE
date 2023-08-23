import numpy as np
from sklearn.preprocessing import StandardScaler
from .helpers import resample_signals, period_batching

def dataset_fusion(dataset_list, sampling_frequencies, no_periods_per_slice):
    """
    Create a fused dataset from multiple datasets with varying sampling frequencies.

    :param dataset_list: List of 2D or 3D arrays (file, samples, features) containing dataset samples
    :param sampling_frequencies: List of sampling frequencies corresponding to each dataset
    :param no_periods_per_slice: Number of periods per slice for period batching
    :return: Fused dataset
    """
    variety = any(len(np.shape(data)) == 3 for data in dataset_list)

    if variety:
        # Apply variety for each 3D dataset (file, samples, features)
        dataset_list = [np.vstack(data) for data in dataset_list]

    # Resample datasets
    data_size_multiplier = [x / min(sampling_frequencies) for x in sampling_frequencies]
    resampled_dataset_list = [
        resample_signals(data, old_fs=sampling_frequencies[idx], new_fs=min(sampling_frequencies)) 
        for idx, data in enumerate(dataset_list)
    ]

    # Scale datasets
    scalers = []
    scaled_dataset_list = []
    for data in resampled_dataset_list:
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(data)
        scaled_dataset_list.append(scaled_data)
        scalers.append(scaler)

    # Period Batching
    split_dataset_list = [
        period_batching(data=data, no_periods=no_periods_per_slice) for data in scaled_dataset_list
    ]
    
    # Fuse datasets
    fused_dataset = np.vstack(list(filter(None.__ne__, chain.from_iterable(zip_longest(*split_dataset_list)))))

    print(f"Fused dataset shape: {fused_dataset.shape}")

    return fused_dataset