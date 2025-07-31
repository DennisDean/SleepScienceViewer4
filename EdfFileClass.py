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
"""


# Import Modules
import os
import logging
from typing import List, Dict
import datetime
import pandas as pd
import csv
import json
from pathlib import Path
from multitaper_spectrogram_python_class import MultitaperSpectrogram
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtWidgets import QVBoxLayout, QSizePolicy
import numpy as np
from matplotlib.ticker import MultipleLocator
import math

# Set up logging
logger = logging.getLogger(__name__)

# Utilities
def generate_timestamped_filename(prefix: str, ext: str = ".csv", output_dir: str = "") -> str:
    """Add a time stamp to a generated file

    prefix: str: File name
    ext: str = File type string
    output_dir: str = Output directory if set)
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}{ext}"
    return os.path.join(output_dir, filename) if output_dir else filename
def generate_filename(prefix: str, ext: str = ".csv", output_dir: str = "") -> str:
    """Add a time stamp to a generated file

    prefix: str: File name
    ext: str = File type string
    output_dir: str = Output directory if set)
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
        self.number_of_signals = number_of_signals
        self.signal_labels = np.empty(number_of_signals, dtype='U16')
        self.transducer_type = np.empty(number_of_signals, dtype='U80')
        self.physical_dimension = np.empty(number_of_signals, dtype='U8')
        self.physical_min = np.empty(number_of_signals, dtype='float64')
        self.physical_max = np.empty(number_of_signals, dtype='float64')
        self.digital_min = np.empty(number_of_signals, dtype='float64')
        self.digital_max = np.empty(number_of_signals, dtype='float64')
        self.prefiltering = np.empty(number_of_signals, dtype='U80')
        self.samples_in_record = np.empty(number_of_signals, dtype='float64')
        self.reserve_2 = np.empty(number_of_signals, dtype='U32')
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
    def convert_dictionary_to_table(self, signal_keys: List[str], stat_keys: List[str], stat_dict: Dict[str, Dict[str, float]]) -> List[List[float]]:
        """Convert a stats dictionary into a list of lists for easy table display."""
        table = []
        for signal in signal_keys:
            row = [stat_dict[signal][stat] for stat in stat_keys]
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
        """
        os.makedirs(output_dir, exist_ok=True)
        if time_stamped:
            file_path = file_path or generate_timestamped_filename("edf_signal_stats", ".csv", output_dir)
        else:
            file_path = file_path or generate_filename("edf_signal_stats", ".csv", output_dir, time_stamped=False)

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
class EdfSignals:
    """Class for storing and summarizing EDF signal data loaded from an EDF file."""
    BYTES_PER_SAMPLE = 2
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

        # Compute signal length in seconds
        signal_key                = signal_labels[0]
        signals                   = signals_dict[signal_key]
        sampling_time             = signal_sampling_time_dict[signal_key]
        self.signal_length_in_sec = sampling_time*len(signals)

        # Define maximum number of options for a stepped signal
        self.stepped_signal_cutoff  = 10
        self.stepped_sampling_cutoff = 0.05
    # Setup
    def set_output_dir(self, output_dir: str):
        """Set the directory to use for output files."""
        os.makedirs(output_dir, exist_ok=True)
        self.output_dir = output_dir
    # Return signals
    def return_edf_signal(self, signal_key: str, signal_type: str):
        edf_signal = self.signals_dict[signal_key]
        signal_label = signal_key
        signal_type = signal_type
        signal_units = self.signal_units_dict[signal_key]
        signal_sampling_time = self.signal_sampling_time_dict[signal_key]

        signal_obj = EdfSignal(signal_type, signal_label, signal_units,
                               signal_sampling_time, edf_signal)

        return signal_obj
    def return_signal_segment(self, signal_key: str, signal_type: str, epoch_num, epoch_width):
        """
         Return the signal segment for a given epoch number and epoch width.

         Parameters:
             signal_key (str): Key for the signal in the signals dictionary.
             signal_type (str): Type of signal (not used here but passed for potential future logic).
             epoch_num (int): Epoch index (0-based).
             epoch_width (float): Epoch duration in seconds.

         Returns:
             np.ndarray: Segment of the signal for the given epoch.
         """
        edf_signal = self.signals_dict[signal_key]
        signal_units = self.signal_units_dict[signal_key]
        sampling_time = self.signal_sampling_time_dict[signal_key]  # in seconds

        # Convert sampling time to sampling frequency
        sampling_frequency = 1.0 / sampling_time

        # Calculate sample indices for the epoch
        start_index = int(epoch_num * epoch_width * sampling_frequency)
        end_index = int((epoch_num + 1) * epoch_width * sampling_frequency)

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
    def return_signal_length_seconds(self, signal_key, epoch_width):
        num_samples = len(self.signals_dict[signal_key])
        signal_sampling_time = self.signal_sampling_time_dict[signal_key]
        signal_length_seconds = num_samples*signal_sampling_time
        return signal_length_seconds
    def return_eeg_signals_from_list(self, signal_list:List[str]):
        return [s for s in signal_list if 'eeg' in s.lower()]
    def return_stepped_signals_from_list(self, signal_list:List[str]):
        signal_type = 'stepped'
        epoch_num = 1
        epoch_width = 30
        self.stepped_signal_list = []
        for signal_key in signal_list:
            sampling_time = self.signal_sampling_time_dict[signal_key]
            # s_segment = self.return_signal_segment(signal_key, signal_type, epoch_num, epoch_width)
            # num_unique_points = len(list(set(s_segment)))
            if sampling_time > self.stepped_sampling_cutoff:
                self.stepped_signal_list.append(signal_key)
        return self.stepped_signal_list
    def return_continuous_signals_from_list(self, signal_list:List[str]):
        signal_type = 'stepped'
        epoch_num = 1
        epoch_width = 30
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
    def export_signals_to_txt(self, output_dir: str):
        """
        Exports each signal as a separate .txt file with time-value columns.

        Parameters:
        - output_dir (str): Directory where the signal text files will be saved.
        """
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        for label in self.signal_labels:
            signal = self.signals_dict[label]
            sampling_interval = self.signal_sampling_time[label]
            unit = self.signal_units.get(label, "")

            # Create time array
            time = np.arange(len(signal)) * sampling_interval

            # Create file-safe label
            safe_label = label.replace(" ", "_").replace("/", "_").replace("-", "_")
            edf_base = os.path.splitext(os.path.basename(self.source_edf_filename))[0]

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
        """
        if not self.edf_signals_stats.signal_stats:
            raise ValueError("Signal stats not computed yet.")

        if output_dir != None:
            self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        if filename != None:
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
            filename: Output filename. If None, a timestamped filename will be generated.
        """
        if not self.edf_signals_stats.signal_stats:
            raise ValueError("Signal stats not computed yet.")
        if output_dir != None:
            self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        if filename != None:
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
        """Create EdfSignals object from array data.

        Args:
            data: 2D numpy array with shape (n_signals, n_samples).
            labels: Signal labels.
            sampling_time: Sampling times for each signal.
            units: Units for each signal.

        Returns:
            EdfSignals instance.
        """
        obj = cls(labels)
        for i, label in enumerate(labels):
            obj.signals[label] = data[i, :].tolist()
            obj.signal_sampling_time[i] = sampling_time[i]
            obj.signal_units[label] = units[i]
        return obj
    # Visualization
    def plot_signal_segment(self, signal_key: str, signal_type: str, epoch_num: int, epoch_width: float,
                            parent_widget=None, x_tick_settings:tuple[int, int] = [5,1]):
        """
        Plot a signal segment for a given epoch and embed it in a QWidget if provided.

        Parameters:
            signal_key (str): Key for the signal in the signal dictionary.
            signal_type (str): Type of the signal.
            epoch_num (int): Epoch index (0-based).
            epoch_width (float): Width of the epoch in seconds.
            parent_widget (QWidget or None): If provided, embed plot in this widget.
        """

        # Set Plot defaults
        grid_color = 'gray'
        signal_color = 'blue'

        if signal_key == '':
            # Create empty signal
            sampling_time   = 0
            signal_units    = ''
            num_points      = 100
            signal_segment  = [0]*num_points
            sampling_time   = epoch_width/num_points
            time_axis       = np.arange(len(signal_segment)+1) * sampling_time
            signal_segment  = [0] * (num_points+1)
            signal_color    = grid_color
            logger.info(f"EDF Signal - plot_signal_segment: Signal key is empty. Plotting with a generated signal of zeros.")
        else:
            # Get signal and metadata
            signal_segment = self.return_signal_segment(signal_key, signal_type, epoch_num, epoch_width)
            sampling_time  = self.signal_sampling_time_dict[signal_key]
            signal_units   = self.signal_units_dict[signal_key]
            time_axis      = np.arange(len(signal_segment)) * sampling_time

        # Create figure and axis
        fig = Figure(figsize=(12, 2))
        ax = fig.add_subplot(111)
        ax.plot(time_axis, signal_segment, color= signal_color, linewidth=1)

        # Format plot
        ax.set_title(f"{signal_key} - Epoch {epoch_num}")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel(f"Amplitude ({signal_units})")
        ax.grid(True)

        # Compute vertical padding (5% headroom above and below)
        y_min = np.min(signal_segment)
        y_max = np.max(signal_segment)
        y_pad = 0.1 * (y_max - y_min if y_max != y_min else 1)
        ax.set_ylim(y_min - y_pad, y_max + y_pad)

        # Force x limit
        x_pad = x_tick_settings[1] / 2
        ax.set_xlim(-x_pad, epoch_width + x_pad)

        # Set x-axis grid lines (5s major, 2s minor)
        ax.xaxis.set_minor_locator(MultipleLocator(x_tick_settings[1]))
        ax.xaxis.set_major_locator(MultipleLocator(x_tick_settings[0]))
        ax.grid(axis='x', which='major', linestyle='-', linewidth=1, color='gray')
        # ax.grid(axis='x', which='minor', linestyle=':', linewidth=0.5, color='lightgray')

        # Remove ticks and labels, but preserve gridlines
        # ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)

        # Compute vertical padding (5% headroom above and below)
        fig.subplots_adjust(left=0, right=1, top=0.95, bottom=0.05)

        if parent_widget:
            logger.info(f'plot_signal_segment: parent widget found')
            # Create a new Figure Canvas
            canvas = FigureCanvas(fig)
            canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            canvas.updateGeometry()
            canvas.setStyleSheet("background-color: white;")  # Qt background

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

            """
            canvas = FigureCanvas(fig)
            canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            canvas.updateGeometry()

            existing_layout = parent_widget.layout()
            if existing_layout:
                logger.info(f'plot_signal_segment: existing layout found')
                while existing_layout.count():
                    item = existing_layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.setParent(None)
            else:
                logger.info(f'plot_signal_segment: existing layout NOT found')
                existing_layout = QVBoxLayout(parent_widget)
                parent_widget.setLayout(existing_layout)

            existing_layout.setContentsMargins(0, 0, 0, 0)
            existing_layout.addWidget(canvas)
            """
        else:
            pass
            # logger.warning("No parent_widget provided — opening standalone plot window.")
            # Standalone display
            # plt.figure(figsize=(10, 4))
            # plt.plot(time_axis, signal_segment, color='blue', linewidth=1)
            # plt.xlabel("Time (s)")
            # plt.ylabel(f"Amplitude ({signal_units})")
            # plt.title(f"{signal_key} - Epoch {epoch_num}")
            # plt.grid(True)
            # plt.tight_layout()
            # plt.show()
    # Utilities
    def __str__(self):
        """String representation of the EdfSignals object."""
        if not self.signals:
            return "EDF Signals: Initialized with no signals"
        return f"EDF Signals: {', '.join(self.signal_labels)}"
