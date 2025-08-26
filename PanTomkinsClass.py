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

def main():

    # ECG test file
    ecg_fn = "./Exports/signals/learn-nsrr01_ECG.txt"
    time, ecg = np.loadtxt(ecg_fn,skiprows = 1, unpack  = True)

    # Test Parameters
    fs               = 1/(time[2] - time[1])
    num_test_samples = int(60*fs)

    # ECG test file
    ecg_fn = "./Exports/signals/learn-nsrr01_ECG.txt"
    time, ecg = np.loadtxt(ecg_fn,skiprows = 1, unpack = True)

    # Test Parameters
    fs = 1/(time[2] - time[1])
    num_test_samples = int(30*fs)

    # filter
    lowcut = 0.5
    highcut = 50
    filtered_ekg = apply_bandpass_filter(ecg[:num_test_samples], fs, lowcut, highcut)

    # Derivative via gradiaent
    diff_ecg = np.gradient(filtered_ekg)

    # Squaring
    squared_ecg = np.square(diff_ecg)

    # Smoothed
    window_size = int(0.100*fs)
    smoothed_ecg = np.convolve(squared_ecg, np.ones(window_size)/window_size, mode = 'same')

    # --- Peak detection with find_peaks ---
    # Distance: enforce refractory period (200 ms)
    min_distance = int(0.2 * fs)

    # Initial detection
    peaks, properties = find_peaks(
        smoothed_ecg,
        distance=min_distance,
        prominence=np.percentile(smoothed_ecg, 90) * 0.2  # rough threshold
    )

    # Optional: refine peak positions on the bandpassed ECG
    r_peaks = []
    search_window = int(0.05 * fs)  # ±50 ms
    for p in peaks:
        start = max(0, p - search_window)
        end = min(len(filtered_ekg), p + search_window)
        refined = start + np.argmax(filtered_ekg[start:end])
        r_peaks.append(refined)
    r_peaks = np.array(r_peaks)

    # Print results
    print("Detected R-peaks:", r_peaks)
    print("Corresponding times:", time[r_peaks])

    fig, axs = plt.subplots(5, 1)
    axs[0].plot(time[:num_test_samples],  ecg[:num_test_samples],          label='Signal 1', color='blue')
    axs[0].plot(time[r_peaks], ecg[r_peaks], 'o', color = 'red')

    axs[1].plot(time[:num_test_samples],  filtered_ekg, label='Signal 1', color='blue')
    axs[1].plot(time[r_peaks], filtered_ekg[r_peaks], 'o', color = 'red')

    #axs[2].plot(time[:num_test_samples],  diff_ecg,     label='Signal 1', color='blue')
    #axs[3].plot(time[:num_test_samples],  squared_ecg,  label='Signal 1', color='blue')
    #axs[4].plot(time[:num_test_samples],  smoothed_ecg, label='Signal 1', color='blue')

    plt.tight_layout()
    plt.show()
    pass
if __name__ == "__main__":
    main()
