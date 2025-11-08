# Integrating computation with in the Sleep Science Viewer Example

""""
This code is companion to the paper:
        "Sleep Neurophysiological Dynamics Through the Lens of Multitaper Spectral Analysis"
           Michael J. Prerau, Ritchie E. Brown, Matt T. Bianchi, Jeffrey M. Ellenbogen, Patrick L. Purdon
           December 7, 2016 : 60-92
           DOI: 10.1152/physiol.00062.2015
         which should be cited for academic use of this code.

         A full tutorial on the multitaper spectrogram can be found at: # https://www.sleepEEG.org/multitaper

        Copyright 2021 Michael J. Prerau Laboratory. - https://www.sleepEEG.org
        Authors: Michael J. Prerau, Ph.D., Thomas Possidente, Mingjian He

        BSD 3-Clause License
"""

# To Do

# Analysis Imports
import math
import numpy as np
import numpy.typing as npt
from scipy.signal.windows import dpss
from scipy.signal import detrend, resample
from typing import Tuple, Literal, Optional, Callable

# Logistical Imports
import timeit
from joblib import Parallel, delayed, cpu_count
import logging

# Graphics library
from PySide6.QtCore import Qt

# Visualization imports
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import FuncFormatter
from matplotlib.figure import Figure
from matplotlib import cm
from matplotlib.axes import Axes
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

# Interface
from PySide6.QtWidgets import QSizePolicy, QDialog, QVBoxLayout, QDialogButtonBox

# Cause error upon warning
import warnings

# Set up logging
logger = logging.getLogger(__name__)

# Stage Utilities
def reorder_stages(stages: list[str]) -> list[str]:
    """
    Reorders sleep stages so Wake is first, REM is second, and NREM stages follow in numerical order.

    Args:
        stages: List of stage labels (e.g., ['N1', 'N2', 'REM', 'W', 'N3'])

    Returns:
        Reordered list of stages
    """
    ordered = []

    # 1. Add Wake stages first
    wake_patterns = ['W', 'WAKE', 'AWAKE']
    for stage in stages:
        if any(pattern in stage.upper() for pattern in wake_patterns) and stage not in ordered:
            ordered.append(stage)

    # 2. Add REM stages second
    for stage in stages:
        if stage.upper().strip() == 'REM' and stage not in ordered:
            ordered.append(stage)

    # 3. Add NREM stages in numerical order
    nrem_patterns = ['N1', 'N2', 'N3', 'N4', 'STAGE 1', 'STAGE 2', 'STAGE 3', 'STAGE 4', 'S1', 'S2', 'S3', 'S4']
    for pattern in nrem_patterns:
        for stage in stages:
            if stage.upper().strip() == pattern and stage not in ordered:
                ordered.append(stage)

    # 4. Add general NREM if no specific stages found
    has_specific_nrem = any('N' in s.upper() and any(c.isdigit() for c in s) for s in stages)
    if not has_specific_nrem:
        for stage in stages:
            if 'NREM' in stage.upper() and stage not in ordered:
                ordered.append(stage)

    # 5. Add any remaining stages
    for stage in stages:
        if stage not in ordered:
            ordered.append(stage)

    return ordered

# Except from original file. See below for full description