class EdfSignal:
    def __init__(self, signal_type:str, signal_label:str, signal_units:str,
                signal_sampling_time:float, edf_signal:List):
        self.signal_type:str = signal_type
        self.signal_label:str = signal_label
        self.signal:List = edf_signal
        self.signal_units:str = signal_units
        self.signal_sampling_time:float = signal_sampling_time
        self.output_dir = os.getcwd()
        pass
    def set_output_dir(self, output_dir: str):
        """Set the directory to use for output files."""
        os.makedirs(output_dir, exist_ok=True)
    def __str__(self):
        return f'EDF Signal: {self.signal_type}, {self.signal_label}, # of pts = {len(self.signal)} '
class EdfSignalAnalysis:
    def __init__(self, edf_signal_ob:EdfSignal, param_dict:dict[str,str|float|int]={}, verbose = False):
        self.edf_signal_ob = edf_signal_ob
        self.param_dict = param_dict
        self.completed_analyses = []
        self.verbose = verbose
    def multitapper_spectrogram(self, param_dict:dict[str,str|float|int]={}):
        # Multitapper Spectrogram Parameters
        data = np.array(self.edf_signal_ob.signal)       # Numpy signal
        fs   = 1/self.edf_signal_ob.signal_sampling_time # Sampling frequency in hz

        frequency_range = None
        time_bandwidth = 5
        num_tapers     = None
        window_params  = None
        min_nfft       = 0
        detrend_opt    = 'linear'
        multiprocess   = False
        n_jobs         = None
        weighting      = 'unity'
        plot_on        = True
        return_fig     = False
        clim_scale     = True
        verbose        = True
        xyflip         = False
        ax             = None

        # Compute spectrogram
        multi_taper_spectrum_obj = MultitaperSpectrogram(data, fs)
        multi_taper_spectrum_obj.compute_spectrogram()
        self.completed_analyses.append('Multitaper Analysis')

        # Write multi taper parameters to
        if self.verbose == True:
            multi_taper_spectrum_obj.display_spectrogram_props()

        return multi_taper_spectrum_obj
    def __str__(self):
        return f'EDF Signal Analysis: {self.edf_signal_obj}'
