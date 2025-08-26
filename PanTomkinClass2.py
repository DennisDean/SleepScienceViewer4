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

class PanTompkinsDetector:
    def __init__(self, fs, init_seconds=2.0):
        self.fs = fs
        self.integration_window = int(0.15 * fs)
        self.lag = self.integration_window // 2
        self.search_back_factor = 1.66
        self.refractory_period = 1 # int(0.15 * fs)
        self.twave_window = int(0.36 * fs)

        # Initialize thresholds
        self.SPKI = self.NPKI = None
        self.SPKF = self.NPKF = None
        self.THI1 = self.TH_F1 = None
        self.THI2 = self.TH_F2 = None

        self.prev_slope = 0
        self.last_R = -np.inf
        self.RR_intervals = []

        print(f'fs = {fs}, self.integration_window = {self.integration_window}, self.lag  = {self.lag }')
        print(f'self.search_back_factor = {self.search_back_factor}, self.refractory_period  = {self.refractory_period }, self.twave_window  = {self.twave_window}')
    def _initialize_thresholds(self, int_signal, filt_signal):
        init_len = int(self.fs * 2)  # first 2 s
        self.SPKI = np.max(int_signal[:init_len])
        self.NPKI = np.mean(int_signal[:init_len])
        self.SPKF = np.max(filt_signal[:init_len])
        self.NPKF = np.mean(filt_signal[:init_len])
        self._update_thresholds()

        print(f'SPKI = {self.SPKI}, NPKI = {self.NPKI}, SPKF = {self.SPKF}, NPKF = {self.NPKF}')

    def _update_thresholds(self):
        self.THI1 = self.NPKI + 0.25 * (self.SPKI - self.NPKI)
        self.TH_F1 = self.NPKF + 0.25 * (self.SPKF - self.NPKF)
        self.THI2 = 0.5 * self.THI1
        self.TH_F2 = 0.5 * self.TH_F1
        print(f'THI1 = {self.THI1}, TH_F1 = {self.TH_F1}, THI2 = {self.THI2}, NPKF = {self.TH_F2}')
    def detect(self, ecg:np.array, lowcut:float = 0.5, highcut:float = 50):

        # Filter ECG
        filtered_ecg = apply_bandpass_filter(ecg, self.fs, lowcut, highcut)
        diff_ecg = np.gradient(filtered_ecg)
        squared_ecg = np.square(diff_ecg)

        # Prepare integrated signal
        I = np.convolve(squared_ecg, np.ones(self.integration_window)/self.integration_window, mode="same")

        # Initialize thresholds on first call
        if self.SPKI is None:
            self._initialize_thresholds(I, filtered_ecg)

        peaks, _ = find_peaks(I, distance=self.refractory_period)
        print(f'peaks = {peaks}')

        R_peaks = []
        for p in peaks:
            # Lag correction
            p_corr = p - self.lag
            if p_corr < 0 or p_corr >= len(filtered_ecg):
                continue

            # Refinement search
            sw = self.integration_window // 2
            start = max(0, p_corr - sw)
            end   = min(len(filtered_ecg), p_corr + sw)
            pF = start + np.argmax(filtered_ecg[start:end])

            # Slope for T-wave discrimination
            slope = filtered_ecg[pF] - filtered_ecg[pF-1] if pF > 0 else 0

            # Check thresholds
            if I[p] > self.THI1 and filtered_ecg[pF] > self.TH_F1:
                if (pF - self.last_R) < self.twave_window and slope < 0.5 * self.prev_slope:
                    # T wave — update noise
                    self.NPKI = 0.125*I[p] + 0.875*self.NPKI
                    self.NPKF = 0.125*filtered_ecg[pF] + 0.875*self.NPKF
                else:
                    # Accept R
                    R_peaks.append(pF)
                    self.SPKI = 0.125*I[p] + 0.875*self.SPKI
                    self.SPKF = 0.125*filtered_ecg[pF] + 0.875*self.SPKF
                    self.prev_slope = slope
                    if R_peaks:
                        self.RR_intervals.append((pF - self.last_R) / self.fs)
                        self.last_R = pF
            else:
                # Noise
                self.NPKI = 0.125*I[p] + 0.875*self.NPKI
                self.NPKF = 0.125*filtered_ecg[pF] + 0.875*self.NPKF

            # Refresh thresholds
            self._update_thresholds()

            # Search back if RR too long
            if self.RR_intervals:
                avg_rr = np.mean(self.RR_intervals[-8:])
                if (pF - self.last_R) / self.fs > self.search_back_factor * avg_rr:
                    sb_start = self.last_R + self.refractory_period
                    sb_end   = p
                    if sb_end > sb_start:
                        segment = I[sb_start:sb_end]
                        if segment.size:
                            q = sb_start + np.argmax(segment)
                            R_peaks.append(q)
                            self.RR_intervals.append((q - self.last_R) / self.fs)
                            self.last_R = q
        print(f'R_peaks = {R_peaks}')
        return np.array(R_peaks)
def main():

    # ECG test file
    ecg_fn = "./Exports/signals/learn-nsrr01_ECG.txt"
    time, ecg = np.loadtxt(ecg_fn,skiprows = 1, unpack  = True)

    # Test Parameters
    fs               = 1/(time[2] - time[1])
    num_test_samples = int(30*fs)

    detector = PanTompkinsDetector(fs)
    r_peaks = detector.detect(ecg[:num_test_samples])

    print (r_peaks)

    plt.plot(time[:num_test_samples], ecg[:num_test_samples])
    plt.plot(time[r_peaks], ecg[r_peaks], 'ro')
    plt.show()
    pass
if __name__ == "__main__":
    main()
