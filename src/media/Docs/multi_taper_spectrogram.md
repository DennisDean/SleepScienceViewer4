# Multi-Taper Spectrogram Module

## Overview

This module implements multi-taper spectral analysis for sleep data.


## Purpose

The `MultitaperSpectrogram` class provides comprehensive spectral analysis capabilities for time-series data, particularly optimized for sleep research applications. It offers advantages over traditional Fourier transform methods by providing better control over the time-frequency trade-off through configurable multi-taper parameters.

## Key Features

### Core Functionality
- **Multi-taper spectral analysis** using DPSS (Discrete Prolate Spheroidal Sequences) tapers
- **Flexible time-frequency resolution** through adjustable time-bandwidth parameters
- **Multiprocessing support** for faster computation on large datasets
- **Multiple weighting schemes**: unity, eigenvalue, and adaptive weighting

### Visualization Capabilities
- Interactive spectrogram plots with customizable colormaps
- Data heatmap visualization for non-spectral data
- Stage-wise spectral summaries (average power across frequencies)
- Band-wise boxplot summaries grouped by sleep stage
- Colorbar legend dialogs for interpreting visualizations

### Sleep Stage Analysis
- Automatic stage mask generation from hypnogram data
- Stage-wise spectral statistics computation
- Configurable spectral band analysis (delta, theta, alpha, sigma, beta, gamma)
- Support for standard sleep stage classifications (Wake, REM, N1-N4, NREM)

### Integration Features
- PySide6 Qt widget integration for GUI applications
- Event handling for interactive plot exploration (double-click callbacks)
- Export capabilities for results and configurations
- Memory-efficient processing with optional multiprocessing

## Class: MultitaperSpectrogram

### Initialization Parameters

```python
MultitaperSpectrogram(
    data,              # 1D numpy array: time series data
    fs,                # float: sampling frequency (Hz)
    frequency_range,   # list: [min_freq, max_freq] (default: [0, nyquist])
    time_bandwidth,    # float: time-half bandwidth product (default: 5)
    num_tapers,        # int: number of DPSS tapers (default: floor(2*time_bandwidth - 1))
    window_params,     # list: [window_size_sec, step_size_sec] (default: [5, 1])
    min_nfft,          # int: minimum FFT size for zero-padding (default: 0)
    detrend_opt,       # str: 'linear', 'constant', or 'off' (default: 'linear')
    multiprocess,      # bool: use multiprocessing (default: False)
    n_jobs,            # int: number of CPU cores (default: None = all-1)
    weighting,         # str: 'unity', 'eigen', or 'adapt' (default: 'unity')
    plot_on,           # bool: plot results (default: True)
    return_fig,        # bool: return figure object (default: False)
    clim_scale,        # bool: auto-scale colormap (default: True)
    verbose,           # bool: print spectrogram properties (default: True)
    xyflip,            # bool: transpose output matrix (default: False)
    ax                 # matplotlib axes: plot destination (default: None)
)
```

### Main Methods

#### Computation
- **`compute_spectrogram()`** - Computes the multi-taper spectrogram
- **`compute_spectral_summary(analysis_range, stage_mask)`** - Computes average and standard deviation across time
- **`compute_band_statistics(band_range, analysis_range)`** - Computes power within specific frequency bands

#### Visualization
- **`plot(parent_widget, ...)`** - Plots the spectrogram with customizable options
- **`plot_data(parent_widget, ...)`** - Plots raw data as a heatmap
- **`plot_spectral_summary(parent_widget, ...)`** - Plots 1D average spectrum by stage
- **`plot_band_summary(parent_widget, ...)`** - Plots boxplots of band power by stage
- **`show_colorbar_legend_dialog()`** - Displays colorbar legend in a dialog window
- **`show_heatmap_legend_dialog()`** - Displays heatmap colorbar legend

#### Utility
- **`display_spectrogram_props()`** - Prints spectrogram parameters to console
- **`get_multi_taper_results()`** - Returns dictionary with computed results
- **`get_multi_taper_properties()`** - Returns dictionary with computation parameters
- **`generate_stage_masks(epoch, stages, spectral_times)`** - Creates boolean masks for sleep stages