class EdfFile:
    """Class for loading and processing information stored in an EDF file."""
    # Define class variables
    def __init__(self, file_path: str = None, signal_labels: list = None, epochs: any = None,
            verbose: bool = True, time_stamped_files: bool = False, output_dir: str = os.getcwd()):

        """Initialize an EdfFile instance.

            Args:
                file_path: Path to the EDF file.
                signal_labels: List of signal labels to load.
                epochs: Epoch information (optional).
                verbose: Enable verbose logging.
                output_dir: Directory to use for output files.
        """
        self.file_w_path = file_path or ''
        self.file_name = os.path.basename(file_path) if file_path else ''
        self.signal_labels = signal_labels or []
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
    def load_signal_header(self, f, number_of_signals: int) -> EdfSignalHeader:
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
        if output_dir != None:
            self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        if filename != None:
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
    DEBUG = 0

    # Test Data
    EDF_FILE_PATH  = "/home/dennis/PycharmProjects/EdfFile/sampleEdfFiles/"
    EDF_FILE_NAME  = "/home/dennis/PycharmProjects/EdfFile/sample.edf"
    EDF_FILE_NAME2 = "sample2.edf"
    EDF_FILE_NAME3 = "SC4001E0-PSG.edf"
    EDF_FILE_NAME4 = "SC4001EC-Hypnogram.edf"

    edf = EdfFile("sample.edf")
    edf.load()
    edf.calculate_signal_stats()
    edf.summary()

    # -----------------------------------------------------------------------
    # test edf class with file 1
    edf_file_name = EDF_FILE_NAME
    edf_file_class = EdfFile(edf_file_name)
    edf_file_class = edf_file_class.load()
    logger.info('\n-----------------------------------')
    logger.info('Use name only')
    edf_file_class.summary()
    edf_file_class.calculate_signal_stats()
    edf_file_class.set_output_dir(Path("./exports"))
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

    # Simulate EDF signals
    signals = {
        'EEG Fz-Cz': np.random.normal(0, 10, 1000),
        'EEG Pz-Oz': np.random.normal(0, 5, 1000),
    }

    edf_file = EdfFile(os.path.join(edf_file_path4, edf_file_name4))
    edf_file.load()
    edf_file.calculate_signal_stats()

    # Export to CSV
    edf_file.edf_signals.output_dir = Path("./exports/edf_stats/")
    edf_file.edf_signals.export_sig_stats_to_csv()
    edf_file.edf_signals.export_sig_stats_to_csv(Path("signal_stats.csv"))

    # Export to a specific directory
    edf_file.edf_signals.output_dir=Path("./exports/edf_stats/")
    edf_file.set_output_dir(Path("./exports/json/"))
    edf_file.export_summary_to_json()
    edf_file.edf_signals.set_output_dir(Path("./exports/json/"))
    edf_file.edf_signals.export_sig_stats_to_csv(Path("signal_stats.csv"))
    edf_file.edf_signals.export_sig_stats_to_excel(Path("signal_stats.xlsx"))
if __name__ == "__main__":
    main()