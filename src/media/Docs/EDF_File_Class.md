# EDF File Class - Python Native EDF File Reader

A Python library for reading, analyzing, and visualizing European Data Format (EDF) files, commonly used in sleep studies and physiological signal recordings.

## Overview

The EDF File Class provides native Python access to information stored in EDF files, including headers, signal metadata, and time-series data. It offers a comprehensive set of tools for signal processing, statistical analysis, and visualization.

## Features

- **Complete EDF File Support**
  - Read EDF headers and signal metadata
  - Load and process multi-channel physiological signals
  - Handle both continuous and stepped signals
  
- **Signal Processing**
  - Butterworth bandpass filtering
  - Notch filtering (50/60 Hz power line noise removal)
  - Multi-taper spectrogram analysis
  - Automatic noise detection based on delta/beta band power

- **Statistical Analysis**
  - Comprehensive signal statistics (mean, median, percentiles, etc.)
  - Export statistics to CSV/Excel formats
  - Signal quality assessment

- **Visualization**
  - Signal segment plotting with customizable time scales
  - Sleep stage background coloring
  - Integration with PySide6 for GUI applications
  - Matplotlib-based plotting

- **Data Export**
  - JSON summary exports
  - CSV/Excel statistical reports
  - Text file signal exports

## Installation

### Requirements

```bash
pip install numpy scipy matplotlib pandas PySide6 sympy openpyxl
```

### Optional Dependencies

For multi-taper spectrogram analysis:
```bash
# Install the multitaper_spectrogram_python_class module (separate package)
```

## Quick Start

### Basic Usage

```python
from edf_file_class import EdfFile
import os

# Load an EDF file
edf_file = EdfFile('/path/to/your/file.edf')
edf_file.load()

# Display summary
edf_file.summary()

# Calculate signal statistics
edf_file.calculate_signal_stats()
```

### Export Statistics

```python
# Set output directory
edf_file.set_output_dir('./exports')

# Export to CSV
edf_file.edf_signals.export_sig_stats_to_csv('signal_stats.csv')

# Export to Excel
edf_file.edf_signals.export_sig_stats_to_excel('signal_stats.xlsx')

# Export JSON summary
edf_file.export_summary_to_json('edf_summary.json')
```

### Signal Processing

```python
# Get a specific signal
signal_key = 'EEG Fpz-Cz'
edf_signal = edf_file.edf_signals.return_edf_signal(signal_key)

# Apply bandpass filter (0.5-30 Hz) and notch filter (60 Hz)
filter_params = [0.5, 30, 60]  # [lowcut, highcut, notch_freq]

# Perform multi-taper spectrogram analysis
from edf_file_class import EdfSignalAnalysis

analysis = EdfSignalAnalysis(
    edf_signal,
    filter_param=filter_params,
    window_params=[5, 1],  # [window_size, step_size]
    n_jobs=4
)

spectrogram = analysis.multitapper_spectrogram()
```

### Signal Visualization

```python
# Plot a 30-second epoch
epoch_num = 10
epoch_width = 30.0
signal_key = 'EEG Fpz-Cz'

edf_file.edf_signals.plot_signal_segment(
    signal_key=signal_key,
    signal_type='Continuous',
    epoch_num=epoch_num,
    epoch_width=epoch_width,
    filter_param=[0.5, 30, 60],  # Optional filtering
    y_axis_units='µV'
)
```

### Working with Sleep Stages

```python
# Plot signal with sleep stage background colors
sleep_stages = [
    {'start_time': 0, 'end_time': 30, 'stage': 'N2'},
    {'start_time': 30, 'end_time': 60, 'stage': 'N3'}
]

edf_file.edf_signals.plot_signal_segment(
    signal_key='EEG Fpz-Cz',
    signal_type='Continuous',
    epoch_num=0,
    epoch_width=60,
    sleep_stages=sleep_stages
)
```

## Core Classes

