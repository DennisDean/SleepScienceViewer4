"""
EDF File Class provides python native access to information stored in an EDF file

EDF File Class

Overview:
The EDF File Class provides access to information stored in an EDF File. The set of classes are
designed to provide Python access to the EDF Header, EDF Signal Header, and the EDF Signals.

The objectives in creating a Python Native format are to facilitate data analysis.

Author:
Dennis A. Dean, II, PhD
Sleep Science

Completion Date: June 20, 2025

Acknowledgement:
The python code models previous Matlab versions of the code written by Case Western Reserve
University and by Matlab code I wrote when I was at Brigham and Women's Hospital. The previously
authored Matlab code benefited from feedback received following public release of the MATLAB
code on MATLAB central.

Copyright 2025 Dennis A. Dean II
This file is part of the SleepScienceViewer project.

This source code is licensed under the GNU Affero General Public License v3.0.
See the LICENSE file in the root directory of this source tree or visit
https://www.gnu.org/licenses/agpl-3.0.html for full terms.
"""

# To Do List

# Import Modules
# OS Imports

# Extend Existing Class
from FigureGraphicsViewClass import FigureGraphicsView

import copy
import os
import logging
from typing import List, Dict, Optional
from pathlib import Path

# Logic support
from sympy.logic.boolalg import Boolean

# Interface
from PySide6.QtCore import Qt

# Interface  and Plotting
from PySide6.QtWidgets import QVBoxLayout, QSizePolicy
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt

# Scientific Computing
import numpy as np
from scipy import signal
from scipy.signal import butter, sosfiltfilt
from scipy.signal import iirnotch, filtfilt
import math

# Data Types
import datetime
import pandas as pd
import csv
import json

# Analsysis Classes
from multitaper_spectrogram_python_class import MultitaperSpectrogram

import warnings
DEBUG = True
if DEBUG:
    warnings.filterwarnings('error')

# Set up logging
logger = logging.getLogger(__name__)

