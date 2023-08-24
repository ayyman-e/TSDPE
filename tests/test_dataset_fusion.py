import numpy as np
from tsdpe import dataset_fusion  # Adjust this import to your package structure
from tsdpe.helpers import (
    resample_signals,
    period_batching,
)  # Adjust this import to your package structure


def generate_sine_wave(freq, sample_rate, duration):
    """Generate a sine wave of a given frequency, sample rate, and duration."""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    return np.sin(2 * np.pi * freq * t)


def test_dataset_fusion_shape():
    # Generate sine wave datasets
    dataset1 = generate_sine_wave(1, 10, 10).reshape(
        -1, 1
    )  # 1 Hz, 10 samples/sec, 1 second
    dataset2 = generate_sine_wave(1, 20, 10).reshape(
        -1, 1
    )  # 1 Hz, 20 samples/sec, 1 second

    # Since each dataset is a 2D array with one feature, you can optionally stack them to make them multi-feature
    dataset1 = np.hstack([dataset1] * 5)
    dataset2 = np.hstack([dataset2] * 5)

    sampling_frequencies = [10, 20]
    no_periods_per_slice = 2

    # Run the dataset_fusion function
    fused_dataset = dataset_fusion(
        [dataset1, dataset2], sampling_frequencies, no_periods_per_slice
    )

    # Check the shape of the output
    # Adjust this according to what you expect the output shape to be
    assert fused_dataset.shape == (161, 5)  # Replace with your expected shape


# Add more test cases as needed
