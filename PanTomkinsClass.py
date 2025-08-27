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
    num_test_samples = int(15*fs)

    # filter
    lowcut = 0.5
    highcut = 50
    filtered_ekg = apply_bandpass_filter(ecg[:num_test_samples], fs, lowcut, highcut)

    # Derivative via gradiaent
    diff_ecg = np.gradient(filtered_ekg)

    # Squaring
    squared_ecg = np.square(diff_ecg)

    # Smoothed
    integration_window = int(0.20*fs)
    smoothed_ecg = np.convolve(squared_ecg, np.ones(integration_window)/integration_window, mode = 'same')

    # Initialize threshold variables using an initial segment (e.g., first 2 sec or few peaks)
    SPKI = np.max(smoothed_ecg[:int(2 * fs)])  # heuristic seed
    NPKI = np.mean(smoothed_ecg[:int(2 * fs)])  # heuristic seed
    SPKF = SPKI
    NPKF = NPKI
    THI1 = NPKI + 0.25 * (SPKI - NPKI)
    THF1 = NPKF + 0.25 * (SPKF - NPKF)
    THI2, THF2 = 0.5 * THI1, 0.5 * THF1

    # --- Peak detection with find_peaks ---
    # Distance: enforce refractory period (200 ms)
    min_distance = int(0.2 * fs)

    # Initial detection
    r_peaks, properties = find_peaks(
        smoothed_ecg,
        distance=min_distance,
        prominence=np.percentile(smoothed_ecg, 90) * 0.2  # rough threshold
    )

    #lag = integration_window // 2
    #lag_corrected_peaks = r_peaks - lag
    #r_peaks = lag_corrected_peaks[lag_corrected_peaks >= 0]

    # Tie integration window to search window
    search_window = integration_window // 2

    # Optional: refine peak positions on the bandpassed ECG
    refined_r_peaks = []
    for p in r_peaks:
        start = max(0, p - search_window)
        end = min(len(filtered_ekg), p + search_window)
        refined = start + np.argmax(filtered_ekg[start:end])
        refined_r_peaks.append(refined)

    refined = np.array(refined_r_peaks)

    # 4) RR interval detection + search-back initialization
    rr_intervals = np.diff(refined) / fs  # in seconds
    RR_list = rr_intervals.tolist()

    def rr_avgs(rrs):
        if not rrs:
            return None, None
        avg1 = np.mean(rrs[-8:])
        regul = [r for r in rrs if avg1 * 0.92 < r < avg1 * 1.16]
        avg2 = np.mean(regul) if regul else avg1
        return avg1, avg2

    # 5) Search-back for missed beats
    final_peaks = [refined[0]]
    for current in refined[1:]:
        last_peak = final_peaks[-1]
        delta_t = (current - last_peak) / fs

        avg1, avg2 = rr_avgs(RR_list)

        if avg2 and delta_t > 1.66 * avg2:
            # Search back interval
            start = last_peak + int(0.2 * fs)
            end = current - int(0.2 * fs)
            seg = smoothed_ecg[start:end]
            if seg.size:
                peak_idx = start + np.argmax(seg)
                final_peaks.append(peak_idx)
                RR_list.append((peak_idx - last_peak) / fs)

        final_peaks.append(current)
        RR_list.append((current - last_peak) / fs)

    final_peaks = np.array(final_peaks)
    r_peaks = final_peaks

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