# Utilities
def generate_timestamped_filename(prefix: str, ext: str = ".csv", output_dir: str = "") -> str:
    """Add a time stamp to a generated file

    prefix: str: File name
    ext: str = File type string
    output_dir: str = Output directory if set
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}{ext}"
    return os.path.join(output_dir, filename) if output_dir else filename
def generate_filename(prefix: str, ext: str = ".csv", output_dir: str = "") -> str:
    """Add a time stamp to a generated file

    prefix: str: File name
    ext: str = File type string
    output_dir: str = Output directory if set
    """
    filename = f"{prefix}{ext}"
    return os.path.join(output_dir, filename) if output_dir else filename
def convert_to_serializable(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    elif hasattr(obj, '__dict__'):
        return convert_to_serializable(vars(obj))
    else:
        return obj

# Filtering
def apply_bandpass_filter(data, fs, lowcut, highcut, order=5):
    """
    Applies a Butterworth bandpass filter to  data.

    Args:
        data (np.ndarray): The 1D  signal.
        fs (float): The sampling frequency of the data.
        lowcut (float): The lower cutoff frequency.
        highcut (float): The upper cutoff frequency.
        order (int): The filter order.

    Returns:
        np.ndarray: The filtered  signal.
    """

    if validate_bandpass_params(fs, lowcut, highcut, order):
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        sos = butter(order, [low, high], btype='bandpass', output='sos')
        filtered_data = sosfiltfilt(sos, data)
        logger.info(f'Band pass filter applied.')
    else:
        filtered_data = data
        logger.error(f'Band pass filter not applied. Parameters are not valid')
    return filtered_data
def validate_bandpass_params(fs, lowcut, highcut, order)->bool:
    # Set return value
    valid_params = True

    # Check parameter values
    if fs is None or fs <= 0:
        valid_params = False
        logger.error("fs (sampling rate) must be a positive number.")
    if lowcut is None or highcut is None:
        valid_params = False
        logger.error("Both lowcut and highcut must be provided for a bandpass filter.")
    if not (np.isfinite(lowcut) and np.isfinite(highcut)):
        valid_params = False
        logger.error("lowcut and highcut must be finite numbers.")
    if lowcut <= 0:
        valid_params = False
        logger.error(f"lowcut must be > 0 Hz. got lowcut={lowcut}")
    if highcut <= 0:
        valid_params = False
        logger.error(f"highcut must be > 0 Hz. got highcut={highcut}")
    if lowcut >= highcut:
        valid_params = False
        logger.error(f"lowcut must be less than highcut. got lowcut={lowcut}, highcut={highcut}")

    # Check frequency values
    nyq  = 0.5*fs
    low  = lowcut/nyq
    high = highcut/nyq
    if not (0 < low < 1):
        valid_params = False
        logger.error(f"Normalized low frequency must be between 0 and 1. lowcut={lowcut} Hz -> {low:.6f}")
    if not (0 < high < 1):
        valid_params = False
        logger.error(
            f"Normalized high frequency must be between 0 and 1. highcut={highcut} Hz -> {high:.6f}")
    if not (low < high):
        valid_params = False
        logger.error(f"Normalized low must be less than normalized high. low={low:.6f}, high={high:.6f}")

    # Check Order parameter
    if order <=0:
        valid_params = False
        logger.error(f"Order must be greater than zero: order={order:i}")
    if order > 20:
        valid_params = False
        logger.error(f"Order too high (>20), may cause numerical instability: order={order:i}")

    return valid_params
def apply_notch_filter(signal_data, fs, notch_freq:int = 60, Q=30.0): # noinspection PyPep8Naming
    """
    Apply a 50 Hz (Europe) or 60 Hz (US) notch filter to EEG/sleep study data.

    Parameters
    ----------
    signal_data : array_like
        Input signal.
    fs : float
        Sampling frequency in Hz.
    notch_freq : 60Hz US and 50Hz for Europe
        "US" for 60 Hz or "EU" for 50 Hz.
    Q : float 20-35 common, <20 wider and frequency drift, 40-50 narrow incomplete filtering
        Quality factor. Higher = narrower notch.

    Returns
    -------
    filtered_signal : ndarray
        Filtered output.
    """

    nyquist = fs/2

    if 0 < notch_freq < nyquist:
        notch_freq = notch_freq
        b, a = iirnotch(w0=notch_freq, Q=Q, fs=fs)
        return_signal = filtfilt(b, a, signal_data)
        logger.info(f'Notch filter applied: notch = {notch_freq}')
    else:
        return_signal = signal_data
        logger.error('Notch filter not applied: Sampling rate too low to apply filter')
    return return_signal

# EDF Classes
class EdfHeader:
    """Class for storing and summarizing EDF header information."""
    # EDF field sizes
    EDF_HEADER_SIZE = 256
    EDF_VERSION_SIZE = 8
    PATIENT_ID_SIZE = 80
    LOCAL_REC_ID_SIZE = 80
    RECORDING_STARTDATE_SIZE = 8
    RECORDING_STARTTIME_SIZE = 8
    NUMBER_OF_HEADER_BYTES = 8
    RESERVE_1_SIZE = 44
    NUMBER_DATA_RECORDS_SIZE = 8
    DATA_RECORD_DURATION_SIZE = 8
    NUMBER_OF_SIGNALS_SIZE = 4
    def __init__(self, *args):
        """Initialize EDF Header.

        Args:
            *args: Either no arguments or 10 arguments matching header fields.
        """
        if len(args) == 0:
            self.edf_ver = 0
            self.patient_id = ""
            self.local_rec_id = ""
            self.recording_startdate = datetime.date(1900, 1, 1)
            self.recording_starttime = datetime.time(12, 0, 0)
            self.num_header_bytes = 0
            self.reserve_1 = 0
            self.num_data_records = 0
            self.data_record_duration = 0.0
            self.num_signals = 0
        elif len(args) == 10:
            (self.edf_ver, self.patient_id, self.local_rec_id, self.recording_startdate,
             self.recording_starttime, self.num_header_bytes, self.reserve_1,
             self.num_data_records, self.data_record_duration, self.num_signals) = args
        else:
            raise ValueError("EdfHeader constructor expects either 0 or 10 arguments.")
    def summary(self):
        """Log a summary of the EDF header information."""
        logger.info("EDF Header Summary:")
        fields = (
            ('EDF Version:', self.edf_ver),
            ('Patient ID:', self.patient_id),
            ('Local Rec. ID:', self.local_rec_id),
            ('Start Date:', self.recording_startdate),
            ('Start Time:', self.recording_starttime),
            ('Num Header Bytes:', self.num_header_bytes),
            ('Reserve 1:', self.reserve_1),
            ('Num Data Records:', self.num_data_records),
            ('Data Record Duration:', self.data_record_duration),
            ('Num Signals:', self.num_signals),
        )

        for label, value in fields:
            logger.info(f"{label:<20} {value}")
    def __str__(self) -> str:
        """String representation of the EDF header."""
        return (f"EDF Header: EDF Version = {self.edf_ver}, ID = {self.patient_id}, "
                f"records = {self.num_data_records}, duration = {self.data_record_duration}, "
                f"signals = {self.num_signals}")
class EdfSignalHeader:
    """Class representing EDF signal header parameters and methods for summarizing."""

    SIGNAL_LABELS_SIZE = 16
    TRANSDUCER_TYPE_SIZE = 80
    PHYSICAL_DIMENSION_SIZE = 8
    PHYSICAL_MIN_SIZE = 8
    PHYSICAL_MAX_SIZE = 8
    DIGITAL_MIN_SIZE = 8
    DIGITAL_MAX_SIZE = 8
    PREFILTERING_SIZE = 80
    SAMPLE_IN_RECORD_SIZE = 8
    RESERVE_2_SIZE = 32
    BYTES_PER_SAMPLE = 2

    def __init__(self, number_of_signals: int):
        """Initialize EdfSignalHeader.
        Args:
            number_of_signals: Number of signals in the EDF file.
        """
        self.number_of_signals  = number_of_signals
        self.signal_labels      = np.empty(number_of_signals, dtype='U16')
        self.transducer_type    = np.empty(number_of_signals, dtype='U80')
        self.physical_dimension = np.empty(number_of_signals, dtype='U8')
        self.physical_min       = np.empty(number_of_signals, dtype='float64')
        self.physical_max       = np.empty(number_of_signals, dtype='float64')
        self.digital_min        = np.empty(number_of_signals, dtype='float64')
        self.digital_max        = np.empty(number_of_signals, dtype='float64')
        self.prefiltering       = np.empty(number_of_signals, dtype='U80')
        self.samples_in_record  = np.empty(number_of_signals, dtype='float64')
        self.reserve_2          = np.empty(number_of_signals, dtype='U32')
    def summary(self):
        """Log a summary of the EDF signal header information."""
        logger.info("EDF Signal Header Summary:")
        header = (
            f"{'Signal Label':<20} {'Unit':<8} {'Phy Min':>10} {'Phy Max':>10} "
            f"{'Dig Min':>10} {'Dig Max':>10} {'Sam/Rec':>10} "
            f"{'Transducer':<30} {'Prefilter':<30}"
        )
        logger.info(header)
        logger.info("-" * len(header))

        for i in range(self.number_of_signals):
            row = (
                f"{self.signal_labels[i]:<20} {self.physical_dimension[i]:<8} "
                f"{self.physical_min[i]:10.2f} {self.physical_max[i]:10.2f} "
                f"{self.digital_min[i]:10.2f} {self.digital_max[i]:10.2f} "
                f"{self.samples_in_record[i]:10.2f} "
                f"{self.transducer_type[i]:<30} {self.prefiltering[i]:<30}"
            )
            logger.info(row)

    # Python
    def __str__(self) -> str:
        """String representation of signal labels."""
        if self.signal_labels.size == 0:
            return "Signal Labels: None"
        return f"Signal Labels: {', '.join(self.signal_labels.tolist())}"
class EdfSignalsStats:
    """Class for computing and storing EDF signal statistics."""
    signal_stats_template = {
        'Samples': None, 'Mean': None, 'Median': None, 'SDev': None,
        'Min': None, 'Max': None, '5th': None, '25th': None,
        '75th': None, '95th': None
    }
    signal_stats_labels = list(signal_stats_template.keys())
    def __init__(self):
        """Initialize an empty EdfSignalsStats object."""
        self.signal_stats: Dict[str, Dict[str, float]] = {}
        self.signal_labels: List[str] = []
    def calculate(self, signals: Dict[str, List[float]]):
        """Compute statistics for each signal.

        Args:
            signals: Dictionary with signal labels as keys and signal data as values.
        """
        self.signal_stats = {}
        self.signal_labels = list(signals.keys())

        stat_funcs = {
            'Samples': lambda x: len(x),
            'Mean': lambda x: float(np.mean(x)),
            'Median': lambda x: float(np.median(x)),
            'SDev': lambda x: float(np.std(x)),
            'Min': lambda x: float(np.min(x)),
            'Max': lambda x: float(np.max(x)),
            '5th': lambda x: float(np.percentile(x, 5)),
            '25th': lambda x: float(np.percentile(x, 25)),
            '75th': lambda x: float(np.percentile(x, 75)),
            '95th': lambda x: float(np.percentile(x, 95)),
        }

        for label in self.signal_labels:
            data = signals[label]
            stats = {key: func(data) for key, func in stat_funcs.items()}
            self.signal_stats[label] = stats

        return self
    @staticmethod
    def convert_dictionary_to_table(signal_keys: List[str], stat_keys: List[str], stat_dict: Dict[str, Dict[str, float]]) -> List[List[float]]:
        """Convert a stats dictionary into a list of lists for easy table display."""
        table = []
        for signal_key in signal_keys:
            row = [stat_dict[signal_key][stat] for stat in stat_keys]
            table.append(row)
        return table
    def summary(self):
        """Print a summary of signal statistics to the logger."""
        if not self.signal_stats:
            logger.info("No statistics have been computed.")
            return

        stat_keys = self.signal_stats_labels
        table = self.convert_dictionary_to_table(self.signal_labels, stat_keys, self.signal_stats)

        header = (
            f"{'Signal':<20} {'Samples':<10} {'Mean':>10} {'Median':>10} {'SDev':>10} "
            f"{'Min':>10} {'Max':>10} {'5th':>10} {'25th':>10} {'75th':>10} {'95th':>10}"
        )
        logger.info("EDF Signal Statistics Summary:")
        logger.info(header)
        logger.info("-" * len(header))

        for i, label in enumerate(self.signal_labels):
            row = table[i]
            logger.info(
                f"{label:<20} "
                f"{int(row[0]):<10} "
                f"{row[1]:10.2f} {row[2]:10.2f} {row[3]:10.2f} "
                f"{row[4]:10.2f} {row[5]:10.2f} "
                f"{row[6]:10.2f} {row[7]:10.2f} {row[8]:10.2f} {row[9]:10.2f}"
            )
    def export_sig_stats_csv(self, file_path: str = None, output_dir: str = "./", time_stamped:bool = False):
        """Export signal statistics to a CSV file.

        Args:
            file_path: Filename for export. If None, a timestamped filename will be generated.
            output_dir: Directory to save file in.
            time_stamped (bool): Adds time string to file name if true
        """
        os.makedirs(output_dir, exist_ok=True)
        if time_stamped:
            file_path = file_path or generate_timestamped_filename("edf_signal_stats", ".csv", output_dir)
        else:
            file_path = file_path or generate_filename("edf_signal_stats", ".csv", output_dir)

        logger.info(f"Exporting signal stats to CSV: {file_path}")

        try:
            with open(file_path, mode='w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(['Signal'] + self.signal_stats_labels)
                for label in self.signal_labels:
                    row = [label] + [self.signal_stats[label][stat] for stat in self.signal_stats_labels]
                    writer.writerow(row)
            logger.info("CSV export successful.")
        except Exception as e:
            logger.error(f"CSV export failed: {e}")
    def export_sig_stats_excel(self, file_path: str = None, output_dir: str = "./", time_stamped:bool = False):
        """Export signal statistics to an Excel file.

        Args:
            file_path: Filename for export. If None, a timestamped filename will be generated.
            output_dir: Directory to save file in.
            time_stamped: if true, add a time stamp to the file name
        """
        os.makedirs(output_dir, exist_ok=True)
        if time_stamped:
            file_path = file_path or generate_timestamped_filename("edf_signal_stats", ".xlsx", output_dir)
        else:
            file_path = file_path or generate_filename("edf_signal_stats", ".xlsx", output_dir)

        logger.info(f"Exporting signal stats to Excel: {file_path}")

        try:
            data = []
            for label in self.signal_labels:
                row = {'Signal': label}
                row.update({stat: self.signal_stats[label][stat] for stat in self.signal_stats_labels})
                data.append(row)

            df = pd.DataFrame(data)
            df.to_excel(file_path, index=False)
            logger.info("Excel export successful.")
        except Exception as e:
            logger.error(f"Excel export failed: {e}")

    # Python
    def __str__(self):
        return f'EDF Signal Stats: {self.signal_labels}'
class EdfSignals:
    """Class for storing and summarizing EDF signal data loaded from an EDF file."""
    BYTES_PER_SAMPLE = 2 # Set to original standard value. May support larger bytes per sample in the future
    signals: Dict[str, List[float]]
    signal_units: Dict[str, str]
    signal_sampling_time: Dict[int, float]
    def __init__(self, signal_labels: List[str], signals_dict:Dict[str,List[float]],
                 signal_sampling_time_dict:Dict[str,float],signal_units_dict:Dict[str,str]):
        """Initialize EdfSignals.

        Args:
            signal_labels: List of signal labels.
        """
        self.signal_labels = signal_labels # Not implemented. Don't use. Used to select signals to load/keep
        self.eeg_signal_labels = self.return_eeg_signals_from_list(signal_labels)
        self.eeg_signal_labels.sort()
        self.signals_dict: Dict[str, List[float]] = signals_dict
        self.signal_units_dict: Dict[str, str] = signal_units_dict
        self.signal_sampling_time_dict:Dict[str,float] = signal_sampling_time_dict
        self.edf_signals_stats = EdfSignalsStats()
        self.output_dir = os.getcwd()

        # Stepped Channel Information Passed in from annotation file
        self.stepped_channel_labels                  = []
        self.stepped_channel_dict: dict[str,Boolean] = {}

        # Compute signal length in seconds
        signal_key                = signal_labels[0]
        signals                   = signals_dict[signal_key]
        sampling_time             = signal_sampling_time_dict[signal_key]
        self.signal_length_in_sec = sampling_time*len(signals)

        # Define maximum number of options for a stepped signal
        self.stepped_signal_cutoff   = 10      # temporary approach to guess continuous signals
        self.stepped_sampling_cutoff = 0.05   # temporary approach to guess continuous signals
        self.stepped_signal_dict     = {}

        # Default colors manually synced between EDF and XML classes
        self.default_stage_colors = {
            'W': '#FFE4B5',  # Light orange
            'Wake': '#FFE4B5',  # Light orange
            'REM': '#FFB6C1',  # Light pink
            'N1': '#D8BFD8',      # Thistle
            'N2': '#B0E0E6',  # Powder blue
            'N3': '#98FB98',  # Pale green
            'N4': '#3CB371',      # Medium sea green (darker than N3)
            'Artifact': '#FA8072'  # Salmon
        }

        # Storage of stepped signals
        self.stepped_signal_list = None
        self.continuous_signal_list = None

        # Setup
    def set_output_dir(self, output_dir: str):
        """Set the directory to use for output files."""
        os.makedirs(output_dir, exist_ok=True)
        self.output_dir = output_dir

    # Return signals
    def return_edf_signal(self, signal_key: str, signal_type: str='Continuous',
                          epoch_width:float|None=None):
        edf_signal = self.signals_dict[signal_key]
        signal_label = signal_key
        signal_type = signal_type
        signal_units = self.signal_units_dict[signal_key]
        signal_sampling_time = self.signal_sampling_time_dict[signal_key]

        if epoch_width is not None:
            signal_obj = EdfSignal(signal_type, signal_label, signal_units,
                                   signal_sampling_time, edf_signal, epoch_width = epoch_width)
        else:
            signal_obj = EdfSignal(signal_type, signal_label, signal_units,
                                  signal_sampling_time, edf_signal)

        return signal_obj
    def return_signal_segment(self, signal_key: str, _signal_type: str, epoch_num, epoch_width):
        """
         Return the signal segment for a given epoch number and epoch width.

         Parameters:
             signal_key (str): Key for the signal in the signal's dictionary.
             _signal_type (str): Type of signal (not used here but passed for potential future logic).
             epoch_num (int): Epoch index (0-based).
             epoch_width (float): Epoch duration in seconds.

         Returns:
             np.ndarray: Segment of the signal for the given epoch.
         """
        edf_signal = self.signals_dict[signal_key]
        sampling_time = self.signal_sampling_time_dict[signal_key]  # in seconds

        # Convert sampling time to sampling frequency
        sampling_frequency = 1.0 / sampling_time

        # Calculate sample indices for the epoch
        start_index = int(epoch_num * epoch_width * sampling_frequency)
        end_index = int((epoch_num + 1) * epoch_width * sampling_frequency)

        # Slice the signal array
        signal_segment = edf_signal[start_index:end_index]

        return signal_segment
    def return_signal_segments(self, signal_key: str, _signal_type: str, epoch_start:int, epoch_end: int, epoch_width:int):
        """
         Return the signal segment for a given epoch number and epoch width.

         Parameters:
             _signal_type (str): Envisioned as a way to label strings. Abandoned the approach, will delete in a future review
             signal_key (str): Key for the signal in the signal's dictionary.
             epoch_width (float): Epoch duration in seconds.
             epoch_start (int): Start epoch
             epoch_end (int): End epoch of segment
             epoch_width (int): Width of epoch in seconds

         Returns:
             np.ndarray: Segment of the signal for the given epoch.
         """
        edf_signal    = self.signals_dict[signal_key]
        sampling_time = self.signal_sampling_time_dict[signal_key]  # in seconds

        # Convert sampling time to sampling frequency
        sampling_frequency = 1.0 / sampling_time


        # Calculate sample indices for the epoch
        start_index   = int(epoch_start * epoch_width * sampling_frequency)
        end_index     = int((epoch_end + 1) * epoch_width * sampling_frequency)

        # Slice the signal array
        signal_segment = edf_signal[start_index:end_index]

        return signal_segment

    # Return signal information
    def return_num_epochs(self, signal_key, epoch_width):
        num_samples = len(self.signals_dict[signal_key])
        signal_sampling_time = self.signal_sampling_time_dict[signal_key]
        max_epochs = math.ceil(float(num_samples*signal_sampling_time)/epoch_width)
        return max_epochs
    def return_num_epochs_from_width(self, epoch_width):
        max_epochs = math.ceil(float(self.signal_length_in_sec )/epoch_width)
        return max_epochs
    def return_signal_length_seconds(self, signal_key):
        num_samples = len(self.signals_dict[signal_key])
        signal_sampling_time = self.signal_sampling_time_dict[signal_key]
        signal_length_seconds = num_samples*signal_sampling_time
        return signal_length_seconds
    @staticmethod
    def return_eeg_signals_from_list(signal_list:List[str]):
        return [s for s in signal_list if 'eeg' in s.lower()]
    def return_stepped_signals_from_list(self, signal_list:List[str]):
        # this is a first pass function that allows other functions to be made. Ideally the stepped channels
        # will be passed in when the annotation file is assigned.

        # signal_type = 'stepped'
        self.stepped_signal_list = []
        if self.stepped_signal_dict is None:
            for signal_key in signal_list:
                sampling_time = self.signal_sampling_time_dict[signal_key]
                # s_segment = self.return_signal_segment(signal_key, signal_type, epoch_num, epoch_width)
                # num_unique_points = len(list(set(s_segment)))
                if sampling_time > self.stepped_sampling_cutoff:
                    self.stepped_signal_list.append(signal_key)
        else:
            for signal_key in signal_list:
                if signal_key in self.stepped_signal_dict.keys():
                    self.stepped_signal_list.append(signal_key)
        return self.stepped_signal_list
    def return_continuous_signals_from_list(self, signal_list:List[str]):
        # Use sampling rate to select continuous signals for spectral analysis
        self.continuous_signal_list = []
        for signal_key in signal_list:
            sampling_time = self.signal_sampling_time_dict[signal_key]
            if sampling_time < self.stepped_sampling_cutoff:
                self.continuous_signal_list.append(signal_key)

        logger.info(f'input list ({signal_list}), continuous ({self.continuous_signal_list})')
        return self.continuous_signal_list
    def return_continuous_signals_for_spectrogram(self, signal_list: List[str]):
        self.continuous_signal_list = []

        for signal_key in signal_list:
            sampling_time = self.signal_sampling_time_dict[signal_key]
            if sampling_time < self.stepped_sampling_cutoff:
                self.continuous_signal_list.append(signal_key)

        return self.continuous_signal_list

    # Calculate
    def calc_edf_signal_stats(self):
        """Calculate statistics for each signal."""
        self.edf_signals_stats = self.edf_signals_stats.calculate(self.signals_dict)
        return self

    # Summarize and export
    def summary(self):
        """Summarize EDF signals using logger."""
        if not self.signals_dict:
            logger.info("No signal data loaded.")
            return

        if not self.edf_signals_stats.signal_stats:
            logger.info("Signal metadata (stats not yet calculated):")
            for label in self.signal_labels:
                samp_time = self.signal_sampling_time_dict[label]
                logger.info(f"{label:<20} Sampling Time: {samp_time:.3f} s")
        else:
            logger.info("Signal summary statistics:")
            self.edf_signals_stats.summary()
    def export_signals_to_txt(self, output_dir: str, edf_file_name:str):
        """
        Exports each signal as a separate .txt file with time-value columns.

        Parameters:
        - output_dir (str): Directory where the signal text files will be saved.
        """
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        for label in (label for label in self.signal_labels if label != ''):
            signal_data = self.signals_dict[label]
            sampling_interval = self.signal_sampling_time_dict[label]
            unit = self.signal_units_dict.get(label, "")

            # Create time array
            time = np.arange(len(signal_data)) * sampling_interval

            # Create file-safe label
            safe_label = label.replace(" ", "_").replace("/", "_").replace("-", "_")
            edf_base = os.path.splitext(os.path.basename(edf_file_name))[0]

            # Construct filename
            filename = f"{edf_base}_{safe_label}.txt"
            filepath = os.path.join(output_dir, filename)

            # Write to file
            with open(filepath, 'w') as f:
                # Write header
                f.write(f"Time (s)\t{label} ({unit})\n")

                # Write data
                for t, v in zip(time, signal):
                    f.write(f"{t:.6f}\t{v:.6f}\n")
    def export_sig_stats_to_csv(self, filename: str = None, time_stamped: bool = False, output_dir:str = None):
        """Export signal statistics to a CSV file.

        Args:
            filename: Output filename. If None, a timestamped filename will be generated.
            time_stamped (bool): add time stamp to file name if true
            output_dir (str): Set output directory
        """
        if not self.edf_signals_stats.signal_stats:
            raise ValueError("Signal stats not computed yet.")

        if output_dir is not None:
            self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        if filename is not None:
            filename = os.path.join(self.output_dir, filename)
        if time_stamped:
            filename = filename or generate_timestamped_filename("edf_signal_stats", ".csv", self.output_dir)
        else:
            filename = filename or generate_filename("edf_signal_stats", ".csv", self.output_dir)
        df = pd.DataFrame.from_dict(self.edf_signals_stats.signal_stats, orient='index')
        df.insert(0, "Unit", [self.signal_units_dict.get(k, '') for k in df.index])
        df.insert(1, "SamplingTime", [self.signal_sampling_time_dict.get(k, '') for k in df.index])

        df.to_csv(filename, index_label="Signal")
        logger.info(f"Signal stats exported to CSV: {filename}")
    def export_sig_stats_to_excel(self, filename: str = None, time_stamped: bool = False, output_dir: str = None):
        """Export signal statistics to an Excel file.

        Args:
            filename (str): Output filename. If None, a timestamped filename will be generated.
            output_dir (str): Sets output directory for writing generated file
            time_stamped (bool): Will add time to filename if set to true
        """
        if not self.edf_signals_stats.signal_stats:
            raise ValueError("Signal stats not computed yet.")
        if output_dir is not None:
            self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        if filename is not None:
            filename = os.path.join(self.output_dir, filename)
        if time_stamped:
            filename = filename or generate_timestamped_filename("edf_signal_stats", ".xlsx", self.output_dir)
        else:
            filename = filename or generate_filename("edf_signal_stats", ".xlsx", self.output_dir)
        df = pd.DataFrame.from_dict(self.edf_signals_stats.signal_stats, orient='index')
        df.insert(0, "Unit", [self.signal_units_dict.get(k, '') for k in df.index])
        df.insert(1, "SamplingTime", [self.signal_sampling_time_dict.get(k, '') for k in df.index])

        df.to_excel(filename, index_label="Signal")

        logger.info(f"Signal stats exported to Excel: {filename}")
    @classmethod
    def from_array(cls, data: np.ndarray, labels: List[str], sampling_time: List[float], units: List[str]):
        """Create EdfSignals object from array data."""

        # Supply signal_sampling_time_dict as empty dict
        obj = cls(labels, signals_dict={}, signal_sampling_time_dict={}, signal_units_dict={})

        for i, label in enumerate(labels):
            obj.signals[label] = data[i, :].tolist()
            obj.signal_sampling_time[i] = sampling_time[i]
            obj.signal_units[label] = units[i]

        return obj

    # Visualization
    def plot_signal_segment(self, signal_key: str, signal_type: str, epoch_num: int, epoch_width: float,
                            parent_widget=None, x_tick_settings:Optional[list[int]] = None, annotation_marker=None,
                            convert_time_f=lambda x:x, time_axis_units='', is_signal_stepped = False,
                            stepped_dict: dict | None = None, turn_xaxis_labels_off = False,
                            filter_param:Optional[list[float]] = None, y_limits:Optional[list[float]] = None,
                            y_axis_units:str|None = None, sleep_stages: Optional[list[dict]] = None, signal_color:str|None = None):
        """
        Plot a signal segment for a given epoch and embed it in a QWidget if provided.

        Parameters:
            annotation_marker (float): Draws a vertical line at the offset time if set
            signal_key (str): Key for the signal in the signal dictionary.
            signal_type (str): Type of the signal.
            epoch_num (int): Epoch index (0-based).
            epoch_width (float): Width of the epoch in seconds.
            parent_widget (QWidget or None): If provided, embed plot in this widget.
            sleep_stages (list[dict]): IF provided, signal segment plots background rectanges in stage asigned colors
            y_axis_units (str): If provided, units added to the y-axis
            signal_color (str): Set signal color
            filter_param (list): Bandpass (low, high), and notch (electrical freq 50 or 60 )
            turn_xaxis_labels_off (bool): Used to create a common x-axis
            x_tick_settings (list[int,int]) Use to set the signal width
            y_limits (list[float,float]) Used to set common y-axis limits across multiple plots
            stepped_dict (dict) Dictionary of stepped signals that includes y-axis values and labels
            is_signal_stepped (bool) Directs to handle y-axis generation to include stepped y-axis values
            time_axis_units (str) Adds units to y-axis values when set
            convert_time_f (function) applied to x-axis values to set labels to predefined units
        """

        # Set Plot defaults
        grid_color                  = 'gray'
        signal_color                = 'blue' if signal_type is None else signal_color
        tick_label_fontsize         = 6.5
        annotation_line_width       = 2
        y_top_bottom_padding_factor = 2
        default_stage_colors        = self.default_stage_colors
        hypnogram_marker_color      = 'purple'
        constant_signal_adj_per     = 0.50

        if x_tick_settings is None:
            x_tick_settings = [5, 1]

        if filter_param is None:
            filter_param = [-1, -1, -1]

        if stepped_dict is None:
            stepped_dict = {}

        if signal_key == '':
            # Create empty signal
            num_points = 100
            signal_segment = [0] * num_points
            sampling_time = epoch_width / num_points
            time_axis = np.arange(len(signal_segment) + 1) * sampling_time
            signal_segment = [0] * (num_points + 1)
            signal_color = grid_color
            logger.info(
                f"EDF Signal - plot_signal_segment: Signal key is empty. Plotting with a generated signal of zeros.")
        else:
            # Get signal and metadata
            signal_segment = self.return_signal_segment(signal_key, signal_type, epoch_num, epoch_width)
            sampling_time  = self.signal_sampling_time_dict[signal_key]
            time_axis      = np.arange(len(signal_segment)) * sampling_time

            # Check if filtering parameters are provided
            filter_test = True in [ x>0 for x in filter_param]
            if filter_test:
                lowcut  = filter_param[0]
                highcut = filter_param[1]
                notch   = filter_param[2]

                if 0 < lowcut < highcut:
                    fs = 1/sampling_time
                    logger.info(
                        f'Setting filtering parameters: fs = {fs}, lowcut = {lowcut}, highcut  = {highcut}, notch = {notch}')

                    signal_segment_np = apply_bandpass_filter(np.array(signal_segment), fs, lowcut, highcut)
                    signal_segment    = signal_segment_np.tolist()
                    logger.info(
                        f'Setting filtering parameters: fs = {fs}, lowcut = {lowcut}, highcut  = {highcut}, notch = {notch}')

                if notch >0:
                    fs = 1 / sampling_time
                    logger.info(f'Filtering {signal_key} notch parameters: notch = {notch}')
                    apply_notch_filter(np.array(signal_segment), fs, notch_freq = notch)

        # Create figure and axis
        fig = Figure(figsize=(12, 2))
        ax = fig.add_subplot(111)

        # ADD SLEEP STAGE RECTANGLES BEFORE PLOTTING THE SIGNAL
        if sleep_stages and signal_key != "":
            # Get the y-axis limits first (we'll need them for rectangle height)
            if is_signal_stepped:
                y_min_temp = 0
                y_max_temp = len(stepped_dict)
            else:
                if y_limits is not None:
                    y_min_temp = y_limits[0]
                    y_max_temp = y_limits[1]
                else:
                    y_min_temp = np.min(signal_segment)
                    y_max_temp = np.max(signal_segment)
                    if y_min_temp == y_max_temp:
                        pass

            # Adjust temporary y limits for a constant signal
            if y_min_temp - y_max_temp == 0:
                temp_val = y_min_temp
                y_min_temp = temp_val - constant_signal_adj_per*temp_val
                y_max_temp = temp_val + constant_signal_adj_per * temp_val

            # Add rectangles for each sleep stage
            for stage_info in sleep_stages:
                start_time = stage_info.get('start_time')
                end_time = stage_info.get('end_time', epoch_width)
                stage_name = stage_info.get('stage', 'Unknown')

                # Get color - use provided color, default for stage, or gray fallback
                if 'color' in stage_info:
                    rect_color = stage_info['color']
                elif stage_name in default_stage_colors:
                    rect_color = default_stage_colors[stage_name]
                else:
                    rect_color = '#D3D3D3'  # Light gray for unknown stages

                # Create rectangle
                width = end_time - start_time
                height = y_max_temp - y_min_temp

                rect = Rectangle(
                    (start_time, y_min_temp),
                    width,
                    height,
                    facecolor=rect_color,
                    alpha=0.99,  # Semi-transparent
                    edgecolor='none',
                    zorder=0  # Put rectangles behind the signal
                )
                ax.add_patch(rect)

        ax.plot(time_axis, signal_segment, color=signal_color, linewidth=1, zorder=2)

        # Format plot
        ax.grid(True, zorder=1)

        # Compute vertical padding (5% headroom above and below)
        if is_signal_stepped:
            # Set y axis range
            y_min = 0
            y_max = len(stepped_dict)
            y_pad = y_max/10
            ax.set_ylim(y_min-y_pad, y_max+y_pad)

            # Set y axis labels
            y_tick_values = range(y_min, y_max, 1)
            y_tick_labels = stepped_dict
            ax.set_yticks(y_tick_values)
            ax.set_yticklabels(y_tick_labels)
            ax.tick_params(axis='y', length=1, width=0.8, direction='in', labelsize=tick_label_fontsize)
        else:
            if y_limits is not None:
                y_min = y_limits[0]
                y_max = y_limits[1]
            else:
                y_min = np.min(signal_segment)
                y_max = np.max(signal_segment)
            y_pad = 0.1 * (y_max - y_min if y_max != y_min else 1)
            # Set y_Axis units
            if y_axis_units is not None:
                ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{int(y)} {y_axis_units}"))
            if turn_xaxis_labels_off:
                # take back the room for labels
                y_top_bottom_padding_factor = 1
                y_pad = 0.03 * (y_max - y_min if y_max != y_min else 1)
            ax.set_ylim(y_min - y_top_bottom_padding_factor*y_pad, y_max + y_pad)
            ax.tick_params(axis='y', length=1, width=0.8, direction='in', labelsize=tick_label_fontsize)


        # Force x limit
        epoch_width     = int(epoch_width)
        major_tick_step = int(x_tick_settings[0])
        minor_tick_step = int(x_tick_settings[1])
        x_pad           = float(minor_tick_step)/4
        ax.set_xlim(-x_pad, epoch_width + x_pad)

        # Set major and minor ticks
        major_ticks = list(range(0, int(epoch_width + 1), int(major_tick_step)))
        minor_ticks = [x for x in range(0, epoch_width + 1, minor_tick_step) if x not in major_ticks]

        # Set tick parameters
        ax.tick_params(axis='x', which='major', direction='in')
        ax.tick_params(axis='x', which='minor', direction='in')

        # Set major and minor ticks
        ax.set_xticks(major_ticks)
        ax.set_xticks(minor_ticks, minor=True)

        # Set labels only for major ticks
        ax.set_xticklabels([f"{convert_time_f(x)}{time_axis_units}" for x in major_ticks],
                               fontsize=tick_label_fontsize)
        if turn_xaxis_labels_off:
            ax.set_xticklabels([])
        else:
            pass
            # ax.set_yticklabels([])

        ax.tick_params(axis='y', labelsize=tick_label_fontsize)

        # Enable grid lines for major and minor ticks
        ax.grid(axis='x', which='major', linestyle='-', linewidth=1, color='gray')
        ax.grid(axis='x', which='minor', linestyle='--', linewidth=0.5, color='darkgray')

        # Remove ticks and labels, but preserve gridlines
        for spine in ax.spines.values():
            spine.set_visible(False)

        # Compute vertical padding (5% headroom above and below)
        if turn_xaxis_labels_off:
            fig.subplots_adjust(left=.03, right=0.99, top=0.92, bottom=0.05)
        else:
            fig.subplots_adjust(left=.03, right=0.99, top=0.93, bottom=0.35)

        if annotation_marker is not None:
            ax.axvline(x=annotation_marker, color=hypnogram_marker_color, linestyle='-', label=f'Set Point: {annotation_marker}',
                       linewidth=annotation_line_width)

        if parent_widget:
            logger.info(f'plot_signal_segment: parent widget found')
            # Create a new Figure Canvas
            canvas = FigureCanvas(fig)
            canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            canvas.updateGeometry()
            canvas.setStyleSheet("background-color: white;")  # Qt background

            canvas.setContextMenuPolicy(Qt.CustomContextMenu)
            canvas.customContextMenuRequested.connect(parent_widget.show_context_menu)

            # Assign figure to parent_widget so save dialog knows what to save
            parent_widget.figure = fig
            parent_widget.canvas_item = canvas


            existing_layout = parent_widget.layout()
            if existing_layout:
                while existing_layout.count():
                    item = existing_layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.setParent(None)
            else:
                existing_layout = QVBoxLayout(parent_widget)
                parent_widget.setLayout(existing_layout)

            existing_layout.setContentsMargins(0, 0, 0, 0)
            existing_layout.addWidget(canvas)

    # Python
    def __str__(self):
        """String representation of the EdfSignals object."""
        if not hasattr(self, 'signals'):
            return "EDF Signals: Initialized with no signals"
        return f"EDF Signals: {', '.join(self.signal_labels)}"
class EdfSignal:
    def __init__(self, signal_type:str, signal_label:str, signal_units:str,
                signal_sampling_time:float, edf_signal:List, epoch_width:float = 30.0):
        self.signal_type:str = signal_type
        self.signal_label:str = signal_label
        self.signal:List = edf_signal
        self.signal_units:str = signal_units
        self.signal_sampling_time:float = signal_sampling_time
        self.output_dir = os.getcwd()

        # Epoch Analysis Width
        self.epoch_width = epoch_width
        pass
    @staticmethod
    def set_output_dir(output_dir: str):
        """Set the directory to use for output files."""
        os.makedirs(output_dir, exist_ok=True)

    # Python
    def __str__(self):
        return f'EDF Signal: {self.signal_type}, {self.signal_label}, # of pts = {len(self.signal)} '
class EdfSignalAnalysis:
    # Intitialize
    def __init__(self, edf_signal_obj:EdfSignal, param_dict:dict[str,str|float|int]|None=None, verbose = False,
                 window_params:list|None=None, n_jobs:int=1, multiprocess:bool = False, filter_param:list=None,
                 noise_detect_param_dict:dict|None=None):
        if param_dict is None:
            param_dict = {}

        self.edf_signal_obj = edf_signal_obj
        self.param_dict = param_dict
        self.completed_analyses = []
        self.verbose = verbose

        # Get multi-taper variables if avaialble
        self.mt_window_params = window_params
        if window_params is None:
            self.mt_window_params = [5,1]
        self.mt_n_jobs = n_jobs
        self.mt_multiprocess = multiprocess

        # Get filter parameters
        self.filter_param = [-1,-1,-1]
        if filter_param is not None:
            self.filter_param = filter_param

        # Get noise detection parameters
        self.noise_mask_dict:dict|None = None
        self.noise_detect_param_dict:dict|None = None
        self.noise_keys:list|None = None
        if noise_detect_param_dict is not None:
            self.noise_detect_param_dict = noise_detect_param_dict
            self.noise_keys = ['delta_time_mask',  'beta_time_mask',
                               'delta_epoch_mask', 'beta_epoch_mask',
                               'union_time_mask',  'intersection_time_mask',
                               'union_epoch_mask', 'intersection_epoch_mask']

    # Methods
    def multitapper_spectrogram(self, ):
        # Multitapper Spectrogram Parameters
        data = np.array(self.edf_signal_obj.signal)       # Numpy signal
        signal_segment = copy.deepcopy(data)
        fs   = 1/self.edf_signal_obj.signal_sampling_time # Sampling frequency in hz

        # Signal Information
        signal_key = self.edf_signal_obj.signal_label
        sampling_time = self.edf_signal_obj.signal_sampling_time

        # Check if filtering parameters are provided
        filter_param = self.filter_param
        filter_test = True in [x > 0 for x in filter_param]
        if filter_test:
            lowcut = filter_param[0]
            highcut = filter_param[1]
            notch = filter_param[2]

            if 0 < lowcut < highcut:
                fs = 1 / sampling_time
                logger.info(
                    f'Setting filtering parameters: fs = {fs}, lowcut = {lowcut}, highcut  = {highcut}, notch = {notch}')
                signal_segment = apply_bandpass_filter(np.array(signal_segment), fs, lowcut, highcut)
                logger.info(
                    f'Setting filtering parameters: fs = {fs}, lowcut = {lowcut}, highcut  = {highcut}, notch = {notch}')

            if notch > 0:
                fs = 1 / sampling_time
                logger.info(f'Filtering {signal_key} notch parameters: notch = {notch}')
                apply_notch_filter(signal_segment, fs, notch_freq=notch)

        # Compute spectrogram
        multi_taper_spectrum_obj = MultitaperSpectrogram(signal_segment, fs,
                                                         window_params=self.mt_window_params,
                                                         n_jobs=self.mt_n_jobs,
                                                         multiprocess=self.mt_multiprocess)
        multi_taper_spectrum_obj.compute_spectrogram()

        # Check for post analysis noise detection
        if self.noise_detect_param_dict is not None:
            epoch_width = self.edf_signal_obj.epoch_width
            noise_mask_dict = self.simple_noise_detection(epoch_width, multi_taper_spectrum_obj.mt_spectrogram,
                                    multi_taper_spectrum_obj.sfreqs,multi_taper_spectrum_obj.stimes,
                                    self.noise_detect_param_dict)
            self.noise_mask_dict = noise_mask_dict

        # Update log
        self.completed_analyses.append('Multitaper Analysis')

        # Write multi taper parameters to
        if self.verbose:
            multi_taper_spectrum_obj.display_spectrogram_props()

        return multi_taper_spectrum_obj
    @staticmethod
    def simple_noise_detection(epoch_width, spectrogram_results, sfreqs, stimes, noise_detect_param_dict):
        """
        Detects noisy epochs based on delta and beta band power.

        Args:
            epoch_width (float): Epoch duration in seconds (e.g., 30)
            spectrogram_results (np.ndarray): Spectrogram data, shape (n_freqs, n_times)
                                              or (n_channels, n_freqs, n_times)
            sfreqs (np.ndarray): Frequency vector
            stimes (np.ndarray): Time vector (in seconds)
            noise_detect_param_dict (dict): Parameters with required keys:
                'apply_noise_detection', 'delta_low', 'delta_high', 'beta_low', 'beta_high',
                'noise_delta_factor', 'noise_beta_factor'

        Returns:
            noise_mask (dict): Dictionary with boolean masks:
                - 'delta_time_mask', 'beta_time_mask'
                - 'delta_epoch_mask', 'beta_epoch_mask'
                - 'union_time_mask', 'union_epoch_mask'
                - 'intersection_time_mask', 'intersection_epoch_mask'
        """
        noise_mask = {}

        # --- User toggle ---
        if  not noise_detect_param_dict:
            logger.info('Noise detection parameters are empty. Skipping noise detection.')
            return noise_mask

        logger.info('Starting simple noise detection.')

        # --- Unpack parameters ---
        noise_delta_low = noise_detect_param_dict['delta_low']
        noise_delta_high = noise_detect_param_dict['delta_high']
        noise_delta_factor = noise_detect_param_dict['delta_factor']
        noise_beta_low = noise_detect_param_dict['beta_low']
        noise_beta_high = noise_detect_param_dict['beta_high']
        noise_beta_factor = noise_detect_param_dict['beta_factor']

        # --- Frequency band masks ---
        delta_freq_mask = (sfreqs >= noise_delta_low) & (sfreqs < noise_delta_high)
        beta_freq_mask = (sfreqs >= noise_beta_low) & (sfreqs < noise_beta_high)

        # --- Handle input shape ---
        if spectrogram_results.ndim == 3:
            power_by_time = np.mean(spectrogram_results, axis=0)  # (n_freqs, n_times)
        elif spectrogram_results.ndim == 2:
            power_by_time = spectrogram_results  # (n_freqs, n_times)
        else:
            raise ValueError("spectrogram_results must be 2D or 3D (channels x freqs x times)")

        # --- Compute band power by time ---
        delta_power_t = np.sum(power_by_time[delta_freq_mask, :], axis=0)
        beta_power_t = np.sum(power_by_time[beta_freq_mask, :], axis=0)

        # --- Compute thresholds ---
        delta_avg = np.mean(delta_power_t)
        beta_avg = np.mean(beta_power_t)
        delta_threshold = noise_delta_factor * delta_avg
        beta_threshold = noise_beta_factor * beta_avg

        logger.info(f"Δ-band avg={delta_avg:.3f}, threshold={delta_threshold:.3f}")
        logger.info(f"β-band avg={beta_avg:.3f}, threshold={beta_threshold:.3f}")

        # --- Spectrogram-resolution masks (True = keep, False = noisy) ---
        delta_time_mask = delta_power_t < delta_threshold
        beta_time_mask = beta_power_t < beta_threshold

        # --- Combined time masks ---
        union_time_mask = delta_time_mask | beta_time_mask  # exclude if noisy in either
        intersection_time_mask = delta_time_mask & beta_time_mask  # exclude only if both noisy

        # --- Epoch-resolution masks ---
        n_epochs = int(np.ceil(stimes[-1] / epoch_width))
        delta_epoch_mask = np.ones(n_epochs, dtype=bool)
        beta_epoch_mask = np.ones(n_epochs, dtype=bool)
        union_epoch_mask = np.ones(n_epochs, dtype=bool)
        intersection_epoch_mask = np.ones(n_epochs, dtype=bool)

        for i in range(n_epochs):
            start_t = i * epoch_width
            end_t = start_t + epoch_width
            epoch_inds = np.where((stimes >= start_t) & (stimes < end_t))[0]
            if len(epoch_inds) == 0:
                continue

            # If any time point is noisy → epoch is noisy
            delta_epoch_mask[i] = np.all(delta_time_mask[epoch_inds])
            beta_epoch_mask[i] = np.all(beta_time_mask[epoch_inds])

            # Union: exclude if *either* band is noisy
            union_epoch_mask[i] = np.all(union_time_mask[epoch_inds])

            # Intersection: exclude only if *both* bands are noisy
            intersection_epoch_mask[i] = np.all(intersection_time_mask[epoch_inds])

        # --- Collect all masks ---
        noise_mask.update({
            'delta_time_mask': delta_time_mask,
            'beta_time_mask': beta_time_mask,
            'delta_epoch_mask': delta_epoch_mask,
            'beta_epoch_mask': beta_epoch_mask,
            'union_time_mask': union_time_mask,
            'intersection_time_mask': intersection_time_mask,
            'union_epoch_mask': union_epoch_mask,
            'intersection_epoch_mask': intersection_epoch_mask,
        })

        # Summarize to logger:
        mask_length = float(len(delta_time_mask))
        num_scoring_epochs = np.ceil(stimes[-1])
        for key in noise_mask.keys():
            m_length = mask_length if 'epoch' not in key else num_scoring_epochs
            sepochs_percent_excluded = np.sum(np.logical_not(noise_mask[key]))/m_length
            sepochs_excluded = np.sum(np.logical_not(noise_mask[key]))
            logger.info(f'{key}: spectral epochs excluded = {sepochs_excluded}, % excluded = {sepochs_percent_excluded:.2%}')

        return noise_mask

    # Python
    def __str__(self):
        return f'EDF Signal Analysis: {self.param_dict}'
class EdfFile:
    """Class for loading and processing information stored in an EDF file."""
    # Define class variables
    def __init__(self, file_path: str = None, signal_labels: list = None, epochs: list = None,
            verbose: bool = True, output_dir: str = str(os.getcwd())):

        """Initialize an EdfFile instance.

            Args:
                file_path (str): Path to the EDF file.
                signal_labels (list): List of signal labels to load.
                epochs (list): Epoch information (optional).
                verbose (bool): Enable verbose logging.
                output_dir (str): Directory to use for output files.
        """
        self.file_w_path = file_path or ''
        self.file_name = os.path.basename(file_path) if file_path else ''
        self.signal_labels = signal_labels or []  # not implemented yet
        self.epochs = epochs

        self._file_set = bool(file_path)
        self._signal_labels_set = signal_labels is not None
        self._epochs_set = epochs is not None

        self.edf_header = EdfHeader()
        self.edf_signal_header = None
        self.edf_signals = None

        self.output_dir = output_dir
        self.verbose = verbose

        if not verbose:
            logger.setLevel(logging.CRITICAL + 1)
    def set_output_dir(self, output_dir: str):
        """Set the directory to use for output files."""
        os.makedirs(output_dir, exist_ok=True)
        self.output_dir = output_dir
    # Load Functions
    def load_header(self, f) -> EdfHeader:
        """Load the EDF header from an open file object."""
        h = self.edf_header

        def read_str(size): return f.read(size).decode().strip()

        h.edf_ver = read_str(h.EDF_VERSION_SIZE)
        h.patient_id = read_str(h.PATIENT_ID_SIZE)
        h.local_rec_id = read_str(h.LOCAL_REC_ID_SIZE)
        h.recording_startdate = read_str(h.RECORDING_STARTDATE_SIZE)
        h.recording_starttime = read_str(h.RECORDING_STARTTIME_SIZE)
        h.num_header_bytes = int(read_str(h.NUMBER_OF_HEADER_BYTES))
        h.reserve_1 = read_str(h.RESERVE_1_SIZE)
        h.num_data_records = int(read_str(h.NUMBER_DATA_RECORDS_SIZE))
        h.data_record_duration = float(read_str(h.DATA_RECORD_DURATION_SIZE))
        h.num_signals = int(read_str(h.NUMBER_OF_SIGNALS_SIZE))

        return h
    @staticmethod
    def load_signal_header(f, number_of_signals: int) -> EdfSignalHeader:
        """Load EDF signal header information from an open file object."""
        sh = EdfSignalHeader(number_of_signals)

        var_sizes = np.array([
            sh.SIGNAL_LABELS_SIZE, sh.TRANSDUCER_TYPE_SIZE, sh.PHYSICAL_DIMENSION_SIZE,
            sh.PHYSICAL_MIN_SIZE, sh.PHYSICAL_MAX_SIZE, sh.DIGITAL_MIN_SIZE,
            sh.DIGITAL_MAX_SIZE, sh.PREFILTERING_SIZE, sh.SAMPLE_IN_RECORD_SIZE,
            sh.RESERVE_2_SIZE
        ])

        headers = []
        for size in var_sizes:
            block = f.read(size * number_of_signals).decode()
            fields = [block[i * size:(i + 1) * size].strip() for i in range(number_of_signals)]
            headers.append(fields)

        sh.signal_labels = headers[0]
        sh.tranducer_type = headers[1]
        sh.physical_dimension = headers[2]
        sh.physical_min = list(map(float, headers[3]))
        sh.physical_max = list(map(float, headers[4]))
        sh.digital_min = list(map(int, headers[5]))
        sh.digital_max = list(map(int, headers[6]))
        sh.prefiltering = headers[7]
        sh.samples_in_record = list(map(int, headers[8]))
        sh.reserve_2 = headers[9]

        return sh
    def load_signals(self, f) -> EdfSignals:
        """Load signals from an open EDF file object and convert to physical units."""
        n_records = self.edf_header.num_data_records
        n_signals = self.edf_header.num_signals
        duration = self.edf_header.data_record_duration
        samples_per_rec = self.edf_signal_header.samples_in_record
        bytes_per_sample = EdfSignals.BYTES_PER_SAMPLE
        labels = self.edf_signal_header.signal_labels

        raw_data = [np.zeros(n_records * samples_per_rec[i], dtype=np.int16) for i in range(n_signals)]

        for record_idx in range(n_records):
            for sig_idx in range(n_signals):
                n_samples = samples_per_rec[sig_idx]
                raw_bytes = f.read(n_samples * bytes_per_sample)
                data = np.frombuffer(raw_bytes, dtype='<i2')
                start = record_idx * n_samples
                raw_data[sig_idx][start:start + n_samples] = data

        # Create Signal Dictionary
        signals_dict = {}
        for i, label in enumerate(labels):
            digital = raw_data[i]
            dig_min, dig_max = self.edf_signal_header.digital_min[i], self.edf_signal_header.digital_max[i]
            phy_min, phy_max = self.edf_signal_header.physical_min[i], self.edf_signal_header.physical_max[i]
            scale = (phy_max - phy_min) / (dig_max - dig_min)
            physical = (digital - dig_min) * scale + phy_min
            signals_dict[label] = physical

        # Create signal sampling time dict
        signal_sampling_time_dict = {}
        signal_sampling_time = [duration / s if s else 0.0 for s in samples_per_rec]
        for i in range(len(signal_sampling_time)):
            signal_sampling_time_dict[labels[i]] = signal_sampling_time[i]

        # Create Signal Unit Dictionary
        signal_units_dict = {}
        for i, label in enumerate(labels):
            if i < len(self.edf_signal_header.physical_dimension):
                signal_units_dict[label] = self.edf_signal_header.physical_dimension[i]

        signal_obj = \
            EdfSignals(labels, signals_dict, signal_sampling_time_dict, signal_units_dict)

        return signal_obj
    def load(self):
        """Fully load the EDF file, including header, signal header, and signals."""
        if not self._file_set:
            raise ValueError("File path not set.")

        if self.verbose:
            logger.info(f"Loading complete EDF file: {self.file_w_path}")

        try:
            with open(self.file_w_path, 'rb') as f:
                self.edf_header = self.load_header(f)
                self.edf_signal_header = self.load_signal_header(f, self.edf_header.num_signals)
                self.edf_signals = self.load_signals(f)
        except Exception as e:
            raise RuntimeError(f"Failed to fully load EDF file: {e}")
        return self
    # Calculate
    def calculate_signal_stats(self):
        """Calculate statistics for each loaded signal."""
        if not self.edf_signals:
            raise RuntimeError("Signals not loaded yet.")
        self.edf_signals.calc_edf_signal_stats()
    # Return and exports
    def return_edf_header(self) -> EdfHeader:
        """Load and return the EDF header only."""
        if not self._file_set:
            raise ValueError("File path not set.")

        if self.verbose:
            logger.info(f"Loading EDF header: {self.file_w_path}")

        try:
            with open(self.file_w_path, 'rb') as f:
                self.edf_header = self.load_header(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load EDF header: {e}")

        return self.edf_header
    def return_edf_and_signal_headers(self):
        """Load and return both EDF header and signal header."""
        if not self._file_set:
            raise ValueError("File path not set.")

        if self.verbose:
            logger.info(f"Loading EDF and signal headers: {self.file_w_path}")

        try:
            with open(self.file_w_path, 'rb') as f:
                self.edf_header = self.load_header(f)
                self.edf_signal_header = self.load_signal_header(f, self.edf_header.num_signals)
        except Exception as e:
            raise RuntimeError(f"Failed to load EDF headers: {e}")

        return self.edf_header, self.edf_signal_header
    # utilities
    def export_summary_to_json(self, filename: str = None, time_stamped: bool = False, output_dir: str = None):
        """Export a summary of the EDF file contents to a JSON file."""
        if not self.edf_signals:
            raise RuntimeError("Signals not loaded.")
        if output_dir is not None:
            self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        if filename is not None:
            filename = os.path.join(self.output_dir, filename)
        if time_stamped:
            filename = (filename or
                        generate_timestamped_filename("edf_summary", ".json", self.output_dir))
        else:
            filename =  (filename
                         or generate_filename("edf_summary", ".json", self.output_dir))
        summary = {
            "header": vars(self.edf_header),
            "signal_header": vars(self.edf_signal_header),
            "signal_stats": self.edf_signals.edf_signals_stats.signal_stats
        }

        serializable_summary = convert_to_serializable(summary)

        with open(filename, "w") as f:
            json.dump(serializable_summary, f, indent=4)

        logger.info(f"Exported summary to {filename}")
    def summary(self):
        """Print a summary of the EDF file contents to the logger."""
        if self.edf_header:
            logger.info("EDF Header Summary:")
            self.edf_header.summary()

        if self.edf_signal_header:
            logger.info("Signal Header Summary:")
            self.edf_signal_header.summary()

        if self.edf_signals and self.edf_signals.signals_dict:
            logger.info("Signal Data Summary:")
            self.edf_signals.summary()
    def __str__(self):
        return f'EDF File: {self.file_w_path}'

# Main
def main():
    """Less than complete testing"""

    # Test Data
    EDF_FILE_PATH  = "/home/dennis/PycharmProjects/EdfFile/sampleEdfFiles/"
    EDF_FILE_NAME  = "/home/dennis/PycharmProjects/EdfFile/sample.edf"
    EDF_FILE_NAME2 = "sample2.edf"
    EDF_FILE_NAME3 = "SC4001E0-PSG.edf"


    # -----------------------------------------------------------------------
    # test edf class with file 1
    edf_file_name = EDF_FILE_NAME
    edf_file_class = EdfFile(edf_file_name)
    edf_file_class = edf_file_class.load()
    logger.info('\n-----------------------------------')
    logger.info('Use name only')
    edf_file_class.summary()
    edf_file_class.calculate_signal_stats()
    edf_file_class.set_output_dir("./exports")
    edf_file_class.export_summary_to_json('edf_summary.json')

    #-----------------------------------------------------------------------
    # test edf class signal load with file 3 and file path
    edf_file_name3   = EDF_FILE_NAME3
    edf_file_path    = EDF_FILE_PATH
    edf_file_class3  = EdfFile(os.path.join(edf_file_path,edf_file_name3))
    edf_file_class3  = edf_file_class3.load()
    logger.info('\n-----------------------------------')
    logger.info('use name and path')
    edf_file_class3.summary()

    #-----------------------------------------------------------------------
    # test edf class with file 2 with file path
    edf_file_name2  = EDF_FILE_NAME2
    edf_file_path   = EDF_FILE_PATH
    edf_file_class2 = EdfFile(os.path.join(edf_file_path, edf_file_name2))
    edf_file_class2 = edf_file_class2.load()
    logger.info('\n-----------------------------------')
    logger.info('Use name and path')
    edf_file_class2.summary()

    #-----------------------------------------------------------------------
    # test edf class with file 2 with file path
    edf_file_name4   = 'learn-nsrr01.edf'
    edf_file_path4   = '/home/dennis/PycharmProjects/EdfFile/tutorial/edfs'
    edf_file_class4  = EdfFile(os.path.join(edf_file_path4, edf_file_name4))
    edf_file_class4  = edf_file_class4.load()
    edf_file_class4.edf_signals  = edf_file_class4.edf_signals.calc_edf_signal_stats()
    logger.info('\n-----------------------------------')
    logger.info('NSRR Example')
    edf_file_class4.summary()

    edf_file = EdfFile(os.path.join(edf_file_path4, edf_file_name4))
    edf_file.load()
    edf_file.calculate_signal_stats()

    # Export to CSV
    edf_file.edf_signals.output_dir = "./exports/edf_stats/"
    edf_file.edf_signals.export_sig_stats_to_csv()
    edf_file.edf_signals.export_sig_stats_to_csv(str(Path("signal_stats.csv")))

    # Export to a specific directory
    edf_file.edf_signals.output_dir = os.path.join(".", "exports", "edf_stats")
    edf_file.set_output_dir(str(Path("./exports/json/")))
    edf_file.export_summary_to_json()
    edf_file.edf_signals.set_output_dir(str(Path("./exports/json/")))
    edf_file.edf_signals.export_sig_stats_to_csv(str(Path("signal_stats.csv")))
    edf_file.edf_signals.export_sig_stats_to_excel(str(Path("signal_stats.xlsx")))

    # 1. Define signal parameters
    fs = 1000  # Sampling frequency in Hz
    t = np.linspace(0, 1, fs, endpoint=False)  # 1 second of signal
    f_signal = 10  # Desired signal frequency in Hz
    f_noise = 60  # Noise frequency to remove (e.g., power line hum) in Hz

    # 2. Create a synthetic signal with noise
    clean_signal = np.sin(2 * np.pi * f_signal * t)
    noisy_signal = clean_signal + 0.5 * np.sin(2 * np.pi * f_noise * t)  # Add 60 Hz noise

    # 3. Design the notch filter
    # w0: normalized frequency to remove (f_noise / (fs/2))
    # Q: Quality factor, determines bandwidth of the notch
    w0 = f_noise / (fs / 2)
    Q = 30  # A higher Q value results in a narrower notch

    b, a = signal.iirnotch(w0, Q)

    # 4. Apply the filter to the noisy signal
    filtered_signal = signal.filtfilt(b, a, noisy_signal)

    # 5. Plot the results for comparison
    plt.figure(figsize=(12, 6))

    plt.subplot(3, 1, 1)
    plt.plot(t, clean_signal)
    plt.title('Clean Signal')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')

    plt.subplot(3, 1, 2)
    plt.plot(t, noisy_signal)
    plt.title(f'Noisy Signal (with {f_noise} Hz hum)')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')

    plt.subplot(3, 1, 3)
    plt.plot(t, filtered_signal)
    plt.title(f'Filtered Signal (60 Hz notch)')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')

    plt.tight_layout()
    plt.show()

    # Optional: Plot frequency response of the filter
    w, h = signal.freqz(b, a, worN=8000)
    plt.figure()
    plt.plot((fs * 0.5 / np.pi) * w, abs(h))
    plt.title('Notch Filter Frequency Response')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Gain')
    plt.grid()
    plt.show()
if __name__ == "__main__":
    main()