# Pan Tomkins QRS Detection

# import modules
import numpy as np
from scipy.signal import butter, sosfiltfilt
import matplotlib.pyplot as plt

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
    print(time[1:10])
    print(ecg[1:10])
    fs = 1/(time[2] - time[1])
    test_samples = int(30*fs)

    print(test_samples)

    # filter
    fs = 250  # Example sampling frequency
    lowcut = 0.5
    highcut = 50
    filtered_ekg = apply_bandpass_filter(ecg[:test_samples], fs, lowcut, highcut)

    # Derivative via gradiaent
    dy_dx = np.gradient(ecg[:test_samples])

    # Squaring
    sq_dy_dx = np.square(dy_dx)

    plt.plot(time[:test_samples],ecg[:test_samples], label='Signal 1', color='blue')
    plt.plot(time[:test_samples], filtered_ekg[:test_samples], label='Signal 1', color='red')
    plt.plot(time[:test_samples], dy_dx[:test_samples], label='Signal 1', color='red')
    plt.xlabel("Time (s)")
    plt.ylabel("EKG")
    plt.title("Pan Tomkin Example")
    plt.show()

    pass
if __name__ == "__main__":
    main()