### `EdfFile`
Main class for loading and managing EDF files.

**Key Methods:**
- `load()` - Load complete EDF file
- `return_edf_header()` - Get header information only
- `calculate_signal_stats()` - Compute signal statistics
- `export_summary_to_json()` - Export file summary

### `EdfSignals`
Manages signal data and metadata.

**Key Methods:**
- `return_edf_signal(signal_key)` - Get specific signal
- `return_signal_segment(signal_key, epoch_num, epoch_width)` - Extract epoch
- `plot_signal_segment()` - Visualize signal segments
- `export_sig_stats_to_csv()` - Export statistics

### `EdfSignalAnalysis`
Performs advanced signal analysis.

**Key Methods:**
- `multitapper_spectrogram()` - Compute multi-taper spectrogram
- `simple_noise_detection()` - Detect noisy epochs

### `EdfHeader`
Stores EDF file header information.

### `EdfSignalHeader`
Stores signal-specific metadata (sampling rates, units, calibration).

## Signal Processing Functions

### Bandpass Filter
```python
from edf_file_class import apply_bandpass_filter

filtered_signal = apply_bandpass_filter(
    data=signal_data,
    fs=sampling_frequency,
    lowcut=0.5,
    highcut=30.0,
    order=5
)
```

### Notch Filter
```python
from edf_file_class import apply_notch_filter

filtered_signal = apply_notch_filter(
    signal_data=signal_data,
    fs=sampling_frequency,
    notch_freq=60,  # US: 60 Hz, EU: 50 Hz
    Q=30.0
)
```

## Advanced Features

### Noise Detection

Automatically detect noisy epochs based on delta and beta band power:

```python
noise_params = {
    'delta_low': 0.5,
    'delta_high': 4.0,
    'delta_factor': 2.5,
    'beta_low': 15.0,
    'beta_high': 30.0,
    'beta_factor': 2.5
}

analysis = EdfSignalAnalysis(
    edf_signal,
    noise_detect_param_dict=noise_params
)

spectrogram = analysis.multitapper_spectrogram()
noise_masks = analysis.noise_mask_dict
```

### Custom Time Formatting

```python
# Convert seconds to minutes
convert_to_minutes = lambda x: x / 60

edf_file.edf_signals.plot_signal_segment(
    signal_key='EEG',
    epoch_num=0,
    epoch_width=300,
    convert_time_f=convert_to_minutes,
    time_axis_units='min'
)
```

## File Formats

### Supported EDF Variants
- Standard EDF (European Data Format)
- EDF+ (with annotations)

### Export Formats
- **CSV** - Signal statistics and data
- **Excel** (.xlsx) - Formatted statistical reports
- **JSON** - Complete file summaries
- **TXT** - Time-series signal data

## Examples

See the `main()` function in the source code for comprehensive examples including:
- Loading multiple EDF files
- Statistical analysis and export
- Signal filtering demonstrations
- Visualization examples

## Acknowledgments

This Python implementation is based on previous MATLAB versions developed at:
- Case Western Reserve University
- Brigham and Women's Hospital

The code has benefited from community feedback following public release on MATLAB Central.

## License

This source code is licensed under the **GNU Affero General Public License v3.0**.

See the LICENSE file in the root directory or visit https://www.gnu.org/licenses/agpl-3.0.html for full terms.

Copyright 2025 Dennis A. Dean II, PhD - Sleep Science

## Author

**Dennis A. Dean, II, PhD**  
Sleep Science  
Completion Date: June 20, 2025

## Contributing

Contributions are welcome! Please ensure:
- Code follows existing style conventions
- Functions include docstrings
- New features include usage examples
- Changes are tested with sample EDF files

## Support

For issues, questions, or feature requests, please open an issue on the GitHub repository.

---

**Note:** This library is designed for research and clinical applications involving physiological signal analysis, particularly in sleep medicine and neuroscience.