#### Event Management
- **`setup_events()`** - Establishes event handlers for interactive plots
- **`cleanup_events()`** - Removes event handlers to prevent memory leaks

### Output

The spectrogram computation produces three main outputs:

1. **`mt_spectrogram`** - 2D numpy array of spectral power (frequency × time)
2. **`stimes`** - 1D array of time points (seconds) for each spectrum
3. **`sfreqs`** - 1D array of frequency values (Hz) in the spectrogram

## Usage Example

```python
import numpy as np
from multi_taper_module import MultitaperSpectrogram

# Generate sample data
fs = 200  # Hz
duration = 600  # seconds
t = np.arange(0, duration, 1/fs)
data = np.random.randn(len(t))  # Replace with actual EEG data

# Configure parameters
mts = MultitaperSpectrogram(
    data=data,
    fs=fs,
    frequency_range=[0, 25],
    time_bandwidth=3,
    num_tapers=5,
    window_params=[4, 1],
    multiprocess=True
)

# Compute spectrogram
mts.compute_spectrogram()

# Display properties
mts.display_spectrogram_props()

# Plot results
mts.plot()

# Get results
results = mts.get_multi_taper_results()
spectrogram = results['spectrogram']
times = results['spectral_times']
freqs = results['spectral_frequency']
```

## Integration with Sleep Science Viewer

This module is designed to integrate seamlessly with the Sleep Science Viewer application:

### Settings Section
- Signal selection (up to 10 signals)
- X-axis label display options
- Signal reference and filter parameters (in development)

### Parameters Section
- **Noise Detection**: Identifies large perturbations in sleep EEG
- **Multi-Taper Configuration**: Time-bandwidth product, number of tapers, window parameters
- **Spectral Band Definition**: Six customizable frequency bands (default: delta, theta, alpha, sigma, beta, gamma)

### Analysis Options
- **Analysis Range**: First Wake, First Wake and Sleep, Sleep Only, Ending Wake
- **Stage-wise Summaries**: Automatic grouping by sleep stage
- **Hypnogram Integration**: Uses stage annotations for targeted analysis

### Export Capabilities
- Configuration files (XML format)
- Results files per signal
- Noise detection masks (delta, beta, union, intersection)

## Dependencies

- **numpy** - Array operations and numerical computing
- **scipy** - Signal processing (DPSS tapers, detrending, FFT)
- **matplotlib** - Plotting and visualization
- **PySide6** - Qt GUI integration
- **joblib** - Parallel processing support

## Technical Notes

### Multi-Taper Method
The multi-taper approach uses multiple orthogonal tapers (DPSS sequences) to estimate the power spectrum. This provides:
- **Reduced variance** compared to single-taper methods
- **Better control** of spectral leakage
- **Flexible time-frequency resolution** through the time-bandwidth parameter

### Computation Steps
1. Compute DPSS tapers based on time-bandwidth product
2. Multiply data segments by DPSS tapers
3. Compute FFT for each tapered segment
4. Average across tapers (with optional weighting)
5. Convert to one-sided power spectral density

### Performance Optimization
- **Multiprocessing**: Automatically uses available CPU cores minus one
- **Efficient indexing**: Pre-computes window indices to avoid repeated calculations
- **Memory management**: Processes data in windowed segments

### Color Scheme
Default stage colors follow sleep research conventions:
- Wake (W): Light gray
- REM: Light pink
- N1: Thistle (light purple)
- N2: Powder blue
- N3: Pale green
- N4: Medium sea green
- Artifact: Salmon

## Acknowledgement

The source code builds on the multi-taper spectrogram code made pubically available. See
the referenced publication below for additional detail. As requested, the orgininal refence is also
included in the source code.

> **"Sleep Neurophysiological Dynamics Through the Lens of Multitaper Spectral Analysis"**  
> Michael J. Prerau, Ritchie E. Brown, Matt T. Bianchi, Jeffrey M. Ellenbogen, Patrick L. Purdon  
> December 7, 2016 : 60-92  
> DOI: 10.1152/physiol.00062.2015
