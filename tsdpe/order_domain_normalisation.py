"""
OrderDomainNormalisation Class
==============================

This class implements functionalities for order domain normalization of time-series data. 
The class provides methods to fit model parameters and to transform data into the order domain.

Class
-----
- OrderDomainNormalisation: The main class for implementing order domain normalisation.

Example
-------
.. code-block:: python

    from TSDPE.OrderDomainNormalisation import OrderDomainNormalisation
    
    odn = OrderDomainNormalisation()
    odn.fit_parameters(fs=1000, bandwidth_orders=5)
    order_axis, transformed_data = odn.transform(data, fs=1000, fo=50)

Dependencies
------------
- NumPy
- SciPy

Authors
-------
Ayman Elhalwagy

License
-------
MIT
"""

import numpy as np
from scipy.signal import welch, decimate
from scipy.fft import rfft, rfftfreq
from scipy.interpolate import (
    interp1d,
    PchipInterpolator,
    Akima1DInterpolator,
    CubicSpline,
)


class OrderDomainNormalisation:
    """
    Class that implements order domain normalisation.
    """

    def __init__(self):
        """
        Initialize order_domain_normalisation.

        Args:
            bandwidth (float): The desired bandwidth in Hz.
        """
        self.orders_fft = None
        self.orders_welch = None
        self.fitted_fs = None
        self.fitted_fo = None
        self.max_orders = None
        self.fft_size = None

    def fit_parameters(self, fs, bandwidth_orders):
        self.fitted_fs = fs
        self.bandwidth_orders = bandwidth_orders
        self.fft_size = int(2 ** np.ceil(np.log2(self.fitted_fs)))
        self.order_axis = np.linspace(0, self.bandwidth_orders, self.fft_size // 2 + 1)

    def transform(self, data, fs, fo, method="linear", psd=False):
        """
        Transform the data using the fitted model.

        Args:
            data (numpy.ndarray): The data to be transformed.
            fs (float): Sample frequency.
            fo (float): Fundamental frequency.
            psd (bool): If True, return the power spectral density.
        """
        if method == "linear":
            interp_func = interp1d
        elif method == "cubic_spline":
            interp_func = CubicSpline
        elif method == "nearest":
            interp_func = lambda x, y: interp1d(x, y, kind="nearest")
        elif method == "polynomial":
            interp_func = lambda x, y: interp1d(x, y, kind="quadratic")
        elif method == "pchip":
            interp_func = PchipInterpolator
        elif method == "akima":
            interp_func = Akima1DInterpolator
        # Calculate orders
        # orders_fft = self.fft_freq / fo

        # Initialize an empty list to hold the results
        results = []

        # Ensure that data is a 2D array
        if len(data.shape) == 1:
            data = data.reshape(-1, 1)

        # Process each channel individually
        for channel in range(data.shape[1]):
            channel_data = data[:, channel]

            if fs != self.fitted_fs:
                old_time = np.arange(0, len(channel_data) / fs, 1 / fs)
                new_time = np.arange(0, len(channel_data) / fs, 1 / self.fitted_fs)

                if fs < self.fitted_fs:
                    print(
                        "WARNING: The current sampling rate is lower than the fitted sampling rate. Upsampling may cause inaccuracies and artefacts."
                    ) if channel == 0 else None
                    cs = CubicSpline(old_time, channel_data)
                    channel_data = cs(new_time)
                elif fs > self.fitted_fs:
                    print(
                        "The current sampling rate is higher than the fitted sampling rate. Resampling signal."
                    ) if channel == 0 else None
                    # Downsample the signal to match the fitted sampling frequency
                    decimation_factor = int(fs / self.fitted_fs)

                    # Split the decimation into multiple stages if the decimation factor is too large
                    max_decimation_factor = 13
                    while decimation_factor > max_decimation_factor:
                        channel_data = decimate(channel_data, max_decimation_factor)
                        decimation_factor = decimation_factor // max_decimation_factor
                    channel_data = decimate(channel_data, decimation_factor)

            if len(channel_data) < self.fft_size:
                # Zero-pad the signal to match the FFT size
                channel_data = np.pad(
                    channel_data,
                    (0, self.fft_size - len(channel_data)),
                    mode="constant",
                )

            if psd:
                _, channel_result = welch(
                    channel_data,
                    fs=self.fitted_fs,
                    nperseg=self.fft_size * 2,
                    noverlap=0,
                )
                channel_result = channel_result[: len(self.order_axis)]
            else:
                yf = rfft(channel_data, n=self.fft_size * 2)
                channel_result = 2.0 / self.fft_size * 2 * np.abs(yf)
                channel_result = channel_result[: len(self.order_axis)]

            # Normalize by fundamental frequency to get orders
            freq_bins = rfftfreq(self.fft_size * 2, 1 / self.fitted_fs)[
                : self.fft_size // 2 + 1
            ]
            # plt.figure()
            # plt.semilogy(freq_bins,channel_result)
            # plt.show()
            orders = freq_bins / fo

            # Interpolate to align with reference order axis
            order_interp_func = interp_func(
                orders, channel_result, fill_value="extrapolate"
            )
            channel_result_interpolated = order_interp_func(self.order_axis)

            results.append(channel_result_interpolated)

        # Stack results into a 2D array
        results = np.stack(results, axis=-1)

        return self.order_axis, results