# MULTITAPER SPECTROGRAM #
class MultitaperSpectrogram:
    stimes: npt.NDArray[np.float64]
    sfreqs: npt.NDArray[np.float64]
    def __init__(self, data:npt.NDArray, fs:float, frequency_range:list[float]|None=None, time_bandwidth=5,
                 num_tapers=None, window_params:list[float]=None, min_nfft=0,
                 detrend_opt:Literal['linear', 'constant', 'off']='linear', multiprocess=False,
                 n_jobs=None, weighting='unity', plot_on=True, return_fig=False, clim_scale=True,
                 verbose=True, xyflip=False, ax=None):
        """ Compute multitaper spectrogram of timeseries data
        Usage:
        mt_spectrogram, stimes, sfreqs = multitaper_spectrogram(data, fs, frequency_range=None, time_bandwidth=5,
                                                            num_tapers=None, window_params=None, min_nfft=0,
                                                            detrend_opt='linear', multiprocess=False, cpus=False,
                                                            weighting='unity', plot_on=True, return_fig=False,
                                                            clim_scale=True, verbose=True, xyflip=False):
        Arguments:
                data (1d np.array): time series data -- required
                fs (float): sampling frequency in Hz  -- required
                frequency_range (list): 1x2 list - [<min frequency>, <max frequency>] (default: [0 nyquist])
                time_bandwidth (float): time-half bandwidth product (window duration*half bandwidth of main lobe)
                                        (default: 5 Hz*s)
                num_tapers (int): number of DPSS tapers to use (default: [will be computed
                                  as floor(2*time_bandwidth - 1)])
                window_params (list): 1x2 list - [window size (seconds), step size (seconds)] (default: [5 1])
                detrend_opt (string): detrend data window ('linear' (default), 'constant', 'off')
                                      (Default: 'linear')
                min_nfft (int): minimum allowable NFFT size, adds zero padding for interpolation (closest 2^x)
                                (default: 0)
                multiprocess (bool): Use multiprocessing to compute multitaper spectrogram (default: False)
                n_jobs (int): Number of cpus to use if multiprocess = True (default: False). Note: if default is left
                            as None and multiprocess = True, the number of cpus used for multiprocessing will be
                            all available - 1.
                weighting (str): weighting of tapers ('unity' (default), 'eigen', 'adapt');
                plot_on (bool): plot results (default: True)
                return_fig (bool): return plotted spectrogram (default: False)
                clim_scale (bool): automatically scale the colormap on the plotted spectrogram (default: True)
                verbose (bool): display spectrogram properties (default: True)
                xyflip (bool): transpose the mt_spectrogram output (default: False)
                ax (axes): a matplotlib axes to plot the spectrogram on (default: None)
        Returns:
                mt_spectrogram (TxF np array): spectral power matrix
                stimes (1xT np array): timepoints (s) in mt_spectrogram
                sfreqs (1xF np array)L frequency values (Hz) in mt_spectrogram

        Example:
        In this example we create some chirp data and run the multitaper spectrogram on it.
            import numpy as np  # import numpy
            from scipy.signal import chirp  # import chirp generation function
            # Set spectrogram params
            fs = 200  # Sampling Frequency
            frequency_range = [0, 25]  # Limit frequencies from 0 to 25 Hz
            time_bandwidth = 3  # Set time-half bandwidth
            num_tapers = 5  # Set number of tapers (optimal is time_bandwidth*2 - 1)
            window_params = [4, 1]  # Window size is 4s with step size of 1s
            min_nfft = 0  # No minimum nfft
            detrend_opt = 'constant'  # detrend each window by subtracting the average
            multiprocess = True  # use multiprocessing
            cpus = 3  # use 3 cores in multiprocessing
            weighting = 'unity'  # weight each taper at 1
            plot_on = True  # plot spectrogram
            return_fig = False  # do not return plotted spectrogram
            clim_scale = False # don't auto-scale the colormap
            verbose = True  # print extra info
            xyflip = False  # do not transpose spect output matrix

            # Generate sample chirp data
            t = np.arange(1/fs, 600, 1/fs)  # Create 10 min time array from 1/fs to 600 stepping by 1/fs
            f_start = 1  # Set chirp freq range min (Hz)
            f_end = 20  # Set chirp freq range max (Hz)
            data = chirp(t, f_start, t[-1], f_end, 'logarithmic')
            # Compute the multitaper spectrogram
            spect, stimes, sfreqs = multitaper_spectrogram(data, fs, frequency_range, time_bandwidth, num_tapers,
                                                           window_params, min_nfft, detrend_opt, multiprocess,
                                                           cpus, weighting, plot_on, return_fig, clim_scale,
                                                           verbose, xyflip):

        This code is companion to the paper:
        "Sleep Neurophysiological Dynamics Through the Lens of Multitaper Spectral Analysis"
           Michael J. Prerau, Ritchie E. Brown, Matt T. Bianchi, Jeffrey M. Ellenbogen, Patrick L. Purdon
           December 7, 2016 : 60-92
           DOI: 10.1152/physiol.00062.2015
         which should be cited for academic use of this code.

         A full tutorial on the multitaper spectrogram can be found at: # https://www.sleepEEG.org/multitaper

        Copyright 2021 Michael J. Prerau Laboratory. - https://www.sleepEEG.org
        Authors: Michael J. Prerau, Ph.D., Thomas Possidente, Mingjian He

        ______________________________________________________________________________________________________________

        """
        # Input
        self.data: npt.NDArray[np.float64]        = data
        self.fs: float                            = fs
        self.frequency_range: list[float] = frequency_range
        self.time_bandwidth:float                 = time_bandwidth
        self.num_tapers: int                      = num_tapers
        self.window_params: list[float]   = window_params
        self.min_nfft: int                        = min_nfft

        detrend_opt_input: str = detrend_opt.lower()  # normalize
        if detrend_opt_input not in ('linear', 'constant', 'off'):
            raise ValueError(f"Invalid detrend option: {detrend_opt}")
        self.detrend_opt: Literal['linear', 'constant', 'off'] = detrend_opt_input

        self.multiprocess: bool = multiprocess
        self.n_jobs: int        = n_jobs
        self.weighting: str     = weighting
        self.plot_on: bool      = plot_on
        self.return_fig: bool   = return_fig
        self.clim_scale: bool   = clim_scale
        self.verbose: bool      = verbose
        self.xyflip: bool       = xyflip
        self.ax: Axes               = ax


        # Computed taper parameters
        self.winsize_samples: int|None = None    # number of samples in single time window
        self.winstep_samples: Optional[int] |None = None    # number of samples in a single window step
        self.window_start:Optional[np.ndarray]|None = None    # array of timestamps representing the beginning time for each window
        self.num_windows: int|None = None    # Number of windows in the data
        self.nfft:int|None  = None    # length of signal to calculate fft on

        self.window_start: Optional[np.ndarray] = None        # array of timestamps representing the beginning time for each                                           window -- required
        self.datawin_size: Optional[float]|None = None    # seconds in one window -- required
        self.data_window_params: Optional[Tuple[float, float]] = None # [window length(s), window step size(s)] - - required

        self.window_idxs:list = None
        self.freq_inds:list = None

        # Store Result information
        self.mt_spectrogram:list = None
        self.stimes:npt.NDArray[np.float64] = None
        self.sfreqs:npt.NDArray[np.float64] = None
        self.spectrogram_computed:bool = None

        # Visualization Variables
        self.current_spectrogram_ax:Optional[Axes] = None
        self.current_spectrogram_fig: Optional[Figure] = None
        self.current_spectrogram_canvas: Optional[FigureCanvas] = None
        self.spectrogram_double_click_callback: Optional[Callable] = None

        # Save heatmap data and parameters for legend
        self.heatmap_data                      = None
        self.heatmap_fs                        = None
        self.heatmap_original_data             = None
        self.heatmap_time_points               = None
        self.heatmap_cmap                      = None
        self.clim_scale                        = clim_scale
        self.heatmap_clim                      = None
        self.current_heatmap_ax                = None
        self.current_heatmap_fig               = None
        self.current_heatmap_canvas            = None
        self.heatmap_double_click_callback     = None

        # Store Matplotlib Connections
        self.spectrogram_connection = []
        self.heatmap_connection = []
        self.average_connection = []
        self.bandplot_connection  = []
        self.heapmap_double_click_callback = None

        # Create a custom color map
        gradient_colors = ['#FFE4B5', '#FFE4B5', '#FFB6C1', '#D8BFD8', '#B0E0E6', '#98FB98', '#3CB371']
        custom_cmap_continuous = LinearSegmentedColormap.from_list("SleepViewerGradient", gradient_colors)
        self.spectrogram_colormap = custom_cmap_continuous

        # Plot parameters
        self.spectral_bands_default = [[0.5, 4.0], [4.0, 8.0], [8.0, 12.0], [12.0, 15.0], [15.0, 30.0], [30.0, 60.0]]
        self.spectral_bands_titles_default = ['delta', 'beta', 'alpha', 'sigma', 'beta', 'gamma']

        # Colors
        self.default_stage_colors = {
            'W': '#B5B5B5',       # Light orange '#FFE4B5', converting to gray
            'Wake': '#E4E4E4',    # Light orange
            'REM': '#FFB6C1',     # Light pink
            'N1': '#D8BFD8',      # Thistle
            'N2': '#B0E0E6',      # Powder blue
            'N3': '#98FB98',      # Pale green
            'N4': '#3CB371',      # Medium sea green (darker than N3)
            'NREM': '#87CEEB',    # Sky blue
            'Artifact': '#FA8072' # Salmon
        }


        # Spectrogram Result Dictionary
    # Manage connections
    def cleanup_events(self):
        for cid in self.spectrogram_connection:
            try:
                self.current_spectrogram_fig.canvas.mpl_disconnect(cid)
            except ValueError:
                pass  # In case connection is already gone
        self.spectrogram_connection.clear()

        for cid in self.heatmap_connection:
            try:
                self.current_heatmap_fig.canvas.mpl_disconnect(cid)
            except ValueError:
                pass  # In case connection is already gone
        self.heatmap_connection.clear()

        logger.info(f'Multitaper Spectrogram - clean up events')
    def setup_events(self):
        # Only setup if not already connected (avoid duplicate connections)
        if self.spectrogram_connection or self.heatmap_connection:
            return  # Already setup

        # Reconnect spectrogram event handlers
        cid = self.current_spectrogram_fig.canvas.mpl_connect('button_press_event', self._on_spectrogram_double_click)
        self.spectrogram_connection.append(cid)

        # Reconnect heatmap event handlers
        cid = self.current_heatmap_fig.canvas.mpl_connect('button_press_event', self._on_heatmap_double_click)
        self.heatmap_connection.append(cid)

        logger.info(f'Multi-taper Spectrogram - setup up events')

    # Computer
    def compute_spectrogram(self):
        #  Process user input
        [data, fs, frequency_range, time_bandwidth, num_tapers,
         winsize_samples, winstep_samples, window_start,
         num_windows, nfft, detrend_opt, _plot_on, _verbose] = self.process_input()

        # Set up spectrogram parameters
        [window_idxs, stimes, sfreqs, freq_inds] = self.process_spectrogram_params(fs, nfft, frequency_range, window_start,
                                                                              winsize_samples)
        self.window_idxs = window_idxs
        self.stimes = stimes
        self.sfreqs = sfreqs
        self.freq_inds = freq_inds

        # Store computer information to display spectrogram parameter
        self.winsize_samples = winsize_samples
        self.winstep_samples = winstep_samples
        self.data_window_params = [winsize_samples, winstep_samples]

        # Split data into segments and preallocate
        data_segments = data[window_idxs]

        # COMPUTE THE MULTITAPER SPECTROGRAM
        #     STEP 1: Compute DPSS tapers based on desired spectral properties
        #     STEP 2: Multiply the data segment by the DPSS Tapers
        #     STEP 3: Compute the spectrum for each tapered segment
        #     STEP 4: Take the mean of the tapered spectra

        # Compute DPSS tapers (STEP 1)
        try:
            dpss_tapers, dpss_eigen = dpss(winsize_samples, time_bandwidth, num_tapers, return_ratios=True)
            dpss_eigen = np.reshape(dpss_eigen, (num_tapers, 1))
        except ValueError as e:
            logger.info(f'Invalid parameters: {e}')
            self.spectrogram_computed = False
            return

        # pre-compute weights
        if self.weighting == 'eigen':
            wt = dpss_eigen / num_tapers
        elif self.weighting == 'unity':
            wt = np.ones(num_tapers) / num_tapers
            wt = np.reshape(wt, (num_tapers, 1))  # reshape as column vector
        else:
            wt = 0

        tic = timeit.default_timer()  # start timer

        # Set up calc_mts_segment() input arguments
        mts_params = (dpss_tapers, nfft, freq_inds, detrend_opt, num_tapers, dpss_eigen, self.weighting, wt)

        if self.multiprocess:  # use multiprocessing
            self.n_jobs = max(cpu_count() - 1, 1) if self.n_jobs is None else self.n_jobs
            mt_spectrogram = np.vstack(Parallel(n_jobs=self.n_jobs)(delayed(self.calc_mts_segment)(
                data_segments[num_window, :], *mts_params) for num_window in range(num_windows)))
            logger.info(f'Computing multi-process spectrogram with {self.n_jobs} job(s)')
        else:  # if no multiprocessing, compute normally
            mt_spectrogram = np.apply_along_axis(self.calc_mts_segment, 1, data_segments, *mts_params)

        # Compute one-sided PSD spectrum
        mt_spectrogram = mt_spectrogram.T
        dc_select = np.where(sfreqs == 0)[0]
        nyquist_select = np.where(sfreqs == fs/2)[0]
        select = np.setdiff1d(np.arange(0, len(sfreqs)), np.concatenate((dc_select, nyquist_select)))

        mt_spectrogram = np.vstack([mt_spectrogram[dc_select, :], 2*mt_spectrogram[select, :],
                                   mt_spectrogram[nyquist_select, :]]) / fs

        # Flip if requested
        if self.xyflip:
            mt_spectrogram = mt_spectrogram.T

        # End timer and get elapsed compute time
        toc = timeit.default_timer()
        if self.verbose:
            logger.info("Multitaper compute time: " + "%.2f" % (toc - tic) + " seconds")

        if np.all(mt_spectrogram.flatten() == 0):
            logger.info("Data was all zeros, no output")

        # Store information
        self.mt_spectrogram = mt_spectrogram
        self.stimes = stimes
        self.sfreqs = sfreqs
        self.spectrogram_computed = True
    def process_input(self):
        """ Helper function to process multitaper_spectrogram() arguments
                Used:
                        data (1d np.array): time series data-- required
                        fs (float): sampling frequency in Hz  -- required
                        frequency_range (list): 1x2 list - [<min frequency>, <max frequency>] (default: [0 nyquist])
                        time_bandwidth (float): time-half bandwidth product (window duration*half bandwidth of main lobe)
                                                (default: 5 Hz*s)
                        num_tapers (int): number of DPSS tapers to use (default: None [will be computed
                                          as floor(2*time_bandwidth - 1)])
                        window_params (list): 1x2 list - [window size (seconds), step size (seconds)] (default: [5 1])
                        min_nfft (int): minimum allowable NFFT size, adds zero padding for interpolation (closest 2^x)
                                        (default: 0)
                        detrend_opt (string): detrend data window ('linear' (default), 'constant', 'off')
                                              (Default: 'linear')
                        plot_on (True): plot results (default: True)
                        verbose (True): display spectrogram properties (default: true)
                Returns:
                        data (1d np.array): same as input
                        fs (float): same as input
                        frequency_range (list): same as input or calculated from fs if not given
                        time_bandwidth (float): same as input or default if not given
                        num_tapers (int): same as input or calculated from time_bandwidth if not given
                        winsize_samples (int): number of samples in single time window
                        winstep_samples (int): number of samples in a single window step
                        window_start (1xm np.array): array of timestamps representing the beginning time for each window
                        num_windows (int): number of windows in the data
                        nfft (int): length of signal to calculate fft on
                        detrend_opt ('string'): same as input or default if not given
                        plot_on (bool): same as input
                        verbose (bool): same as input
        """
        # Get inputs
        data: npt.NDArray[np.float64]  = self.data
        fs: float = self.fs
        frequency_range: list[float] = self.frequency_range
        time_bandwidth:float = self.time_bandwidth
        num_tapers: int = self.num_tapers
        window_params: Tuple[float, float] = self.window_params
        min_nfft: int = self.min_nfft

        detrend_opt_input: str = self.detrend_opt.lower()  # normalize input
        if detrend_opt_input not in ('linear', 'constant', 'off'):
            raise ValueError(f"Invalid detrend option: {self.detrend_opt}")
        detrend_opt: Literal['linear', 'constant', 'off'] = detrend_opt_input

        plot_on: bool = self. plot_on
        verbose: bool = self.verbose

        # Make sure data is 1 dimensional np array
        if len(data.shape) != 1:
            if (len(data.shape) == 2) & (data.shape[1] == 1):  # if it's 2d, but can be transferred to 1d, do so
                data = np.ravel(data[:, 0])
            elif (len(data.shape) == 2) & (data.shape[0] == 1):  # if it's 2d, but can be transferred to 1d, do so
                data = np.ravel(data.T[:, 0])
            else:
                raise TypeError("Input data is the incorrect dimensions. Should be a 1d array with shape (n,) where n is \
                                the number of data points. Instead data shape was " + str(data.shape))

        # Set frequency range if not provided
        if frequency_range is None:
            frequency_range = [0, fs / 2]

        # Set detrending method
        detrend_opt_lower = detrend_opt.lower()
        if detrend_opt_lower not in ('linear', 'constant', 'off'):
            raise ValueError(f"Invalid detrend option: {detrend_opt_lower}")
        detrend_opt: Literal['linear', 'constant', 'off'] = detrend_opt_lower
        if detrend_opt != 'linear':
            if detrend_opt in ['const', 'constant']:
                detrend_opt = 'constant'
            elif detrend_opt in ['none', 'false', 'off']:
                detrend_opt = 'off'
            else:
                raise ValueError("'" + str(detrend_opt) + "' is not a valid argument for detrend_opt. The choices " +
                                 "are: 'constant', 'linear', or 'off'.")
        # Check if frequency range is valid
        if frequency_range[1] > fs / 2:
            frequency_range[1] = fs / 2
            warnings.warn('Upper frequency range greater than Nyquist, setting range to [' +
                          str(frequency_range[0]) + ', ' + str(frequency_range[1]) + ']')

        # Set number of tapers if none provided
        if num_tapers is None:
            num_tapers = math.floor(2 * time_bandwidth) - 1

        # Warn if number of tapers is suboptimal
        if num_tapers != math.floor(2 * time_bandwidth) - 1:
            warnings.warn('Number of tapers is optimal at floor(2*TW) - 1. consider using ' +
                          str(math.floor(2 * time_bandwidth) - 1))

        # If no window params provided, set to defaults
        if window_params is None:
            window_params = tuple([5, 1])

        # Check if window size is valid, fix if not
        if window_params[0] * fs % 1 != 0:
            winsize_samples = round(window_params[0] * fs)
            warnings.warn('Window size is not divisible by sampling frequency. Adjusting window size to ' +
                          str(winsize_samples / fs) + ' seconds')
        else:
            winsize_samples = window_params[0] * fs

        # Check if window step is valid, fix if not
        if window_params[1] * fs % 1 != 0:
            winstep_samples = round(window_params[1] * fs)
            warnings.warn('Window step size is not divisible by sampling frequency. Adjusting window step size to ' +
                          str(winstep_samples / fs) + ' seconds')
        else:
            winstep_samples = window_params[1] * fs

        # Get total data length
        len_data = len(data)

        # Check if length of data is smaller than window (bad)
        if len_data < winsize_samples:
            raise ValueError("\nData length (" + str(len_data) + ") is shorter than window size (" +
                             str(winsize_samples) + "). Either increase data length or decrease window size.")

        # Find window start indices and num of windows
        window_start = np.arange(0, len_data - winsize_samples + 1, winstep_samples)
        num_windows = len(window_start)

        # Get num points in FFT
        if min_nfft == 0:  # avoid divide by zero error in np.log2(0)
            nfft = max(2 ** math.ceil(np.log2(abs(winsize_samples))), winsize_samples)
        else:
            nfft = max(max(2 ** math.ceil(np.log2(abs(winsize_samples))), winsize_samples),
                       2 ** math.ceil(np.log2(abs(min_nfft))))

        return ([data, fs, frequency_range, time_bandwidth, num_tapers,
                 int(winsize_samples), int(winstep_samples), window_start, num_windows, nfft,
                 detrend_opt, plot_on, verbose])
    @staticmethod
    def process_spectrogram_params(fs, nfft, frequency_range, window_start, datawin_size):
        """ Helper function to create frequency vector and window indices
            Arguments:
                 fs (float): sampling frequency in Hz  -- required
                 nfft (int): length of signal to calculate fft on -- required
                 frequency_range (list): 1x2 list - [<min frequency>, <max frequency>] -- required
                 window_start (1xm np array): array of timestamps representing the beginning time for each
                                              window -- required
                 datawin_size (float): seconds in one window -- required
            Returns:
                window_idxs (nxm np array): indices of timestamps for each window
                                            (nxm where n=number of windows and m=datawin_size)
                stimes (1xt np array): array of times for the center of the spectral bins
                sfreqs (1xf np array): array of frequency bins for the spectrogram
                freq_inds (1d np array): boolean array of which frequencies are being analyzed in
                                          an array of frequencies from 0 to fs with steps of fs/nfft
        """

        # create frequency vector
        df = fs / nfft
        sfreqs: npt.NDArray[np.float64]  = np.arange(0, fs, df)

        # Get frequencies for given frequency range
        freq_inds = (sfreqs >= frequency_range[0]) & (sfreqs <= frequency_range[1])
        sfreqs = sfreqs[freq_inds]

        # Compute times in the middle of each spectrum
        window_middle_samples = window_start + round(datawin_size / 2)
        stimes: npt.NDArray[np.float64]  = window_middle_samples / fs

        # Get indexes for each window
        window_idxs = np.atleast_2d(window_start).T + np.arange(0, datawin_size, 1)
        window_idxs = window_idxs.astype(int)

        return [window_idxs, stimes, sfreqs, freq_inds]

    # Command Line
    def display_spectrogram_props(self):
        """ Prints spectrogram properties
            Arguments copied from class:
                fs (float): sampling frequency in Hz  -- required
                time_bandwidth (float): time-half bandwidth product (window duration*1/2*frequency_resolution) -- required
                num_tapers (int): number of DPSS tapers to use -- required
                data_window_params (list): 1x2 list - [window length(s), window step size(s)] -- required
                frequency_range (list): 1x2 list - [<min frequency>, <max frequency>] -- required
                nfft(float): number of fast fourier transform samples -- required
                detrend_opt (str): detrend data window ('linear' (default), 'constant', 'off') -- required
            Returns:
                This function does not return anything
        """

        fs                 = self.fs
        time_bandwidth     = self.time_bandwidth
        num_tapers         = self.num_tapers
        data_window_params = self.data_window_params
        frequency_range    = self.frequency_range
        nfft               = self.nfft
        detrend_opt        = self.detrend_opt

        # Compute (normalize) data window params
        data_window_params = np.asarray(data_window_params) / fs

        # Print spectrogram properties
        logger.info("Multitaper Spectrogram Properties: ")
        logger.info('     Spectral Resolution: ' + str(2 * time_bandwidth / data_window_params[0]) + 'Hz')
        logger.info('     Window Length: ' + str(data_window_params[0]) + 's')
        logger.info('     Window Step: ' + str(data_window_params[1]) + 's')
        logger.info('     Time Half-Bandwidth Product: ' + str(time_bandwidth))
        logger.info('     Number of Tapers: ' + str(num_tapers))
        logger.info('     Frequency Range: ' + str(frequency_range[0]) + "-" + str(frequency_range[1]) + 'Hz')
        logger.info('     NFFT: ' + str(nfft))
        logger.info('     Detrend: ' + detrend_opt + '\n')

    # Spectrogram Functions
    def plot(self, parent_widget=None, x_tick_settings:Optional[list[int]] = None, convert_time_f=lambda x:x/3600.0,
             time_axis_unit:str|None = 'h', turn_axis_units_off:bool = False, double_click_callback=None,
             axis_only:bool=False, show_legend:bool=False):
        # Plot multitaper spectrogram

        # cleanup handlers since plots are writing to the same graphics view
        self.cleanup_events()

        # Define plotting variables
        label_fontsize = 8
        tick_label_fontsize = 8
        use_y_ticks = False

        # Set x values
        if x_tick_settings is None:
            # Assuming a night of data
            # Hourly major, 15 minutes
            x_tick_settings = [3600, 900]
        major_tick_step, minor_tick_step = x_tick_settings

        # Get spectrogram information from class
        mt_spectrogram = self.mt_spectrogram
        spect_data = self.nanpow2db(mt_spectrogram) if mt_spectrogram is not None else None
        stimes = np.array(self.stimes)
        sfreqs = np.array(self.sfreqs)

        # Set x and y axes
        dx = stimes[1] - stimes[0]
        dy = sfreqs[1] - sfreqs[0]
        extent = [stimes[0] - dx, stimes[-1] + dx, sfreqs[-1] + dy, sfreqs[0] - dy]

        # Create the figure and canvas
        fig = Figure()
        im = None
        if not axis_only:
            ax = fig.add_subplot(111)
            im = ax.imshow(spect_data, extent=extent, aspect='auto')
            if show_legend:
                cbar = fig.colorbar(im, ax=ax, fraction=0.035, pad=0.02)
                cbar.ax.tick_params(labelsize=tick_label_fontsize)
                cbar.ax.yaxis.set_major_formatter(FuncFormatter(lambda val, pos: f"{val} dB"))
        else:
            # Create a matching axis for time alignment with the spectrogram
            ax = fig.add_subplot(111)

            # Plot a zero-valued line to define identical x-axis scaling
            y = np.zeros_like(stimes)
            ax.plot(stimes, y, alpha=0)  # invisible line, just for scale

            # Ensure identical x-limits as the spectrogram would use
            ax.set_xlim(extent[0], extent[1])

            # Keep a small vertical range
            ax.set_ylim(-0.1, 0.1)

            # Hide all spines except the bottom one (the time axis)
            for spine in ax.spines.values():
                spine.set_visible(False)
            ax.spines['bottom'].set_visible(True)
            ax.spines['bottom'].set_position(('data', 0))

            # Hide y-axis completely
            ax.get_yaxis().set_visible(False)

            # Set up major tick locations and labels
            major_ticks = np.arange(stimes[0], stimes[-1] + major_tick_step, major_tick_step)
            ax.set_xticks(major_ticks)
            ax.set_xticklabels(
                [f"{int(convert_time_f(x))}{time_axis_unit}" for x in major_ticks],
                fontsize=tick_label_fontsize
            )

            # Optional: minor ticks for aesthetics
            minor_ticks = np.arange(stimes[0], stimes[-1] + minor_tick_step, minor_tick_step)
            ax.set_xticks(minor_ticks, minor=True)
            ax.tick_params(axis='x', which='both', length=3, direction='in')

            # Make background transparent (optional)
            ax.set_facecolor('none')
            fig.patch.set_facecolor('none')

        # Store references for event handling
        self.current_spectrogram_ax = ax
        self.current_spectrogram_fig = fig
        self.spectrogram_double_click_callback = double_click_callback

        # Set major and minor ticks
        major_ticks = list(range(1, int(stimes[-1] + 1), int(major_tick_step)))
        minor_ticks = [x for x in range(0, int(stimes[-1] + 1), minor_tick_step) if x not in major_ticks]

        # Set tick parameters
        ax.tick_params(axis='x', which='major', direction='in')
        ax.tick_params(axis='x', which='minor', direction='in')

        # Set major and minor ticks
        ax.set_xticks(major_ticks)
        ax.set_xticks(minor_ticks, minor=True)

        # Set labels only for major ticks
        ax.set_xticklabels([f"{int(convert_time_f(x))} {time_axis_unit}" for x in major_ticks],
                               fontsize=tick_label_fontsize)

        if turn_axis_units_off:
            ax.set_xticklabels([])

        # Customize plot
        y_label = ""
        if parent_widget:
            # Enable expanding to fill the parent widget
            y_label = "F(Hz)"
            # color_bar_label = 'dB'
        else:
            if not axis_only:
                if parent_widget:
                    y_label = "F(Hz)"
                else:
                    y_label = "Frequency (Hz)"
                    color_bar_label = 'PSD (dB)'
                    fig.colorbar(im, ax=ax, label=color_bar_label, shrink=0.8)

        # fig.colorbar(im, ax=ax, label=color_bar_label, shrink=0.8)
        if not axis_only:
            ax.set_xlabel("Time (HH:MM:SS)")
            ax.set_ylabel(y_label)
            cmap = self.spectrogram_colormap
            im.set_cmap(cmap)
            ax.invert_yaxis()

        if not axis_only:
            ax.yaxis.set_major_formatter(FuncFormatter(lambda y_val, _: f"{int(y_val)} Hz"))
            if use_y_ticks:
                yticks = ax.get_yticks()
                ax.set_yticklabels([f"{int(y)} Hz" for y in yticks])
                ax.tick_params(axis='y', labelsize=label_fontsize)

        if self.clim_scale and not axis_only:
            clim = np.percentile(spect_data, [5, 98])
            im.set_clim(clim)

        # Ensure x and y labels aer the same size
        ax.tick_params(axis='x', labelsize=tick_label_fontsize)
        ax.tick_params(axis='y', labelsize=tick_label_fontsize)

        # Embed canvas into the provided QWidget
        if parent_widget:
            # Create the canvas
            canvas = FigureCanvas(fig)
            canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            canvas.updateGeometry()

            # connect right-click
            canvas.setContextMenuPolicy(Qt.CustomContextMenu)
            canvas.customContextMenuRequested.connect(parent_widget.show_context_menu)

            # fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
            fig.subplots_adjust(left=0.03, right=0.99, top=0.94, bottom=0.06)

            # Assign figure to parent_widget so save dialog knows what to save
            parent_widget.figure = fig
            parent_widget.canvas_item = canvas

            # Connect double-click event handler
            cid = canvas.mpl_connect('button_press_event', self._on_spectrogram_double_click)
            self.spectrogram_connection.append(cid)

            # Store canvas reference
            self.current_spectrogram_canvas = canvas



            # Remove existing layout and widgets if they exist
            existing_layout = parent_widget.layout()
            if existing_layout:
                while existing_layout.count():
                    item = existing_layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.setParent(None)
            else:
                existing_layout = QVBoxLayout(parent_widget)
                parent_widget.setLayout(existing_layout)

            # Add new canvas
            existing_layout.setContentsMargins(0, 0, 0, 0)
            existing_layout.addWidget(canvas)

            if not axis_only:
                ax.set_xlabel("")
                ax.set_ylabel("")
                im.set_cmap(self.spectrogram_colormap)
                ax.invert_yaxis()

            if self.clim_scale and not axis_only:
               clim = np.percentile(spect_data, [5, 98])
               im.set_clim(clim)
        elif parent_widget is None:
            pass
    def show_colorbar_legend_dialog(self):
        # Check that spectrogram was computed
        if not hasattr(self, 'mt_spectrogram') or self.mt_spectrogram is None:
            logger.error("Error: Spectrogram data not available. Generate spectrogram first.")
            return

        # Create dialog
        dialog = QDialog()
        dialog.setWindowTitle("Spectrogram Colorbar Legend")
        dialog.setModal(True)
        dialog.resize(300, 400)  # Adjust size as needed

        # Create layout
        layout = QVBoxLayout()

        # Create matplotlib figure for colorbar only
        fig = Figure(figsize=(2, 6))
        canvas = FigureCanvas(fig)

        # Get the same data range and colormap as your spectrogram
        mt_spectrogram = self.mt_spectrogram
        spect_data = self.nanpow2db(mt_spectrogram)

        # Use the same colormap as in your plot function
        cmap = self.spectrogram_colormap

        # Set data range
        if hasattr(self, 'clim_scale') and self.clim_scale:
            clim = np.percentile(spect_data, [5, 98])
            vmin, vmax = clim
        else:
            vmin, vmax = np.nanmin(spect_data), np.nanmax(spect_data)

        # Create a simple axes for the colorbar
        ax = fig.add_axes(tuple([0.1, 0.1, 0.3, 0.8]))  # [left, bottom, width, height]

        # Create colorbar directly
        vmin_val = float(vmin) if vmin is not None else None
        vmax_val = float(vmax) if vmax is not None else None
        norm = mcolors.Normalize(vmin=vmin_val, vmax=vmax_val)
        sm = cm.ScalarMappable(norm=norm, cmap=cmap)
        sm.set_array([])

        cbar = fig.colorbar(sm, cax=ax)
        cbar.set_label('PSD (dB)', fontsize=12)
        cbar.ax.tick_params(labelsize=10)

        # Make sure the canvas draws
        canvas.draw()

        # Add canvas to dialog
        layout.addWidget(canvas)

        # Add close button
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(dialog.accept)
        layout.addWidget(buttons)

        dialog.setLayout(layout)

        # Show dialog
        dialog.exec()
    def clear_spectrogram_results(self):
        # Clear heatmap results
        for attr in [
            "mt_spectrogram",
            "stimes",
            "sfreqs",
            "spectrogram_computed",
        ]:
            if not hasattr(self, attr):
                setattr(self, attr, None)
    def _on_spectrogram_double_click(self, event):
        """Handle double-click events on the spectrogram plot."""
        if event.dblclick and event.inaxes:
            x_value = event.xdata  # Time in seconds
            y_value = event.ydata  # Frequency in Hz

            if x_value is not None and y_value is not None:
                # Convert time to hours:minutes format for display
                # hours = int(x_value // 3600)
                # minutes = int((x_value % 3600) // 60)
                # seconds = int(x_value % 60)
                # time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

                # Call the callback function if provided
                if (hasattr(self, 'spectrogram_double_click_callback') and
                        self.spectrogram_double_click_callback is not None):
                    self.spectrogram_double_click_callback(x_value, y_value)

    # Data Heatmap to support data visualization without spectrogram
    def plot_data(self, parent_widget=None, double_click_callback=None):
        """
        Plot data as a heatmap alternative to spectrogram.

        Parameters:
        -----------
        data : array-like
            Time series data to plot as heatmap
        fs : float
            Sampling frequency
        parent_widget : QWidget, optional
            Parent widget to embed the plot (PySide6)
        double_click_callback : callable, optional
            Callback function for double-click events
        """

        # cleanup handlers since plots are writing to the same graphics view
        self.cleanup_events()

        # Get data input
        data = self.data
        fs = self.fs

        # Set column limit for safe visualization
        max_points = 2 ** 23  # ~8.4 million

        # Check if data length exceeds limit
        n_points = data.shape[-1]  # works for 1D or 2D (time on last axis)

        if n_points > max_points:
            downsample_factor = int(np.ceil(n_points / max_points))
            new_length = n_points // downsample_factor

            logger.info(
                f"Data has {n_points:,} points, exceeding display limit ({max_points:,}). "
                f"Downsampling by factor {downsample_factor} to {new_length:,} points.",
            )

            # Downsample the data (time dimension)
            if data.ndim == 1:
                data = resample(data, new_length)
            else:
                data = resample(data, new_length, axis=-1)

            # Adjust fs accordingly
            fs = fs / downsample_factor

        # Bringing some plotting parameters to the top
        label_fontsize = 6



        # Convert 1D data to single row heatmap for display
        if data.ndim == 1:
            # Reshape 1D data to single row (1 x N) for heatmap
            heatmap_data = data.reshape(1, -1)
        else:
            heatmap_data = data

        # Create time axis
        total_duration = len(data) / fs
        time_points = np.linspace(0, total_duration, heatmap_data.shape[1])

        # Set up extent for imshow - single row heatmap
        dt = time_points[1] - time_points[0] if len(time_points) > 1 else 1/fs
        extent = [time_points[0] - dt/2, time_points[-1] + dt/2,
                  0.5, -0.5]  # Single row from -0.5 to 0.5

        # Save heatmap data and parameters for legend
        self.heatmap_data = heatmap_data
        self.heatmap_fs = fs
        self.heatmap_original_data = data
        self.heatmap_time_points = time_points

        # Save colormap and limits after setting them
        # Store the colormap - create it the same way as in the plot
        self.heatmap_cmap = self.spectrogram_colormap
        if hasattr(self, 'clim_scale') and self.clim_scale:
            self.heatmap_clim = np.percentile(heatmap_data, [5, 95])
        else:
            self.heatmap_clim = (np.nanmin(heatmap_data), np.nanmax(heatmap_data))

        # Create the figure and canvas
        fig = Figure()
        ax = fig.add_subplot(111)

        # Plot heatmap
        im = ax.imshow(heatmap_data, extent=extent, aspect='auto', origin='upper')

        # Store references for event handling
        self.current_heatmap_ax = ax
        self.current_heatmap_fig = fig
        self.heapmap_double_click_callback = double_click_callback

        # Customize plot
        if parent_widget:
            # Enable expanding to fill the parent widget
            y_label = ""
        else:
            y_label = "Data"
            color_bar_label = 'Amplitude'
            fig.colorbar(im, ax=ax, label=color_bar_label, shrink=0.8)

        ax.set_xlabel("Time (s)")
        ax.set_ylabel(y_label)

        # Apply colormap
        cmap = self.spectrogram_colormap
        im.set_cmap(cmap)

        # Set y-axis to show single row
        ax.set_yticks([0])
        ax.set_yticklabels([''])
        ax.set_ylim(-0.5, 0.5)

        ax.tick_params(axis='y', labelsize=label_fontsize)

        # Set color limits based on data percentiles
        if hasattr(self, 'clim_scale') and self.clim_scale:
            clim = np.percentile(heatmap_data, [5, 95])
            im.set_clim(tuple(clim))

        # Embed canvas into the provided QWidget
        if parent_widget:
            # Create the canvas
            canvas = FigureCanvas(fig)
            # canvas.setSizePolicy(canvas.sizePolicy().Expanding, canvas.sizePolicy().Expanding)
            canvas.updateGeometry()

            # Connect double-click event handler
            cid = canvas.mpl_connect('button_press_event', self._on_heatmap_double_click)
            self.heatmap_connection.append(cid)

            # Store canvas reference
            self.current_spectrogram_canvas = canvas

            fig.subplots_adjust(left=0.03, right=0.99, top=0.94, bottom=0.06)

            # Remove existing layout and widgets if they exist
            existing_layout = parent_widget.layout()
            if existing_layout:
                while existing_layout.count():
                    item = existing_layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.setParent(None)
            else:
                existing_layout = QVBoxLayout(parent_widget)
                parent_widget.setLayout(existing_layout)

            # Add new canvas
            existing_layout.setContentsMargins(0, 0, 0, 0)
            existing_layout.addWidget(canvas)

            ax.set_xlabel("")
            ax.set_ylabel("")
            im.set_cmap(self.spectrogram_colormap)

            if hasattr(self, 'clim_scale') and self.clim_scale:
                clim = np.percentile(heatmap_data, [5, 95])
                im.set_clim(tuple(clim))

        # Optionally return for other use
        if hasattr(self, 'return_fig') and self.return_fig:
            return heatmap_data, time_points, None, (fig, ax)

        return fig, ax
    def _on_heatmap_double_click(self, event):
        """Handle double-click events on the spectrogram plot."""
        if event.dblclick and event.inaxes:
            x_value = event.xdata  # Time in seconds
            y_value = event.ydata  # Frequency in Hz

            if x_value is not None and y_value is not None:
                # Convert time to hours:minutes format for display
                # hours = int(x_value // 3600)
                # minutes = int((x_value % 3600) // 60)
                # seconds = int(x_value % 60)
                # time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

                # Call the callback function if provided
                if (hasattr(self, 'heatmap_double_click_callback') and
                        self.heatmap_double_click_callback is not None):
                    self.heatmap_double_click_callback(x_value, y_value)
    def show_heatmap_legend_dialog(self):
        """
        Show a colorbar legend dialog for the data heatmap.
        """
        # Check that heatmap data is available
        if not hasattr(self, 'heatmap_data') or self.heatmap_data is None:
            logger.error(f"Error: Heatmap data not available. Generate heatmap first: {self.heatmap_data}.")
            return

        # Create dialog
        dialog = QDialog()
        dialog.setWindowTitle("Data Heatmap Colorbar Legend")
        dialog.setModal(True)
        dialog.resize(300, 400)  # Adjust size as needed

        # Create layout
        layout = QVBoxLayout()

        # Create matplotlib figure for colorbar only
        fig = Figure(figsize=(2, 6))
        canvas = FigureCanvas(fig)

        # Get the same colormap as your heatmap
        if hasattr(self, 'heatmap_cmap'):
            cmap = self.heatmap_cmap
        else:
            # Fallback to default colormap
            cmap = mcolors.ListedColormap(self.spectrogram_colormap)

        # Get data range from saved heatmap info
        vmin, vmax = self.heatmap_clim

        # Create a simple axes for the colorbar
        rect: tuple[float, float, float, float] = (0.1, 0.1, 0.3, 0.8)
        ax = fig.add_axes(rect)  # [left, bottom, width, height]

        # Create colorbar directly
        norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
        sm = cm.ScalarMappable(norm=norm, cmap=cmap)
        sm.set_array([])

        cbar = fig.colorbar(sm, cax=ax)
        cbar.set_label('Amplitude', fontsize=12)
        cbar.ax.tick_params(labelsize=10)

        # Make sure the canvas draws
        canvas.draw()

        # Add canvas to dialog
        layout.addWidget(canvas)

        # Add close button
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(dialog.accept)
        layout.addWidget(buttons)

        dialog.setLayout(layout)

        # Show dialog
        dialog.exec()
    def get_heatmap_info(self):
        """
        Get information about the current heatmap for display or debugging.
        Returns dictionary with heatmap parameters.
        """
        if not hasattr(self, 'heatmap_data'):
            return None

        info = {
            'data_shape': self.heatmap_data.shape,
            'sampling_frequency': self.heatmap_fs,
            'duration_seconds': len(self.heatmap_original_data) / self.heatmap_fs,
            'data_range': self.heatmap_clim,
            'total_samples': len(self.heatmap_original_data),
            'time_resolution': self.heatmap_time_points[1] - self.heatmap_time_points[0] if len(self.heatmap_time_points) > 1 else 1/self.heatmap_fs
        }
        return info
    def clear_data_heatmap_variables(self):
        logger.info('Clearing heatmap information')
        # Clear heatmap information
        for attr in [
            "heatmap_data",
            "heatmap_fs",
            "heatmap_original_data",
            "heatmap_time_points",
            "heatmap_cmap",
            "clim_scale",
            "heatmap_clim",
        ]:
            if not hasattr(self, attr):
                setattr(self, attr, None)

    # Summary function
    def get_multi_taper_results(self):
        multi_taper_result_dict = {'spectrogram':None, 'spectral_times':None,
                                   'spectral_frequency':None, 'spectrogram_computed':False }
        if self.spectrogram_computed:
            multi_taper_result_dict = {'spectrogram':self.mt_spectrogram,'spectral_times':self.stimes,
                                       'spectral_frequency':self.sfreqs, 'spectrogram_computed':True}
        return multi_taper_result_dict
    def get_multi_taper_properties(self):
        # Get properties
        fs = self.fs
        time_bandwidth = self.time_bandwidth
        num_tapers = self.num_tapers
        data_window_params = self.data_window_params
        frequency_range = self.frequency_range
        nfft = self.nfft
        detrend_opt = self.detrend_opt

        # Compute (normalize) data window params
        data_window_params = np.asarray(data_window_params) / fs

        multi_taper_param_dict = {'spectral_resolution':None,'window_length':None,'window_step':None,
                                  'time_half_bandwidth_product':None,'number_of_tapers':None,
                                  'frequency_range':None,'nfft':None,'detrend':None}
        if self.spectrogram_computed:
            multi_taper_param_dict['spectral_resolution'] = 2 * time_bandwidth / data_window_params[0]
            multi_taper_param_dict['window_length'] = data_window_params[0]
            multi_taper_param_dict['window_step'] = data_window_params[1]
            multi_taper_param_dict['time_half_bandwidth_product'] = time_bandwidth
            multi_taper_param_dict['number_of_tapers'] = num_tapers
            multi_taper_param_dict['frequency_range'] = [frequency_range[0], frequency_range[1]]
            multi_taper_param_dict['nfft'] = nfft
            multi_taper_param_dict['detrend'] = detrend_opt
        return multi_taper_param_dict
    def compute_spectral_summary(self, analysis_range:list=None,
                                 stage_mask:list|None=None):
        # Update log
        logger.info(f'Computing spectral summary by stage{analysis_range}')

       # checks
        if not self.spectrogram_computed:
            return None

        # Get ispectral data and times
        mt_spectrogram = self.mt_spectrogram
        stimes = self.stimes

        # Compute masks
        stimes_np = np.array(stimes)
        mask = stimes_np is not None
        if analysis_range is not None:
            analysis_range = analysis_range
            mask = (stimes_np >= analysis_range[0]) & (stimes_np < analysis_range[1])

        # Merge stage mask if present
        if stage_mask is not None:
            mask &= stage_mask

        # Compute statistics
        spectrogram_np = np.array(mt_spectrogram)
        spectrogram_avg = np.mean(spectrogram_np[:,mask], axis=1)
        spectrogram_std = np.std(spectrogram_np[:,mask], axis=1, ddof=1)


        return spectrogram_avg, spectrogram_std
    def plot_spectral_summary(self, parent_widget=None, turn_axis_units_off: bool = False,
                              axis_only: bool = False, analysis_range:list|None=None,
                              stage_information:tuple[int,list]|None = None, stage_colors:dict|None=None):
        """Plot 1D spectral summary (average power across frequencies)"""

        # Cleanup handlers
        self.cleanup_events()

        # Define plotting variables
        label_fontsize = 6
        tick_label_fontsize = 6
        x_label_text = "Frequency (Hz)"
        y_label_text = "Average PSD (dB)"

        # Get spectral summary data
        spectral_summary, spectrogram_std = self.compute_spectral_summary(analysis_range=analysis_range)
        if spectral_summary is None:
            logger.warning("No spectral summary available to plot")
            return

        # Average spectrum should stages not be provided
        sfreqs = self.sfreqs
        summary_db = self.nanpow2db(spectral_summary) #  # Convert to dB if needed

        # Create time series for each stage
        sum_db_list = []
        if stage_information is not None:
            # Process stage information
            epoch = stage_information[0]
            stages = stage_information[1]
            masks, mlabels = self.generate_stage_masks(epoch, stages, self.stimes)
            for mask_tuple in zip(masks, mlabels):
                stage_mask, stage_label = mask_tuple
                spect_sum, spect_std = self.compute_spectral_summary(analysis_range=analysis_range,
                                                                     stage_mask=stage_mask)
                sum_db = self.nanpow2db(spect_sum)
                sum_db_list.append(sum_db)
        else:
            sum_db_list.append(summary_db)
            mlabels = ['Avg']

        # Set Colors
        if stage_colors is not None:
            stage_dict = self.default_stage_colors
        else:
            stage_dict = self.default_stage_colors

        # Create the figure and canvas
        fig = Figure()
        ax = fig.add_subplot(111)

        if not axis_only:
            # Plot the 1D spectral summary
            for plot_tuple in zip(sum_db_list, mlabels):
                sum_db, mlabel = plot_tuple
                plot_color = stage_dict[mlabel]
                ax.plot(sfreqs, sum_db, linewidth=2.0, color=plot_color, label=mlabel)
                ax.set_xlabel(x_label_text, fontsize=label_fontsize)
                ax.set_ylabel(y_label_text, fontsize=label_fontsize)
                ax.grid(True, alpha=0.3)
                ax.legend(fontsize=tick_label_fontsize, loc='upper right', handlelength=1.0)
        else:
            # Minimal axis for alignment
            for sum_db in sum_db_list:
                ax.plot(sfreqs, sum_db, alpha=0)
                ax.set_xlim(sfreqs[0], sfreqs[-1])

            # Hide all spines except bottom
            for spine in ax.spines.values():
                spine.set_visible(False)
            ax.spines['bottom'].set_visible(True)

            # Hide y-axis
            ax.get_yaxis().set_visible(False)

            # Make background transparent
            ax.set_facecolor('none')
            fig.patch.set_facecolor('none')

        # Store references
        self.current_spectrogram_ax = ax
        self.current_spectrogram_fig = fig
        self.current_spectrogram_canvas = None

        # Set tick parameters
        ax.tick_params(axis='x', labelsize=tick_label_fontsize, direction='in', length=1, pad=-8)
        ax.tick_params(axis='y', labelsize=tick_label_fontsize, direction='in')
        for label in ax.get_xticklabels():
            label.set_text(f' {label.get_text()}')
            label.set_horizontalalignment('center')

        if turn_axis_units_off:
            ax.set_xticklabels([])

        # Embed canvas into the provided QWidget
        if parent_widget:
            canvas = FigureCanvas(fig)

            canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            canvas.updateGeometry()

            # Store canvas reference
            self.current_spectrogram_canvas = canvas

            # Adjust figure margins
            fig.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15)

            # Remove existing layout and widgets
            existing_layout = parent_widget.layout()
            if existing_layout:
                while existing_layout.count():
                    item = existing_layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.setParent(None)
            else:
                existing_layout = QVBoxLayout(parent_widget)
                parent_widget.setLayout(existing_layout)

            # Add new canvas
            existing_layout.setContentsMargins(0, 0, 0, 0)
            existing_layout.addWidget(canvas)

            if not axis_only:
                ax.set_xlabel("Frequency (Hz)", fontsize=label_fontsize)
                ax.set_ylabel("Average PSD (dB)", fontsize=label_fontsize)
    def plot_band_summary(self, parent_widget=None, axis_only: bool = False,
                          analysis_range:list|None=None, spectral_bands:list|None=None, spectral_titles:list|None=None,
                          stage_information:tuple[int,list]|None = None, stage_colors:dict|None=None):

        """
            Plot 1D spectral summary (average power across frequencies),
            grouped by frequency band with subgroups for each sleep stage.
            """

        if stage_information is None or spectral_bands is None:
            logger.error("Missing required inputs: stage_information or spectral_bands")
            return

        epoch, stages = stage_information
        unique_stages = reorder_stages(list(set(stages)))

        fig = Figure()
        ax = fig.add_subplot(111)
        # fig, ax = plt.subplots(figsize=(10, 5))

        positions = []
        stage_labels = []
        band_centers = []
        band_names = []

        label_fontsize = 8
        pos = 1
        spacing = 2

        # Iterate over spectral bands
        for band_idx, band_range in enumerate(spectral_bands):
            band_name = spectral_titles[band_idx] if spectral_titles else f"Band {band_idx + 1}"
            band_data = self.compute_band_statistics(band_range, analysis_range)  # ← your data getter

            start_pos = pos

            # Iterate over sleep stages
            for stage in unique_stages:
                stage_mask = np.array(stages) == stage
                stage_values = band_data[stage_mask] if len(band_data) == len(stages) else np.random.rand(10)

                # Optional: color by stage
                color = stage_colors[stage] if stage_colors and stage in stage_colors else None

                if len(stage_values) > 0:
                    ax.boxplot(stage_values, positions=[pos], patch_artist=True, widths=0.7,
                           boxprops=dict(facecolor=color if color else 'lightgray', alpha=0.7))

                positions.append(pos)
                stage_labels.append(stage)
                pos += 1

            end_pos = pos - spacing - 1
            band_centers.append((start_pos + end_pos + spacing) / 2)
            band_names.append(band_name)

            pos += spacing

        # Set stage labels under each box
        ax.set_xticks(positions)
        ax.set_xticklabels(stage_labels, rotation=45, ha='right', fontsize=label_fontsize)

        # Add band group labels below
        for center, band in zip(band_centers, band_names):
            ax.text(center, 0.045, band, ha='center', va='top', fontsize=label_fontsize,
                    transform=ax.get_xaxis_transform())

        ax.set_xlabel('')
        ax.set_ylabel('Average Power',fontsize=label_fontsize)
        #ax.set_title('Spectral Power by Band and Sleep Stage')

        plt.tight_layout()
        #plt.show()

        # Embed canvas into the provided QWidget
        if parent_widget:
            canvas = FigureCanvas(fig)
            canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            canvas.updateGeometry()

            # Store canvas reference
            self.current_spectrogram_canvas = canvas

            # Adjust figure margins
            fig.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15)

            # Remove existing layout and widgets
            existing_layout = parent_widget.layout()
            if existing_layout:
                while existing_layout.count():
                    item = existing_layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.setParent(None)
            else:
                existing_layout = QVBoxLayout(parent_widget)
                parent_widget.setLayout(existing_layout)

            # Add new canvas
            existing_layout.setContentsMargins(0, 0, 0, 0)
            existing_layout.addWidget(canvas)

            if not axis_only:
                ax.set_ylabel("Average PSD (dB)", fontsize=label_fontsize)
    def compute_band_statistics(self, band_range, analysis_range=None):
        """
        Compute average power within a frequency band for each epoch.
        Returns: 1D numpy array of power values (one per epoch)
        """

        fmin, fmax = band_range
        freqs = np.array(self.sfreqs)  # frequency vector
        spectrogram = np.array(self.mt_spectrogram)  # shape: (freqs, times)

        # Select frequency range
        freq_mask = (freqs >= fmin) & (freqs < fmax)

        # Making band computation safe for a range of signals
        band_power = np.nanmean(spectrogram[freq_mask, :], axis=0) if np.any(freq_mask) else np.full(
            spectrogram.shape[1], np.nan)

        # Optional: limit by analysis time window
        if analysis_range is not None:
            stimes = np.array(self.stimes)
            time_mask = (stimes >= analysis_range[0]) & (stimes < analysis_range[1])
            band_power = band_power[time_mask]

        return band_power


    # SPECTROGRAM HELPER FUNCTIONS
    @staticmethod
    def nanpow2db(y):
        """ Power to dB conversion, setting bad values to nans
            Arguments:
                y (float or array-like): power
            Returns:
                ydB (float or np array): inputs converted to dB with 0s and negatives resulting in nans
        """

        if isinstance(y, int) or isinstance(y, float):
            if y == 0:
                return np.nan
            else:
                ydB = 10 * np.log10(y)
        else:
            if isinstance(y, list):  # if y is a list, turn into array
                y = np.asarray(y)
            y = y.astype(float)  # make sure it's a float array so we can put nans in it
            y[y == 0] = np.nan
            ydB = 10 * np.log10(y)

        return ydB
    @staticmethod
    def is_outlier(data:npt.NDArray[np.floating]) -> npt.NDArray[np.bool_]:
        smad: float = float(1.4826 * np.median(np.abs(data - np.median(data))))# scaled median absolute deviation
        outlier_mask = np.abs(data - np.median(data)) > 3.0 * smad  # outliers are more than 3 smads away from median
        outlier_mask = (outlier_mask | np.isnan(data) | np.isinf(data))
        return outlier_mask
    @staticmethod
    def calc_mts_segment(data_segment, dpss_tapers, nfft, freq_inds, detrend_opt, num_tapers,
                         dpss_eigen, weighting, wt):
        """ Helper function to calculate the multitaper spectrum of a single segment of data
            Arguments:
                data_segment (1d np.array): One window worth of time-series data -- required
                dpss_tapers (2d np.array): Parameters for the DPSS tapers to be used.
                                           Dimensions are (num_tapers, winsize_samples) -- required
                nfft (int): length of signal to calculate fft on -- required
                freq_inds (1d np array): boolean array of which frequencies are being analyzed in
                                          an array of frequencies from 0 to fs with steps of fs/nfft
                detrend_opt (str): detrend data window ('linear' (default), 'constant', 'off')
                num_tapers (int): number of tapers being used
                dpss_eigen (np array):
                weighting (str):
                wt (int or np array):
            Returns:
                mt_spectrum (1d np.array): spectral power for single window
        """

        # If segment has all zeros, return vector of zeros
        if np.all(data_segment == 0):
            return np.zeros(sum(freq_inds))

        if any(np.isnan(data_segment)):
            ret = np.empty(sum(freq_inds))
            ret.fill(np.nan)
            return ret

        # Option to detrend data to remove low frequency DC component
        if detrend_opt != 'off':
            data_segment = detrend(data_segment, type=detrend_opt)

        # Multiply data by dpss tapers (STEP 2)
        # tapered_data = np.multiply(np.mat(data_segment).T, np.mat(dpss_tapers.T))
        # dad: `np.mat` was removed in the NumPy 2.0 release. Use `np.asmatrix` instead
        # dad: tapered_data = np.multiply(np.asmatrix(data_segment).T, np.asmatrix(dpss_tapers.T))
        # dad:Reshape data_segment to column vector and multiply
        # Changed again due to pending depracation
        data_col = data_segment.reshape(-1, 1)  # Make it a column vector
        tapers_transposed = dpss_tapers.T
        tapered_data = data_col * tapers_transposed

        # Compute the FFT (STEP 3)
        fft_data = np.fft.fft(tapered_data, nfft, axis=0)

        # Compute the weighted mean spectral power across tapers (STEP 4)
        spower = np.power(np.imag(fft_data), 2) + np.power(np.real(fft_data), 2)
        if weighting == 'adapt':
            # adaptive weights - for colored noise spectrum (Percival & Walden p368-370)
            tpower = np.dot(np.transpose(data_segment), (data_segment / len(data_segment)))
            spower_iter = np.mean(spower[:, 0:2], 1)
            spower_iter = spower_iter[:, np.newaxis]
            a = (1 - dpss_eigen) * tpower
            for i in range(3):  # 3 iterations only
                # Calc the MSE weights
                b = np.dot(spower_iter, np.ones((1, num_tapers))) / ((np.dot(spower_iter, np.transpose(dpss_eigen))) +
                                                                     (np.ones((nfft, 1)) * np.transpose(a)))
                # Calc new spectral estimate
                wk = (b ** 2) * np.dot(np.ones((nfft, 1)), np.transpose(dpss_eigen))
                spower_iter = np.sum((np.transpose(wk) * np.transpose(spower)), 0) / np.sum(wk, 1)
                spower_iter = spower_iter[:, np.newaxis]

            mt_spectrum = np.squeeze(spower_iter)

        else:
            # eigenvalue or uniform weights
            mt_spectrum = np.dot(spower, wt)
            mt_spectrum = np.reshape(mt_spectrum, nfft)  # reshape to 1D

        return mt_spectrum[freq_inds]

    # Generate Masks
    @staticmethod
    def generate_stage_masks(epoch: float, stages: list[str], spectral_times: np.ndarray) -> tuple[list[np.ndarray], list[str]]:
        """
        Generate boolean masks for each sleep stage based on spectral times.

        Parameters
        ----------
        epoch : float
            Epoch length in seconds (e.g., 30.0).
        stages : list[str]
            List of sleep stages (e.g., ['W', 'N1', 'N2', 'REM', ...]).
        spectral_times : np.ndarray
            Array of times in seconds corresponding to spectrogram frames.

        Returns
        -------
        tuple[list[np.ndarray], list[str]]
            masks  : list of boolean arrays, one per unique stage
            mlabels: list of stage labels corresponding to each mask
        """
        stages = np.array(stages)
        unique_stages = reorder_stages(np.unique(stages))
        masks = []
        mlabels = []

        # Compute epoch start times (one per stage label)
        epoch_starts = np.arange(0, len(stages) * epoch, epoch)
        epoch_ends = epoch_starts + epoch

        for stage in unique_stages:
            mask = np.zeros_like(spectral_times, dtype=bool)
            # For each epoch labeled with this stage, include its time range
            indices = np.where(stages == stage)[0]
            for idx in indices:
                t_start = epoch_starts[idx]
                t_end = epoch_ends[idx]
                mask |= (spectral_times >= t_start) & (spectral_times < t_end)
            masks.append(mask)
            mlabels.append(stage)
        return masks, mlabels
    @staticmethod
    def generate_analysis_range_masks(first_sleep_time:float, last_sleep_time:float, spectral_times: np.ndarray) -> dict[str,npt.NDArray[bool]]:
        """
        Generate boolean masks for each analysis range.

        Parameters
        ----------
        first_sleep_time : float
            Time of first sleep in seconds
        last_sleep_time: list[str]
            List of sleep stages (e.g., ['W', 'N1', 'N2', 'REM', ...]).
        spectral_times : np.ndarray
            Array of times in seconds corresponding to spectrogram frames.

        Returns
        -------
        dict[str, npt.NDArray[bool]
            masks  : list of boolean arrays, one per unique stage
            mlabels: list of analysis range labels
        """

        # Define return dictionary
        analysis_mask_range_dict = {}

        # Define return value
        range_label_list = ['first_wake', 'first_wake_and_sleep', 'sleep_only', 'ending_wake']
        ramge_fun_list = [lambda x: first_sleep_time > x, lambda x: last_sleep_time >= x,
                          lambda x: np.logical_and(first_sleep_time <= x, last_sleep_time >= x),
                          lambda x:x>last_sleep_time]
        for lab, fn in zip(range_label_list, ramge_fun_list):
            analysis_mask_range_dict[lab] = fn(spectral_times)

        return analysis_mask_range_dict
    @staticmethod
    def generate_band_freq_masks(band_param_dict:dict, spectral_freqs: np.ndarray) -> dict[str,npt.NDArray[bool]]:
        """
        Generate boolean masks for each frequency band.

        Parameters
        ----------
        band_param_dict : dict[str, tuple[float, float]]
            Dictionary where each key is a band name, and the value is a
            (low_freq, high_freq) tuple in Hz.
        spectral_freqs : np.ndarray
            1D array of frequencies in Hz corresponding to the spectrogram frequency axis.

        Returns
        -------
        dict[str, npt.NDArray[np.bool_]]
            Dictionary mapping each band name to a boolean mask array where True
            values indicate frequencies within the specified band.
        """

        # Define return dictionary
        analysis_mask_range_dict: dict[str, npt.NDArray[np.bool_]] = {}

        for band_key, (band_low, band_high) in band_param_dict.items():
            mask = (spectral_freqs >= band_low) & (spectral_freqs < band_high)
            analysis_mask_range_dict[band_key] = mask

        return analysis_mask_range_dict

    # Python
    def __str__(self):
        return f'Multi-Taper Spectrogram: Sample Frequency {self.fs} '

#Main
def main():
    pass
    # Removed testing when plotting conflicted with pyside6 widgets

    #"""Less than complete testing"""
    # Set spectrogram params
    #fs              = 200  # Sampling Frequency
    #frequency_range = [0, 25]  # Limit frequencies from 0 to 25 Hz
    #time_bandwidth  = 3  # Set time-half bandwidth
    #num_tapers      = 5  # Set number of tapers (optimal is time_bandwidth*2 - 1)
    #window_params   = [4, 1]  # Window size is 4s with step size of 1s
    #min_nfft        = 0  # No minimum nfft
    #detrend_opt     = 'constant'  # detrend each window by subtracting the average
    #multiprocess    = True  # use multiprocessing
   