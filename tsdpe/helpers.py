from scipy.interpolate import CubicSpline
from scipy.signal import decimate
import numpy as np
from sklearn.preprocessing import StandardScaler


def resample_signals(data, old_fs, new_fs):
    channel_results = []
    for channel in range(data.shape[1]):
        channel_data = data[:, channel]
        if old_fs != new_fs:
                    old_time = np.arange(0, len(channel_data) / old_fs, 1/old_fs)
                    new_time = np.arange(0, len(channel_data) / old_fs, 1/new_fs)

                    if old_fs < new_fs:
                        print("WARNING: The current sampling rate is lower than the fitted sampling rate. Upsampling may cause inaccuracies and artefacts.") if channel == 0 else None
                        cs = CubicSpline(old_time, channel_data)
                        channel_data = cs(new_time)
                        channel_results.append(channel_data)                    
                    elif old_fs > new_fs:
                        print("The current sampling rate is higher than the fitted sampling rate. Resampling signal.") if channel == 0 else None
                        # Downsample the signal to match the fitted sampling frequency
                        decimation_factor = int(old_fs / new_fs)
                        
                        # Split the decimation into multiple stages if the decimation factor is too large
                        max_decimation_factor = 13
                        while decimation_factor > max_decimation_factor:
                            channel_data = decimate(channel_data, max_decimation_factor)
                            decimation_factor = decimation_factor // max_decimation_factor
                        channel_data = decimate(channel_data, decimation_factor)
                        channel_results.append(channel_data)         
        else:                 
            print("The current sampling rate matches the fitted sampling rate. No resampling required.")
            channel_results.append(channel_data)
    return np.stack(channel_results, axis=-1)

def period_batching(data, no_periods):
    zero_crossings = [idx for idx in range(1, len(data[:, 0])) if data[idx - 1, 0] > float(0) >= data[idx, 0]]
    return [data[zero_crossings[idx]:zero_crossings[idx + no_periods]] for idx in
            range(1, len(zero_crossings) - no_periods, no_periods)]

# def resample_signals(data, old_samp_freq, new_samp_freq):
#     if old_samp_freq == new_samp_freq:
#         return data
#     else:
#         print("old data shape:", data.shape)
#         duration = data.shape[0] / old_samp_freq
#         new_num_data_samples = int(duration * new_samp_freq)
#         resampled_data = []
#         for x in range(data.shape[1]):
#             new_signal = scipy.signal.resample(data[:, x], new_num_data_samples)
#             resampled_data.append(new_signal)
#         resampled_data = np.vstack(resampled_data)
#         resampled_data = np.transpose(resampled_data)
#         print("resampled data shape:", resampled_data.shape)
#         return resampled_data

