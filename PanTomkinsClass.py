# Pan Tomkins QRS Detection

# import modules
import numpy as np
from scipy.signal import butter, sosfiltfilt
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def apply_bandpass_filter(data, fs, lowcut, highcut, order=5):
    """
    Applies a Butterworth bandpass filter to EKG data.

    Args:
        data (np.ndarray): The 1D EKG signal.
        fs (float): The sampling frequency of the data.
        lowcut (float): The lower cutoff frequency.
        highcut (float): The upper cutoff frequency.
        order (int): The filter order.

    Returns:
        np.ndarray: The filtered EKG signal.
    """
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    sos = butter(order, [low, high], btype='bandpass', output='sos')
    filtered_data = sosfiltfilt(sos, data)
    return filtered_data

class PanTomkinsClass:
    def __init__(self, signal):
        PASS
    def band_pass(self,low_pass:float = 5, high_pass:float = 15):
        PASS
def main():

    # ECG test file
    ecg_fn = "./Exports/signals/learn-nsrr01_ECG.txt"
    time, ecg = np.loadtxt(ecg_fn,skiprows = 1, unpack  = True)

    # Test Parameters
    fs               = 1/(time[2] - time[1])
    num_test_samples = int(30*fs)

    # filter
    lowcut  = 0.5
    highcut = 50
    filtered_ekg = apply_bandpass_filter(ecg[:num_test_samples], fs, lowcut, highcut)

    # Derivative via gradiaent
    diff_ecg = np.gradient(filtered_ekg)

    # Squaring
    squared_ecg = np.square(diff_ecg)

    # Smoothed
    integration_window  = int(0.150*fs)
    smoothed_ecg = np.convolve(squared_ecg,
                               np.ones(integration_window)/integration_window,
                               mode = 'same')

    # --- Peak detection with find_peaks ---
    # Distance: enforce refractory period (200 ms)
    min_distance = int(0.2 * fs)

    # Initial detection
    r_peaks, properties = find_peaks(
        smoothed_ecg,
        distance=int(0.2 * fs),  # 200 ms refractory
        prominence=np.percentile(smoothed_ecg, 90) * 0.2
    )

    # --- Step 1: Lag correction ---
    lag = integration_window // 2
    lag_corrected_peaks = r_peaks - lag
    lag_corrected_peaks = lag_corrected_peaks[lag_corrected_peaks >= 0]


    # Refinement search window = half the integration window
    search_window = integration_window // 2
    refined_r_peaks = []
    for p in r_peaks:
        start = max(0, p - search_window)
        end = min(len(filtered_ekg), p + search_window)
        refined = start + np.argmax(ecg[start:end])
        refined_r_peaks.append(refined)


    # Print results
    print("Detected R-peaks:", r_peaks)
    print("Corresponding times:", time[r_peaks])


    fig, axs = plt.subplots(5, 1)
    axs[0].plot(time[:num_test_samples],  ecg[:num_test_samples],          label='Signal 1', color='blue')
    axs[0].plot(time[refined_r_peaks], ecg[refined_r_peaks], 'o', color = 'red')

    axs[1].plot(time[:num_test_samples],  filtered_ekg, label='Signal 1', color='blue')
    axs[1].plot(time[refined_r_peaks], ecg[refined_r_peaks], 'o', color = 'red')

    axs[2].plot(time[:num_test_samples],  diff_ecg,     label='Signal 1', color='blue')
    axs[3].plot(time[:num_test_samples],  squared_ecg,  label='Signal 1', color='blue')
    axs[4].plot(time[:num_test_samples],  smoothed_ecg, label='Signal 1', color='blue')

    plt.tight_layout()
    plt.show()
    pass
if __name__ == "__main__":
    main()
