# Analysis Imports
import math
import numpy as np
import numpy.typing as npt
from openpyxl.pivot.fields import Boolean
from scipy.signal.windows import dpss
from scipy.signal import detrend
from typing import Tuple, TypeAlias, Literal

# Logistical Imports
import warnings
import timeit
from joblib import Parallel, delayed, cpu_count
import logging

# Visualization imports
import colorcet  # this import is necessary to add rainbow colormap to matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from matplotlib import cm
from PySide6.QtWidgets import QVBoxLayout, QSizePolicy, QWidget
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QGraphicsScene
import matplotlib.pyplot as plt
from scipy.signal import chirp  # import chirp generation function


# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # or DEBUG for more detail

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

"""
Revisions
- added function variable type to primary definition
- replaced np.mat with np.asmatrix
- force matplot lib to use QT(PySide6)
- restructured to class format
- added ability to create plot in test and to plot to a widget
- converted computation to a class
"""
# MULTITAPER SPECTROGRAM #
class MultitaperSpectrogram:
    def __init__(self, data:np.array, fs:float, frequency_range=None, time_bandwidth=5, num_tapers=None, window_params=None,
                           min_nfft=0, detrend_opt='linear', multiprocess=False, n_jobs=None, weighting='unity',
                           plot_on=True, return_fig=False, clim_scale=True, verbose=True, xyflip=False, ax=None):
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
        self.frequency_range: Tuple[float, float] = frequency_range
        self.time_bandwidth:float                 = time_bandwidth
        self.num_tapers: int                      = num_tapers
        self.window_params: Tuple[float, float]   = window_params
        self.min_nfft: int                        = min_nfft
        self.detrend_opt: Literal['Linear', 'constant', 'off'] = detrend_opt
        self.multiprocess: Boolean = multiprocess
        self.n_jobs: int           = n_jobs
        self.weighting: str        = weighting
        self.plot_on: Boolean      = plot_on
        self.return_fig: Boolean   = return_fig
        self.clim_scale: Boolean   = clim_scale
        self.verbose: Boolean      = verbose
        self.xyflip: Boolean       = xyflip
        self.ax:axes               = ax


        # Computed taper parameters
        self.winsize_samples: int  = None    # number of samples in single time window
        self.winstep_samples: int  = None    # number of samples in a single window step
        self.window_start:np.array = None    # array of timestamps representing the beginning time for each window
        self.num_windows: int      = None    # Number of windows in the data
        self.nfft:int              = None    # length of signal to calculate fft on

        self.window_start: np.array = None    # array of timestamps representing the beginning time for each                                           window -- required
        self.datawin_size: float    = None    # seconds in one window -- required
        self.data_window_params:Tuple[float, float]  = [None, None] # [window length(s), window step size(s)] - - required
    def compute_spectrogram(self):
        #  Process user input
        [data, fs, frequency_range, time_bandwidth, num_tapers,
         winsize_samples, winstep_samples, window_start,
         num_windows, nfft, detrend_opt, plot_on, verbose] = self.process_input()

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
        dpss_tapers, dpss_eigen = dpss(winsize_samples, time_bandwidth, num_tapers, return_ratios=True)
        dpss_eigen = np.reshape(dpss_eigen, (num_tapers, 1))

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
    def process_input(self):
        """ Helper function to process multitaper_spectrogram() arguments
                Arguments:
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
        frequency_range: Tuple[float, float]  = self.frequency_range
        time_bandwidth:float = self.time_bandwidth
        num_tapers: int = self.num_tapers
        window_params: Tuple[float, float] = self.window_params
        min_nfft: int = self.min_nfft
        detrend_opt: Literal['Linear', 'constant', 'off'] = self.detrend_opt
        plot_on: Boolean = self. plot_on
        verbose: Boolean = self.verbose

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
        detrend_opt = detrend_opt.lower()
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
            window_params = [5, 1]

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
    def process_spectrogram_params(self, fs, nfft, frequency_range, window_start, datawin_size):
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
        sfreqs = np.arange(0, fs, df)

        # Get frequencies for given frequency range
        freq_inds = (sfreqs >= frequency_range[0]) & (sfreqs <= frequency_range[1])
        sfreqs = sfreqs[freq_inds]

        # Compute times in the middle of each spectrum
        window_middle_samples = window_start + round(datawin_size / 2)
        stimes = window_middle_samples / fs

        # Get indexes for each window
        window_idxs = np.atleast_2d(window_start).T + np.arange(0, datawin_size, 1)
        window_idxs = window_idxs.astype(int)

        return [window_idxs, stimes, sfreqs, freq_inds]
    def display_spectrogram_props(self):
        """ Prints spectrogram properties
            Arguments:
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
    def plot(self, parent_widget=None):
        # Plot multitaper spectrogram

        mt_spectrogram = self.mt_spectrogram
        spect_data = self.nanpow2db(mt_spectrogram)
        stimes = self.stimes
        sfreqs = self.sfreqs

        # Set x and y axes
        dx = stimes[1] - stimes[0]
        dy = sfreqs[1] - sfreqs[0]
        extent = [stimes[0] - dx, stimes[-1] + dx, sfreqs[-1] + dy, sfreqs[0] - dy]

        # Create the figure and canvas
        fig = Figure()
        ax = fig.add_subplot(111)
        im = ax.imshow(spect_data, extent=extent, aspect='auto')

        # Customize plot
        if parent_widget:
            # Enable expanding to fill the parent widget
            y_label = "F(Hz)"
            color_bar_label = 'dB'
        else:
            y_label = "Frequency (Hz)"
            color_bar_label = 'PSD (dB)'
            fig.colorbar(im, ax=ax, label=color_bar_label, shrink=0.8)

        # fig.colorbar(im, ax=ax, label=color_bar_label, shrink=0.8)
        ax.set_xlabel("Time (HH:MM:SS)")
        ax.set_ylabel(y_label)
        im.set_cmap(cm.get_cmap('cet_rainbow4'))
        ax.invert_yaxis()

        if self.clim_scale:
            clim = np.percentile(spect_data, [5, 98])
            im.set_clim(clim)

        # Embed canvas into the provided QWidget

        if parent_widget:
            # Create the canvas
            canvas = FigureCanvas(fig)
            canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            canvas.updateGeometry()

            fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

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
            im.set_cmap(cm.get_cmap('cet_rainbow4'))
            ax.invert_yaxis()

            if self.clim_scale:
               clim = np.percentile(spect_data, [5, 98])
               im.set_clim(clim)
        elif parent_widget == None:
            plt.figure()
            plt.imshow(spect_data, extent=extent, aspect='auto', cmap='cet_rainbow4')
            plt.colorbar(label='PSD (dB)')
            plt.xlabel("Time (HH:MM:SS)")
            plt.ylabel("Frequency (Hz)")
            plt.gca().invert_yaxis()
            plt.show()

        # Optionally return for other use
        if self.return_fig:
            return mt_spectrogram, stimes, sfreqs, (fig, ax)
    # HELPER FUNCTIONS
    def nanpow2db(self, y):
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
            if isinstance(y, list):  # if list, turn into array
                y = np.asarray(y)
            y = y.astype(float)  # make sure it's a float array so we can put nans in it
            y[y == 0] = np.nan
            ydB = 10 * np.log10(y)

        return ydB
    def is_outlier(data):
        smad = 1.4826 * np.median(abs(data - np.median(data)))  # scaled median absolute deviation
        outlier_mask = abs(data - np.median(data)) > 3 * smad  # outliers are more than 3 smads away from median
        outlier_mask = (outlier_mask | np.isnan(data) | np.isinf(data))
        return outlier_mask
    def calc_mts_segment(self, data_segment, dpss_tapers, nfft, freq_inds, detrend_opt, num_tapers,
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
        if all(data_segment == 0):
            ret = np.empty(sum(freq_inds))
            ret.fill(0)
            return ret

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
        tapered_data = np.multiply(np.asmatrix(data_segment).T, np.asmatrix(dpss_tapers.T))

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
# Main
def main():

    """Less than complete testing"""
    # Set spectrogram params
    fs              = 200  # Sampling Frequency
    frequency_range = [0, 25]  # Limit frequencies from 0 to 25 Hz
    time_bandwidth  = 3  # Set time-half bandwidth
    num_tapers      = 5  # Set number of tapers (optimal is time_bandwidth*2 - 1)
    window_params   = [4, 1]  # Window size is 4s with step size of 1s
    min_nfft        = 0  # No minimum nfft
    detrend_opt     = 'constant'  # detrend each window by subtracting the average
    multiprocess    = True  # use multiprocessing
    n_jobs          = 3  # use 3 cores in multiprocessing
    weighting       = 'unity'  # weight each taper at 1
    plot_on         = True  # plot spectrogram
    return_fig      = False  # do not return plotted spectrogram
    clim_scale      = False # do not auto-scale colormap
    verbose         = False  # print extra info
    xyflip          = False  # do not transpose spect output matrix

    # Generate sample chirp data
    t = np.arange(1/fs, 600, 1/fs)  # Create 10 min time array from 1/fs to 600 stepping by 1/fs
    f_start = 1  # Set chirp freq range min (Hz)
    f_end = 20  # Set chirp freq range max (Hz)
    data = chirp(t, f_start, t[-1], f_end, 'logarithmic')

    # Compute the multitaper spectrogram
    multi_spectrogram_obj = MultitaperSpectrogram(data, fs, frequency_range, time_bandwidth, num_tapers, window_params,
        min_nfft, detrend_opt, multiprocess, n_jobs, weighting, plot_on, return_fig, clim_scale, verbose, xyflip)
    multi_spectrogram_obj.compute_spectrogram()
    multi_spectrogram_obj.display_spectrogram_props()
    multi_spectrogram_obj.plot()

if __name__ == "__main__":
    main()
